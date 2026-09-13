from __future__ import annotations

import os
import random
from datetime import datetime, timezone

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

DEVICES = [
    {"id": 1, "name": "Core Router", "ip": "192.168.1.1", "type": "Router", "status": "online", "latency": 7, "uptime": 99.99},
    {"id": 2, "name": "Office Switch", "ip": "192.168.1.10", "type": "Switch", "status": "online", "latency": 3, "uptime": 99.97},
    {"id": 3, "name": "API Server", "ip": "10.0.0.21", "type": "Server", "status": "warning", "latency": 86, "uptime": 99.81},
    {"id": 4, "name": "Backup Server", "ip": "10.0.0.22", "type": "Server", "status": "online", "latency": 18, "uptime": 99.92},
    {"id": 5, "name": "Warehouse AP", "ip": "192.168.2.14", "type": "Access Point", "status": "offline", "latency": None, "uptime": 97.34},
]
VALID_STATUSES = {"online", "warning", "offline"}


def jitter_enabled() -> bool:
    return os.getenv("SIMULATE_JITTER", "true").lower() in {"1", "true", "yes", "on"}


def serialize_device(device: dict) -> dict:
    item = dict(device)
    if jitter_enabled() and item["status"] != "offline" and item["latency"] is not None:
        item["latency"] = max(1, item["latency"] + random.randint(-3, 5))
    return item


@app.get("/")
def dashboard():
    return render_template("dashboard.html")


@app.get("/api/devices")
def devices():
    status = request.args.get("status", "").strip().lower()
    device_type = request.args.get("type", "").strip().lower()

    results = DEVICES
    if status:
        if status not in VALID_STATUSES:
            return jsonify({"error": "invalid status"}), 400
        results = [d for d in results if d["status"] == status]
    if device_type:
        results = [d for d in results if d["type"].lower() == device_type]

    return jsonify([serialize_device(device) for device in results])


@app.get("/api/devices/<int:device_id>")
def device_detail(device_id: int):
    device = next((d for d in DEVICES if d["id"] == device_id), None)
    if device is None:
        return jsonify({"error": "device not found"}), 404
    return jsonify(serialize_device(device))


@app.get("/api/summary")
def summary():
    total = len(DEVICES)
    online = sum(d["status"] == "online" for d in DEVICES)
    warning = sum(d["status"] == "warning" for d in DEVICES)
    offline = sum(d["status"] == "offline" for d in DEVICES)
    latencies = [d["latency"] for d in DEVICES if d["latency"] is not None]
    avg_latency = round(sum(latencies) / len(latencies), 1) if latencies else None

    return jsonify(
        {
            "total": total,
            "online": online,
            "warning": warning,
            "offline": offline,
            "avg_latency": avg_latency,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/api/alerts")
def alerts():
    active_alerts = []
    for device in DEVICES:
        if device["status"] == "offline":
            active_alerts.append(
                {
                    "severity": "critical",
                    "device_id": device["id"],
                    "device": device["name"],
                    "message": "Device is unreachable",
                }
            )
        elif device["status"] == "warning":
            active_alerts.append(
                {
                    "severity": "warning",
                    "device_id": device["id"],
                    "device": device["name"],
                    "message": "Latency is above threshold",
                }
            )
    return jsonify(active_alerts)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "network-monitor-dashboard"})


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5000")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true",
    )
