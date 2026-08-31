# Backend

The backend is a FastAPI modular monolith. Install it in a virtual environment with `pip install -r requirements-dev.txt`, then run `uvicorn app.main:app --reload`.

Current endpoints:

- `GET /api/v1/health`
- `GET /api/v1/jobs/search?q=data+engineer&limit=10&offset=0`

The JobTech endpoint is a live, read-only passthrough for the first executable slice. Normalization, persistence, and deduplication will be added behind this API boundary.
