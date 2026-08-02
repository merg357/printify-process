## 2026-08-02 - LRU Cache immutability for API Responses
**Learning:** When using @functools.lru_cache to memoize third-party API queries in Python, returning mutable objects like lists can cause unintended state mutations if modified downstream.
**Action:** Always cast the return type of cached API responses to an immutable structure like a tuple and explicitly update the type hints (e.g., -> tuple).
