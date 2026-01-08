from datetime import timedelta, datetime
import logging
import async_timeout
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import LOGIN_URL, TASKS_URL

_LOGGER = logging.getLogger(__name__)

class GymUpdateCoordinator(DataUpdateCoordinator):
    """Manages the data update via API."""

    def __init__(self, hass, username, password, member_id, member_name):
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
        try:
            async with self.session.post(LOGIN_URL, json=payload, timeout=10) as resp:
                # If it's not 200 OK, log the error to know what API tells
                if resp.status != 200:
                    text = await resp.text()
                    _LOGGER.error("Error logging in (Status %s): %s", resp.status, text)
                    return None
                
                data = await resp.json()
                return data.get("token")
        except Exception as e:
            _LOGGER.error("Network error trying to login: %s", e)
            return None

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
                    if resp.status != 200:
                        raise UpdateFailed(f"API answered with status {resp.status}")
                        
                    res_json = await resp.json()
                    events_list = res_json.get("getAllAppointmentsByClientByPageOrDate", [])
                    sessions = []
                    i = 0

                    while i < len(events_list):
                        current_event = events_list[i]
                        
                        # We are looking for an Exit (9) with an Entry (5) next to it
                        if current_event.get("type") == "9" and (i + 1) < len(events_list):
                            next_event = events_list[i+1]
                            
                            if next_event.get("type") == "5":
                                duration_minutes = 0
                                try:
                                    fmt = "%Y-%m-%d %H:%M:%S"
    
                                    # Clean strings (remove 'Z' if it exists)
                                    start_str = f"{current_event.get('data')} {next_event.get('hora').replace('Z', '')}"
                                    exit_str = f"{current_event.get('data')} {current_event.get('hora').replace('Z', '')}"
                                    
                                    entry_time = datetime.strptime(start_str, fmt)
                                    exit_time = datetime.strptime(exit_str, fmt)
                                    
                                    # 2. Calcular a diferença
                                    duration = exit_time - entry_time
                                    duration_minutes = round(duration.total_seconds() / 60)
                                    
                                    # Validação: se o ginásio registar saída antes da entrada (erro de log), pomos 0
                                    if duration_minutes < 0:
                                        duration_minutes = 0
                                except (ValueError, TypeError, AttributeError) as e:
                                    _LOGGER.debug("Error processing sessions times: %s", e)
                                    duration_minutes = 0

                                sessions.append({
                                    "date": current_event.get("data"),
                                    "start": next_event.get("hora"),
                                    "exit": current_event.get("hora"),
                                    "duration": duration_minutes
                                })
                                i += 2
                                continue
                        
                        i += 1

                    return {
                        "count": len(sessions),
                        "sessions": sessions
                    }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")