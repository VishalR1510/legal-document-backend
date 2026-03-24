from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "Legal Document Analysis API"
    GEMINI_API_KEY: str = ""
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_PATH: str = "local_qdrant_db"
    QDRANT_URL: str = ""  # Cloud Qdrant URL
    QDRANT_API_KEY: str = ""  # Cloud Qdrant API key

    class Config:
        env_file = str(Path(__file__).parent.parent.parent / ".env")
        case_sensitive = False

settings = Settings()
