## 2026-07-24 - Cache Printify API variants for batch loops
**Learning:** During iterative batch operations (like product creation loops), third-party API queries for static or infrequently changing resources (e.g., blueprint variants) create N+1 network bottlenecks.
**Action:** Apply `@functools.lru_cache(maxsize=None)` to memoize these network requests. Cast the parsed JSON return values from lists to immutable tuples to ensure thread safety and prevent accidental downstream state mutations, updating type hints appropriately.
