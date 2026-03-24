import google.generativeai as genai
from app.core.config import settings
from app.models.schemas import MarketReport, TradeOpportunity
from typing import List, Dict
import json
import logging
from datetime import datetime
from cachetools import TTLCache

logger = logging.getLogger(__name__)

class AIAnalysisService:
    def __init__(self):
        # 5-minute TTL cache for up to 100 sectors
        self.cache = TTLCache(maxsize=100, ttl=300)
        
        # Robust check for API key
        api_key = settings.GEMINI_API_KEY
        if api_key and api_key != "your_gemini_api_key_here":
            try:
                genai.configure(api_key=api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash-lite')
                logger.info("Gemini AI model initialized successfully.")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {e}")
                self.model = None
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not set or invalid.")

    async def analyze_sector(self, sector: str, raw_data: List[Dict[str, str]]) -> MarketReport:
        """
        Analyze the collected raw data and generate a structured report.
        Uses in-memory cache to stay within AI quota limits.
        """
        if sector in self.cache:
            logger.info(f"Cache hit for sector: {sector}")
            return self.cache[sector]

        if not self.model:
            return self._generate_fallback_report(sector)

        context = "\n".join([f"Title: {d['title']}\nSnippet: {d['snippet']}" for d in raw_data])
        
        prompt = f"""
        Act as a professional market analyst focusing on the Indian market.
        Analyze the following recent data for the '{sector}' sector in India:
        
        {context}
        
        Based on this data, provide:
        1. A high-level summary of the current market state.
        2. At least 3 specific trade opportunities.
        3. For each opportunity, provide a title, description, potential, and risk.
        4. A final structured markdown report.
        
        Return the response EXACTLY in JSON format with the following keys:
        - summary: string
        - opportunities: list of objects (each with title, description, potential, risk)
        - markdown_report: string (complete formatted markdown report)
        """

        try:
            response = self.model.generate_content(prompt)
            # Find the JSON block in the response
            text = response.text
            json_start = text.find('{')
            json_end = text.rfind('}') + 1
            data = json.loads(text[json_start:json_end])
            
            report = MarketReport(
                sector=sector,
                timestamp=datetime.now().isoformat(),
                summary=data.get("summary", ""),
                opportunities=[TradeOpportunity(**o) for o in data.get("opportunities", [])],
                news_sources=[d['link'] for d in raw_data if 'link' in d],
                markdown_report=data.get("markdown_report", "")
            )
            
            # Save to cache
            self.cache[sector] = report
            return report
        except Exception as e:
            logger.error(f"Error in AI analysis: {e}")
            return self._generate_fallback_report(sector, error_msg=str(e))

    def _generate_fallback_report(self, sector: str, error_msg: str = "") -> MarketReport:
        content = f"Analysis for {sector} sector is currently unavailable."
        if error_msg:
            content += f" Error details: {error_msg}"
        
        return MarketReport(
            sector=sector,
            timestamp=datetime.now().isoformat(),
            summary=content,
            opportunities=[],
            news_sources=[],
            markdown_report=f"# Market Analysis: {sector}\n\nAnalysis unavailable.\n\n**Error Details:**\n{error_msg}"
        )

ai_analysis_service = AIAnalysisService()
