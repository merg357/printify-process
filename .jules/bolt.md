## 2026-10-08 - Memoize repeated blueprint API calls
**Learning:** In static-blueprint loops (e.g., creating merch across multiple designs), repeatedly calling get_variants on the Printify API for the same blueprint causes severe N+1 bottlenecks.
**Action:** Use @functools.lru_cache(maxsize=None) for third-party variant API calls in bulk processing loops, ensuring the return type is cast to a tuple to avoid mutable state side-effects from cached lists.
