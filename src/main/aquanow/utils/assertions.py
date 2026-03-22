from src.main.aquanow.utils.helper import get_data, quote_id_from_response, response_type


def assert_common_quote_success_contract(body, data, expected, expected_response_type):
    assert response_type(body) == expected_response_type

    quote_id = quote_id_from_response(body)
    assert quote_id, f"quoteId missing from response: {body}"

    required_fields = [
        "accountId",
        "quoteId",
        "symbol",
        "side",
        "deliverCurrency",
        "receiveCurrency",
        "quoteTime",
        "expireTime",
        "deliverQuantity",
        "receiveQuantity",
        "price",
    ]
    for field in required_fields:
        assert field in data, f"Missing field '{field}' in response data: {data}"

    assert data["quoteId"] == quote_id
    assert str(data["quoteId"]).strip()

    assert data["accountId"]
    assert data["symbol"] == expected["symbol"]
    assert data["side"] == expected["side"]
    assert data["deliverCurrency"] == expected["deliverCurrency"]
    assert data["receiveCurrency"] == expected["receiveCurrency"]
    assert data["deliverCurrency"] != data["receiveCurrency"]

    assert isinstance(data["quoteTime"], int), (
        f"quoteTime should be int, got: {type(data['quoteTime'])}"
    )
    assert isinstance(data["expireTime"], int), (
        f"expireTime should be int, got: {type(data['expireTime'])}"
    )
    assert data["quoteTime"] > 0
    assert data["expireTime"] > data["quoteTime"]

    assert float(data["price"]) > 0
    assert float(data["deliverQuantity"]) > 0
    assert float(data["receiveQuantity"]) > 0


def assert_error_like_response(body, success_response_type):
    if not body:
        return

    assert response_type(body) != success_response_type, (
        f"Negative response unexpectedly matched success type '{success_response_type}': {body}"
    )

    data = body.get("data")
    if isinstance(data, dict):
        assert not data.get("quoteId"), (
            f"Negative response unexpectedly returned quoteId: {body}"
        )

    assert any(key in body for key in ("message", "error", "errors", "detail", "status", "type")), (
        f"Negative response body does not contain any recognizable error indicator: {body}"
    )


def looks_like_successful_execute(body: dict) -> bool:
    data = get_data(body)
    return (
        response_type(body) == "rfqExecuteQuoteAck"
        and bool(data.get("quoteId"))
        and bool(data.get("tradeDate"))
        and bool(data.get("valueDate"))
    )


def assert_execute_success_contract(body, data, expected_quote_id, expected_account_id):
    assert response_type(body) == "rfqExecuteQuoteAck", (
        f"Unexpected execute response type: {body}"
    )

    required_fields = [
        "quoteId",
        "accountId",
        "tradeDate",
        "valueDate",
    ]
    for field in required_fields:
        assert field in data, f"Missing field '{field}' in execute response data: {data}"

    assert data["quoteId"] == expected_quote_id, (
        f"Executed quoteId mismatch. Expected {expected_quote_id}, got {data['quoteId']}"
    )
    assert data["accountId"] == expected_account_id, (
        f"Executed accountId mismatch. Expected {expected_account_id}, got {data['accountId']}"
    )
    assert str(data["tradeDate"]).strip(), (
        f"tradeDate missing/empty in execute response: {data}"
    )
    assert str(data["valueDate"]).strip(), (
        f"valueDate missing/empty in execute response: {data}"
    )


def assert_not_successful_execute(body):
    if not body:
        return

    assert not looks_like_successful_execute(body), (
        f"Response unexpectedly behaved like a successful execution: {body}"
    )


def assert_error_like_execute_response(body):
    if not body:
        return

    assert_not_successful_execute(body)

    assert any(key in body for key in ("message", "error", "errors", "detail", "status", "type")), (
        f"Execute negative response does not contain any recognizable error indicator: {body}"
    )