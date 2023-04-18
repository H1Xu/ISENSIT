from homeassistant.components.sensor import SensorEntity


class CO2Sensor(SensorEntity):
    """Representation of a CO2 Sensor."""

    def __init__(self, mqtt_client, mqtt_topic, co2_topic):
        """Initialize the sensor."""
        self._mqtt_client = mqtt_client
        self._mqtt_topic = mqtt_topic
        self._co2_topic = co2_topic
        self._state = None

    async def async_added_to_hass(self):
        """Subscribe MQTT events."""
        await self._mqtt_client.async_subscribe(self._co2_topic, self._async_update)

    async def async_will_remove_from_hass(self):
        """Unsubscribe MQTT events."""
        await self._mqtt_client.async_unsubscribe(self._co2_topic)

    async def _async_update(self, topic, payload, qos):
        """Handle MQTT message received."""
        self._state = int(payload)
        self.async_write_ha_state()

    @property
    def name(self):
        """Return the name of the sensor."""
        return "ISENSIT CO2 Sensor"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return "ppm"
