
from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_V1_PREFIX: str = "/api"
    PROJECT_NAME: str = "GitHub Portfolio Analyzer"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]
    
    # External API Keys
    GITHUB_TOKEN: str = ""  # Optional: increases rate limit
    OPENAI_API_KEY: str = ""  # Optional: enables AI feedback
    OPENROUTER_API_KEY: str = ""  # Alternative to OpenAI
    
    # GitHub API Configuration
    GITHUB_API_BASE_URL: str = "https://api.github.com"
    GITHUB_API_VERSION: str = "2022-11-28"
    
    # Scoring Weights (should sum to 100)
    WEIGHT_ACTIVITY: float = 25.0
    WEIGHT_DOCUMENTATION: float = 20.0
    WEIGHT_QUALITY: float = 25.0
    WEIGHT_PROFESSIONALISM: float = 15.0
    WEIGHT_IMPACT: float = 15.0
    
    # Analysis Parameters
    MIN_REPOS_FOR_ANALYSIS: int = 1
    MAX_REPOS_TO_ANALYZE: int = 50
    RECENT_ACTIVITY_DAYS: int = 365
    
    # AI Configuration
    AI_MODEL: str = "gpt-4o-mini"
    AI_TEMPERATURE: float = 0.7
    AI_MAX_TOKENS: int = 1500
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    Using lru_cache ensures settings are loaded only once.
    """
    return Settings()


# Global settings instance
settings = get_settings()
