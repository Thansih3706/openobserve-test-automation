import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://api-dev.aquanow.io").rstrip("/")
    api_key: str = os.getenv("API_KEY", "")
    api_secret: str = os.getenv("API_SECRET", "")
    account_id: str = os.getenv("ACCOUNT_ID", "")
    deliver_quantity: str = os.getenv("DELIVER_QUANTITY", "100")
    get_quote_path: str = os.getenv("GET_QUOTE_PATH", "/trades/v2/getQuote")
    create_quote_path: str = os.getenv("CREATE_QUOTE_PATH", "/trades/v2/createQuote")
    execute_quote_path: str = os.getenv("EXECUTE_QUOTE_PATH", "/trades/v2/executeQuote")
    expire_quote_path: str = os.getenv("EXPIRE_QUOTE_PATH", "/trades/v1/expireQuote")
    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "20"))
    order_poll_seconds: int = int(os.getenv("ORDER_POLL_SECONDS", "15"))
    order_poll_interval: int = int(os.getenv("ORDER_POLL_INTERVAL", "2"))


def get_settings() -> Settings:
    settings = Settings()
    missing = []

    if not settings.api_key or settings.api_key == "YOUR_API_KEY":
        missing.append("API_KEY")
    if not settings.api_secret or settings.api_secret == "YOUR_API_SECRET":
        missing.append("API_SECRET")
    if not settings.account_id or settings.account_id == "YOUR_ACCOUNT_ID":
        missing.append("ACCOUNT_ID")

    if missing:
        raise ValueError(
            f"Missing or placeholder environment variables: {', '.join(missing)}"
        )

    return settings