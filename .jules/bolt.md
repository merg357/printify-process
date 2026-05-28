## 2024-05-28 - Caching API calls in iterative loops
**Learning:** Found N+1 query patterns in Printify API loops across `merg_bridge.py` and `create_merch.py`. Multiple items with the same blueprint ID repeatedly trigger network requests for the same static variants data.
**Action:** Always wrap third-party lookup functions (like blueprint variants) with `@functools.lru_cache(maxsize=None)` when iterating over items, and ensure thread safety by casting the return type to an immutable `tuple`.
