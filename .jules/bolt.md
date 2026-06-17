## 2026-06-17 - Prevent N+1 API calls with LRU caching
**Learning:** In bulk product creation loops, querying the API for the same blueprint variants repeatedly causes significant N+1 network latency bottlenecks. Caching mutable lists can lead to unintended state mutations down the line.
**Action:** Always use `@functools.lru_cache(maxsize=None)` to memoize infrequently changing third-party API data, and ensure you cast the return type to an immutable `tuple` (with appropriate `tuple[int, ...]` type hints) to guarantee thread safety while remaining compatible with `json.dumps()`.
