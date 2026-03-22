import allure
import requests


class BaseAPITest:
    def attach_last_request(self, client, name: str) -> None:
        if not getattr(client, "last_request", None):
            return

        last_request = client.last_request

        from src.main.aquanow.utils.helper import attach_request_details

        attach_request_details(
            name=name,
            method=last_request.get("method"),
            url=last_request.get("url"),
            headers=last_request.get("headers"),
            params=last_request.get("params"),
            json_body=last_request.get("json_body"),
        )

    def attach_response(self, name: str, response: requests.Response) -> None:
        from src.main.aquanow.utils.helper import attach_response_details

        attach_response_details(name, response)

    def record_api_call(self, client, name: str, response: requests.Response) -> None:
        self.attach_last_request(client, name)
        self.attach_response(name, response)

    def assert_status_code(self, response: requests.Response, expected_codes) -> None:
        if isinstance(expected_codes, int):
            expected_codes = (expected_codes,)

        assert response.status_code in expected_codes, (
            f"Unexpected status code {response.status_code}. "
            f"Expected one of {expected_codes}. Response body: {response.text}"
        )

    def attach_text(self, name: str, value: str) -> None:
        allure.attach(str(value), name, allure.attachment_type.TEXT)

    def attach_json_text(self, name: str, value: str) -> None:
        allure.attach(str(value), name, allure.attachment_type.JSON)