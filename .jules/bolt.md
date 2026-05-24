## 2024-05-30 - Prevent N+1 API Calls with LRU Cache and Tuples
**Learning:** Using `@functools.lru_cache` on functions that fetch third-party API data within iterative product creation loops prevents N+1 network bottlenecks. When caching API responses, returning mutable objects like lists can cause unintended downstream state mutations from shared references.
**Action:** Always cast cached return values to immutable structures (e.g., `tuple`) and update type hints to guarantee thread safety and prevent functional regressions.
