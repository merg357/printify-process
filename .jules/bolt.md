## 2026-10-15 - Memoize variant API queries
**Learning:** Calling static third-party API queries (e.g., fetching blueprint variants from Printify) within iterative product creation loops causes an N+1 network bottleneck.
**Action:** Use Python's @functools.lru_cache(maxsize=None) to memoize these responses, ensuring the return type is cast to an immutable structure (like tuple) to guarantee thread safety and prevent unintended downstream state mutations.
