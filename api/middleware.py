"""Rate limiting and error handling. Auth is optional: set API_TOKEN to require a bearer token."""
import os
import time
from collections import defaultdict, deque

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

RATE_LIMIT = int(os.getenv("RATE_LIMIT_PER_MIN", "30"))


def install(app: FastAPI) -> None:
    hits: dict[str, deque] = defaultdict(deque)

    @app.middleware("http")
    async def guard(request: Request, call_next):
        token = os.getenv("API_TOKEN")
        if token and request.headers.get("authorization") != f"Bearer {token}":
            return JSONResponse({"detail": "unauthorized"}, status_code=401)
        ip = request.client.host if request.client else "?"
        now = time.time()
        q = hits[ip]
        while q and now - q[0] > 60:
            q.popleft()
        if len(q) >= RATE_LIMIT:
            return JSONResponse({"detail": "rate limit exceeded"}, status_code=429)
        q.append(now)
        try:
            return await call_next(request)
        except Exception as e:  # last-resort handler so clients get JSON, not a stack trace
            return JSONResponse({"detail": f"internal error: {type(e).__name__}"}, status_code=500)
