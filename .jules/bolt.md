## 2024-05-14 - Memoization of third-party API variant queries
**Learning:** Calling the Printify API repeatedly for unchanged blueprint variant mappings creates an N+1 bottleneck during iterative merchandise generation (e.g. `cmd_create` loop).
**Action:** Always use `@functools.lru_cache(maxsize=None)` for static blueprint queries, while returning immutable `tuple`s to maintain safety and allow caching.
