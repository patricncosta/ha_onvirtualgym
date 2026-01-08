
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Setup the sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([GymAttendancesSensor(coordinator)])

class GymAttendancesSensor(CoordinatorEntity, SensorEntity):
    """Monthly Attendances Sensor."""

    def __init__(self, coordinator):
        super().__init__(coordinator)
        self.entity_id = f"sensor.{coordinator.username.lower().replace(" ", "_").replace(".", "_")}_attendances"
        self._attr_translation_key = "onvirtualgym_monthly_attendances"
        self._attr_unique_id = f"onvirtualgym_{coordinator.member_id}_attendances"
        self._attr_icon = "mdi:dumbbell"
        self._attr_has_entity_name = True

    @property
    def native_value(self):
        """Returns the number of workouts (activity count / 2)."""
        return self.coordinator.data.get("count")

    @property
    def extra_state_attributes(self):
        """Formatted attributes for dashboard."""
        sessions = self.coordinator.data.get("sessions", [])
        attrs = {"history": sessions}
            
        return attrs

    # @property
    # def translation_placeholders(self):
    #     """Sets the values for the variables in the location files."""
    #     return {
    #         "member_name": self.coordinator.member_name
    #     }