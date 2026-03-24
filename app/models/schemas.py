from pydantic import BaseModel, Field
from typing import List, Optional


class AnalysisRequest(BaseModel):
    sector: str = Field(
        ...,
        description="The industry sector to analyze (e.g., 'pharmaceuticals', 'technology','banking','automotive','telecommunications','energy','healthcare','consumer goods','retail','real estate','media and entertainment','logistics and supply chain','agriculture','mining and metals','textiles','chemicals','education','tourism and hospitality','sports')",
    )


class TradeOpportunity(BaseModel):
    title: str
    description: str
    potential: str
    risk: str


class MarketReport(BaseModel):
    sector: str
    timestamp: str
    summary: str
    opportunities: List[TradeOpportunity]
    news_sources: List[str]
    markdown_report: str
