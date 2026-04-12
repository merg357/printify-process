## 2024-05-24 - Memoizing Static API Calls in Bulk Processing
**Learning:** Repetitive third-party API queries (like fetching blueprint variants from Printify) inside bulk processing loops create severe N+1 bottlenecks.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize functions that return static data fetched from APIs to prevent redundant network calls during loops.
