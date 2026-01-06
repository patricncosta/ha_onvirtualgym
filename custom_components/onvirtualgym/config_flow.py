import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN, LOGIN_URL

class GymConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Fluxo de configuração via UI."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            # Validar credenciais e obter socio_id antes de criar a entrada
            session = async_get_clientsession(self.hass)
            try:
                async with session.post(LOGIN_URL, json=user_input) as resp:
                    data = await resp.json()
                    if resp.status == 200 and data.get("token"):
                        # Extraímos o socio_id do primeiro cliente no login
                        socio_id = data["loginUserClient"][0]["numSocio"]
                        user_name = data["loginUserClient"][0]["nome"]
                        
                        return self.async_create_entry(
                            title=user_name, 
                            data={**user_input, "socio_id": socio_id}
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