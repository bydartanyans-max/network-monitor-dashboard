# Network Monitor Dashboard

A portfolio-ready Flask dashboard for visualizing network device health, latency, uptime and operational alerts.

## Features
- Responsive monitoring dashboard
- Device status overview: online / warning / offline
- Simulated live latency updates for demo purposes
- Uptime and average-latency KPIs
- Active alert panel
- Device filtering by status and type
- Device detail endpoint
- REST endpoints for devices, summaries and alerts
- Environment-based configuration
- Automated tests with pytest
- GitHub Actions CI
- Docker support
- Health-check endpoint

> The included data is simulated for demonstration. The project does **not** scan external networks or probe real devices by default.

## Tech Stack
- Python 3.12
- Flask
- HTML / CSS / JavaScript
- REST / JSON APIs
- pytest
- GitHub Actions
- Docker

## API
- `GET /api/devices` — list devices
- `GET /api/devices?status=offline` — filter by status
- `GET /api/devices?type=server` — filter by type
- `GET /api/devices/<id>` — device detail
- `GET /api/summary` — monitoring KPIs
- `GET /api/alerts` — active warnings and critical alerts
- `GET /health` — service health check

## Configuration

```bash
PORT=5000
SIMULATE_JITTER=true
FLASK_DEBUG=false
```

Set `SIMULATE_JITTER=false` for deterministic API responses, for example during automated tests.

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`.

## Run Tests

```bash
pip install -r requirements-dev.txt
pytest -q
```

## Docker

```bash
docker build -t network-monitor-dashboard .
docker run -p 5000:5000 network-monitor-dashboard
```

## Portfolio Purpose

This project demonstrates REST API design, operational dashboard development, asynchronous front-end refresh, alert modeling, API filtering, automated testing, CI and containerization.
