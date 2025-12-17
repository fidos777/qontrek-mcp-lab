"""
Test KuasaTurbo Gateway Health Endpoints
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from starlette.testclient import TestClient
from kuasaturbo.api.gateway import app

client = TestClient(app)


def test_root_endpoint():
    """Test root health check"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "KuasaTurbo Gateway"
    assert data["version"] == "1.0.0"
    assert data["status"] == "operational"
    print("✓ Root endpoint working")


def test_health_endpoint():
    """Test detailed health check"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "components" in data
    assert data["components"]["api"] == "operational"
    print("✓ Health endpoint working")


if __name__ == "__main__":
    test_root_endpoint()
    test_health_endpoint()
    print("\n✅ All health tests passed")
