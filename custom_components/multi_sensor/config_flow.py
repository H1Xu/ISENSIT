"""Config flow for ISENSIT integration.
from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from .const import DOMAIN


class ISENSITFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a ISENSIT config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Skip validation
            return self.async_create_entry(title=user_input["sensor_id"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required("sensor_id"): str}
            )
        )"""
from homeassistant import config_entries
from homeassistant.core import callback

class ISENSITFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    ...

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self._show_form(
                description_placeholders={
                    "placeholder_text": "Please enter the sensor ID",
                },
                errors={},
                title="ISENSIT Configuration",
            )

        # Get the sensor ID from the user input
        sensor_id = user_input["sensor_id"]

        # Store the sensor ID in the options
        options = {
            "sensor_id": sensor_id,
        }

        # Create the config entry and return the options
        return self.async_create_entry(title="", data=options)
    
    def _show_form(self, description_placeholders, errors, title):
        """Show the form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "sensor_id",
                        description={"suggested_value": description_placeholders["placeholder_text"]},
                    ): str
                }
            ),
            errors=errors,
            description_placeholders=description_placeholders,
            title=title,
        )

