## 2026-09-20 - Memoize static third-party API configurations in loops
**Learning:** When iterative scripts query third-party APIs (like Printify) for static configurations (e.g., product variants for a blueprint) inside loops, they quickly hit N+1 performance bottlenecks.
**Action:** Memoize these specific configuration lookups using @functools.lru_cache. Always convert the return type from a list to an immutable tuple to guarantee thread-safe caching and prevent downstream mutation.
