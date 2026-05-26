## 2024-05-18 - [Network Optimization in Bulk Processing Scripts]
**Learning:** Repetitive third-party API queries for static data (like blueprint variants) inside loops cause severe network bottlenecks. The script was calling `get_variants` repeatedly for the same blueprint IDs during bulk creation.
**Action:** Use Python`s `@functools.lru_cache(maxsize=None)` to memoize these network-bound functions, significantly reducing execution time during bulk runs without sacrificing code readability.
