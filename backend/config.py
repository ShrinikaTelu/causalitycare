from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API
    gemini_api_key: str
    
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

settings = Settings()
