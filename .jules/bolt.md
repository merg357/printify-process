## 2024-06-09 - N+1 Network Bottlenecks in API Scripts
**Learning:** Making repetitive third-party API calls for static or infrequently changing data (like Printify blueprint variants) within an iteration loop creates severe N+1 network bottlenecks. When caching list returns, returning mutable objects can lead to unintended downstream modifications.
**Action:** Always use `@functools.lru_cache(maxsize=None)` on functions that fetch static configuration data and ensure the cached return values are cast to immutable types (like `tuple`) to guarantee thread safety and prevent regressions.
