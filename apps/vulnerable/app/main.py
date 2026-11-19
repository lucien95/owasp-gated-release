"""Expense Claims API, VULNERABLE version. Deliberately insecure; see README.md."""

from fastapi import FastAPI

from app import auth, claims, imports

# PLANTED FLAW (A02:2025 Security Misconfiguration): debug mode returns full stack traces,
# including SQL text, to whoever caused the error.
app = FastAPI(title="Expense Claims API (vulnerable)", version="0.4.0", debug=True)
app.include_router(auth.router)
app.include_router(imports.router)
app.include_router(claims.router)


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: answers 'ok' while the process is running."""
    return {"status": "ok"}
