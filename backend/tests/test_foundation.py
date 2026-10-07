import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import check_db_connection
from app.core.redis import redis_manager

client = TestClient(app)

def test_liveness_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

def test_api_v1_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"

def test_readiness_probe():
    response = client.get("/api/v1/ready")
    assert response.status_code in [200, 503]
    data = response.json()
    assert "database" in data
    assert "redis" in data

def test_db_connection_ping():
    db_res = check_db_connection()
    assert db_res["status"] == "healthy"

def test_redis_fallback():
    redis_res = redis_manager.check_connection()
    assert redis_res["status"] == "healthy"
