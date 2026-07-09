## 2026-07-09 - Printify API N+1 Network Bottleneck
**Learning:** Fetching static blueprint variants from Printify inside an iterative product creation loop (like `cmd_create`) causes severe N+1 network latency. By default, API wrappers re-fetch identical data per iteration.
**Action:** Always memoize static/infrequently changing third-party API queries using `@functools.lru_cache` and ensure returned data structures (like lists) are cast to immutable types (e.g. tuples) to prevent shared reference mutations.
