from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Configura os sensores."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([GymAttendancesSensor(coordinator)])

class GymAttendancesSensor(CoordinatorEntity, SensorEntity):
    """Sensor de Presenças Mensais."""

    def __init__(self, coordinator):
        """Inicializa o sensor."""
        super().__init__(coordinator)
        self._attr_translation_key = "ginasio_presencas_mensais"
        self._attr_unique_id = f"ginasio_{coordinator.socio_id}_presencas"
        self._attr_native_unit_of_measurement = "Treinos"
        self._attr_icon = "mdi:dumbbell"
        self._attr_has_entity_name = True

    @property
    def native_value(self):
        """Retorna o número de treinos (contagem / 2)."""
        return self.coordinator.data.get("count")

    @property
    def extra_state_attributes(self):
        """Atributos formatados."""
        history = self.coordinator.data.get("raw_data", [])
        
        attrs = {
            "history": history,
            "total_events": len(history)
        }

        if history:
            # Assume que o primeiro da lista é o mais recente
            attrs["last_activity"] = f"{history[0]['event']} at {history[0]['time']}"
            attrs["last_day"] = history[0]['date']

        return attrs