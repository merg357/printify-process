## 2026-10-26 - Memoize Printify Variant Queries
**Learning:** During batch product creation processes, the same Printify blueprint `get_variants` queries are repeatedly executed for each product being generated, resulting in an N+1 network bottleneck.
**Action:** Apply `@functools.lru_cache(maxsize=None)` to static third-party API query functions to cache their results, and strictly cast the return types to immutable tuples instead of lists to guarantee thread safety and prevent downstream state mutations in cache-enabled functions.
