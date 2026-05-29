## 2024-05-29 - Safe Memoization of API Responses
**Learning:** When using `@functools.lru_cache` to memoize third-party API queries returning parsed JSON lists, returning a mutable list can lead to thread-safety issues or unintended downstream state mutations due to shared references across batch iterations.
**Action:** Always cast the output of cached API response data to an immutable structure (e.g., `tuple(...)`) and update type hints accordingly to guarantee thread safety, preserve application state, and leverage caching safely in bulk network ops.
