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
        super().__init__(coordinator)
        self._attr_translation_key = "ginasio_presencas_mensais"
        self._attr_unique_id = f"ginasio_{coordinator.socio_id}_presencas"
        self._attr_native_unit_of_measurement = "Treinos"
        self._attr_icon = "mdi:dumbbell"
        self._attr_has_entity_name = True # Isto faz com que o nome seja [Nome da Integração] [Nome da Entidade]

    @property
    def native_value(self):
        """Retorna o número de treinos (contagem / 2)."""
        return self.coordinator.data.get("count")

    @property
    def extra_state_attributes(self):
        """Atributos extra para ver detalhes das entradas/saídas."""
        return {"historico": self.coordinator.data.get("raw_data")}