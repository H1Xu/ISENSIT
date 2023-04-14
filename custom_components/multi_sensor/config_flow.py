"""Adds config flow for worlds_air_quality_index integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from homeassistant.helpers.translation import localized

from .const import (
    DOMAIN,
)


class WorldsAirQualityIndexConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    #Handle a config flow for worlds_air_quality_index integration.

    VERSION = 1

    async def async_step_user(self, user_input = None):
        #Handle the initial step of user input.
        errors = {}

        if user_input is None:
        #verify input of users

            return await self.async_step_sensor_id()
            #if input then call step staion id function
        
        return self.async_show_form(
            title = localized(self.hass, "componenet.multi_sensor.title"),
            step_id = "user",
            data_schema = vol.Schema(
                {
                    vol.Required("sensor_id"): str,
                    #vol method requires station id to be string
                }
            ),
        )
        



    async def async_step_sensor_id(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title = "sensor ID",
                data = {},
            )
        
        return self.async_show_form(
            step_id = "sensor_id",
            data_schema = vol.Schema({
                vol.Required("sensor_id"):str
            }),
        )
