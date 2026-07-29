## 2026-07-29 - Printify API N+1 Bottleneck in Product Creation
**Learning:** Printify blueprint variant APIs are queried repetitively inside O(M*N) loops (Images × Blueprints) during bulk product creation, causing severe N+1 network bottlenecks since variants are static per blueprint/provider.
**Action:** Always use `@functools.lru_cache(maxsize=None)` for static third-party API queries like `get_variants` inside iterative loops, ensuring the return value is cast to an immutable `tuple` for thread safety and cache integrity.
