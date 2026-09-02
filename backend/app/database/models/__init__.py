"""Exports the persistence models that compose the application's database metadata.
Importing this package makes all tables visible to Alembic autogeneration."""

from app.database.models.jobs import Application, ApplicationStatus, Job, RawJobPosting

__all__ = ["Application", "ApplicationStatus", "Job", "RawJobPosting"]
