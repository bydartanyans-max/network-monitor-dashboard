# Network Monitor Dashboard

A portfolio-ready Flask dashboard for visualizing network device health, latency, uptime and operational alerts.

## Features
- Responsive operations dashboard
- Device status overview (online / warning / offline)
- Live demo latency updates with 5-second refresh
- Uptime and average-latency KPIs
- Active alert panel
- REST endpoints for devices, summaries and alerts
- Health-check endpoint

> The included data is simulated for demonstration. The project does **not** scan external networks or probe real devices by default.

## Stack
Python, Flask, HTML, CSS, JavaScript

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## API
- `GET /api/devices`
- `GET /api/summary`
- `GET /api/alerts`
- `GET /health`

## Portfolio purpose
Demonstrates backend API design, dashboard UI, asynchronous data refresh, operational monitoring concepts and clean Flask project structure.
