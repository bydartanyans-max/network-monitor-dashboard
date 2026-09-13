import importlib

import pytest


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("SIMULATE_JITTER", "false")
    import app as app_module

    importlib.reload(app_module)
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_devices_list(client):
    response = client.get("/api/devices")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 5
    assert data[0]["name"] == "Core Router"


def test_filter_by_status(client):
    response = client.get("/api/devices?status=offline")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["status"] == "offline"


def test_invalid_status(client):
    response = client.get("/api/devices?status=broken")
    assert response.status_code == 400


def test_device_detail(client):
    response = client.get("/api/devices/3")
    assert response.status_code == 200
    assert response.get_json()["name"] == "API Server"


def test_missing_device(client):
    response = client.get("/api/devices/999")
    assert response.status_code == 404


def test_summary(client):
    response = client.get("/api/summary")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 5
    assert data["online"] == 3
    assert data["warning"] == 1
    assert data["offline"] == 1


def test_alerts(client):
    response = client.get("/api/alerts")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    severities = {item["severity"] for item in data}
    assert severities == {"critical", "warning"}
