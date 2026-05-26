## 2024-05-02 - N+1 Network Bottleneck in Blueprint Variant Fetching
**Learning:** Discovered a specific performance bottleneck where static blueprint variants are repeatedly fetched in product creation loops (e.g., `create_merch.py`, `create_merch_v2.py`, `merch_factory.py`, `merg_bridge.py`, `printify_manager.py`). This causes an N+1 network call problem during bulk operations.
**Action:** Always use Python's `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries within iterative product creation loops.
