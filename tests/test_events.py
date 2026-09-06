import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_ingest_event_unauthorized(client):
    payload = {
        "source": "test_service",
        "event_type": "ping",
        "priority": "low",
        "payload": {"data": "test"}
    }
    # No API key header provided -> should be 403
    response = await client.post("/api/v1/events/ingest", json=payload)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_ingest_event_authorized(client):
    payload = {
        "source": "test_service",
        "event_type": "user.signup",
        "priority": "high",
        "payload": {"user_id": 42}
    }
    headers = {"X-Pulse-Key": "pulse_dev_secret_key_123"}
    response = await client.post("/api/v1/events/ingest", json=payload, headers=headers)

    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "accepted"
    assert "event_id" in data


@pytest.mark.asyncio
async def test_metrics_endpoint(client):
    response = await client.get("/api/v1/events/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "total_events_processed" in data
    assert data["engine_status"] == "active"