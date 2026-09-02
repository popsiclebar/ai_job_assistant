"""Defines source, canonical job, and personal application persistence models.
Raw provider fidelity stays separate from normalized job and workflow state."""

import uuid
from datetime import date, datetime
from enum import StrEnum

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class ApplicationStatus(StrEnum):
    """Restrict application tracking to the lifecycle accepted in the product brief."""

    ACTIVE = "active"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    EXPIRED = "expired"


class Job(Base):
    """Represent one normalized real-world opportunity shared by source listings."""

    __tablename__ = "jobs"
    __table_args__ = (
        CheckConstraint(
            "work_mode IS NULL OR work_mode IN ('on_site', 'hybrid', 'remote')",
            name="ck_jobs_work_mode",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    company: Mapped[str | None] = mapped_column(Text)
    location: Mapped[str | None] = mapped_column(Text)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)
    employment_start: Mapped[str | None] = mapped_column(Text)
    employment_type: Mapped[str | None] = mapped_column(Text)
    work_schedule: Mapped[str | None] = mapped_column(Text)
    work_mode: Mapped[str | None] = mapped_column(String(20))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    application_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    application_url: Mapped[str | None] = mapped_column(Text)


class RawJobPosting(Base):
    """Retain the latest complete payload for one source-specific job listing."""

    __tablename__ = "raw_job_postings"
    __table_args__ = (
        UniqueConstraint("source", "source_job_id", name="uq_raw_job_source_identity"),
        UniqueConstraint("id", "job_id", name="uq_raw_job_and_canonical_job"),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="SET NULL"),
        index=True,
    )
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    source_job_id: Mapped[str] = mapped_column(String(255), nullable=False)
    source_url: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    retrieved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    raw_payload: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False)


class Application(Base):
    """Track the user's status and generated documents for one canonical job."""

    __tablename__ = "applications"
    __table_args__ = (
        ForeignKeyConstraint(
            ["raw_job_posting_id", "job_id"],
            ["raw_job_postings.id", "raw_job_postings.job_id"],
            name="fk_application_source_for_job",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    raw_job_posting_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True))
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(
            ApplicationStatus,
            name="application_status",
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        nullable=False,
        default=ApplicationStatus.ACTIVE,
        server_default=ApplicationStatus.ACTIVE.value,
    )
    application_date: Mapped[date | None] = mapped_column(Date)
    resume_html: Mapped[str | None] = mapped_column(Text)
    cover_letter_html: Mapped[str | None] = mapped_column(Text)
