## 2026-09-03 - Cache repeated API metadata calls
**Learning:** In bulk operation scripts (like creating multiple merchandise designs across the same set of products), fetching invariant provider data (e.g., variants) in the inner loop causes an N+1 network bottleneck.
**Action:** Use `@functools.lru_cache(maxsize=None)` for API metadata lookups and cast the return value to an immutable type (like `tuple`) to ensure safe memoization.
