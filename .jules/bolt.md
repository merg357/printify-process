## 2026-07-30 - N+1 Network Bottleneck in Printify Merch Creation
**Learning:** During bulk product generation, fetching blueprint variants for every single item causes a severe N+1 API bottleneck. Since blueprint and print provider variants are static, this results in significant unnecessary network overhead.
**Action:** Use `@functools.lru_cache(maxsize=None)` with an immutable tuple return type for third-party variant queries in loops to safely eliminate redundant requests without mutating state.
