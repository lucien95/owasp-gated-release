"""Expense Claims API, VULNERABLE version. Deliberately insecure; see README.md."""

from fastapi import FastAPI

app = FastAPI(title="Expense Claims API (vulnerable)", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: answers 'ok' while the process is running."""
    return {"status": "ok"}
