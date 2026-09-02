"""Checks the persistence metadata without requiring a running PostgreSQL service.
These tests protect the accepted table boundaries and identity constraints."""

from sqlalchemy import UniqueConstraint

from app.database.base import Base
from app.database.models import ApplicationStatus  # noqa: F401


def test_database_metadata_contains_three_job_domain_tables() -> None:
    """Keep raw source data, canonical jobs, and applications in separate tables."""
    assert set(Base.metadata.tables) == {"applications", "jobs", "raw_job_postings"}


def test_raw_postings_have_source_identity_and_published_date() -> None:
    """Ensure source deduplication and posting age remain available to ingestion."""
    table = Base.metadata.tables["raw_job_postings"]
    unique_columns = {
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert "published_at" in table.columns
    assert ("source", "source_job_id") in unique_columns
    assert "content_hash" not in table.columns


def test_application_status_matches_product_brief() -> None:
    """Restrict tracking states to the six statuses accepted for the MVP."""
    assert {status.value for status in ApplicationStatus} == {
        "active",
        "applied",
        "interview",
        "offer",
        "rejected",
        "expired",
    }
