# AI Job Seeking Assistant

A local-first application for discovering Swedish jobs, evaluating job fit, preparing truthful HTML application documents, and tracking applications.

The project is currently in its foundation phase. The first executable slice contains a FastAPI backend, a typed JobTech client boundary, and a minimal Next.js frontend.

## Repository layout

- `backend/` — FastAPI, deterministic workflows, agents, retrieval, and persistence.
- `frontend/` — Next.js dashboard and job/application/profile interfaces.
- `docs/` — public architecture and usage documentation.
- `.agents/` — ignored local decisions, plans, and progress notes.

The backend is a modular monolith. Agents, RAG, database access, and external integrations have explicit internal boundaries but share one deployable backend until independent scaling is justified.

## Safety

This repository is intended to be public. Never commit:

- API keys or `.env` files
- resumes or other personal documents
- fetched job payloads or local databases
- generated resumes, cover letters, or application exports

Use `.env.example` as the configuration template.

## Development

Backend:

```bash
cp .env.example .env
docker compose up -d postgres
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000`. Backend API documentation is available at `http://localhost:8000/docs`.

## Current scope

See [docs/architecture.md](docs/architecture.md) for the public module boundaries. Detailed decisions, plans, and progress are maintained locally in the ignored `.agents/` directory.
