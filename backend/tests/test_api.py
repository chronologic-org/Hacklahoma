import pytest
from fastapi.testclient import TestClient
from ..src.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_integration_plan_endpoint():
    response = client.post(
        "/api/integration/plan",
        json={"user_input": "Connect Weather API with SMS API"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "plan" in data
    assert "supervisor_output" in data
    assert "code_output" in data
    assert "test_output" in data
    assert "evaluation" in data 