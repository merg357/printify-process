## 2026-06-25 - N+1 Network Bottleneck in Printify Blueprint Iteration
**Learning:** The codebase makes identical network requests to fetch blueprint variants in a nested loop for every image uploaded, resulting in an N+1 API bottleneck that severely impacts performance during product creation.
**Action:** Apply `@functools.lru_cache` to memoize repetitive, static API calls, ensuring to cast the result to an immutable tuple to guarantee thread safety and prevent downstream state mutations.
