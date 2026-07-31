## 2026-07-31 - Printify N+1 Blueprint Variant Fetching
**Learning:** Iterative product creation loops repeatedly fetch static blueprint variants from Printify, causing an N+1 API network bottleneck.
**Action:** Always apply `@functools.lru_cache(maxsize=None)` to static third-party API fetches inside bulk processing loops. Return immutable `tuple` types instead of `list` to ensure thread-safe caching and prevent downstream state mutations, since `json.dumps()` natively serializes tuples into JSON arrays safely.
