import hashlib
import hmac
import json
import time
from typing import Dict


class AquanowAuth:
    def __init__(self, api_key: str, api_secret: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")

    def _nonce(self) -> str:
        return str(int(time.time() * 1000))

    def build_headers(self, method: str, api_path: str) -> Dict[str, str]:
        nonce = self._nonce()

        signature_content = json.dumps(
            {
                "httpMethod": method.upper(),
                "path": api_path,
                "nonce": nonce,
            },
            separators=(",", ":"),
        )

        signature = hmac.new(
            self.api_secret,
            signature_content.encode("utf-8"),
            hashlib.sha384,
        ).hexdigest()

        return {
            "x-nonce": nonce,
            "x-api-key": self.api_key,
            "x-signature": signature,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }