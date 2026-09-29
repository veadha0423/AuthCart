# AuthCart API

FastAPI service for user authentication, product browsing, and user-owned shopping carts.

## Run locally

Create and activate a virtual environment, install dependencies, then start the API:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
if (-not (Test-Path env/.env)) { Copy-Item env/.env.example env/.env }
uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`.

Set a unique `AUTHCART_SECRET_KEY` in `env/.env` before starting the app. Keep that
file private; it is ignored by Git and excluded from Docker build context.

## Run with Docker

After creating and configuring `env/.env`, start the API with:

```powershell
docker compose up --build
```

Compose injects the values at runtime instead of baking them into the image.

## Tests

```powershell
python -m unittest discover -s tests
```

## Project layout

```text
app/
  api/
    endpoints/    # Auth, product, and cart endpoints
    router.py     # API route aggregation
  core/           # Settings and security helpers
  db/             # Engine, session, and ORM base
  models.py       # SQLAlchemy entities
  schemas.py      # Request schemas
  main.py         # FastAPI application and lifespan
tests/            # Automated checks
```