from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')
    DATABASE_URL: Optional[str]
    SECRET_KEY: Optional[str]
