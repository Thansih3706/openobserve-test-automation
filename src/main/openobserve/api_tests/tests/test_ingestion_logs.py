import json
import pytest
import allure
from utils.client import ingest_logs, search_logs_with_retry


@pytest.mark.smoke
@allure.title("OpenObserve Logs Smoke - Ingest and Search Verification")
@allure.severity(allure.severity_level.CRITICAL)
def test_ingest_and_search_logs(base_url, org_name, auth, unique_stream_name, sample_logs):
    stream_name = unique_stream_name

    allure.dynamic.parameter("org_name", org_name)
    allure.dynamic.parameter("stream_name", stream_name)
    allure.dynamic.parameter("log_count", len(sample_logs))

    with allure.step("Ingest sample log records into a unique stream"):
        ingest_response = ingest_logs(
            base_url=base_url,
            org_name=org_name,
            auth=auth,
            stream_name=stream_name,
            logs=sample_logs,
        )

        allure.attach(
            json.dumps(sample_logs, indent=2),
            "Request Payload - Ingest Logs",
            allure.attachment_type.JSON,
        )
        allure.attach(
            str(ingest_response.status_code),
            "Ingest Response Status Code",
            allure.attachment_type.TEXT,
        )
        allure.attach(
            ingest_response.text,
            "Ingest Response Body",
            allure.attachment_type.TEXT,
        )

        assert ingest_response.status_code == 200, (
            f"Ingestion failed. Status: {ingest_response.status_code}, "
            f"Body: {ingest_response.text}"
        )

    with allure.step("Search the stream using the logs search API with retry"):
        search_response, search_payload, hits, response_json = search_logs_with_retry(
            base_url=base_url,
            org_name=org_name,
            auth=auth,
            stream_name=stream_name,
            retries=5,
            delay=2,
        )

        allure.attach(
            json.dumps(search_payload, indent=2),
            "Request Payload - Search Logs",
            allure.attachment_type.JSON,
        )
        allure.attach(
            str(search_response.status_code),
            "Search Response Status Code",
            allure.attachment_type.TEXT,
        )
        allure.attach(
            json.dumps(response_json, indent=2),
            "Search Response JSON",
            allure.attachment_type.JSON,
        )

        assert search_response.status_code == 200, (
            f"Search failed. Status: {search_response.status_code}, "
            f"Body: {search_response.text}"
        )

    with allure.step("Validate that ingested records are returned with matching field values"):
        assert len(hits) >= len(sample_logs), (
            f"Expected at least {len(sample_logs)} hits, got {len(hits)}. "
            f"Full response: {response_json}"
        )

        returned_messages = {item.get("message") for item in hits}
        returned_levels = {item.get("level") for item in hits}
        returned_codes = {item.get("code") for item in hits}

        expected_messages = {log["message"] for log in sample_logs}
        expected_levels = {log["level"] for log in sample_logs}
        expected_codes = {log["code"] for log in sample_logs}

        allure.attach(
            json.dumps(sorted(list(returned_messages)), indent=2),
            "Returned Messages",
            allure.attachment_type.JSON,
        )
        allure.attach(
            json.dumps(sorted(list(expected_messages)), indent=2),
            "Expected Messages",
            allure.attachment_type.JSON,
        )
        assert isinstance(response_json, dict), "Search response must be a JSON object"
        assert "hits" in response_json, "Search response missing 'hits' key"
        assert isinstance(hits, list), "'hits' must be a list"

        assert expected_messages.issubset(returned_messages), (
            f"Expected messages {expected_messages} not fully found in returned messages {returned_messages}"
        )
        assert expected_levels.issubset(returned_levels), (
            f"Expected levels {expected_levels} not fully found in returned levels {returned_levels}"
        )
        assert expected_codes.issubset(returned_codes), (
            f"Expected codes {expected_codes} not fully found in returned codes {returned_codes}"
        )