"""
Configuration management for cloud fusion backend.

Centralized configuration using Pydantic settings with environment variable
support and validation.

Author: Dr. Maya Anderson
Date: 2024-01-20
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support.
    
    Configuration is loaded from environment variables with fallback
    to default values. Supports .env file loading.
    
    Example .env file:
        DATABASE_URL=postgresql://user:pass@localhost:5432/bio_resilience
        REDIS_URL=redis://localhost:6379/0
        MQTT_BROKER=mqtt.bio-resilience.org
        SECRET_KEY=your-secret-key-here
    """
    
    # Application
    APP_NAME: str = "Bio-Resilience Engine"
    VERSION: str = "0.4.2"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/bio_resilience",
        description="PostgreSQL connection URL"
    )
    
    # Redis
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL for caching"
    )
    
    # MQTT
    MQTT_BROKER: str = Field(
        default="mqtt.bio-resilience.org",
        description="MQTT broker hostname"
    )
    MQTT_PORT: int = Field(
        default=1883,
        description="MQTT broker port"
    )
    
    # Security
    SECRET_KEY: str = Field(
        default="development-secret-key-change-in-production",
        description="Secret key for JWT signing"
    )
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="Allowed CORS origins"
    )
    
    # Fusion Engine
    FUSION_UPDATE_RATE_HZ: float = 1.0
    FUSION_PREDICTION_HORIZON_SEC: int = 300
    
    # Model Paths
    LSTM_MODEL_PATH: str = "models/activity_lstm.pt"
    FATIGUE_MODEL_PATH: str = "models/fatigue_predictor.pt"
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Global settings instance
settings = Settings()
