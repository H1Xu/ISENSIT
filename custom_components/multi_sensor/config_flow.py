"""Adds config flow for worlds_air_quality_index integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
)


class WorldsAirQualityIndexConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    #Handle a config flow for worlds_air_quality_index integration.

    VERSION = 1

    async def async_step_user(self, user_input = None):
        #Handle the initial step of user input.

        if user_input is None:
        #verify input of users

            return await self.async_step_station_id(title = "Welcome to ISENSIT", data = user_input)
            #if input then call step staion id function
        
        return self.async_show_form(
            step_id = "user",
            data_schema = vol.Schema(
                {
                    vol.Required("station_id", description = "Sensor ID"): str,
                    #vol method requires station id to be string
                }
            ),
             description_placeholders={
                "Sensor ID"
            },
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
