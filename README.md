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

### Period Energy (kWh)
- **Production This Month** — Total energy produced this month
- **Production This Year** — Total energy produced this year
- **Production Total** — Total energy produced (all time)

### Plant Info
- **Plant Name** — Name of the PV installation
- **Plant Capacity** — Rated capacity (W)
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

## Dashboard

A ready-to-use Lovelace dashboard is included in `dashboard/plexlog_dashboard.yaml` that replicates the Plexlog web portal layout with an overview card and 4 chart views (day, month, year, total).

### Setup

1. Open `dashboard/plexlog_dashboard.yaml`
2. Replace all instances of `PLANT_NAME` with your device name slug
   (find it in **Settings > Devices & Services > Plexlog** > click your device > look at any entity ID)
3. In HA, go to **Settings > Dashboards > Add Dashboard**
4. Switch to YAML mode (three dots > Raw configuration editor) and paste the content

### Note on Charts

Charts use HA's built-in long-term statistics and will populate over time from when the integration was installed. For the Total View with true yearly bars, consider installing [apexcharts-card](https://github.com/RomRider/apexcharts-card) via HACS (see commented alternative in the YAML).

## API Documentation

[Plexlog Portal API Documentation](https://doc.plexlog.de/de/dokumentation/portal/plexlog-portal-api/)
