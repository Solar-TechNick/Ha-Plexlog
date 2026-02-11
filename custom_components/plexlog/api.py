"""Plexlog API client."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

import aiohttp

from .const import API_PATH, INTERVAL_DAILY

_LOGGER = logging.getLogger(__name__)


class PlexlogApiError(Exception):
    """Exception for Plexlog API errors."""


class PlexlogAuthError(PlexlogApiError):
    """Exception for authentication errors."""


class PlexlogApi:
    """Client for the Plexlog Portal API."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
        api_key: str,
        plant_id: str,
    ) -> None:
        """Initialize the API client."""
        self._session = session
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._plant_id = plant_id

    def _build_url(self, **params: str) -> str:
        """Build API URL with parameters."""
        base_params = {
            "api_key": self._api_key,
            "plant_id": self._plant_id,
        }
        base_params.update(params)
        query = "&".join(f"{k}={v}" for k, v in base_params.items() if v is not None)
        return f"{self._base_url}{API_PATH}?{query}"

    async def _request(self, **params: str) -> Any:
        """Make an API request."""
        url = self._build_url(**params)
        _LOGGER.debug("Plexlog API request: %s", url.split("api_key=")[0] + "api_key=***")
        try:
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=30), ssl=False) as resp:
                if resp.status == 401 or resp.status == 403:
                    raise PlexlogAuthError("Invalid API key or unauthorized access")
                if resp.status != 200:
                    text = await resp.text()
                    raise PlexlogApiError(
                        f"API request failed with status {resp.status}: {text}"
                    )
                return await resp.json(content_type=None)
        except aiohttp.ClientError as err:
            raise PlexlogApiError(f"Communication error: {err}") from err

    async def async_get_plant_info(self) -> dict[str, Any]:
        """Get plant/installation information (no interval = info only)."""
        return await self._request()

    async def async_get_plant_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        interval: str = INTERVAL_DAILY,
    ) -> dict[str, Any]:
        """Get plant energy data."""
        if from_date is None:
            today = datetime.now()
            from_date = today.strftime("%d.%m.%Y")
        if to_date is None:
            to_date = from_date

        return await self._request(
            **{"from": from_date, "to": to_date, "interval": interval, "type": "plant"}
        )

    async def async_get_inverter_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        interval: str = INTERVAL_DAILY,
    ) -> dict[str, Any]:
        """Get inverter data."""
        if from_date is None:
            today = datetime.now()
            from_date = today.strftime("%d.%m.%Y")
        if to_date is None:
            to_date = from_date

        return await self._request(
            **{"from": from_date, "to": to_date, "interval": interval, "type": "inverter"}
        )

    async def async_get_meter_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        interval: str = INTERVAL_DAILY,
    ) -> dict[str, Any]:
        """Get meter data."""
        if from_date is None:
            today = datetime.now()
            from_date = today.strftime("%d.%m.%Y")
        if to_date is None:
            to_date = from_date

        return await self._request(
            **{"from": from_date, "to": to_date, "interval": interval, "type": "meter"}
        )

    async def async_get_battery_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        interval: str = INTERVAL_DAILY,
    ) -> dict[str, Any]:
        """Get battery data."""
        if from_date is None:
            today = datetime.now()
            from_date = today.strftime("%d.%m.%Y")
        if to_date is None:
            to_date = from_date

        return await self._request(
            **{"from": from_date, "to": to_date, "interval": interval, "type": "battery"}
        )

    async def async_get_wallbox_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        interval: str = INTERVAL_DAILY,
    ) -> dict[str, Any]:
        """Get wallbox/EV charger data."""
        if from_date is None:
            today = datetime.now()
            from_date = today.strftime("%d.%m.%Y")
        if to_date is None:
            to_date = from_date

        return await self._request(
            **{"from": from_date, "to": to_date, "interval": interval, "type": "wallbox"}
        )

    async def async_get_device_data(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        interval: str = INTERVAL_DAILY,
    ) -> dict[str, Any]:
        """Get all device data."""
        if from_date is None:
            today = datetime.now()
            from_date = today.strftime("%d.%m.%Y")
        if to_date is None:
            to_date = from_date

        return await self._request(
            **{"from": from_date, "to": to_date, "interval": interval, "type": "device"}
        )

    async def async_test_connection(self) -> bool:
        """Test the API connection and credentials."""
        try:
            result = await self.async_get_plant_info()
            return result is not None
        except PlexlogAuthError:
            raise
        except PlexlogApiError:
            return False
