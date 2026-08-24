## 2026-08-24 - Memoizing API queries safely in Python
**Learning:** When using @functools.lru_cache to memoize API responses, returning a mutable list can lead to downstream state mutation bugs if callers modify the list.
**Action:** Always cast memoized data structures to immutable types (like tuple instead of list) and update corresponding downstream type hints to guarantee thread safety and prevent unintended side effects.
