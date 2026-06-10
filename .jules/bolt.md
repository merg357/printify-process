## 2024-06-10 - N+1 Network Bottleneck in Bulk Pipeline
**Learning:** Repeatedly fetching static blueprint variants from Printify within iterative product creation loops causes an N+1 network bottleneck. Since JSON parsing returns mutable lists, using `functools.lru_cache` safely requires converting the return type to an immutable tuple.
**Action:** Use `@functools.lru_cache(maxsize=None)` for static third-party API queries in loops, and cast the return value to a `tuple` to ensure immutability and thread safety.
