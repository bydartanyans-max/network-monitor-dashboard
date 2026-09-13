from flask import Flask, jsonify, render_template
from datetime import datetime, timezone
import random

app = Flask(__name__)

DEVICES = [
    {"id": 1, "name": "Core Router", "ip": "192.168.1.1", "type": "Router", "status": "online", "latency": 7, "uptime": 99.99},
    {"id": 2, "name": "Office Switch", "ip": "192.168.1.10", "type": "Switch", "status": "online", "latency": 3, "uptime": 99.97},
    {"id": 3, "name": "API Server", "ip": "10.0.0.21", "type": "Server", "status": "warning", "latency": 86, "uptime": 99.81},
    {"id": 4, "name": "Backup Server", "ip": "10.0.0.22", "type": "Server", "status": "online", "latency": 18, "uptime": 99.92},
    {"id": 5, "name": "Warehouse AP", "ip": "192.168.2.14", "type": "Access Point", "status": "offline", "latency": None, "uptime": 97.34},
]

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.get("/api/devices")
def devices():
    # Demo jitter so the dashboard feels live without probing real hosts.
    payload = []
    for device in DEVICES:
        item = dict(device)
        if item["status"] != "offline" and item["latency"] is not None:
            item["latency"] = max(1, item["latency"] + random.randint(-3, 5))
        payload.append(item)
    return jsonify(payload)

@app.get("/api/summary")
def summary():
    total = len(DEVICES)
    online = sum(d["status"] == "online" for d in DEVICES)
    warning = sum(d["status"] == "warning" for d in DEVICES)
    offline = sum(d["status"] == "offline" for d in DEVICES)
    latencies = [d["latency"] for d in DEVICES if d["latency"] is not None]
    return jsonify({
        "total": total,
        "online": online,
        "warning": warning,
        "offline": offline,
        "avg_latency": round(sum(latencies) / len(latencies), 1),
        "checked_at": datetime.now(timezone.utc).isoformat()
    })

@app.get("/api/alerts")
def alerts():
    alerts = []
    for d in DEVICES:
        if d["status"] == "offline":
            alerts.append({"severity": "critical", "device": d["name"], "message": "Device is unreachable"})
        elif d["status"] == "warning":
            alerts.append({"severity": "warning", "device": d["name"], "message": "Latency is above threshold"})
    return jsonify(alerts)

@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "network-monitor-dashboard"})

if __name__ == "__main__":
    app.run(debug=True)
