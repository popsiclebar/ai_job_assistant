"""Creates raw postings, canonical jobs, and personal application tracking.

Revision ID: 20260902_0001
Revises:
Create Date: 2026-09-02
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "20260902_0001"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

application_status = postgresql.ENUM(
    "active",
    "applied",
    "interview",
    "offer",
    "rejected",
    "expired",
    name="application_status",
    create_type=False,
)


def upgrade() -> None:
    """Create the first persistence schema and its integrity constraints."""
    application_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("company", sa.Text(), nullable=True),
        sa.Column("location", sa.Text(), nullable=True),
        sa.Column("job_description", sa.Text(), nullable=False),
        sa.Column("employment_start", sa.Text(), nullable=True),
        sa.Column("employment_type", sa.Text(), nullable=True),
        sa.Column("work_schedule", sa.Text(), nullable=True),
        sa.Column("work_mode", sa.String(length=20), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("application_deadline", sa.DateTime(timezone=True), nullable=True),
        sa.Column("application_url", sa.Text(), nullable=True),
        sa.CheckConstraint(
            "work_mode IS NULL OR work_mode IN ('on_site', 'hybrid', 'remote')",
            name="ck_jobs_work_mode",
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "raw_job_postings",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source", sa.String(length=50), nullable=False),
        sa.Column("source_job_id", sa.String(length=255), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "retrieved_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("raw_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id", "job_id", name="uq_raw_job_and_canonical_job"),
        sa.UniqueConstraint("source", "source_job_id", name="uq_raw_job_source_identity"),
    )
    op.create_index("ix_raw_job_postings_job_id", "raw_job_postings", ["job_id"])

    op.create_table(
        "applications",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("job_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("raw_job_posting_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "status",
            application_status,
            server_default="active",
            nullable=False,
        ),
        sa.Column("application_date", sa.Date(), nullable=True),
        sa.Column("resume_html", sa.Text(), nullable=True),
        sa.Column("cover_letter_html", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["raw_job_posting_id", "job_id"],
            ["raw_job_postings.id", "raw_job_postings.job_id"],
            name="fk_application_source_for_job",
        ),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("job_id"),
    )


def downgrade() -> None:
    """Remove the first persistence schema and its enum type."""
    op.drop_table("applications")
    op.drop_index("ix_raw_job_postings_job_id", table_name="raw_job_postings")
    op.drop_table("raw_job_postings")
    op.drop_table("jobs")
    application_status.drop(op.get_bind(), checkfirst=True)
