## 2026-09-29 - Memoize Printify variant API queries
**Learning:** Using `@functools.lru_cache` to memoize static third-party API queries in bulk product creation loops prevents N+1 network bottlenecks. However, returning mutable lists from cached functions can lead to unintended downstream state mutations from shared references.
**Action:** Cast the return type to an immutable structure (like `tuple`) when using `lru_cache` to guarantee thread safety and prevent regressions. Update all downstream type hints accordingly.
