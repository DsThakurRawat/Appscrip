import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/analyze/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_token_generation():
    response = client.post("/analyze/token")
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_analyze_unauthorized():
    response = client.get("/analyze/technology")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_analyze_invalid_sector():
    # Get a token first
    token_resp = client.post("/analyze/token").json()
    token = token_resp["access_token"]
    
    # Try an invalid sector (too short)
    response = client.get(
        "/analyze/te", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 422  # Validation error
