"""Config flow for ISENSIT integration."""
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
        )



"""Config flow for ISENSIT Sensor integration.
from homeassistant import config_entries
from homeassistant.const import CONF_NAME

from .const import DOMAIN


class ISENSITSensorFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a ISENSIT Sensor config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            # Show the configuration form to the user
            return self.async_show_form(
                step_id="user",
                data_schema=self.get_data_schema(),
                errors={},
                description_placeholders={
                    "title": "ISENSIT Sensor Configuration",
                    "description": "Please enter sensor ID"
                },
            )

        # Data has been submitted, create the entity
        return self.async_create_entry(
            title=user_input[CONF_NAME],
            data=user_input,
        )

    def get_data_schema(self):
        """Return the data schema."""
        return {
            config_entries.Optional(CONF_NAME): str,
            config_entries.Required("sensor_id"): str,
        }"""
