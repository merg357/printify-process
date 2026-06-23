## 2024-06-23 - Memoizing Static Printify Blueprint Queries
**Learning:** In batch merchandise creation pipelines (e.g., `printify_manager.py`), fetching blueprint variants repeatedly causes N+1 network bottlenecks because the variants for a specific blueprint and provider rarely change during a single execution.
**Action:** Use `@functools.lru_cache(maxsize=None)` on `get_variants` and ensure the return type is explicitly cast to a `tuple` (e.g., `tuple(...)`) to ensure immutability and thread safety for cached responses, while updating type hints appropriately.
