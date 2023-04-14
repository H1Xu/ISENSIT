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



"""Config flow for multi-sensor integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME
from .const import DOMAIN


class MultiSensorFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for multi-sensor."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self._show_form()

        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data={CONF_NAME: user_input[CONF_NAME]},
        )

    @callback
    def _show_form(self, errors=None):
        """Show the form to the user."""
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {vol.Required(CONF_NAME, default="Station ID"): str}
            ),
            errors=errors,
            description_placeholders={
                "title": "Multi-sensor integration configuration"
            },
        )
