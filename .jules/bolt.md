## 2026-07-04 - N+1 Network Bottleneck in Printify API Loops
**Learning:** Fetching blueprint variants inside loops like `cmd_create` causes redundant network calls because blueprints/providers are static per run. Caching these responses avoids N+1 requests, but caching mutable lists can cause cross-loop state pollution.
**Action:** Use `@functools.lru_cache(maxsize=None)` for static third-party API lookups and cast the result to an immutable `tuple` (updating the type hint to `-> tuple[int, ...]`) to guarantee thread safety while keeping compatibility with `json.dumps()`.
