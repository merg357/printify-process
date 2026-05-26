## 2024-05-18 - Memoizing Printify Catalog Queries
**Learning:** The application queries Printify for product blueprint variants repeatedly during bulk product creation, leading to N+1 network requests since these variants rarely change.
**Action:** Always apply Python's `@functools.lru_cache(maxsize=None)` to functions fetching static catalog data in loops to eliminate redundant network bottlenecks.
