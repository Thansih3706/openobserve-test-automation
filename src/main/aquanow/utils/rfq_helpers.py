import pytest

from src.main.aquanow.utils.helper import get_data, quote_id_from_response
from src.main.aquanow.utils.assertions import assert_common_quote_success_contract


def create_quote_for_execution(
    test_instance,
    client,
    settings,
    rfq_payload,
    payload_builder,
    case,
):
    payload = payload_builder(rfq_payload, case["payload_overrides"])
    expected = case["expected"]

    create_response = client.create_quote(payload)
    test_instance.record_api_call(client, "Create RFQ Quote", create_response)
    test_instance.assert_status_code(create_response, 200)

    create_body = create_response.json()
    create_data = get_data(create_body)
    quote_id = quote_id_from_response(create_body)

    assert_common_quote_success_contract(
        body=create_body,
        data=create_data,
        expected=expected,
        expected_response_type="rfqCreateQuoteAck",
    )

    assert quote_id, f"quoteId missing from createQuote response: {create_body}"
    assert create_data["accountId"] == settings.account_id
    assert create_data["accountId"] == payload["accountId"]

    if "tradeSide" in payload:
        assert create_data["side"].lower() == payload["tradeSide"].lower()

    if "ticker" in payload:
        assert create_data["symbol"] == payload["ticker"]

    if payload.get("receiveQuantity") is not None:
        assert float(create_data["receiveQuantity"]) == pytest.approx(
            float(payload["receiveQuantity"]), rel=1e-6
        )

    if payload.get("deliverQuantity") is not None:
        assert float(create_data["deliverQuantity"]) == pytest.approx(
            float(payload["deliverQuantity"]), rel=1e-6
        )

    return payload, expected, create_body, create_data, quote_id