## 2026-10-19 - Cache N+1 API Calls
**Learning:** Static blueprint configuration endpoints (like variant info) are unnecessarily hit repeatedly during nested looping logic (N+1 queries), creating a noticeable and severe backend network bottleneck.
**Action:** Use Python's `@functools.lru_cache` directly on the retrieval methods (e.g. `get_variants`), but crucially ensure the returned list is explicitly cast to a `tuple` prior to being cached, preserving immutability to prevent unexpected downstream mutation issues across instances.
