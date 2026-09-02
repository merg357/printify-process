## 2026-09-02 - Caching blueprint variants
**Learning:** Found an N+1 query problem where `get_variants` in multiple files repeatedly fetches print provider variants for every product created, leading to unnecessary API calls and latency during bulk creation.
**Action:** Always use `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries (e.g., fetching blueprint variants from Printify). Ensure the return type is cast to a `tuple` instead of a list for thread safety.
