## 2026-08-22 - Memoizing bulk API operations
**Learning:** In bulk operations (like creating many products), identical API queries for static data (like blueprints) create severe N+1 network bottlenecks. Returning mutable lists from `@functools.lru_cache` can lead to unintended downstream mutations of cached references.
**Action:** Always memoize static third-party API queries in iterative product creation loops using `@functools.lru_cache(maxsize=None)` and return immutable structures (e.g., `tuple`) to prevent N+1 issues and ensure thread safety.
