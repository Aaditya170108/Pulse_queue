from sqlalchemy import Column, String, DateTime, JSON
from datetime import datetime, timezone
from app.core.database import Base

class EventRecord(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    source = Column(String, index=True, nullable=False)
    event_type = Column(String, index=True, nullable=False)
    priority = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    status = Column(String, default="processed")
    received_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))