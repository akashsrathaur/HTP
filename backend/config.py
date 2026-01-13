"""
Configuration management for the Virtual Identity System.
Uses Pydantic Settings for environment variable management.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
import secrets


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = Field(
        default="sqlite+aiosqlite:///./vid_system.db",
        description="Database connection URL"
    )
    
    # JWT Settings
    jwt_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret key for JWT token signing"
    )
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    
    # HMAC Signing Key for QR Codes
    hmac_secret_key: str = Field(
        default_factory=lambda: secrets.token_urlsafe(32),
        description="Secret key for HMAC signing of QR codes"
    )
    
    # VID Settings
    vid_expiry_minutes: int = 60  # VIDs expire after 1 hour
    vid_usage_limit: int = 1  # One-time use by default
    
    # Rate Limiting
    rate_limit_verification: str = "10/minute"  # VID verification endpoint
    rate_limit_generation: str = "5/minute"  # VID generation endpoint
    
    # Security
    bcrypt_rounds: int = 12
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:8000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()
