"""Exposes read-only job discovery endpoints.
The initial route delegates JobTech transport while normalization is built next."""

from typing import Any

import httpx
from fastapi import APIRouter, HTTPException, Query, status

from app.core.config import get_settings
from app.integrations.jobtech.client import JobTechClient

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/search")
async def search_jobs(
    q: str = Query(min_length=1, max_length=200),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
) -> dict[str, Any]:
    """Search JobTech with validated query and pagination parameters."""
    settings = get_settings()
    try:
        async with JobTechClient(
            base_url=settings.jobtech_base_url,
            timeout_seconds=settings.jobtech_timeout_seconds,
        ) as client:
            return await client.search(q=q, limit=limit, offset=offset)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="JobTech is temporarily unavailable.",
        ) from exc
