from pydantic_settings import BaseSettings
from typing import Optional
import warnings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API (optional at startup, required for analyze endpoint)
    gemini_api_key: Optional[str] = None
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Database
    database_url: str = "sqlite:///./causalitycare.db"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Initialize settings
settings = Settings()

# Warn if API key is missing
if not settings.gemini_api_key:
    warnings.warn(
        "⚠️  GEMINI_API_KEY not set! "
        "Set environment variable GEMINI_API_KEY or add to .env file. "
        "The /analyze endpoint will fail without this.",
        RuntimeWarning
    )
