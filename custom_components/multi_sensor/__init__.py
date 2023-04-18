"""The ISENSIT component."""
import asyncio
import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import CONF_NAME
from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_component import EntityComponent
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

DOMAIN = "isensit"

CONF_MQTT_BROKER = "broker"
CONF_MQTT_PORT = "port"
CONF_MQTT_USERNAME = "username"
CONF_MQTT_PASSWORD = "password"
CONF_MQTT_TOPIC = "topic"
CONF_SENSORS = "sensors"

DEFAULT_PORT = 1883
DEFAULT_NAME = "ISENSIT"
DEFAULT_TOPIC = "ISENSIT/#"

PLATFORMS = ["sensor"]

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_MQTT_BROKER): cv.string,
                vol.Optional(CONF_MQTT_PORT, default=DEFAULT_PORT): cv.port,
                vol.Optional(CONF_MQTT_USERNAME): cv.string,
                vol.Optional(CONF_MQTT_PASSWORD): cv.string,
                vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
                vol.Optional(CONF_MQTT_TOPIC, default=DEFAULT_TOPIC): cv.string,
                vol.Optional(CONF_SENSORS): vol.All(
                    cv.ensure_list,
                    [
                        {
                            vol.Required(CONF_NAME): cv.string,
                            vol.Required(CONF_MQTT_TOPIC): cv.string,
                            vol.Required("unique_id"): cv.string,
                            vol.Optional("device_class"): cv.string,
                            vol.Optional("state_topic"): cv.string,
                            vol.Optional("unit_of_measurement"): cv.string,
                            vol.Optional("value_template"): cv.template,
                        }
                    ],
                ),
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistantType, config: dict):
    """Set up the ISENSIT component."""
    component = EntityComponent(_LOGGER, DOMAIN, hass)

    conf = config[DOMAIN]

    name = conf[CONF_NAME]
    broker = conf[CONF_MQTT_BROKER]
    port = conf[CONF_MQTT_PORT]
    username = conf.get(CONF_MQTT_USERNAME)
    password = conf.get(CONF_MQTT_PASSWORD)
    topic = conf[CONF_MQTT_TOPIC]

    sensors = conf.get(CONF_SENSORS, [])

    coordinator = ISENSITDataUpdateCoordinator(hass, broker, port, username, password, topic)

    await coordinator.async_refresh()

    if coordinator.last_update_success:
        _LOGGER.info("Connected to ISENSIT MQTT broker")
    else:
        _LOGGER.error("Could not connect to ISENSIT MQTT broker")

    for sensor in sensors:
        name = sensor[CONF_NAME]
        topic = sensor[CONF_MQTT_TOPIC]
        unique_id = sensor["unique_id"]
        device_class = sensor.get("device_class")
        state_topic = sensor.get("state_topic")
        unit_of_measurement = sensor.get("unit_of_measurement")
        value_template = sensor.get("value_template")

        component.async_register_entity_service(
            "update_sensor",
            {
                vol.Required("state_topic"): cv.string,
                vol.Required("unit_of_measurement"): cv.string,
                vol.Optional("value_template"): cv.template,
            },
            "async_update",
        )

        component.async_create_entity(
            CO2Sensor(coordinator.mqtt_client, topic, unique_id, name, device_class, state_topic, unit
