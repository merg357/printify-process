## 2024-05-24 - Memoize Printify Variant API Requests
**Learning:** Fetching blueprint variants inside loops causes N+1 network bottlenecks. When using `@functools.lru_cache` for memoization, returning mutable lists can lead to unintended downstream state mutations from shared references.
**Action:** Always cast cached outputs to immutable structures (like `tuple`) when memoizing API responses in Python to guarantee thread safety and prevent regressions.
