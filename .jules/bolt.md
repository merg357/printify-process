
## 2026-09-06 - Memoize highly static third-party API queries in loops
**Learning:** N+1 network bottlenecks often occur when fetching static variants for the same blueprint/provider during bulk product generation loops.
**Action:** Always use `@functools.lru_cache(maxsize=None)` returning immutable tuples when fetching static reference data (like product variants) inside iterative item creation workflows to eliminate redundant API requests.
