## 2026-07-28 - Memoizing API queries safely in Python
**Learning:** Using @functools.lru_cache on third-party API queries prevents severe N+1 network bottlenecks during bulk iterations. However, caution must be applied when the original function returns a mutable object (like a list) since caching shares the same reference.
**Action:** Always cast the return value to an immutable type (like a tuple) when using lru_cache for API responses to guarantee thread safety and avoid downstream state mutations. Ensure type hints reflect the new return type.
