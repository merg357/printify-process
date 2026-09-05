## 2026-09-05 - Memoization of third-party API results in loops
**Learning:** The application queries a third-party API for standard static resources (product variants) inside an iterative product creation loop, causing significant N+1 network overhead.
**Action:** Always use Python's `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries. Cast the return type to an immutable structure (like `tuple`) to guarantee thread safety and prevent downstream modification from shared references.
