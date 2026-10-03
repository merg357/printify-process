## 2026-10-03 - Printify Variant Caching
**Learning:** In bulk product creation scripts, querying standard blueprint variants (which rarely change) creates an N+1 network bottleneck because the same blueprint/provider combos are repeatedly requested for each design uploaded.
**Action:** Use `@functools.lru_cache` on static external API fetchers inside product creation loops to eliminate redundant HTTP requests, and cast the return value to an immutable tuple to prevent shared-reference mutations across loops.
