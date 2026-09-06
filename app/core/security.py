import os
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY_NAME = "X-Pulse-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

EXPECTED_API_KEY = os.getenv("PULSE_API_KEY", "pulse_dev_secret_key_123")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key or api_key != EXPECTED_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key in 'X-Pulse-Key' header"
        )
    return api_key