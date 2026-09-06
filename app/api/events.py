from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.schemas.event import WebhookPayload, EventResponse
from app.services.event_processor import process_event_task
from app.core.database import get_db
from app.core.security import verify_api_key
from app.models.event import EventRecord

router = APIRouter(prefix="/api/v1/events", tags=["Events"])

@router.post(
    "/ingest",
    response_model=EventResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Ingest incoming webhook event (Protected)"
)
async def ingest_event(
    event: WebhookPayload,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    background_tasks.add_task(process_event_task, event)
    return EventResponse(
        status="accepted",
        event_id=event.event_id,
        message="Event received and queued for asynchronous processing",
        received_at=datetime.now(timezone.utc)
    )

@router.get("/metrics", summary="Get real-time ingestion metrics")
async def get_metrics(db: AsyncSession = Depends(get_db)):
    total_query = select(func.count(EventRecord.event_id))
    total_result = await db.execute(total_query)
    total_count = total_result.scalar() or 0

    return {
        "total_events_processed": total_count,
        "engine_status": "active"
    }

@router.get("/recent", summary="Fetch latest ingested events")
async def get_recent_events(
    limit: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(EventRecord).order_by(desc(EventRecord.received_at)).limit(limit)
    result = await db.execute(query)
    records = result.scalars().all()

    return [
        {
            "event_id": r.event_id,
            "source": r.source,
            "event_type": r.event_type,
            "priority": r.priority,
            "payload": r.payload,
            "status": r.status,
            "received_at": r.received_at
        }
        for r in records
    ]