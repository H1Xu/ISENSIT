"""The multi_sensor component."""
import logging
from typing import Any, List, Optional

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_NAME, CONF_SENSORS
from homeassistant.core import HomeAssistant
from homeassistant.helpers import discovery
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType

from homeassistant.components.mqtt import (
    CONF_QOS,
    CONF_STATE_TOPIC,
    CONF_AVAILABILITY_TOPIC,
    MqttAttributes,
    MqttAvailability,
)
from homeassistant.components.mqtt.subscription import (
    MQTT_SUBSCRIPTION_REGISTRY,
    async_subscribe_topics,
)
from homeassistant.components.mqtt.sensor import PLATFORM_SCHEMA_PREFIX, async_setup_entry_helper

_LOGGER = logging.getLogger(__name__)

SENSOR_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_STATE_TOPIC): cv.string,
        vol.Optional(CONF_AVAILABILITY_TOPIC): cv.string,
        vol.Optional(CONF_QOS, default=0): vol.All(vol.Coerce(int), vol.Range(min=0, max=2)),
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SENSORS): cv.schema_with_slug_keys(SENSOR_SCHEMA),
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    async_add_entities: AddEntitiesCallback,
    discovery_info: Optional[Any] = None,
) -> None:
    """Set up the multi_sensor platform."""

    sensors = [
        MQTTSensor(
            name=sensor_cfg[CONF_NAME],
            state_topic=sensor_cfg[CONF_STATE_TOPIC],
            availability_topic=sensor_cfg.get(CONF_AVAILABILITY_TOPIC),
            qos=sensor_cfg[CONF_QOS],
            unique_id=f"{sensor_cfg[CONF_NAME]}-{sensor_cfg[CONF_STATE_TOPIC]}",
            icon="mdi:chart-line",
        )
        for sensor_cfg in config[CONF_SENSORS].values()
    ]

    async_add_entities(sensors)
    async_subscribe_topics(hass, MQTT_SUBSCRIPTION_REGISTRY, [sensor.subscription_topic for sensor in sensors])


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up MQTT sensors dynamically through MQTT discovery."""

    setup = await async_setup_entry_helper(hass, config_entry, async_add_entities)
    if setup:
        return True

    async def async_discover(discovery_payload):
        """Discover and add an MQTT sensor."""
        discovery_klass = sensor_factory(discovery_payload)

        if discovery_klass is None:
            return

        sensor_name = discovery_payload["name"]
        state_topic = discovery_payload["state_topic"]
        availability_topic = discovery_payload.get("availability_topic")
        qos = discovery_payload.get(CONF_QOS, 0)

        async_add_entities(
            [
                discovery_klass(
                    name=sensor_name,
                    state_topic=state_topic,
                    availability_topic=availability_topic,
                    qos=qos,
                    unique_id=f"{sensor_name}-{state_topic}",
                    icon="mdi:chart-line",
                )
            ]
        )

    # Subscribe to MQTT discovery topics
    await discovery.async_start(
        hass,
        "mqtt",
        async_discover,
        PLATFORM_SCHEMA_PREFIX

