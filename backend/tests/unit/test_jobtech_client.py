"""Verifies JobTech request construction without using the network.
The test protects query and pagination behavior at the provider boundary."""

import httpx
import pytest

from app.integrations.jobtech.client import JobTechClient


@pytest.mark.asyncio
async def test_search_passes_pagination_and_query() -> None:
    """Confirm search parameters reach the expected JobTech endpoint unchanged."""

    async def handler(request: httpx.Request) -> httpx.Response:
        """Inspect the outgoing request and return a representative source payload."""
        assert request.url.path == "/search"
        assert request.url.params["q"] == "data engineer"
        assert request.url.params["limit"] == "5"
        assert request.url.params["offset"] == "10"
        return httpx.Response(200, json={"total": {"value": 1}, "hits": []})

    async with JobTechClient(
        base_url="https://jobtech.example",
        timeout_seconds=1,
        transport=httpx.MockTransport(handler),
    ) as client:
        result = await client.search(q="data engineer", limit=5, offset=10)

    assert result["hits"] == []
