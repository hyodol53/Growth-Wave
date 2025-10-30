
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

    # Praise settings
    PRAISE_LIMIT_PER_PERIOD: int = 5
    PRAISE_AVAILABLE_HASHTAGS: list[str] = [
        "#해결사", "#소통왕", "#협업왕", "#선한영향력", "#빠른실행력", "#디테일장인"
    ]
    PRAISE_ANONYMOUS_ANIMALS: list[str] = [
        "고라니", "너구리", "두루미", "미어캣", "반달곰", "수달", "오소리", "족제비", "호랑이", "코끼리",
        "기린", "사자", "하마", "얼룩말", "코뿔소", "돌고래", "바다표범", "펭귄", "북극곰", "바다사자"
    ]
    PRAISE_ANONYMOUS_ADJECTIVES: list[str] = [
        "용감한", "친절한", "현명한", "날렵한", "고요한", "명랑한", "성실한", "늠름한", "다정한", "재빠른",
        "총명한", "우아한", "강인한", "믿음직한", "평화로운", "유쾌한", "정의로운", "창의적인", "끈기있는", "열정적인"
    ]

    model_config = {"env_file": ".env"}

settings = Settings()
