## 2026-09-08 - Printify API N+1 Queries
**Learning:** Fetching static Printify blueprint variants inside the product creation loop causes N+1 network bottlenecks and risks rate limiting.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize `get_variants`, converting the return type to an immutable tuple to ensure thread-safe caching. JSON serialization natively handles tuples as arrays for the API payload.
