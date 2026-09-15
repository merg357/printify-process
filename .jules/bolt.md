## 2026-09-15 - N+1 Network Bottleneck in Printify Bulk Creation
**Learning:** Bulk merchandise creation loops query the same static catalog data (like blueprint variants) repeatedly, causing severe N+1 API bottlenecks and risking rate limits.
**Action:** Always wrap static third-party API queries in product-creation loops with @functools.lru_cache(maxsize=None) and ensure they return immutable types (like tuples) to guarantee thread safety.
