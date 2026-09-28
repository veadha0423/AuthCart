# AuthCart API

FastAPI service for user authentication, product browsing, and user-owned shopping carts.

## Run locally

Create and activate a virtual environment, install dependencies, then start the API:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:AUTHCART_SECRET_KEY = "replace-with-a-long-random-secret"
uvicorn app.main:app --reload
```

The API documentation is available at `http://127.0.0.1:8000/docs`.

Copy `.env.example` as a reference for supported environment variables. Do not use the
development fallback secret in a deployed environment.

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