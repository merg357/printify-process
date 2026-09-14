## 2026-09-14 - Memoize Printify Blueprint Variant Queries
**Learning:** Third-party API calls for static blueprint variants within iterative product creation loops create an N+1 network bottleneck.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize these responses, casting the returned list to an immutable `tuple` to guarantee thread safety and prevent downstream state mutations.
