## 2026-09-27 - Memoize Printify API Variant Fetches
**Learning:** In loops for bulk product creation across different designs, `get_variants` makes repetitive API requests for the same blueprint and provider IDs, creating an N+1 network bottleneck.
**Action:** Decorate `get_variants` with `@functools.lru_cache(maxsize=None)` and cast the return types to `tuple` to ensure immutability, significantly speeding up bulk operations by eliminating redundant network traffic.
