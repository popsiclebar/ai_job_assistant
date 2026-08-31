"""Exposes a lightweight service-health endpoint.
It lets local tooling verify that FastAPI is running without external dependencies."""

from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Report that the API process can accept requests."""
    return HealthResponse(status="ok")
