## 2024-05-24 - Memoizing Printify API queries
**Learning:** In product creation loops, querying the Printify API for variants (or blueprints) repeatedly causes a significant N+1 network bottleneck because the data is static per blueprint/provider.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize these static third-party API queries.
