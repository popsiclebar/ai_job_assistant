"""Implements asynchronous HTTP transport and response validation for JobTech search.
The client stays source-specific while application services consume typed provider models."""

from types import TracebackType
from typing import Self

import httpx

from app.integrations.jobtech.schemas import JobTechSearchResult


class JobTechClient:
    """Small transport boundary for the public JobTech JobSearch API."""

    def __init__(
        self,
        *,
        base_url: str,
        timeout_seconds: float,
        api_key: str | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        """Configure one reusable asynchronous JobTech HTTP session."""
        headers = {"Accept": "application/json"}
        if api_key:
            headers["api-key"] = api_key

        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            timeout=timeout_seconds,
            transport=transport,
            headers=headers,
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

    async def search(
        self,
        *,
        query: str,
        limit: int,
        offset: int,
        sort: str,
        remote: bool | None,
        experience_required: bool | None,
    ) -> JobTechSearchResult:
        """Fetch and validate one page of current JobTech advertisements."""
        params: dict[str, str | int | bool] = {
            "q": query,
            "limit": limit,
            "offset": offset,
            "sort": sort,
        }
        if remote is not None:
            params["remote"] = remote
        if experience_required is not None:
            params["experience"] = experience_required

        response = await self._client.get(
            "/search",
            params=params,
        )
        response.raise_for_status()
        return JobTechSearchResult.model_validate_json(response.content)
