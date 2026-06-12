## 2024-05-24 - Printify API N+1 Bottleneck
**Learning:** The `merch_factory.py` script repeatedly calls the Printify variants API (`get_variants`) for the same blueprint and provider combinations during iterative product creation, leading to a significant N+1 network bottleneck.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries. Always ensure the cached return value is immutable (e.g., cast lists to tuples) to prevent downstream mutations from corrupting the cache.
