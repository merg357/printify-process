
## 2026-08-05 - Blueprint Variant N+1 Bottleneck in Iterative Product Creation
**Learning:** The `create_product` loop repeatedly requests invariant variant IDs for the same blueprint and provider. Because Printify blueprints are stable, caching the response prevents an N+1 API bottleneck, but requires returning an immutable `tuple` so the cache isn't mutated by JSON serialization in subsequent requests.
**Action:** Apply `@functools.lru_cache(maxsize=None)` and change return types to `tuple[int, ...]` for all functions that fetch static catalog data within iterative creation loops.
