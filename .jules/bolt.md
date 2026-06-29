## 2026-06-29 - Memoizing Static API Endpoints
**Learning:** Iterative product creation in `printify_manager.py` causes an N+1 network bottleneck because static blueprint variants are fetched via API for every single product generated.
**Action:** Use `@functools.lru_cache(maxsize=None)` and convert the return type to an immutable tuple to memoize static Printify API variant queries across repetitive blueprint iterations.
