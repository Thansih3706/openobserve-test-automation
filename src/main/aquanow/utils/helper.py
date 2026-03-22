import json
from typing import Any, Dict

import allure
import requests


def get_data(body: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(body, dict):
        return {}
    return body.get("data", {})


def quote_id_from_response(body: Dict[str, Any]) -> str | None:
    return get_data(body).get("quoteId")


def response_type(body: Dict[str, Any]) -> str | None:
    if not isinstance(body, dict):
        return None
    return body.get("type")


def pretty_json(data: Any) -> str:
    try:
        return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=False)
    except Exception:
        return str(data)


def attach_request_details(
    *,
    name: str,
    method: str,
    url: str,
    headers: Dict[str, Any] | None = None,
    params: Dict[str, Any] | None = None,
    json_body: Dict[str, Any] | None = None,
) -> None:
    allure.attach(method, f"{name} - HTTP Method", allure.attachment_type.TEXT)
    allure.attach(url, f"{name} - URL", allure.attachment_type.TEXT)

    if headers is not None:
        safe_headers = dict(headers)
        if "x-signature" in safe_headers:
            safe_headers["x-signature"] = "***masked***"
        if "x-api-key" in safe_headers:
            safe_headers["x-api-key"] = "***masked***"

        allure.attach(
            pretty_json(safe_headers),
            f"{name} - Request Headers",
            allure.attachment_type.JSON,
        )

    if params is not None:
        allure.attach(
            pretty_json(params),
            f"{name} - Query Params",
            allure.attachment_type.JSON,
        )

    if json_body is not None:
        allure.attach(
            pretty_json(json_body),
            f"{name} - Request Body",
            allure.attachment_type.JSON,
        )


def attach_response_details(name: str, response: requests.Response) -> None:
    allure.attach(
        str(response.status_code),
        f"{name} - HTTP Status Code",
        allure.attachment_type.TEXT,
    )

    try:
        allure.attach(
            pretty_json(dict(response.headers)),
            f"{name} - Response Headers",
            allure.attachment_type.JSON,
        )
    except Exception:
        pass

    try:
        body = response.json()
        allure.attach(
            pretty_json(body),
            f"{name} - Response Body",
            allure.attachment_type.JSON,
        )
    except Exception:
        allure.attach(
            response.text,
            f"{name} - Response Body",
            allure.attachment_type.TEXT,
        )