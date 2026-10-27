## 2026-10-27 - Memoize static Printify blueprint variant queries
**Learning:** Found an N+1 API bottleneck where the same `get_variants` requests for static blueprint/provider combinations are executed repeatedly inside product creation loops.
**Action:** Use Python's `@functools.lru_cache` on these API wrapper functions. Ensure return types are cast to `tuple` instead of `list` to maintain immutability and thread safety for cached responses. Also verify type hints in upstream and downstream logic.
