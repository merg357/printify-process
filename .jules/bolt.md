## 2026-07-07 - Memoizing API queries returning lists
**Learning:** When using @functools.lru_cache to prevent N+1 API queries (like fetching product variants), returning mutable objects like lists can lead to downstream state mutations.
**Action:** Cast the return type to an immutable structure (e.g., tuple) and explicitly update type hints (-> tuple) to guarantee thread safety and prevent regressions.
