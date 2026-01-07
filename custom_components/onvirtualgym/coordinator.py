from datetime import timedelta, datetime
import logging
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import LOGIN_URL, TASKS_URL

_LOGGER = logging.getLogger(__name__)

class GymUpdateCoordinator(DataUpdateCoordinator):
    """Manages the data update via API."""

    def __init__(self, hass, username, password, member_id):
        super().__init__(
            hass, 
            _LOGGER, 
            name=f"OnVirtualGym ({username})",
            update_interval=timedelta(hours=1)
        )
        self.username = username
        self.password = password
        self.member_id = member_id
        self.member_name = member_name
        self.token = None
        self.session = async_get_clientsession(hass)

    async def _async_get_token(self):
        """Performs login to retrieve new token."""
        payload = {"username": self.username, "password": self.password}
        async with self.session.post(LOGIN_URL, json=payload) as resp:
            data = await resp.json()
            return data.get("token")

    async def _async_update_data(self):
        """Centralizes all API requests."""
        try:
            async with async_timeout.timeout(15):
                # 1. Update Token
                self.token = await self._async_get_token()
                if not self.token:
                    raise UpdateFailed("Auth failed")

                # 2. Get Attendances
                start = datetime.now().strftime('%Y-%m-01')
                end = (datetime.now().replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
                
                params = {
                    "fk_numSocio": self.member_id,
                    "method": "getAllAppointmentsByClientByPageOrDate",
                    "dataInicio": start,
                    "dataFim": end.strftime('%Y-%m-%d'),
                    "filter": "5,9",
                    "version": "10"
                }
                headers = {"Authorization": f"Bearer {self.token}"}

                async with self.session.get(TASKS_URL, params=params, headers=headers) as resp:
                    res_json = await resp.json()
                    attendances_list = res_json.get("getAllAppointmentsByClientByPageOrDate", [])
                    
                    clean_history = []
                    for record in attendances_list[0]:
                        clean_history.append({
                            "event": record.get("label1"),
                            "date": record.get("data"),
                            "time": record.get("hora")
                        })
                    
                    return {
                        "count": int(len(attendances_list) / 2),
                        "raw_data": clean_history
                    }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")