import time

import allure
import pytest

from src.main.aquanow.utils.base_test import BaseAPITest
from src.main.aquanow.utils.helper import get_data
from src.main.aquanow.utils.assertions import (
    assert_execute_success_contract,
    assert_not_successful_execute,
    assert_error_like_execute_response,
)
from src.main.aquanow.utils.rfq_helpers import create_quote_for_execution
from resources.testdata.rfq_test_data import (
    EXECUTE_QUOTE_CASES,
    NEGATIVE_EXECUTE_CASES,
)


@allure.feature("RFQ Trades")
@pytest.mark.rfq
class TestRFQExecute(BaseAPITest):

    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.CRITICAL)
    def test_execute_quote_success(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("payload_overrides", str(case["payload_overrides"]))

        with allure.step("Create RFQ quote to prepare executable quote"):
            _, _, _, _, quote_id = create_quote_for_execution(
                self, client, settings, rfq_payload, payload_builder, case
            )

        with allure.step("Execute RFQ quote before expiry"):
            execute_response = client.execute_quote(quote_id)
            self.record_api_call(client, "Execute RFQ Quote", execute_response)
            self.assert_status_code(execute_response, 200)

        execute_body = execute_response.json()
        execute_data = get_data(execute_body)

        with allure.step("Validate RFQ execute response"):
            assert_execute_success_contract(
                body=execute_body,
                data=execute_data,
                expected_quote_id=quote_id,
                expected_account_id=settings.account_id,
            )

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        NEGATIVE_EXECUTE_CASES,
        ids=[case["id"] for case in NEGATIVE_EXECUTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_execute_invalid_quote_id_matrix(self, client, case):
        allure.dynamic.title(case["title"])
        allure.dynamic.parameter("quoteId", case["quote_id"])

        with allure.step("Submit execute request with invalid quote ID"):
            response = client.execute_quote(case["quote_id"])
            self.record_api_call(client, "Execute Invalid RFQ Quote", response)

        with allure.step("Validate invalid quote ID response"):
            assert response.status_code in case["expected_statuses"], response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if response.status_code == 200 and body:
                assert_not_successful_execute(body)
            elif body:
                assert_error_like_execute_response(body)

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_execute_expired_quote_behavior(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        allure.dynamic.title(f"Expired RFQ Quote should not execute - {case['id']}")
        allure.dynamic.parameter("payload_overrides", str(case["payload_overrides"]))

        with allure.step("Create RFQ quote"):
            _, _, _, _, quote_id = create_quote_for_execution(
                self, client, settings, rfq_payload, payload_builder, case
            )

        with allure.step("Wait for RFQ quote to expire"):
            time.sleep(9)

        with allure.step("Attempt to execute expired RFQ quote"):
            execute_response = client.execute_quote(quote_id)
            self.record_api_call(client, "Execute Expired RFQ Quote", execute_response)
            self.assert_status_code(execute_response, (200, 400, 404, 422))

        try:
            body = execute_response.json()
        except Exception:
            body = {}

        with allure.step("Validate expired quote does not behave like successful execution"):
            if execute_response.status_code == 200:
                assert_not_successful_execute(body)
            elif body:
                assert_error_like_execute_response(body)

        with allure.step("Validate expiry-related error details when present"):
            if body:
                message = body.get("message") or body.get("error") or body.get("detail")
                if message:
                    assert "expire" in str(message).lower(), (
                        f"Expected expiry-related error message, got: {body}"
                    )

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_execute_manually_expired_quote_behavior(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        allure.dynamic.title(f"Manually expired RFQ Quote should not execute - {case['id']}")
        allure.dynamic.parameter("payload_overrides", str(case["payload_overrides"]))

        with allure.step("Create RFQ quote"):
            _, _, _, _, quote_id = create_quote_for_execution(
                self, client, settings, rfq_payload, payload_builder, case
            )

        with allure.step("Expire RFQ quote explicitly"):
            expire_response = client.expire_quote(quote_id)
            self.record_api_call(client, "Expire RFQ Quote", expire_response)
            self.assert_status_code(expire_response, 200)

        with allure.step("Attempt to execute explicitly expired RFQ quote"):
            execute_response = client.execute_quote(quote_id)
            self.record_api_call(client, "Execute Manually Expired RFQ Quote", execute_response)
            self.assert_status_code(execute_response, (200, 500, 400))

        try:
            body = execute_response.json()
        except Exception:
            body = {}

        with allure.step("Validate manually expired quote does not behave like successful execution"):
            if execute_response.status_code == 200:
                assert_not_successful_execute(body)
            elif body:
                assert_error_like_execute_response(body)

        with allure.step("Validate expiry-related error details when present"):
            if body:
                message = body.get("message") or body.get("error") or body.get("detail")
                if message:
                    assert "expire" in str(message).lower(), (
                        f"Expected expiry-related error message, got: {body}"
                    )

    @pytest.mark.negative
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_execute_quote_without_auth_should_fail(
        self, client, rfq_payload, payload_builder, settings, case
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

        with allure.step("Validate unauthorized execute response"):
            assert response.status_code in (401, 403), response.text

            try:
                body = response.json()
            except Exception:
                body = {}

            if body:
                assert_error_like_execute_response(body)

    @pytest.mark.regression
    @pytest.mark.parametrize(
        "case",
        EXECUTE_QUOTE_CASES,
        ids=[case["id"] for case in EXECUTE_QUOTE_CASES],
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_execute_same_quote_twice(
        self, client, settings, rfq_payload, payload_builder, case
    ):
        allure.dynamic.title(f"RFQ Quote cannot be executed twice - {case['id']}")
        allure.dynamic.parameter("payload_overrides", str(case["payload_overrides"]))

        with allure.step("Create RFQ quote"):
            _, _, _, _, quote_id = create_quote_for_execution(
                self, client, settings, rfq_payload, payload_builder, case
            )

        with allure.step("Execute RFQ quote first time"):
            first_execute = client.execute_quote(quote_id)
            self.record_api_call(client, "Execute RFQ Quote - First", first_execute)
            self.assert_status_code(first_execute, 200)

        first_body = first_execute.json()
        first_data = get_data(first_body)

        with allure.step("Validate first execution response"):
            assert_execute_success_contract(
                body=first_body,
                data=first_data,
                expected_quote_id=quote_id,
                expected_account_id=settings.account_id,
            )

        with allure.step("Execute RFQ quote second time"):
            second_execute = client.execute_quote(quote_id)
            self.record_api_call(client, "Execute RFQ Quote - Second", second_execute)
            self.assert_status_code(second_execute, (200, 500, 400))

        try:
            second_body = second_execute.json()
        except Exception:
            second_body = {}

        with allure.step("Validate second execution does not behave like successful execution"):
            if second_execute.status_code == 200 and second_body:
                assert_not_successful_execute(second_body)
            elif second_body:
                assert_error_like_execute_response(second_body)

        with allure.step("Validate duplicate execution error details when present"):
            if second_body:
                message = (
                    second_body.get("message")
                    or second_body.get("error")
                    or second_body.get("detail")
                )
                if message:
                    assert any(
                        term in str(message).lower()
                        for term in ("already", "execut", "invalid", "used", "expire")
                    ), f"Unexpected duplicate execution message: {second_body}"