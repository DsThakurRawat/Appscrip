from fastapi import APIRouter, Depends, Request, Path
from app.models.schemas import MarketReport
from app.services.market_data import market_data_service
from app.services.ai_analysis import ai_analysis_service
from app.core.security import verify_jwt, create_access_token
from app.core.rate_limiter import check_rate_limit
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.post("/token")
async def login(request: Request):
    # In a real app, you'd verify credentials against a database
    # For this assignment, we use a simple check or just issue a token
    access_token = create_access_token(data={"sub": "guest_user"})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/{sector}", response_model=MarketReport)
async def analyze_sector(
    request: Request,
    sector: str = Path(..., description="The industry sector to analyze (e.g., 'technology', 'banking', 'pharma', etc.)"),
    payload: dict = Depends(verify_jwt),
    _rate_limit: None = Depends(check_rate_limit)
):
    """
    Analyze a specific market sector in India and return a structured report.
    """
    # 1. Check cache first
    cached_report = ai_analysis_service.cache.get(sector)
    if cached_report:
        logger.info(f"Cache hit for sector: {sector}")
        return cached_report

    logger.info(f"Analyzing sector: {sector} for user: {payload.get('sub')}")
    
    # 2. Fetch market data
    raw_data = await market_data_service.get_sector_news(sector)
    
    # 3. Analyze with AI
    report = await ai_analysis_service.analyze_sector(sector, raw_data)
    
    return report
