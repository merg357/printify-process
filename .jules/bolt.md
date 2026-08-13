## 2026-08-13 - Memoizing API queries with immutable tuples
**Learning:** Using `@functools.lru_cache` to cache N+1 network queries for product variants is highly effective in iterative creation loops. However, caching functions that return mutable objects (like lists) risks unintended downstream mutations.
**Action:** Always cast the return value of memoized JSON responses to an immutable structure like a `tuple` to ensure thread safety and state preservation. Also remember that `json.dumps()` natively serializes tuples into JSON arrays, making them safe drop-in replacements.
