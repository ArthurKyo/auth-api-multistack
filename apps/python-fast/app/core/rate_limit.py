from collections import defaultdict, deque
from threading import Lock
from time import monotonic

from fastapi import HTTPException, Request, status


class InMemoryRateLimiter:
    def __init__(self):
        self._hits: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: int) -> None:
        now = monotonic()
        cutoff = now - window_seconds

        with self._lock:
            hits = self._hits[key]
            while hits and hits[0] <= cutoff:
                hits.popleft()

            if len(hits) >= limit:
                retry_after = max(1, int(window_seconds - (now - hits[0])))
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests",
                    headers={"Retry-After": str(retry_after)},
                )

            hits.append(now)

    def clear(self) -> None:
        with self._lock:
            self._hits.clear()


rate_limiter = InMemoryRateLimiter()


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"
