## 2026-07-23 - Printify Variants API N+1 Bottleneck
**Learning:** The application queries Printify for the same blueprint variants repeatedly inside nested product creation loops (e.g., in printify_manager.py), causing a severe N+1 network bottleneck.
**Action:** Always memoize static third-party API results (like print providers/variants) and return them as immutable tuples using @functools.lru_cache to ensure safety and prevent redundant API calls during bulk generation scripts.
