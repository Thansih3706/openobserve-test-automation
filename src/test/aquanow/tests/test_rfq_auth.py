import time

import allure
import pytest

from src.main.aquanow.utils.base_test import BaseAPITest
from src.main.aquanow.utils.assertions import (
    assert_error_like_execute_response,
    assert_error_like_response,
)
from src.main.aquanow.utils.rfq_helpers import create_quote_for_execution
from resources.testdata.rfq_test_data import EXECUTE_QUOTE_CASES


@allure.feature("RFQ Trades - Auth")
@pytest.mark.rfq
class TestRFQAuth(BaseAPITest):

    @pytest.mark.negative
    @allure.title("Create RFQ Quote without authentication should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_without_auth_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        with allure.step("Submit CREATE RFQ quote request without authentication"):
            response = client.create_quote_unauthorized(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote - Unauthorized", response)

        with allure.step("Validate unauthorized CREATE response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Get RFQ Quote without authentication should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_quote_without_auth_fails(self, client, get_quote_params):
        allure.dynamic.parameter("payload", str(get_quote_params))

        with allure.step("Submit GET RFQ quote request without authentication"):
            response = client.get_quote_unauthorized(get_quote_params)
            self.record_api_call(client, "Get RFQ Quote - Unauthorized", response)

        with allure.step("Validate unauthorized GET response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqGetQuoteAck")

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_execute_quote_without_auth_fails(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        allure.dynamic.title(
            f"Execute RFQ Quote without authentication should fail - {case['id']}"
        )
        allure.dynamic.parameter("payload_overrides", str(case["payload_overrides"]))

        with allure.step("Create RFQ quote with valid authentication"):
            _, _, _, _, quote_id = create_quote_for_execution(
                self, client, settings, rfq_payload, payload_builder, case
            )

        with allure.step("Attempt to execute RFQ quote without authentication"):
            response = client.execute_quote_unauthorized(quote_id)
            self.record_api_call(client, "Execute RFQ Quote - Unauthorized", response)

        with allure.step("Validate unauthorized EXECUTE response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_execute_response(body)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_expire_quote_without_auth_fails(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        allure.dynamic.title(
            f"Expire RFQ Quote without authentication should fail - {case['id']}"
        )
        allure.dynamic.parameter("payload_overrides", str(case["payload_overrides"]))

        with allure.step("Create RFQ quote with valid authentication"):
            _, _, _, _, quote_id = create_quote_for_execution(
                self, client, settings, rfq_payload, payload_builder, case
            )

        with allure.step("Attempt to expire RFQ quote without authentication"):
            response = client.expire_quote_unauthorized(quote_id)
            self.record_api_call(client, "Expire RFQ Quote - Unauthorized", response)

        with allure.step("Validate unauthorized EXPIRE response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert isinstance(body, dict)
                assert body

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with missing API key should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_missing_api_key_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        with allure.step("Submit CREATE RFQ quote request with missing API key"):
            response = client.create_quote_missing_api_key(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote - Missing API Key", response)

        with allure.step("Validate missing API key response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with missing signature should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_missing_signature_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        with allure.step("Submit CREATE RFQ quote request with missing signature"):
            response = client.create_quote_missing_signature(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote - Missing Signature", response)

        with allure.step("Validate missing signature response"):
            assert response.status_code in (400, 401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with missing nonce should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_missing_nonce_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        with allure.step("Submit CREATE RFQ quote request with missing nonce"):
            response = client.create_quote_missing_nonce(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote - Missing Nonce", response)

        with allure.step("Validate missing nonce response"):
            assert response.status_code in (400, 401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with invalid API key should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_invalid_api_key_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        with allure.step("Submit CREATE RFQ quote request with invalid API key"):
            response = client.create_quote_invalid_api_key(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote - Invalid API Key", response)

        with allure.step("Validate invalid API key response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with invalid signature should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_invalid_signature_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        with allure.step("Submit CREATE RFQ quote request with invalid signature"):
            response = client.create_quote_invalid_signature(rfq_payload)
            self.record_api_call(client, "Create RFQ Quote - Invalid Signature", response)

        with allure.step("Validate invalid signature response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with stale nonce should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_stale_nonce_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        stale_nonce = str(int(time.time() * 1000) - 10 * 60 * 1000)
        allure.dynamic.parameter("nonce", stale_nonce)

        with allure.step("Submit CREATE RFQ quote request with stale nonce"):
            response = client.create_quote_with_custom_nonce(rfq_payload, stale_nonce)
            self.record_api_call(client, "Create RFQ Quote - Stale Nonce", response)

        with allure.step("Validate stale nonce response"):
            assert response.status_code in (400, 401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")

    @pytest.mark.negative
    @allure.title("Create RFQ Quote with replayed nonce should fail")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_quote_replayed_nonce_fails(self, client, rfq_payload):
        allure.dynamic.parameter("payload", str(rfq_payload))

        replay_nonce = str(int(time.time() * 1000))
        allure.dynamic.parameter("nonce", replay_nonce)

        with allure.step("Submit first CREATE RFQ quote request with fixed nonce"):
            first_response = client.create_quote_with_custom_nonce(rfq_payload, replay_nonce)
            self.record_api_call(
                client,
                "Create RFQ Quote - Replay Nonce First Attempt",
                first_response,
            )

        with allure.step("Replay same nonce in second CREATE RFQ quote request"):
            second_response = client.create_quote_with_custom_nonce(rfq_payload, replay_nonce)
            self.record_api_call(
                client,
                "Create RFQ Quote - Replay Nonce Second Attempt",
                second_response,
            )

        with allure.step("Validate replayed nonce response"):
            assert first_response.status_code in (200, 400, 401, 403), first_response.text
            assert second_response.status_code in (400, 401, 403), second_response.text

            try:
                body = second_response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_response(body, "rfqCreateQuoteAck")