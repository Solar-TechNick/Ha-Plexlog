"""Sensor platform for the Plexlog integration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import PlexlogCoordinator


@dataclass(frozen=True, kw_only=True)
class PlexlogSensorEntityDescription(SensorEntityDescription):
    """Description for a Plexlog sensor."""

    data_path: str  # dot-separated path into coordinator data, e.g. "plant.Ertrag"


# --- Plant power sensors (W, from 5-min interval data) ---
PLANT_POWER_SENSORS: tuple[PlexlogSensorEntityDescription, ...] = (
    PlexlogSensorEntityDescription(
        key="plant_power_production",
        translation_key="plant_power_production",
        data_path="plant.Ertrag",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PlexlogSensorEntityDescription(
        key="plant_power_consumption",
        translation_key="plant_power_consumption",
        data_path="plant.Verbrauch",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PlexlogSensorEntityDescription(
        key="plant_power_grid_feedin",
        translation_key="plant_power_grid_feedin",
        data_path="plant.Einspeisung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PlexlogSensorEntityDescription(
        key="plant_power_grid_consumption",
        translation_key="plant_power_grid_consumption",
        data_path="plant.Bezug",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PlexlogSensorEntityDescription(
        key="plant_power_self_consumption",
        translation_key="plant_power_self_consumption",
        data_path="plant.Eigenverbrauch",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PlexlogSensorEntityDescription(
        key="plant_power_battery_charging",
        translation_key="plant_power_battery_charging",
        data_path="plant.Laden",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    PlexlogSensorEntityDescription(
        key="plant_power_battery_discharging",
        translation_key="plant_power_battery_discharging",
        data_path="plant.Entladen",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
)

# --- Plant daily energy sensors (kWh, from daily interval data) ---
PLANT_ENERGY_SENSORS: tuple[PlexlogSensorEntityDescription, ...] = (
    PlexlogSensorEntityDescription(
        key="plant_energy_production_today",
        translation_key="plant_energy_production_today",
        data_path="plant_daily.Ertrag",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PlexlogSensorEntityDescription(
        key="plant_energy_consumption_today",
        translation_key="plant_energy_consumption_today",
        data_path="plant_daily.Verbrauch",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PlexlogSensorEntityDescription(
        key="plant_energy_grid_feedin_today",
        translation_key="plant_energy_grid_feedin_today",
        data_path="plant_daily.Einspeisung",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PlexlogSensorEntityDescription(
        key="plant_energy_grid_consumption_today",
        translation_key="plant_energy_grid_consumption_today",
        data_path="plant_daily.Bezug",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PlexlogSensorEntityDescription(
        key="plant_energy_self_consumption_today",
        translation_key="plant_energy_self_consumption_today",
        data_path="plant_daily.Eigenverbrauch",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PlexlogSensorEntityDescription(
        key="plant_energy_battery_charged_today",
        translation_key="plant_energy_battery_charged_today",
        data_path="plant_daily.Laden",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    PlexlogSensorEntityDescription(
        key="plant_energy_battery_discharged_today",
        translation_key="plant_energy_battery_discharged_today",
        data_path="plant_daily.Entladen",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
)

# --- Plant info sensors (static/meta data) ---
PLANT_INFO_SENSORS: tuple[PlexlogSensorEntityDescription, ...] = (
    PlexlogSensorEntityDescription(
        key="plant_name",
        translation_key="plant_name",
        data_path="plant_info.Name",
    ),
    PlexlogSensorEntityDescription(
        key="plant_capacity",
        translation_key="plant_capacity",
        data_path="plant_info.Anlagenleistung",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
    ),
    PlexlogSensorEntityDescription(
        key="plant_annual_target",
        translation_key="plant_annual_target",
        data_path="plant_info.Jahressoll",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
    ),
)


def _resolve_data_path(data: dict[str, Any], path: str) -> Any | None:
    """Resolve a dot-separated path in nested dict data."""
    keys = path.split(".")
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Plexlog sensors from a config entry."""
    coordinator: PlexlogCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[PlexlogSensor] = []

    # Add plant power sensors
    for description in PLANT_POWER_SENSORS:
        entities.append(PlexlogSensor(coordinator, entry, description))

    # Add plant energy sensors
    for description in PLANT_ENERGY_SENSORS:
        entities.append(PlexlogSensor(coordinator, entry, description))

    # Add plant info sensors
    for description in PLANT_INFO_SENSORS:
        entities.append(PlexlogSensor(coordinator, entry, description))

    # Add dynamic device sensors for inverters, meters, batteries, wallboxes
    data = coordinator.data or {}
    for device_type in ("inverter", "meter", "battery", "wallbox"):
        device_data = data.get(device_type, {})
        if isinstance(device_data, dict):
            for device_name, metrics in device_data.items():
                if isinstance(metrics, dict):
                    for metric_key in metrics:
                        entities.append(
                            PlexlogDeviceSensor(
                                coordinator,
                                entry,
                                device_type=device_type,
                                device_name=str(device_name),
                                metric_key=str(metric_key),
                            )
                        )

    async_add_entities(entities)


class PlexlogSensor(CoordinatorEntity[PlexlogCoordinator], SensorEntity):
    """Representation of a Plexlog sensor."""

    entity_description: PlexlogSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PlexlogCoordinator,
        entry: ConfigEntry,
        description: PlexlogSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": coordinator.plant_info.get("Name", "Plexlog PV System"),
            "manufacturer": "Plexlog",
            "model": "PV Monitoring System",
        }

    @property
    def native_value(self) -> Any | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return _resolve_data_path(
            self.coordinator.data, self.entity_description.data_path
        )


class PlexlogDeviceSensor(CoordinatorEntity[PlexlogCoordinator], SensorEntity):
    """Representation of a dynamically created device-level Plexlog sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: PlexlogCoordinator,
        entry: ConfigEntry,
        device_type: str,
        device_name: str,
        metric_key: str,
    ) -> None:
        """Initialize the device sensor."""
        super().__init__(coordinator)
        self._device_type = device_type
        self._device_name = device_name
        self._metric_key = metric_key
        self._attr_unique_id = (
            f"{entry.entry_id}_{device_type}_{device_name}_{metric_key}"
        )
        self._attr_translation_key = f"{device_type}_{metric_key}"

        # Determine unit and device class based on metric key
        power_metrics = {"Ertrag", "Verbrauch", "Einspeisung", "Bezug",
                         "Eigenverbrauch", "Laden", "Entladen", "Leistung",
                         "AC_Leistung", "DC_Leistung"}
        if metric_key in power_metrics:
            self._attr_native_unit_of_measurement = UnitOfPower.WATT
            self._attr_device_class = SensorDeviceClass.POWER
            self._attr_state_class = SensorStateClass.MEASUREMENT

        # Device info groups sensors under device
        self._attr_device_info = {
            "identifiers": {(DOMAIN, f"{entry.entry_id}_{device_type}_{device_name}")},
            "name": f"{device_name}",
            "manufacturer": "Plexlog",
            "model": device_type.capitalize(),
            "via_device": (DOMAIN, entry.entry_id),
        }

        # Human-readable name
        self._attr_name = f"{metric_key}"

    @property
    def native_value(self) -> Any | None:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        device_data = self.coordinator.data.get(self._device_type, {})
        if isinstance(device_data, dict):
            metrics = device_data.get(self._device_name, {})
            if isinstance(metrics, dict):
                return metrics.get(self._metric_key)
        return None
