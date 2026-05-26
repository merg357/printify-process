## 2024-04-09 - Caching Third-Party API Responses
**Learning:** Repetitive third-party API queries in loops (such as fetching static variant/blueprint data from Printify) can become severe bottlenecks. This is especially true when a small number of blueprints are queried repeatedly across many products.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize API calls for data that does not change during the script's execution, drastically reducing network overhead and improving execution time.
