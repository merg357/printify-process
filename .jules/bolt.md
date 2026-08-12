## 2026-08-12 - Cache N+1 API Calls
**Learning:** N+1 network bottlenecks occur when creating multiple products that query the same Printify blueprint variants repeatedly.
**Action:** Apply @functools.lru_cache to memoize static or infrequently changing third-party API queries in bulk creation loops. Ensure the cached return value is cast to an immutable type (like tuple) to guarantee thread safety and prevent downstream state mutations.
