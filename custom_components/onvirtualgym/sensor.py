
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
        self._attr_translation_key = "onvirtualgym_monthly_attendances"
        self._attr_translation_placeholders = {"member_name": coordinator.member_name}
        self._attr_unique_id = f"onvirtualgym_{coordinator.member_id}_attendances"
        self._attr_icon = "mdi:dumbbell"
        self._attr_has_entity_name = False

    @property
    def native_value(self):
        """Returns the number of workouts (activity count / 2)."""
        return self.coordinator.data.get("count")

    @property
    def extra_state_attributes(self):
        """Formatted attributes for dashboard."""
        history = self.coordinator.data.get("raw_data", [])
        attrs = {"history": history}

        if history:
            # Last activity
            last_activity = history[0]
            attrs["event"] = last_activity.get("label1")
            attrs["time"] = last_activity.get("hora")
            attrs["date"] = last_activity.get("data")
            attrs["last_activity"] = f"{attrs['event']} - {attrs['time']}"
            
        return attrs