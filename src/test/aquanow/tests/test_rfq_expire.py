import allure
import pytest

from src.main.aquanow.utils.base_test import BaseAPITest
from src.main.aquanow.utils.helper import get_data, quote_id_from_response, response_type
from src.main.aquanow.utils.assertions import (
    assert_common_quote_success_contract,
    assert_not_successful_execute,
    assert_error_like_execute_response,
)


@allure.feature("RFQ Trades")
@pytest.mark.rfq
class TestRFQExpire(BaseAPITest):

    @pytest.mark.smoke
    @allure.title("Expire RFQ Quote successfully and validate post-expiry behavior")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_expire_quote_success(self, client, settings, rfq_payload):
        allure.dynamic.parameter("ticker", rfq_payload["ticker"])
        allure.dynamic.parameter("accountId", rfq_payload["accountId"])
        allure.dynamic.parameter("tradeSide", rfq_payload["tradeSide"])
        allure.dynamic.parameter("deliverQuantity", rfq_payload.get("deliverQuantity"))
        allure.dynamic.parameter("receiveQuantity", rfq_payload.get("receiveQuantity"))

        with allure.step("Create RFQ quote"):
            create_response = client.create_quote(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote", create_response)
            self.assert_status_code(create_response, 200)

        create_body = create_response.json()
        create_data = get_data(create_body)
        quote_id = quote_id_from_response(create_body)

        with allure.step("Validate quote creation"):
            assert_common_quote_success_contract(
                body=create_body,
                data=create_data,
                expected={
                    "symbol": create_data["symbol"],
                    "side": create_data["side"],
                    "deliverCurrency": create_data["deliverCurrency"],
                    "receiveCurrency": create_data["receiveCurrency"],
                },
                expected_response_type="rfqCreateQuoteAck",
            )

            assert quote_id, f"quoteId missing from createQuote response: {create_body}"
            assert create_data["quoteId"] == quote_id
            assert create_data["accountId"] == settings.account_id
            assert create_data["accountId"] == rfq_payload["accountId"]

            if "tradeSide" in rfq_payload:
                assert create_data["side"].lower() == rfq_payload["tradeSide"].lower()

            if "ticker" in rfq_payload:
                assert create_data["symbol"] == rfq_payload["ticker"]

            if rfq_payload.get("receiveQuantity") is not None:
                assert float(create_data["receiveQuantity"]) == pytest.approx(
                    float(rfq_payload["receiveQuantity"]), rel=1e-6
                )

            if rfq_payload.get("deliverQuantity") is not None:
                assert float(create_data["deliverQuantity"]) == pytest.approx(
                    float(rfq_payload["deliverQuantity"]), rel=1e-6
                )

        with allure.step("Expire RFQ quote explicitly"):
            expire_response = client.expire_quote(quote_id)
            self.record_api_call(client, "Expire RFQ Quote", expire_response)
            self.assert_status_code(expire_response, 200)

        expire_body = expire_response.json()
        expire_data = get_data(expire_body)

        with allure.step("Validate expire response"):
            assert response_type(expire_body) == "rfqExpireQuoteAck", (
                f"Unexpected expire response type: {expire_body}"
            )

            if expire_data:
                if "quoteId" in expire_data:
                    assert expire_data["quoteId"] == quote_id, (
                        f"Expired quoteId mismatch. Expected {quote_id}, got {expire_data['quoteId']}"
                    )

                if "accountId" in expire_data:
                    assert expire_data["accountId"] == settings.account_id

                if "status" in expire_data and expire_data["status"]:
                    assert "expir" in str(expire_data["status"]).lower(), (
                        f"Expected expired status indicator, got: {expire_body}"
                    )

        with allure.step("Attempt to execute expired RFQ quote"):
            execute_response = client.execute_quote(quote_id)
            self.record_api_call(client, "Execute Expired RFQ Quote", execute_response)
            self.assert_status_code(execute_response, (200, 400, 404, 422))

        try:
            execute_body = execute_response.json()
        except Exception:
            execute_body = {}

        with allure.step("Validate expired quote does not behave like successful execution"):
            if execute_response.status_code == 200:
                assert_not_successful_execute(execute_body)
            elif execute_body:
                assert_error_like_execute_response(execute_body)

        with allure.step("Validate expired quote error details when present"):
            if execute_body:
                message = (
                    execute_body.get("message")
                    or execute_body.get("error")
                    or execute_body.get("detail")
                )
                if message:
                    assert "expire" in str(message).lower(), (
                        f"Expected expiry-related error message, got: {execute_body}"
                    )

    @pytest.mark.regression
    @allure.title("RFQ Quote cannot be expired twice")
    @allure.severity(allure.severity_level.NORMAL)
    def test_expire_same_quote_twice(self, client, settings, rfq_payload):
        allure.dynamic.parameter("ticker", rfq_payload["ticker"])
        allure.dynamic.parameter("accountId", rfq_payload["accountId"])
        allure.dynamic.parameter("tradeSide", rfq_payload["tradeSide"])
        allure.dynamic.parameter("deliverQuantity", rfq_payload.get("deliverQuantity"))
        allure.dynamic.parameter("receiveQuantity", rfq_payload.get("receiveQuantity"))

        with allure.step("Create RFQ quote"):
            create_response = client.create_quote(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote", create_response)
            self.assert_status_code(create_response, 200)

        create_body = create_response.json()
        create_data = get_data(create_body)
        quote_id = quote_id_from_response(create_body)

        with allure.step("Validate quote creation"):
            assert_common_quote_success_contract(
                body=create_body,
                data=create_data,
                expected={
                    "symbol": create_data["symbol"],
                    "side": create_data["side"],
                    "deliverCurrency": create_data["deliverCurrency"],
                    "receiveCurrency": create_data["receiveCurrency"],
                },
                expected_response_type="rfqCreateQuoteAck",
            )

            assert quote_id, f"quoteId missing from createQuote response: {create_body}"
            assert create_data["quoteId"] == quote_id
            assert create_data["accountId"] == settings.account_id

        with allure.step("Expire RFQ quote first time"):
            first_expire = client.expire_quote(quote_id)
            self.record_api_call(client, "Expire RFQ Quote - First", first_expire)
            self.assert_status_code(first_expire, 200)

        first_expire_body = first_expire.json()
        first_expire_data = get_data(first_expire_body)

        with allure.step("Validate first expire response"):
            assert response_type(first_expire_body) == "rfqExpireQuoteAck", (
                f"Unexpected first expire response type: {first_expire_body}"
            )

            if first_expire_data:
                if "quoteId" in first_expire_data:
                    assert first_expire_data["quoteId"] == quote_id

                if "accountId" in first_expire_data:
                    assert first_expire_data["accountId"] == settings.account_id

                with allure.step("Expire RFQ quote second time"):
                    second_expire = client.expire_quote(quote_id)
                    self.record_api_call(client, "Expire RFQ Quote - Second", second_expire)
                    self.assert_status_code(second_expire, (400, 404, 409, 422))

        try:
            second_expire_body = second_expire.json()
        except Exception:
            second_expire_body = {}

        with allure.step("Validate second expire response details when present"):
            if second_expire_body:
                message = (
                    second_expire_body.get("message")
                    or second_expire_body.get("error")
                    or second_expire_body.get("detail")
                )

                assert message, (
                    f"Expected error message in second expire response: {second_expire_body}"
                )

                expected_message = f"quoteId: {quote_id} has alreaady been processed"
                assert message == expected_message, (
                    f"Unexpected second expire message. "
                    f"Expected: {expected_message}, Actual: {message}"
                )