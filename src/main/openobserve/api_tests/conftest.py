import time
import uuid
import os
import pytest
from dotenv import load_dotenv

load_dotenv()


def _required_env(name):
    value = os.getenv(name, "").strip()
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value

@pytest.fixture
def base_url():
    return os.getenv("OO_BASE_URL", "http://localhost:5080")


@pytest.fixture
def org_name():
    return os.getenv("OO_ORG", "default")


@pytest.fixture
def auth():
    username = _required_env("USERNAME")
    password = _required_env("PASSWORD")
    return (username, password)


@pytest.fixture
def unique_stream_name():
    return f"qa_logs_{int(time.time())}_{uuid.uuid4().hex[:6]}"


@pytest.fixture
def sample_logs():
    return [
        {"level": "info", "message": "user login success", "code": "100"},
        {"level": "error", "message": "database connection failed", "code": "500"},
        {"level": "info", "message": "request completed", "code": "200"},
    ]