## 2026-08-10 - Memoize Variant API Queries with Tuples
**Learning:** When using @functools.lru_cache to memoize API calls (like fetching Printify blueprint variants) to prevent N+1 bottlenecks, returning a mutable list can lead to thread-safety issues or unintended state mutations downstream if callers modify the result.
**Action:** Cast the return type to an immutable structure like `tuple` (which serializes safely with `json.dumps`) and explicitly update downstream function type hints (e.g., from `list` to `tuple[int, ...]`) when applying LRU caching to network operations.
