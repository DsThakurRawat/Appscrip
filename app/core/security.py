from fastapi import Header, HTTPException
from app.core.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

# Limiter for rate limiting
limiter = Limiter(key_func=get_remote_address)

async def verify_api_key(x_api_key: str = Header(...)):
    """
    Simple API Key authentication.
    """
    if x_api_key != settings.API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return x_api_key
