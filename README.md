# Plexlog Integration for Home Assistant

Custom Home Assistant integration for [Plexlog](https://www.plexlog.de/) PV monitoring systems.

Fetches all stats from your PV system via the Plexlog Portal API and makes them available as Home Assistant sensors.

## Sensors

### Real-time Power (W)
- **Production Power** — Current PV production
- **Consumption Power** — Current total consumption
- **Grid Feed-in Power** — Current power exported to the grid
- **Grid Consumption Power** — Current power drawn from the grid
- **Self-Consumption Power** — Current self-consumed power
- **Battery Charging Power** — Current battery charge rate
- **Battery Discharging Power** — Current battery discharge rate

### Daily Energy (kWh)
- **Production Today** — Total energy produced today
- **Consumption Today** — Total energy consumed today
- **Grid Feed-in Today** — Total energy exported to grid today
- **Grid Consumption Today** — Total energy drawn from grid today
- **Self-Consumption Today** — Total self-consumed energy today
- **Battery Charged Today** — Total energy charged into battery today
- **Battery Discharged Today** — Total energy discharged from battery today

### Plant Info
- **Plant Name** — Name of the PV installation
- **Plant Capacity** — Rated capacity (kW)
- **Annual Target** — Annual production target (kWh)

### Device Sensors
Automatically creates sensors for each **inverter**, **meter**, **battery**, and **wallbox** connected to your system.

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the three dots in the top right corner → **Custom repositories**
3. Add `https://github.com/Solar-TechNick/Ha-Plexlog` as **Integration**
4. Search for "Plexlog" and install
5. Restart Home Assistant

### Manual

1. Copy the `custom_components/plexlog/` folder into your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**
2. Search for **Plexlog**
3. Enter:
   - **Portal URL** — Your Plexlog portal URL (e.g. `https://yourreseller.data4.plexlog.de`)
   - **API Key** — Created in the portal under *Anlageneinstellungen*
   - **Plant ID** — Numeric ID visible in the dashboard URL
4. The integration will verify the connection and create all sensors

## API Documentation

[Plexlog Portal API Documentation](https://doc.plexlog.de/de/dokumentation/portal/plexlog-portal-api/)
