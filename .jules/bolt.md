## 2026-09-07 - Caching External API Calls in Creation Loops
**Learning:** Repetitive external API requests to fetch static data (like Printify variant IDs) inside loops cause N+1 network bottlenecks, severely slowing down bulk operations.
**Action:** Use `@functools.lru_cache(maxsize=None)` to memoize these calls, but ensure the return type is cast to an immutable structure like `tuple` instead of `list` to maintain thread safety and prevent downstream state mutations.
