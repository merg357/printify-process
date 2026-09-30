## 2026-09-30 - Printify API N+1 Queries
**Learning:** Found an N+1 API query bottleneck during bulk product creation where static Printify catalog variants were repeatedly fetched over the network.
**Action:** Always apply `@functools.lru_cache(maxsize=None)` and cast results to `tuple` to ensure immutability for static data lookups in creation loops.
