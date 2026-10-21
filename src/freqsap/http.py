"""Helpers for robust HTTP requests."""

from __future__ import annotations
import time
import requests

RETRY_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


def get_with_retry(
    url: str,
    headers: dict | None = None,
    timeout: int = 10,
    retries: int = 3,
    backoff: float = 1.0,
) -> requests.Response:
    """Perform a GET request, retrying transient failures with exponential backoff.

    Connection errors, timeouts and HTTP 429/5xx responses are retried. If they
    persist, an exception is raised, so failures are never silent.

    Args:
        url (str): URL to query.
        headers (dict | None): HTTP headers.
        timeout (int): Per-request timeout in seconds.
        retries (int): Number of retries after the first attempt.
        backoff (float): Base delay in seconds, doubled after every attempt.

    Returns:
        requests.Response: Response with a non-retryable status code.

    Raises:
        requests.RequestException: If all attempts fail.
    """
    for attempt in range(retries + 1):
        last = attempt == retries
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout):
            if last:
                raise
        else:
            if response.status_code not in RETRY_STATUS_CODES:
                return response
            if last:
                response.raise_for_status()
        time.sleep(backoff * 2**attempt)
    msg = "unreachable"
    raise RuntimeError(msg)
