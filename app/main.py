from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.events import router as events_router
from app.core.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="PulseQueue Engine",
    description="High-throughput asynchronous webhook ingestion and event processing system",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(events_router)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "PulseQueue",
        "version": "0.1.0"
    }