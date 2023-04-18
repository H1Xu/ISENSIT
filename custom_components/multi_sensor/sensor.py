from homeassistant.components.sensor import SensorEntity


class MultiSensorEntity(CoordinatorEntity):
    """Representation of a MultiSensor entity."""

    def __init__(self, coordinator, config_entry, sensor_type):
        """Initialize the MultiSensor entity."""
        super().__init__(coordinator)
        self._config_entry = config_entry
        self._sensor_type = sensor_type
        self._attr_extra_state_attributes = {ATTR_SENSOR_TYPE: sensor_type}

    async def async_update(self):
        """Update the state of the entity."""
        await super().async_update()

        if self._sensor_type == "co2":
            self._attr_state = self.hass.data[DOMAIN].get("co2")
