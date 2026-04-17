import time

from app.core.locks import InMemoryLockStore


def test_set_nx_blocks_and_ttl_releases():
    store = InMemoryLockStore()
    assert store.set_nx("k", "v", ttl_seconds=1) is True
    assert store.set_nx("k", "v2", ttl_seconds=1) is False

    time.sleep(1.1)
    assert store.set_nx("k", "v3", ttl_seconds=1) is True
