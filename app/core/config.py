from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from dotenv import load_dotenv
import os

# Explicitly load .env from the current directory
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Trade Opportunities API"
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    API_KEY: str = os.getenv("API_KEY", "appscrip_dev_2026")
    RATE_LIMIT: str = "5/minute"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
