"""Defines the stable response contract for API health checks.
The literal status prevents accidental expansion of the initial endpoint."""

from typing import Literal

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Represent a healthy API process."""

    status: Literal["ok"]
