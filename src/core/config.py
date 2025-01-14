from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = str(Path(__file__).parent.parent.parent / ".env")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ROOT_DIR, env_file_encoding="utf-8")

    # LinkedIn settings
    LINKEDIN_LOGIN_URL: str = "https://www.linkedin.com/login"
    LINKEDIN_USERNAME: str = "guest"
    LINKEDIN_PASSWORD: str = "guest"

    # MongoDB settings
    MONGO_URI: str = "mongodb://mongo:mongo@mongodb:27017"
    MONGO_INITDB_USERNAME: str = "mongo"
    MONGO_INITDB_PASSWORD: str = "mongo"


settings = Settings()
