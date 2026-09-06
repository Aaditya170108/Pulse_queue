from fastapi import FastAPI

app = FastAPI(
    title="PulseQueue Engine",
    description="High-throughput asynchronous webhook ingestion and event processing system",
    version="0.1.0"
)

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy",
        "service": "PulseQueue",
        "version": "0.1.0"
    }