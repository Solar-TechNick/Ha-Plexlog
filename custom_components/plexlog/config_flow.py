"""Config flow for the Plexlog integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import PlexlogApi, PlexlogApiError, PlexlogAuthError
from .const import CONF_API_KEY, CONF_BASE_URL, CONF_PLANT_ID, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_BASE_URL, description={"suggested_value": "http://"}): str,
        vol.Required(CONF_API_KEY): str,
        vol.Required(CONF_PLANT_ID): str,
    }
)


class PlexlogConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Plexlog."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Normalize URL
            base_url = user_input[CONF_BASE_URL].rstrip("/")
            if not base_url.startswith(("http://", "https://")):
                base_url = f"http://{base_url}"
            user_input[CONF_BASE_URL] = base_url

            # Check for duplicate entries
            await self.async_set_unique_id(
                f"{user_input[CONF_PLANT_ID]}_{base_url}"
            )
            self._abort_if_unique_id_configured()

            # Test the connection
            session = async_get_clientsession(self.hass)
            api = PlexlogApi(
                session=session,
                base_url=base_url,
                api_key=user_input[CONF_API_KEY],
                plant_id=user_input[CONF_PLANT_ID],
            )

            try:
                await api.async_test_connection()
            except PlexlogAuthError:
                errors["base"] = "invalid_auth"
            except PlexlogApiError:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected exception during config flow")
                errors["base"] = "unknown"
            else:
                # Try to get plant name for the entry title
                title = f"Plexlog {user_input[CONF_PLANT_ID]}"
                try:
                    plant_info = await api.async_get_plant_info()
                    if isinstance(plant_info, dict) and "name" in plant_info:
                        title = plant_info["name"]
                except Exception:
                    pass

                return self.async_create_entry(title=title, data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
