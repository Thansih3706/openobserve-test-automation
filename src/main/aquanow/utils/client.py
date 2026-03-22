from typing import Any, Dict, Optional

import requests

from src.main.aquanow.utils.auth import AquanowAuth
from src.main.aquanow.utils.config import Settings


class AquanowClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.auth = AquanowAuth(settings.api_key, settings.api_secret)
        self.session = requests.Session()
        self.last_request: Dict[str, Any] | None = None

    def _url(self, path: str) -> str:
        return f"{self.settings.base_url}{path}"

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
        auth_enabled: bool = True,
        header_overrides: Optional[Dict[str, Any]] = None,
        headers_to_remove: Optional[list[str]] = None,
    ) -> requests.Response:
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        if auth_enabled:
            headers.update(self.auth.build_headers(method=method, api_path=path))

        if headers_to_remove:
            for header_name in headers_to_remove:
                headers.pop(header_name, None)

        if header_overrides:
            headers.update(header_overrides)

        url = self._url(path)

        self.last_request = {
            "method": method.upper(),
            "path": path,
            "url": url,
            "headers": dict(headers),
            "params": params,
            "json_body": json_body,
        }

        response = self.session.request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            json=json_body,
            timeout=self.settings.request_timeout,
        )
        return response

    def get_quote(self, params: Dict[str, Any]) -> requests.Response:
        return self._request("GET", self.settings.get_quote_path, params=params)

    def create_quote(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request("POST", self.settings.create_quote_path, json_body=payload)

    def execute_quote(self, quote_id: str) -> requests.Response:
        return self._request(
            "POST",
            self.settings.execute_quote_path,
            json_body={"quoteId": quote_id},
        )

    def expire_quote(self, quote_id: str) -> requests.Response:
        return self._request(
            "PUT",
            self.settings.expire_quote_path,
            json_body={"quoteId": quote_id},
        )

    def get_quote_unauthorized(self, params: Dict[str, Any]) -> requests.Response:
        return self._request(
            "GET",
            self.settings.get_quote_path,
            params=params,
            auth_enabled=False,
        )

    def create_quote_unauthorized(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            auth_enabled=False,
        )

    def execute_quote_unauthorized(self, quote_id: str) -> requests.Response:
        return self._request(
            "POST",
            self.settings.execute_quote_path,
            json_body={"quoteId": quote_id},
            auth_enabled=False,
        )

    def expire_quote_unauthorized(self, quote_id: str) -> requests.Response:
        return self._request(
            "PUT",
            self.settings.expire_quote_path,
            json_body={"quoteId": quote_id},
            auth_enabled=False,
        )

    def create_quote_missing_api_key(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            headers_to_remove=["x-api-key"],
        )

    def create_quote_missing_signature(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            headers_to_remove=["x-signature"],
        )

    def create_quote_missing_nonce(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            headers_to_remove=["x-nonce"],
        )

    def create_quote_invalid_api_key(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            header_overrides={"x-api-key": "invalid-api-key"},
        )

    def create_quote_invalid_signature(self, payload: Dict[str, Any]) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            header_overrides={"x-signature": "invalid-signature"},
        )

    def create_quote_with_custom_nonce(self, payload: Dict[str, Any], nonce: str) -> requests.Response:
        return self._request(
            "POST",
            self.settings.create_quote_path,
            json_body=payload,
            header_overrides={"x-nonce": str(nonce)},
        )