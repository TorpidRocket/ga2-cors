from __future__ import annotations

import time
import uuid
from typing import Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response

EMAIL = "22f3002879@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-zfmw2q.example.com"

app = FastAPI(title="Descriptive Statistics API", version="1.0.0")


@app.middleware("http")
async def request_headers_and_cors(request: Request, call_next):
    """Add request metadata to every response and enforce the exact origin allowlist."""
    started = time.perf_counter()
    request_id = str(uuid.uuid4())
    origin = request.headers.get("origin")

    # Handle CORS preflight explicitly so even preflight responses get our headers.
    if request.method == "OPTIONS" and request.url.path == "/stats":
        if origin == ALLOWED_ORIGIN:
            response = Response(status_code=204)
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            requested_headers = request.headers.get("access-control-request-headers")
            if requested_headers:
                # Echo requested header names; this is safe because the origin is allowlisted.
                response.headers["Access-Control-Allow-Headers"] = requested_headers
            response.headers["Vary"] = "Origin"
        else:
            response = JSONResponse(status_code=403, content={"detail": "CORS origin not allowed"})
    else:
        response = await call_next(request)
        if origin == ALLOWED_ORIGIN:
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Vary"] = "Origin"
        # Do not emit ACAO for any other origin.

    elapsed = max(0.0, time.perf_counter() - started)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{elapsed:.6f}"
    return response


@app.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")) -> dict[str, Any]:
    try:
        # Reject empty elements and non-integer values rather than silently ignoring them.
        parts = values.split(",")
        if not parts or any(part.strip() == "" for part in parts):
            raise ValueError("empty value")
        numbers = [int(part.strip()) for part in parts]
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="values must be a comma-separated list of integers")

    if not numbers:
        raise HTTPException(status_code=400, detail="at least one integer is required")

    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": sum(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "mean": sum(numbers) / len(numbers),
    }


@app.get("/")
async def root():
    return {"service": "Descriptive Statistics API", "endpoint": "/stats?values=1,2,3"}


@app.get("/health")
async def health():
    return {"status": "ok"}
