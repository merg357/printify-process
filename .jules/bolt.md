## 2026-08-09 - Safe API Response Memoization
**Learning:** In Python, `json.dumps()` natively serializes tuples into JSON arrays. This means we can memoize third-party API responses using `@functools.lru_cache` safely by returning immutable tuples instead of mutable lists without changing any downstream JSON serialization logic.
**Action:** Always cast cached list comprehensions to tuples when memoizing API queries used in JSON payloads to guarantee thread safety and prevent state mutation.
