## 2024-06-07 - Optimize redundant Printify API variant queries
**Learning:** Repeatedly fetching unchanged product variants from the Printify API during bulk merchandise creation loops causes N+1 network bottlenecks.
**Action:** Apply @functools.lru_cache(maxsize=None) to memoize the static third-party API queries. To guarantee thread safety and prevent unintended downstream state mutations from shared references in cache, cast the return type to an immutable structure (e.g., tuple) and explicitly update all corresponding Python type hints in the function signature.
