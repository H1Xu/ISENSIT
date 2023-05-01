"""Constants for the World Air Quality Index integration."""

from datetime import timedelta

from typing import Final

from homeassistant.const import (
    TEMP_CELSIUS,
    PRESSURE_HPA,
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    DEGREE,
    SPEED_METERS_PER_SECOND,
    LENGTH_MILLIMETERS,
    PERCENTAGE,
    Platform
)
from homeassistant.components.sensor import SensorDeviceClass

DOMAIN = "ISENSIT"
