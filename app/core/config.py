from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MISTRAL_API_KEY: Optional[str] = None

    CHAT_MODEL: str = "mistral-small-latest"
    EMBEDDING_MODEL: str = "mistral-embed"

    class Config:
        env_file = ".env"


settings = Settings()
