from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .const import DOMAIN
from .coordinator import GymUpdateCoordinator

PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Configura a integração via UI."""
    coordinator = GymUpdateCoordinator(
        hass,
        username=entry.data["username"],
        password=entry.data["password"],
        socio_id=entry.data["socio_id"]
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Descarrega a integração."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok