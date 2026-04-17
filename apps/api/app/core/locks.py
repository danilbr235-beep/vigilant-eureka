from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol

from app.core.config import settings


class LockStore(Protocol):
    def set_nx(self, key: str, value: str, ttl_seconds: int) -> bool: ...

    def get(self, key: str) -> str | None: ...

    def delete(self, key: str) -> None: ...


@dataclass
class _Entry:
    value: str
    expires_at: datetime


class InMemoryLockStore:
    def __init__(self) -> None:
        self._data: dict[str, _Entry] = {}

    def set_nx(self, key: str, value: str, ttl_seconds: int) -> bool:
        now = datetime.now(timezone.utc)
        self._cleanup(now)
        if key in self._data:
            return False
        self._data[key] = _Entry(value=value, expires_at=now + timedelta(seconds=ttl_seconds))
        return True

    def get(self, key: str) -> str | None:
        now = datetime.now(timezone.utc)
        self._cleanup(now)
        entry = self._data.get(key)
        return entry.value if entry else None

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def _cleanup(self, now: datetime) -> None:
        expired = [k for k, v in self._data.items() if v.expires_at <= now]
        for key in expired:
            del self._data[key]


class RedisLockStore:
    def __init__(self, redis_url: str) -> None:
        import redis

        self.client = redis.Redis.from_url(redis_url, decode_responses=True)

    def set_nx(self, key: str, value: str, ttl_seconds: int) -> bool:
        return bool(self.client.set(key, value, ex=ttl_seconds, nx=True))

    def get(self, key: str) -> str | None:
        return self.client.get(key)

    def delete(self, key: str) -> None:
        self.client.delete(key)


def build_lock_store() -> LockStore:
    if settings.redis_url:
        try:
            return RedisLockStore(settings.redis_url)
        except Exception:
            return InMemoryLockStore()
    return InMemoryLockStore()


lock_store: LockStore = build_lock_store()
