
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./growth_wave.db"
    SECRET_KEY: str = "a_very_secret_key_that_should_be_changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_V1_STR: str = "/api/v1"

    # IMPORTANT: This is a default key for development.
    # For production, generate a new key using `cryptography.fernet.Fernet.generate_key()`
    # and set it as an environment variable.
    ENCRYPTION_KEY: str = "moxN23-I7gJjA9b3y1b-iGkR5v7y_wZ3-aX9b_c8d_E="

    class Config:
        env_file = ".env"

settings = Settings()
