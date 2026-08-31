## 2026-08-31 - Memoizing Static Printify API Data in Bulk Operations
**Learning:** In bulk merchandise operations (e.g., Printify integrations), blueprint variant queries inside product creation loops cause significant N+1 network bottlenecks because variant IDs are static per script execution.
**Action:** Use `@functools.lru_cache(maxsize=None)` with an immutable return type (like `tuple`) on these static API queries to safely cache and reuse results across the bulk loop without risking state mutation.
