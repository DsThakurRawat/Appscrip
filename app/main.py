from fastapi import FastAPI
from app.api.endpoints import router as api_router
from app.core.config import settings
from app.core.security import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import uvicorn

app = FastAPI(title=settings.PROJECT_NAME)

# Setup Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include API Router
app.include_router(api_router, prefix="/analyze", tags=["analysis"])

@app.get("/")
async def health_check():
    return {"status": "healthy", "project": settings.PROJECT_NAME}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
