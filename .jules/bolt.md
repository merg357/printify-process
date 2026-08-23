## 2026-08-23 - Printify Variant N+1 API Bottleneck
**Learning:** Third-party API queries for static metadata (like Printify blueprint variants) are executed redundantly within product creation loops across multiple scripts (e.g., `printify_manager.py`, `merch_factory.py`), creating an N+1 network bottleneck.
**Action:** Always wrap static/infrequently changing API data retrieval functions with `@functools.lru_cache(maxsize=None)` and ensure the return type is cast to an immutable structure (like `tuple`) to maintain thread safety and prevent downstream state mutations when caching.
