## 2024-05-04 - Printify API N+1 Mitigation
**Learning:** `get_variants` in loops across multiple files causes N+1 network requests to the Printify API for the same blueprint/provider combination.
**Action:** Always memoize `get_variants` or similar static API requests using `@functools.lru_cache(maxsize=None)` to avoid redundant network calls.
