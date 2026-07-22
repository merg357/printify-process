## 2024-07-22 - Network bottlenecks in bulk processing
**Learning:** Found an N+1 network bottleneck where third-party API queries (like fetching printify variants) inside product creation loops are repeated unnecessarily.
**Action:** Always memoize static or infrequently changing third-party API queries using `@functools.lru_cache(maxsize=None)` to prevent redundant network requests and N+1 bottlenecks.
