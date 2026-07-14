## 2026-07-14 - Cache Static API Queries to Prevent N+1

**Learning:** Static third-party API queries (like fetching product variants from Printify) within product creation loops create severe N+1 network bottlenecks, needlessly multiplying HTTP requests for the same exact data.
**Action:** Use `@functools.lru_cache(maxsize=None)` to memoize these lookup functions. When doing so, always ensure the cached function returns an immutable structure (like `tuple` instead of `list`) to guarantee thread safety and prevent downstream state mutations from shared references.
