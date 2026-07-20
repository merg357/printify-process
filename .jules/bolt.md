## 2026-07-20 - Cache Printify API variant lookups
**Learning:** Third-party API calls inside iterative product creation loops create severe N+1 performance bottlenecks, especially when the same static resources (like blueprint variants) are fetched repeatedly.
**Action:** Always memoize static or infrequently changing external API dependencies (using `@functools.lru_cache`) when they are invoked within bounded or unbounded loops, ensuring returned data types are immutable (e.g., tuples) to prevent cache poisoning.
