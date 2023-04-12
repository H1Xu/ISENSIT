"""Adds config flow for worlds_air_quality_index integration."""
from __future__ import annotations

from typing import Any

from .waqi_api import WaqiDataRequester

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from homeassistant.const import (
    CONF_NAME,
    CONF_LATITUDE, 
    CONF_LONGITUDE, 
    CONF_TOKEN,
    CONF_LOCATION,
    CONF_METHOD,
    CONF_ID,
    CONF_TEMPERATURE_UNIT,
    TEMP_FAHRENHEIT,
    TEMP_CELSIUS
)
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    GEOGRAPHIC_LOCALIZATION,
    STATION_ID
)


class WorldsAirQualityIndexConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    #Handle a config flow for worlds_air_quality_index integration.

    VERSION = 1

    async def async_step_user(self, user_input = None):
        #Handle the initial step of user input.

        if user_input is None:
        #verify input of users

            return await self.async_step_station_id()
            #if input then call step staion id function
        
        return self.async_show_form(
            step_id = "user",
            data_schema = vol.Schema(
                {
                    vol.Required("station_id"): str,
                    #vol method requires station id to be string
                }),
            )



    async def async_step_station_id(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title = "Sensor ID",
                data = {},
            )
        
        return self.async_show_form(
            step_id = "station_id",
            data_schema = vol.Schema({
                vol.Required("station_id"):str
            }),
        )
