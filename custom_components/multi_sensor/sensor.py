"""Support for hildebrand glow MQTT sensors."""
from __future__ import annotations

import json
import re
import logging
from typing import Iterable

from homeassistant.components import mqtt
from homeassistant.components.mqtt.models import ReceiveMessage
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.entity import DeviceInfo, EntityCategory
from .const import DOMAIN, CONF_TOPIC_PREFIX
from homeassistant.const import (
    CONF_DEVICE_ID,
    ATTR_DEVICE_ID,

    ENERGY_KILO_WATT_HOUR,
    VOLUME_CUBIC_METERS,
    POWER_KILO_WATT,
    SIGNAL_STRENGTH_DECIBELS,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.util import slugify

_LOGGER = logging.getLogger(__name__)

STATE_SENSOR = [
    {
        "name": "Multisensor: CO2",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": VOLUME_CUBIC_METERS,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:MoleculeCo2",
        "func": lambda js: js['value']
    },
    {
        "name": "Multisensor: Temp",
        "device_class": SensorDeviceClass.ENERGY,
        "unit_of_measurement": VOLUME_CUBIC_METERS,
        "state_class": SensorStateClass.MEASUREMENT,
        "icon": "mdi:MoleculeCo2",
        "func": lambda js: js['value']
    }
]

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Smart Meter sensors."""

    # the config is defaulted to + which happens to mean we will subscribe to all devices
    device_mac = hass.data[DOMAIN][config_entry.entry_id][CONF_DEVICE_ID]
    topic_prefix = hass.data[DOMAIN][config_entry.entry_id][CONF_TOPIC_PREFIX] or "glow"

    deviceUpdateGroups = {}

    @callback
    async def mqtt_message_received(message: ReceiveMessage):
        """Handle received MQTT message."""
        topic = message.topic
        payload = message.payload
        device_id = topic.split("/")[1]
        if (device_mac == '+' or device_id == device_mac):
            updateGroups = await async_get_device_groups(deviceUpdateGroups, async_add_entities, device_id)
            _LOGGER.debug("Received message: %s", topic)
            _LOGGER.debug("  Payload: %s", payload)
            for updateGroup in updateGroups:
                updateGroup.process_update(message)

    data_topic = f"/multisensor/MS-IPe0e2e6742eff/measurements/temperature"

    await mqtt.async_subscribe(
        hass, data_topic, mqtt_message_received, 1
    ) 



async def async_get_device_groups(deviceUpdateGroups, async_add_entities, device_id):
    #add to update groups if not already there
    if device_id not in deviceUpdateGroups:
        _LOGGER.debug("New device found: %s", device_id)
        groups = [
            HildebrandGlowMqttSensorUpdateGroup(device_id, "STATE", STATE_SENSOR),
        ]
        async_add_entities(
            [sensorEntity for updateGroup in groups for sensorEntity in updateGroup.all_sensors],
            #True
        )
        deviceUpdateGroups[device_id] = groups

    return deviceUpdateGroups[device_id]
  

class HildebrandGlowMqttSensorUpdateGroup:
    """Representation of Hildebrand Glow MQTT Meter Sensors that all get updated together."""

    def __init__(self, device_id: str, topic_regex: str, meters: Iterable) -> None:
        """Initialize the sensor collection."""
        self._topic_regex = re.compile(topic_regex)
        self._sensors = [HildebrandGlowMqttSensor(device_id = device_id, **meter) for meter in meters]

    def process_update(self, message: ReceiveMessage) -> None:
        """Process an update from the MQTT broker."""
        topic = message.topic
        payload = message.payload
        if (self._topic_regex.search(topic)):
            _LOGGER.debug("Matched on %s", self._topic_regex.pattern)
            parsed_data = json.loads(payload)
            for sensor in self._sensors:
                sensor.process_update(parsed_data)

    @property
    def all_sensors(self) -> Iterable[HildebrandGlowMqttSensor]:
        """Return all meters."""
        return self._sensors

class HildebrandGlowMqttSensor(SensorEntity):
    """Representation of a room sensor that is updated via MQTT."""

    def __init__(self, device_id, name, icon, device_class, unit_of_measurement, state_class, func, entity_category = EntityCategory.CONFIG, ignore_zero_values = False) -> None:
        """Initialize the sensor."""
        self._device_id = device_id
        self._ignore_zero_values = ignore_zero_values
        self._attr_name = name
        self._attr_unique_id = slugify(device_id + "_" + name)
        self._attr_icon = icon
        if (device_class):
          self._attr_device_class = device_class
        if (unit_of_measurement):
          self._attr_native_unit_of_measurement = unit_of_measurement
        if (state_class):
          self._attr_state_class = state_class
        self._attr_entity_category = entity_category
        self._attr_should_poll = False
        
        self._func = func        
        self._attr_device_info = DeviceInfo(
            connections={("mac", device_id)},
            manufacturer="Hildebrand Technology Limited",
            model="Glow Smart Meter IHD",
            name=f"Glow Smart Meter {device_id}",
        )
        self._attr_native_value = None

    def process_update(self, mqtt_data) -> None:
        """Update the state of the sensor."""
        new_value = self._func(mqtt_data)
        if (self._ignore_zero_values and new_value == 0):
            _LOGGER.debug("Ignored new value of %s on %s.", new_value, self._attr_unique_id)
            return
        self._attr_native_value = new_value
        if (self.hass is not None): # this is a hack to get around the fact that the entity is not yet initialized at first
            self.async_schedule_update_ha_state()

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {ATTR_DEVICE_ID: self._device_id}
