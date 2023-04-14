from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries

from homeassistant.helpers.translation import localized

from .const import DOMAIN


class ISENSITFlowHandler(config_entries.ConfigFlow):
    # Handle a config flow for worlds_air_quality_index integration.

    VERSION = 1

    async def async_step_user(self, user_input=None):
        # Handle the initial step of user input.
        errors = {}

        if user_input is not None:
            return self.async_show_form(
                title=localized(self.hass, "component.multi_sensor.title"),
                step_id="user",
                data_schema=vol.Schema(
                    {
                        vol.Required("sensor_id"): str,
                    }
                ),
                errors=errors,
            )

        return self.async_show_form(
            title=localized(self.hass, "component.multi_sensor.title"),
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("sensor_id"): str,
                }
            ),
            errors=errors,
        )

    async def async_step_sensor_id(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Sensor ID",
                data={"sensor_id": user_input["sensor_id"]},
            )

        return self.async_show_form(
            step_id="sensor_id",
            data_schema=vol.Schema({vol.Required("sensor_id"): str}),
        )
