import allure
import pytest

from src.main.aquanow.utils.base_test import BaseAPITest
from src.main.aquanow.utils.helper import get_data
from src.main.aquanow.utils.assertions import (
    assert_common_quote_success_contract,
    assert_error_like_response,
)
from resources.testdata.rfq_test_data import (
    CREATE_QUOTE_POSITIVE_CASES,
    CREATE_QUOTE_PRECEDENCE_CASES,
    GET_QUOTE_POSITIVE_CASES,
    NEGATIVE_CREATE_CASES,
    NEGATIVE_GET_CASES,
)


@allure.feature("RFQ Trades")
@pytest.mark.rfq
class TestRFQQuote(BaseAPITest):

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case",
        GET_QUOTE_POSITIVE_CASES,
        ids=[case["id"] for case in GET_QUOTE_POSITIVE_CASES],
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_rfq_quote_positive_matrix(
        self, client, settings, get_quote_params, payload_builder, case
    ):
        payload = payload_builder(get_quote_params, case["payload_overrides"])
        expected = case["expected"]

        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("payload", str(payload))

        with allure.step("Execute GET RFQ quote request"):
            response = client.get_quote(payload)
            self.record_api_call(client, "Get RFQ Quote", response)
            self.assert_status_code(response, 200)

        with allure.step("Validate RFQ GET quote response contract"):
            body = response.json()
            data = get_data(body)

            assert_common_quote_success_contract(
                body=body,
                data=data,
                expected=expected,
                expected_response_type="rfqGetQuoteAck",
            )

            assert data["accountId"] == settings.account_id
            assert data["accountId"] == payload["accountId"]

            if "tradeSide" in payload:
                assert data["side"].lower() == payload["tradeSide"].lower()

            if "ticker" in payload:
                assert data["symbol"] == payload["ticker"]

            if "receiveQuantity" in payload:
                assert float(data["receiveQuantity"]) == pytest.approx(
                    float(payload["receiveQuantity"]), rel=1e-6
                )

            if "deliverQuantity" in payload:
                assert float(data["deliverQuantity"]) == pytest.approx(
                    float(payload["deliverQuantity"]), rel=1e-6
                )

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case",
        CREATE_QUOTE_POSITIVE_CASES,
        ids=[case["id"] for case in CREATE_QUOTE_POSITIVE_CASES],
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_rfq_quote_positive_matrix(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        payload = payload_builder(rfq_payload, case["payload_overrides"])
        expected = case["expected"]

        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("payload", str(payload))

        with allure.step("Execute CREATE RFQ quote request"):
            response = client.create_quote(payload)
            self.record_api_call(client, "Create RFQ Quote", response)
            self.assert_status_code(response, 200)

        with allure.step("Validate RFQ CREATE quote response contract"):
            body = response.json()
            data = get_data(body)

            assert_common_quote_success_contract(
                body=body,
                data=data,
                expected=expected,
                expected_response_type="rfqCreateQuoteAck",
            )

            assert data["accountId"] == settings.account_id
            assert data["accountId"] == payload["accountId"]

            if "tradeSide" in payload:
                assert data["side"].lower() == payload["tradeSide"].lower()

            if "ticker" in payload:
                assert data["symbol"] == payload["ticker"]

            if "receiveQuantity" in payload:
                assert float(data["receiveQuantity"]) == pytest.approx(
                    float(payload["receiveQuantity"]), rel=1e-6
                )

            if "deliverQuantity" in payload:
                assert float(data["deliverQuantity"]) == pytest.approx(
                    float(payload["deliverQuantity"]), rel=1e-6
                )

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "case",
        CREATE_QUOTE_PRECEDENCE_CASES,
        ids=[case["id"] for case in CREATE_QUOTE_PRECEDENCE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_rfq_quote_quantity_precedence(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        payload = payload_builder(rfq_payload, case["payload_overrides"])
        expected = case["expected"]

        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("payload", str(payload))

        with allure.step("Create RFQ quote with both deliverQuantity and receiveQuantity"):
            response = client.create_quote(payload)
            self.record_api_call(client, "Create RFQ Quote - Quantity Precedence", response)
            self.assert_status_code(response, 200)

        with allure.step("Validate quantity precedence response"):
            body = response.json()
            data = get_data(body)

            assert_common_quote_success_contract(
                body=body,
                data=data,
                expected=expected,
                expected_response_type="rfqCreateQuoteAck",
            )

            assert data["accountId"] == settings.account_id
            assert data["accountId"] == payload["accountId"]

            if "tradeSide" in payload:
                assert data["side"].lower() == payload["tradeSide"].lower()

            if "ticker" in payload:
                assert data["symbol"] == payload["ticker"]

            if "precedence_field" in expected and "precedence_value" in expected:
                precedence_field = expected["precedence_field"]
                precedence_value = expected["precedence_value"]

                assert precedence_field in ("deliverQuantity", "receiveQuantity"), (
                    f"Invalid precedence_field in test data: {precedence_field}"
                )
                assert float(data[precedence_field]) == pytest.approx(
                    float(precedence_value), rel=1e-6
                ), (
                    f"Expected {precedence_field} to follow precedence value "
                    f"{precedence_value}, but got {data[precedence_field]}"
                )
            elif "receiveQuantity" in expected:
                assert float(data["receiveQuantity"]) == pytest.approx(
                    float(expected["receiveQuantity"]), rel=1e-6
                )
            elif "deliverQuantity" in expected:
                assert float(data["deliverQuantity"]) == pytest.approx(
                    float(expected["deliverQuantity"]), rel=1e-6
                )

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        NEGATIVE_GET_CASES,
        ids=[case["id"] for case in NEGATIVE_GET_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_quote_negative_matrix(
        self, client, get_quote_params, payload_builder, case
    ):
        payload = payload_builder(get_quote_params, case["payload_overrides"])

        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("payload", str(payload))

        with allure.step("Submit invalid GET RFQ quote request"):
            response = client.get_quote(payload)
            self.record_api_call(client, "Get RFQ Quote - Negative", response)

        with allure.step("Validate negative GET quote response"):
            assert response.status_code in case["expected_statuses"], response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            assert_error_like_response(body, "rfqGetQuoteAck")

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        NEGATIVE_CREATE_CASES,
        ids=[case["id"] for case in NEGATIVE_CREATE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_negative_matrix(
        self, client, rfq_payload, payload_builder, case
    ):
        payload = payload_builder(rfq_payload, case["payload_overrides"])

        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("payload", str(payload))

        with allure.step("Submit invalid CREATE RFQ quote request"):
            response = client.create_quote(payload)
            self.record_api_call(client, "Create RFQ Quote - Negative", response)

        with allure.step("Validate negative CREATE quote response"):
            assert response.status_code in case["expected_statuses"], response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            assert_error_like_response(body, "rfqCreateQuoteAck")