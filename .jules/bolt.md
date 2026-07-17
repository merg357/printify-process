## 2026-07-17 - N+1 Network Bottlenecks in Bulk API Operations
**Learning:** The application's architecture heavily relies on iterative bulk processing loops that repeatedly fetch static third-party API data (like Printify blueprint variants). This causes severe N+1 network request bottlenecks.
**Action:** When implementing bulk API operations, proactively memoize static lookups (e.g., using `@functools.lru_cache(maxsize=None)`) and return immutable structures (like tuples) to prevent redundant network I/O while ensuring thread safety.
