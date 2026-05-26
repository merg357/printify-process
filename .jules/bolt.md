## 2024-05-24 - Memoizing Static Printify Blueprint Queries
**Learning:** During bulk operations, the project redundantly queried the Printify API for the same product blueprint variants across multiple items (e.g., repeating the same HTTP request for each Gildan Tee or Hoodie design). This network bottleneck significantly slowed down the bulk creation loop.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` on repetitive and static third-party API query functions (like `get_variants`) to memoize responses, drastically reducing network calls and speeding up the processing loops.
