## 2026-10-06 - Cache Printify Blueprint Variants
**Learning:** In the Printify product creation scripts (`printify_manager.py`, `create_merch.py`, `merch_factory.py`), fetching variants for the same blueprint and print provider is repeatedly executed inside loops creating an N+1 query issue.
**Action:** Use `@functools.lru_cache(maxsize=None)` to memoize the `get_variants` functions across these scripts. Ensure the return type is cast to a `tuple` (immutable) to prevent downstream modification issues from the shared cache state.
