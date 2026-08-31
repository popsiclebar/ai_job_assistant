"""Implements asynchronous HTTP transport for JobTech search.
It deliberately returns source payloads until the normalization contract is defined."""

from types import TracebackType
from typing import Any, Self

import httpx


class JobTechClient:
    """Small transport boundary for the public JobTech JobSearch API."""

    def __init__(
        self,
        *,
        base_url: str,
        timeout_seconds: float,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Configure one reusable asynchronous JobTech HTTP session."""
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout_seconds,
            transport=transport,
            headers={"Accept": "application/json"},
        )

    async def __aenter__(self) -> Self:
        """Support scoped client use without leaking network resources."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Close the underlying HTTP session when leaving its scope."""
        await self.aclose()

    async def aclose(self) -> None:
        """Release connections owned by the underlying HTTP client."""
        await self._client.aclose()

    async def search(self, *, q: str, limit: int, offset: int) -> dict[str, Any]:
        """Fetch one validated page of raw JobTech search results."""
        response = await self._client.get(
            "/search",
            params={"q": q, "limit": limit, "offset": offset},
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise httpx.DecodingError("JobTech returned a non-object JSON response")
        return payload
