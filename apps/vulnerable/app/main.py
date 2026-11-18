"""Expense Claims API, VULNERABLE version. Deliberately insecure; see README.md."""

from fastapi import FastAPI

from app import auth

app = FastAPI(title="Expense Claims API (vulnerable)", version="0.2.0")
app.include_router(auth.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: answers 'ok' while the process is running."""
    return {"status": "ok"}
