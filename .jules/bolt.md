## 2026-06-27 - LRU Cache Immutable Cast
**Learning:** Returning a mutable list from a cached function caused state issues when shared. Casting API variant lists to tuples allows safe memoization.
**Action:** Always cast return values to tuples when using @functools.lru_cache for API lookups.
