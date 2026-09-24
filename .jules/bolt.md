## 2026-09-24 - Memoization of static Printify API queries
**Learning:** Discovered an N+1 API bottleneck in bulk product creation scripts where identical blueprint variant queries were redundantly fetched for each individual item being processed.
**Action:** Always memoize (e.g., using @functools.lru_cache) static or infrequently changing third-party API configurations within iterative generation loops to eliminate redundant network overhead, ensuring returned sequences are cast to immutable types (like tuples) to prevent shared-cache mutations.
