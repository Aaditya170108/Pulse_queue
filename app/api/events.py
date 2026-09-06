from datetime import datetime, timezone
from fastapi import APIRouter, BackgroundTasks, status
from app.schemas.event import WebhookPayload, EventResponse
from app.services.event_processor import process_event_task

router = APIRouter(prefix="/api/v1/events", tags=["Events"])

@router.post(
    "/ingest",
    response_model=EventResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest incoming webhook event"
)
async def ingest_event(event: WebhookPayload, background_tasks: BackgroundTasks):
    # Offload the processing job to the background worker
    background_tasks.add_task(process_event_task, event)

    return EventResponse(
        status="accepted",
        event_id=event.event_id,
        message="Event received and queued for asynchronous processing",
        received_at=datetime.now(timezone.utc)
    )