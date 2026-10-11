## 2026-10-11 - Printify API N+1 Bottleneck
**Learning:** During bulk merchandise operations, iterating over images and dynamically fetching blueprint variants via `get_variants` causes an N+1 network bottleneck because the blueprints are static per run.
**Action:** Use `@functools.lru_cache(maxsize=None)` to memoize third-party API lookups that return static catalog data within loops. Always cast the returned parsed JSON lists to immutable `tuple[int, ...]` to ensure cache thread safety and prevent downstream state mutations, as `json.dumps()` serializes tuples perfectly into JSON arrays.
