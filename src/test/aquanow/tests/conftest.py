import pytest
import copy
from src.main.aquanow.utils.client import AquanowClient
from src.main.aquanow.utils.config import get_settings


@pytest.fixture(scope="session")
def settings():
    return get_settings()


@pytest.fixture(scope="session")
def client(settings):
    return AquanowClient(settings)


@pytest.fixture
def rfq_payload(settings):
    return {
        "ticker": "BTC-USD",
        "accountId": settings.account_id,
        "tradeSide": "buy",
        "deliverQuantity": settings.deliver_quantity,
    }


@pytest.fixture
def get_quote_params(settings):
    return {
        "ticker": "BTC-USD",
        "accountId": settings.account_id,
        "tradeSide": "buy",
        "deliverQuantity": settings.deliver_quantity,
    }


@pytest.fixture
def invalid_rfq_payload(settings):
    return {
        "ticker": "BTC-USD",
        "accountId": settings.account_id,
        "tradeSide": "invalid-side",
        "deliverQuantity": "-100",
    }




def _clean_none_values(payload: dict) -> dict:
    return {k: v for k, v in payload.items() if v is not None}


def build_payload(base_payload: dict, overrides: dict) -> dict:
    payload = copy.deepcopy(base_payload)
    payload.update(overrides)
    return _clean_none_values(payload)


@pytest.fixture
def payload_builder():
    return build_payload