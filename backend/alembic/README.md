# Database migrations

Alembic owns PostgreSQL schema changes for the backend. From this directory, run `alembic upgrade head` to apply pending migrations or `alembic downgrade -1` to reverse the latest migration during local development.

The migration environment reads `DATABASE_URL` through the same application settings used by FastAPI. Create the ignored root `.env` from `.env.example` before running database commands.
