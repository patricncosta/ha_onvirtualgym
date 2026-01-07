import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, LOGIN_URL

class GymConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configuration flow via UI."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validate credentials and get Member ID before creating an entry
            session = async_get_clientsession(self.hass)
            try:
                async with session.post(LOGIN_URL, json=user_input) as resp:
                    data = await resp.json()
                    if resp.status == 200 and data.get("token"):
                        # We extract the Member ID and Full Name of the first client at the login
                        member_id = data["loginUserClient"][0]["numSocio"]
                        member_name = data["loginUserClient"][0]["nome"]
                        
                        return self.async_create_entry(
                            title=user_input["username"], 
                            data={**user_input, "member_id": member_id, "member_name": member_name}
                        )
                    errors["base"] = "invalid_auth"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
            }),
            errors=errors,
        )