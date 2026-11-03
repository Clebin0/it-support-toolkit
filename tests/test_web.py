from fastapi.testclient import TestClient

import web_app
from web_app import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_serves_portuguese_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "IT Support Toolkit" in response.text
    assert 'lang="pt-BR"' in response.text


def test_diagnostic_returns_report(monkeypatch):
    fake = {"hostname": "LAB-01", "recommendations": ["Coleta de teste."]}
    monkeypatch.setattr(web_app, "build_report", lambda: fake)
    response = client.get("/diagnostic")
    assert response.status_code == 200
    assert response.json()["hostname"] == "LAB-01"


def test_diagnostic_hides_internal_exception(monkeypatch):
    def fail():
        raise RuntimeError("sensitive local detail")
    monkeypatch.setattr(web_app, "build_report", fail)
    response = client.get("/diagnostic")
    assert response.status_code == 500
    assert "sensitive local detail" not in response.text
    assert "coleta" in response.json()["detail"].lower()
