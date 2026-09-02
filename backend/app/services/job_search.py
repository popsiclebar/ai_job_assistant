"""Coordinates one user-initiated search from application input to normalized jobs.
This boundary owns provider configuration while routes remain limited to HTTP concerns."""

from app.core.config import Settings
from app.integrations.jobtech.client import JobTechClient
from app.integrations.jobtech.normalizer import normalize_search_result
from app.schemas.jobs import JobSearchRequest, JobSearchResponse


async def search_jobtech_jobs(
    search_request: JobSearchRequest,
    settings: Settings,
) -> JobSearchResponse:
    """Execute one JobTech query and return its source-independent representation."""
    async with JobTechClient(
        base_url=settings.jobtech_base_url,
        timeout_seconds=settings.jobtech_timeout_seconds,
        api_key=settings.jobtech_api_key,
    ) as client:
        source_result = await client.search(
            query=search_request.query,
            limit=search_request.limit,
            offset=search_request.offset,
            sort=search_request.sort,
            remote=search_request.remote,
            experience_required=search_request.experience_required,
        )
    return normalize_search_result(source_result, search_request)
