from functools import lru_cache
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    gemini_api_key: str = ""
    gemini_model: str = "gemini-3.8-flash"
    explanation_backend: str = "gemini"  # gemini | local
    local_explanation_model: str = "MBZUAI/LaMini-Flan-T5-783M"
    app_name: str = "EduGenie"
    max_input_chars: int = 20000
    cors_origins: str = "*"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()
