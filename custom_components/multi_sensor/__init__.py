"""The worlds_air_quality_index component."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import (
    HomeAssistant
)
from homeassistant.const import (
    CONF_LATITUDE, 
    CONF_LONGITUDE, 
    CONF_LOCATION,
    CONF_METHOD,
    CONF_ID,
    CONF_TEMPERATURE_UNIT,
    TEMP_CELSIUS
)

from .const import (
    PLATFORMS
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up World's Air Quality Index from a config entry."""

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(update_listener))
    return True


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload worlds_air_quality_index config entry."""

    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

async def async_migrate_entry(hass, config_entry):
    """Migrate worlds_air_quality_index old entry."""
    config_entries = hass.config_entries
    data = config_entry.data
    version = config_entry.version

    _LOGGER.debug("Migrating World's Air Quality Index entry from version %s", version)


    _LOGGER.info("Migration to version %s successful", version)

    return True
