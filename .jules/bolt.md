## 2024-06-03 - Memoize API variants as immutable tuples
**Learning:** When using `@functools.lru_cache` to cache JSON response lists from APIs, returning a list can lead to thread safety issues or accidental downstream state mutations.
**Action:** Always cast the return value to an immutable `tuple` and update type hints to ensure safety.
