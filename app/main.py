from fastapi import FastAPI
from app.api.events import router as events_router

app = FastAPI(
    title="PulseQueue Engine",
    description="High-throughput asynchronous webhook ingestion and event processing system",
    version="0.1.0"
)

# Register routes
app.include_router(events_router)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "PulseQueue",
        "version": "0.1.0"
    }