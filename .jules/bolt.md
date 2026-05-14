## 2024-05-14 - Memoizing Static API Resources
**Learning:** Making repetitive API calls for static blueprint variants within a loop causes severe network bottlenecking (N+1 queries) when bulk creating products on third-party APIs. Returning mutable objects from a cache can lead to unpredictable state regressions.
**Action:** Always wrap invariant third-party fetch queries in `@functools.lru_cache(maxsize=None)` during bulk creation loops, and rigorously cast the cached return type to an immutable type like `tuple` to ensure thread-safety and prevent reference mutation bugs.
