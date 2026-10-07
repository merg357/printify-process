## 2026-10-07 - Memoize static third-party API data in loops
**Learning:** Fetching static data (like blueprint variants) inside a bulk creation loop causes severe N+1 network bottlenecks.
**Action:** Apply `@functools.lru_cache(maxsize=None)` to memoize the API responses, ensuring the return types are converted to immutable tuples (e.g., `tuple(v["id"] ...)`) for thread-safety and consistent caching.
