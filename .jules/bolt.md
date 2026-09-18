## 2026-09-18 - Memoizing API queries in bulk loops
**Learning:** Fetching static data (like variants) inside loops causes N+1 bottlenecks.
**Action:** Memoize using `@functools.lru_cache` and convert lists to tuples for thread-safe caching.
