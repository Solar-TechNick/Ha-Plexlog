"""Data update coordinator for the Plexlog integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import PlexlogApi, PlexlogApiError, PlexlogAuthError
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, INTERVAL_5MINS

_LOGGER = logging.getLogger(__name__)


class PlexlogCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch data from the Plexlog API."""

    def __init__(self, hass: HomeAssistant, api: PlexlogApi) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.api = api
        self.plant_info: dict[str, Any] = {}

    async def async_setup(self) -> None:
        """Fetch initial plant info."""
        try:
            self.plant_info = await self.api.async_get_plant_info()
        except PlexlogApiError as err:
            _LOGGER.error("Failed to fetch plant info: %s", err)
            self.plant_info = {}

    def _get_today(self) -> str:
        """Get today's date in DD.MM.YYYY format."""
        return datetime.now().strftime("%d.%m.%Y")

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from the Plexlog API."""
        today = self._get_today()
        data: dict[str, Any] = {
            "plant_info": self.plant_info,
            "plant": {},
            "inverter": {},
            "meter": {},
            "battery": {},
            "wallbox": {},
        }

        try:
            # Always fetch plant data (current day, 5-min interval for latest values)
            plant_data = await self.api.async_get_plant_data(
                from_date=today, to_date=today, interval=INTERVAL_5MINS
            )
            _LOGGER.debug("Plexlog plant data (5min) keys: %s", list(plant_data.keys()) if isinstance(plant_data, dict) else type(plant_data))
            _LOGGER.debug("Plexlog plant data (5min) raw: %s", plant_data)
            data["plant"] = self._extract_latest(plant_data)

            # Fetch daily totals for energy sums
            daily_data = await self.api.async_get_plant_data(
                from_date=today, to_date=today
            )
            _LOGGER.debug("Plexlog daily data keys: %s", list(daily_data.keys()) if isinstance(daily_data, dict) else type(daily_data))
            data["plant_daily"] = self._extract_sums(daily_data)

        except PlexlogAuthError as err:
            raise UpdateFailed(f"Authentication failed: {err}") from err
        except PlexlogApiError as err:
            raise UpdateFailed(f"Error fetching plant data: {err}") from err

        # Fetch optional device types based on plant capabilities
        has_battery = self.plant_info.get("has_battery", False)
        has_consumption = self.plant_info.get("has_consumption", False)

        try:
            inverter_data = await self.api.async_get_inverter_data(
                from_date=today, to_date=today, interval=INTERVAL_5MINS
            )
            data["inverter"] = self._extract_device_latest(inverter_data)
        except PlexlogApiError as err:
            _LOGGER.debug("Could not fetch inverter data: %s", err)

        if has_consumption:
            try:
                meter_data = await self.api.async_get_meter_data(
                    from_date=today, to_date=today, interval=INTERVAL_5MINS
                )
                data["meter"] = self._extract_device_latest(meter_data)
            except PlexlogApiError as err:
                _LOGGER.debug("Could not fetch meter data: %s", err)

        if has_battery:
            try:
                battery_data = await self.api.async_get_battery_data(
                    from_date=today, to_date=today, interval=INTERVAL_5MINS
                )
                data["battery"] = self._extract_device_latest(battery_data)
            except PlexlogApiError as err:
                _LOGGER.debug("Could not fetch battery data: %s", err)

        try:
            wallbox_data = await self.api.async_get_wallbox_data(
                from_date=today, to_date=today, interval=INTERVAL_5MINS
            )
            data["wallbox"] = self._extract_device_latest(wallbox_data)
        except PlexlogApiError as err:
            _LOGGER.debug("Could not fetch wallbox data: %s", err)

        return data

    @staticmethod
    def _get_entry_value(entry: dict) -> Any | None:
        """Extract value from a data entry dict (supports both EN and DE keys)."""
        for key in ("value", "Wert"):
            if key in entry:
                return entry[key]
        return None

    def _extract_latest(self, response: Any) -> dict[str, Any]:
        """Extract the latest values from a plant API response.

        The API returns lists of {timestamp, value} pairs per metric.
        We extract the last (most recent) value from each.
        """
        result: dict[str, Any] = {}
        if not isinstance(response, dict):
            return result

        for key, value in response.items():
            if isinstance(value, list) and value:
                last_entry = value[-1]
                if isinstance(last_entry, dict):
                    val = self._get_entry_value(last_entry)
                    if val is not None:
                        result[key] = val
                    else:
                        result[key] = last_entry
                elif isinstance(last_entry, (int, float)):
                    result[key] = last_entry
                else:
                    result[key] = last_entry
            elif isinstance(value, (int, float)):
                result[key] = value
            elif isinstance(value, str):
                result[key] = value

        return result

    def _extract_sums(self, response: Any) -> dict[str, Any]:
        """Extract daily sum values from a daily interval response."""
        result: dict[str, Any] = {}
        if not isinstance(response, dict):
            return result

        for key, value in response.items():
            if isinstance(value, list) and value:
                last_entry = value[-1]
                if isinstance(last_entry, dict):
                    val = self._get_entry_value(last_entry)
                    if val is not None:
                        result[key] = val
                    else:
                        result[key] = last_entry
                elif isinstance(last_entry, (int, float)):
                    result[key] = last_entry
                else:
                    result[key] = last_entry
            elif isinstance(value, (int, float)):
                result[key] = value

        return result

    def _extract_device_latest(self, response: Any) -> dict[str, Any]:
        """Extract the latest values from a device-level API response.

        Device responses may be nested by device name/ID.
        """
        result: dict[str, Any] = {}
        if not isinstance(response, dict):
            return result

        for device_key, device_data in response.items():
            if isinstance(device_data, dict):
                device_result: dict[str, Any] = {}
                for metric_key, metric_value in device_data.items():
                    if isinstance(metric_value, list) and metric_value:
                        last_entry = metric_value[-1]
                        if isinstance(last_entry, dict):
                            val = self._get_entry_value(last_entry)
                            if val is not None:
                                device_result[metric_key] = val
                        elif isinstance(last_entry, (int, float)):
                            device_result[metric_key] = last_entry
                    elif isinstance(metric_value, (int, float)):
                        device_result[metric_key] = metric_value
                result[device_key] = device_result
            elif isinstance(device_data, list) and device_data:
                last_entry = device_data[-1]
                if isinstance(last_entry, dict):
                    val = self._get_entry_value(last_entry)
                    if val is not None:
                        result[device_key] = val
                elif isinstance(last_entry, (int, float)):
                    result[device_key] = last_entry

        return result
