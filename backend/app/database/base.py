"""Defines the shared declarative base for persistent application models.
All Alembic metadata is collected through this single database boundary."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Provide common SQLAlchemy metadata for every persisted model."""
