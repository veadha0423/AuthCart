import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv(Path(__file__).resolve().parents[2] / "env" / ".env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("AUTHCART_APP_NAME", "AuthCart API")
    database_url: str = os.getenv("AUTHCART_DATABASE_URL", "sqlite:///./authcart.db")
    secret_key: str = os.getenv("AUTHCART_SECRET_KEY", "")
    token_algorithm: str = os.getenv("AUTHCART_TOKEN_ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(
        os.getenv("AUTHCART_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )


settings = Settings()