## 2026-10-04 - Cache repetitive static external API calls
**Learning:** Blueprint variants from Printify don't change within a script run, so querying them per product inside a loop results in massive N+1 bottlenecks.
**Action:** Use `@functools.lru_cache` to memoize `get_variants` style functions. Be sure to return immutable `tuple` types instead of `list` to guarantee safe caching.
