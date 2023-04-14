import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from .const import DOMAIN, DEFAULT_NAME, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

CONF_DEVICE_ID = "device_id"

@config_entries.HANDLERS.register(DOMAIN)
class ISENSITFlowHandler(config_entries.ConfigFlow):

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Validate Device ID and other inputs here
            is_valid = True  # Replace this with actual validation

            if is_valid:
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            else:
                errors["base"] = "invalid_device_id"

        data_schema = vol.Schema({
            vol.Required(CONF_DEVICE_ID): str,
            vol.Required(CONF_NAME, default=DEFAULT_NAME): str,
            vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )


    def async_get_options_flow(config_entry):
        return ISENSITOptionsFlowHandler(config_entry)

class ISENSITOptionsFlowHandler(config_entries.OptionsFlow):

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Validate and update options here
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({
            vol.Optional("scan_interval", default=self.config_entry.options.get("scan_interval", DEFAULT_SCAN_INTERVAL)): int,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
            errors=errors
        )
