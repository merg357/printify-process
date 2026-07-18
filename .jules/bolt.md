## 2026-07-18 - Memoize redundant third-party API queries
**Learning:** Iterating over multiple products with the same printify blueprint_id results in duplicate network requests (N+1 bottlenecks) if variants are fetched synchronously per product.
**Action:** Always use Python's @functools.lru_cache(maxsize=None) returning an immutable tuple to safely memoize static third-party API queries in product creation loops.
