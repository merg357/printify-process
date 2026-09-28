## 2026-09-28 - Memoize static variant queries to prevent N+1 API bottlenecks
**Learning:** During bulk merchandise creation, retrieving variant lists from blueprints triggers redundant network requests inside nested loops (N+1 bottleneck). Since blueprint variants rarely change, they are prime candidates for caching.
**Action:** Always memoize static third-party API queries like variant fetches using `@functools.lru_cache(maxsize=None)` in iterative loops. Return immutable data structures (like tuples) to ensure thread safety and prevent downstream state mutations.
