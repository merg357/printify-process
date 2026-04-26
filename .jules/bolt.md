## 2024-05-24 - Memoize Printify Blueprint API Calls
**Learning:** During bulk operations (like uploading designs and creating products), the codebase repeatedly requested the exact same blueprint variants from the Printify API. This static data caused significant network bottlenecks and N+1 query problems because multiple products often share the same blueprint.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` on repetitive and static third-party API queries (like fetching blueprint variants) to prevent network bottlenecks during bulk processing loops.
