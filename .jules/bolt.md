## 2026-09-10 - Memoize Variant API Queries
**Learning:** Printify API queries for variants (like `get_variants`) are called for every product creation, leading to N+1 network requests during batch processing.
**Action:** Always use `@functools.lru_cache(maxsize=None)` and return immutable `tuple` types to memoize static or infrequently changing third-party API queries within iterative loops.
