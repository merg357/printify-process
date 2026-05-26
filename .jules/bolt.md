## 2024-05-24 - Memoize Printify Variant API Calls
**Learning:** During iterative product creation loops across multiple scripts (e.g. `create_merch.py`, `merch_factory.py`, `printify_manager.py`), fetching variants for the same blueprint IDs causes an N+1 network bottleneck because the data is static but requested repeatedly for each product.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries like `get_variants` within iterative product creation loops to eliminate the redundant network requests.
