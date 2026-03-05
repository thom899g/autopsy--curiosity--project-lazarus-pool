"""
Configuration management for Lazarus Pool system.
Handles environment variables, validation, and default values.
"""
import os
from typing import Optional
from pydantic import BaseSettings, Field, validator
from dotenv import load_dotenv

load_dotenv()

class DeepSeekConfig(BaseSettings):
    """DeepSeek API configuration"""
    api_key: str = Field(..., env="DEEPSEEK_API_KEY")
    base_url: str = Field("https://api.deepseek.com", env="DEEPSEEK_BASE_URL")
    model: str = Field("deepseek-chat", env="DEEPSEEK_MODEL")
    temperature: float = Field(0.7, env="DEEPSEEK_TEMPERATURE")
    max_tokens: int = Field(1000, env="DEEPSEEK_MAX_TOKENS")
    
    @validator('api_key')
    def api_key_not_empty(cls, v):
        if not v or v == "your_api_key_here":
            raise ValueError("DEEPSEEK_API_KEY must be set")
        return v

class FirebaseConfig(BaseSettings):
    """Firebase configuration for state persistence"""
    credentials_path: str = Field("./firebase-credentials.json", env="FIREBASE_CREDENTIALS_PATH")
    project_id: Optional[str] = Field(None, env="FIREBASE_PROJECT_ID")
    collection_name: str = Field("lazarus_pool_requests", env="FIREBASE_COLLECTION")
    
    @validator('credentials_path')
    def validate_credentials_path(cls, v):
        if not os.path.exists(v):
            raise FileNotFoundError(f"Firebase credentials not found at {v}")
        return v

class AppConfig(BaseSettings):
    """Application runtime configuration"""
    max_retries: int = Field(3, env="MAX_RETRIES")
    retry_delay: float = Field(2.0, env="RETRY_DELAY")
    timeout_seconds: int = Field(30, env="TIMEOUT_SECONDS")
    log_level: str = Field("INFO", env="LOG_LEVEL")
    
    # Telegram alerting (optional)
    telegram_bot_token: Optional[str] = Field(None, env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: Optional[str] = Field(None, env="TELEGRAM_CHAT_ID")
    
    @validator('log_level')
    def validate_log_level(cls, v):
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of {valid_levels}")
        return v.upper()

class Config:
    """Main configuration container"""
    def __init__(self):
        self.deepseek = DeepSeekConfig()
        self.firebase = FirebaseConfig()
        self.app = AppConfig()
    
    @classmethod
    def load(cls):
        """