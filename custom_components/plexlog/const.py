"""Constants for the Plexlog integration."""

from datetime import timedelta

DOMAIN = "plexlog"

CONF_API_KEY = "api_key"
CONF_PLANT_ID = "plant_id"
CONF_BASE_URL = "base_url"

DEFAULT_SCAN_INTERVAL = timedelta(minutes=5)

API_PATH = "/api/pl/"

# API type parameter values
TYPE_PLANT = "plant"
TYPE_INVERTER = "inverter"
TYPE_METER = "meter"
TYPE_BATTERY = "battery"
TYPE_WALLBOX = "wallbox"
TYPE_SENSOR = "sensor"
TYPE_DEVICE = "device"

# API interval parameter values
INTERVAL_5MINS = "5mins"
INTERVAL_15MINS = "15mins"
INTERVAL_DAILY = "daily"
INTERVAL_MONTHLY = "monthly"
INTERVAL_YEARLY = "yearly"
