from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict
from pydantic import BaseModel, Field
import uuid

class EventPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class WebhookPayload(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str = Field(..., description="Origin of the event")
    event_type: str = Field(..., description="Action trigger type")
    priority: EventPriority = Field(default=EventPriority.MEDIUM)
    payload: Dict[str, Any] = Field(..., description="Arbitrary raw JSON payload")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "json_schema_extra": {
            "example": {
                "source": "sensor_node_01",
                "event_type": "telemetry_ping",
                "priority": "high",
                "payload": {
                    "battery_voltage": 12.4,
                    "temperature": 34.2,
                    "status": "active"
                }
            }
        }
    }

class EventResponse(BaseModel):
    status: str
    event_id: str
    message: str
    received_at: datetime