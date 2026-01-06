from datetime import timedelta, datetime
import logging
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import LOGIN_URL, TASKS_URL

_LOGGER = logging.getLogger(__name__)

class GymUpdateCoordinator(DataUpdateCoordinator):
    """Gere a atualização de dados via API."""

    def __init__(self, hass, username, password, socio_id):
        super().__init__(
            hass, 
            _LOGGER, 
            name="Ginasio Data", 
            update_interval=timedelta(hours=1)
        )
        self.username = username
        self.password = password
        self.socio_id = socio_id
        self.token = None
        self.session = async_get_clientsession(hass)

    async def _async_get_token(self):
        """Faz login para obter novo token."""
        payload = {"username": self.username, "password": self.password}
        async with self.session.post(LOGIN_URL, json=payload) as resp:
            data = await resp.json()
            return data.get("token")

    async def _async_update_data(self):
        """Centraliza todos os pedidos à API."""
        try:
            async with async_timeout.timeout(15):
                # 1. Atualizar Token
                self.token = await self._async_get_token()
                if not self.token:
                    raise UpdateFailed("Falha na autenticação")

                # 2. Obter Presenças
                inicio = datetime.now().strftime('%Y-%m-01')
                fim = (datetime.now().replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                
                params = {
                    "fk_numSocio": self.socio_id,
                    "method": "getAllAppointmentsByClientByPageOrDate",
                    "dataInicio": inicio,
                    "dataFim": fim.strftime('%Y-%m-%d'),
                    "filter": "5,9",
                    "version": "10"
                }
                headers = {"Authorization": f"Bearer {self.token}"}

                async with self.session.get(TASKS_URL, params=params, headers=headers) as resp:
                    res_json = await resp.json()
                    presencas_lista = res_json.get("getAllAppointmentsByClientByPageOrDate", [])
                    
                    return {
                        "count": int(len(presencas_lista) / 2),
                        "raw_data": presencas_lista
                    }
        except Exception as err:
            raise UpdateFailed(f"Erro ao comunicar com API: {err}")