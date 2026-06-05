## 2024-06-05 - Caching Printify Variant Fetches
**Learning:** Using `@functools.lru_cache(maxsize=None)` with immutable tuples prevents N+1 network queries when repeatedly fetching blueprint variants. We must return a `tuple` to ensure thread safety and prevent downstream mutation.
**Action:** Always cast the return type to `tuple` when memoizing list responses from APIs.
