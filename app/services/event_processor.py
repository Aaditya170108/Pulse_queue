import logging
from app.schemas.event import WebhookPayload
from app.models.event import EventRecord
from app.core.database import AsyncSessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pulse-queue")

async def process_event_task(event: WebhookPayload):
    logger.info(f"⚡ [WORKER] Ingesting event {event.event_id} from {event.source}...")

    # Persist record into the database
    async with AsyncSessionLocal() as session:
        async with session.begin():
            record = EventRecord(
                event_id=event.event_id,
                source=event.source,
                event_type=event.event_type,
                priority=event.priority.value,
                payload=event.payload,
                status="processed"
            )
            session.add(record)
        await session.commit()

    if event.priority == "critical":
        logger.warning(f"🚨 CRITICAL ALERT flagged for event {event.event_id}")

    logger.info(f"✅ [WORKER] Event {event.event_id} successfully persisted.")