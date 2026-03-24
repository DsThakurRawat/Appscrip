from fastapi import APIRouter, Depends, Request, Path
from app.models.schemas import MarketReport
from app.services.market_data import market_data_service
from app.services.ai_analysis import ai_analysis_service
from app.core.security import verify_api_key, limiter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/{sector}", response_model=MarketReport)
@limiter.limit("5/minute")
async def analyze_sector(
    request: Request,
    sector: str = Path(
        ...,
        description="The industry sector to analyze (e.g., 'technology', 'banking', 'pharma', etc.)",
    ),
    api_key: str = Depends(verify_api_key),
):
    """
    Analyze a specific market sector in India and return a structured report.
    """
    logger.info(f"Analyzing sector: {sector}")

    # 1. Fetch market data
    raw_data = await market_data_service.get_sector_news(sector)

    # 2. Analyze with AI
    report = await ai_analysis_service.analyze_sector(sector, raw_data)

    return report
