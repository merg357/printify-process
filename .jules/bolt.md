## 2026-10-01 - Memoization of third-party API queries in product loops
**Learning:** Iterative loops that generate products based on fixed configurations (like Printify blueprints) often suffer from N+1 network requests because they re-fetch identical data (like variant IDs) on every iteration.
**Action:** Always use `@functools.lru_cache` to memoize static or infrequently changing API queries within creation loops, and cast the cached return type to an immutable structure (like a `tuple`) to prevent downstream state mutation bugs.
