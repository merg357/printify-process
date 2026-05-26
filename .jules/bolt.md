## 2024-05-26 - Immutable Caching with lru_cache
**Learning:** When using `functools.lru_cache` to cache JSON response parts, it is crucial to return immutable structures like tuples instead of lists. This prevents downstream mutations of cached lists, which would otherwise corrupt the shared cache for N+1 queries.
**Action:** Always cast list comprehensions or dictionary structures derived from API JSON to tuples (or custom immutable structures) before returning them from an `@lru_cache` decorated function.
