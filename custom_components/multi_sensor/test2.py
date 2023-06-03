"""Hisense TV switch entity"""
import logging

from homeassistant.components import mqtt
from homeassistant.components.switch import DEVICE_CLASS_SWITCH, SwitchEntity
from homeassistant.const import CONF_DEVICE_ID

from .const import DEFAULT_NAME, DOMAIN
from homeassistant.components.media_player.const import (
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Start HisenseTV switch setup process."""
    _LOGGER.debug("async_setup_entry config: %s", config_entry.data)
    name = hass.data[DOMAIN][config_entry.entry_id][CONF_DEVICE_ID]
    uid = hass.data[DOMAIN][config_entry.entry_id][CONF_DEVICE_ID]
    if uid is None:
        uid = config_entry.entry_id

    entity = HisenseTvSwitch(
        hass=hass,
        name=name,
        uid=uid
    )
    async_add_entities([entity])


class HisenseTvSwitch(SwitchEntity):
    """Hisense TV switch entity."""

    def __init__(self, hass, name, uid):
        self.hass = hass
        self.name = name
        self.uid = uid
        self._is_on = False

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        await mqtt.async_publish(
            hass=self._hass,
            topic="/multisensor/MS-IPe0e2e6742eff/peripherals/sound/POST",
            payload='{"mode" : "ON", "duration" : 1000}',
            retain=False,
        )

    async def async_turn_off(self, **kwargs):
        """Turn the entity on."""
        await mqtt.async_publish(
            hass=self._hass,
            topic="/multisensor/MS-IPe0e2e6742eff/peripherals/sound/POST",
            payload='{"mode" : "OFF", "duration" : 1000}',
            retain=False,
        )

    @property
    def is_on(self):
        return self._is_on

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, '123344444')},
            "name": self._name,
            "manufacturer": DEFAULT_NAME,
        }

    @property
    def uid(self):
        """Return the unique id of the device."""
        return self.uid

    @property
    def name(self):
        return self._name

    @property
    def device_class(self):
        _LOGGER.debug("device_class")
        return DEVICE_CLASS_SWITCH

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def supported_features(self):
        """Flag media player features that are supported."""
        _LOGGER.debug("supported_features")
        return (
                SUPPORT_TURN_ON
                | SUPPORT_TURN_OFF
        )
