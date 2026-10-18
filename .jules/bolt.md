## 2026-10-18 - Memoize variant API queries
**Learning:** Bulk product creation loops trigger N+1 network bottlenecks when frequently querying static third-party API endpoints (e.g., Printify blueprint variants).
**Action:** Always memoize static or infrequently changing third-party API queries within iterative loops using `@functools.lru_cache`. Cast list responses to tuples to ensure thread safety and prevent downstream state mutations.
