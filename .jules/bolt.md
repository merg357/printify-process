## 2026-08-25 - Memoizing Variant API Queries
**Learning:** In bulk merchandise creation loops, querying third-party APIs for static blueprint variants causes an N+1 network bottleneck, adding significant latency per product.
**Action:** Always use Python's `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries. Ensure the return type is cast to an immutable structure (e.g., `tuple`) to guarantee thread safety and prevent unintended downstream state mutations from shared references.
