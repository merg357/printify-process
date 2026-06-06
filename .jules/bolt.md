## 2024-05-18 - Safe Caching for API Responses
**Learning:** When using `@functools.lru_cache` to memoize responses, returning mutable objects (like parsed JSON lists) can lead to unintended downstream state mutations from shared references.
**Action:** Always cast the return type to an immutable structure (e.g., `tuple`) and update typing to guarantee thread safety and prevent regressions.
