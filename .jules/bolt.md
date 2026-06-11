## 2024-05-24 - Printify API N+1 Mitigation with Tuple Caching
**Learning:** When using `@functools.lru_cache` to memoize third-party API queries (like fetching blueprint variants in `printify_manager.py`), returning mutable lists can lead to unintended downstream state mutations. Also, `json.dumps()` natively serializes Python tuples into JSON arrays, so they are safe drop-in replacements for API payloads.
**Action:** Always cast cached JSON lists to `tuple` and update function type hints (e.g., `-> tuple`) when applying memoization to network-bound data retrieval functions.
