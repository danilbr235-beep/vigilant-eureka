from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


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


lock_store = InMemoryLockStore()
