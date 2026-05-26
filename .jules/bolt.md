## 2024-06-25 - N+1 Bottleneck in API Query Memoization
**Learning:** Found an N+1 network bottleneck across Python scripts managing bulk merch creation (`create_merch.py`, `merch_factory.py`, `printify_manager.py`). The `get_variants` function is called redundantly for the same `blueprint_id` and `print_provider_id` inside iterative product loops.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize these static third-party API queries to avoid redundant network overhead during bulk operations.
