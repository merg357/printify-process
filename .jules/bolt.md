## 2024-06-25 - Printify Variant API Memoization
**Learning:** During bulk merchandise creation across multiple scripts (`printify_manager.py`, `create_merch.py`, `merch_factory.py`, `merg_bridge.py`), fetching product variants for standard blueprints created an N+1 API call bottleneck. Each iteration requested static blueprint data redundantly, slowing down processing loops significantly.
**Action:** Always use `@functools.lru_cache(maxsize=None)` to memoize static or infrequently changing third-party API queries (like blueprint definitions) within iterative product creation loops.
