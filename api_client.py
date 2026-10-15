import requests

from error import APIError, APIResponseError
from helper import format_template, get_by_path


class APIClient:
    def __init__(self, timeout=10):
        self.session = requests.Session()
        self.timeout = timeout

    def build_request(self, api_config, params):
        method = api_config["method"].upper()
        url = format_template(api_config["url"], params)
        headers = format_template(api_config.get("headers", {}), params)
        payload = format_template(api_config.get("payload_template", {}), params)

        kwargs = {}

        if method in ("GET", "HEAD", "DELETE"):
            kwargs["params"] = payload
        else:
            kwargs["json"] = payload

        return method, url, headers, kwargs

    def fetch_balance(self, api_config, params):
        method, url, headers, kwargs = self.build_request(api_config, params)

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
        except requests.RequestException as exc:
            raise APIError(f"HTTP request failed for {url}: {exc}") from exc

        try:
            data = response.json()
        except ValueError as exc:
            raise APIResponseError(
                f"Invalid JSON response from {url}: {exc}"
            ) from exc

        field = api_config["response_balance_field"]
        raw_balance = get_by_path(data, field)

        if raw_balance is None:
            raise APIResponseError(
                f"Balance field '{field}' not found in response from {url}"
            )

        try:
            return float(raw_balance)
        except (TypeError, ValueError) as exc:
            raise APIResponseError(
                f"Balance field '{field}' is not numeric: {raw_balance!r}"
            ) from exc