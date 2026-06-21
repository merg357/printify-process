## YYYY-MM-DD - Memoizing Printify API Variant Lookups
**Learning:** Making repeated requests for static data like Printify variant blueprints creates a severe N+1 network bottleneck during bulk merchandise creation loops. While standard `lru_cache` works perfectly for this, caching mutable list returns is an anti-pattern that risks downstream state mutations.
**Action:** Always cast memoized, shared, read-only structures to immutable tuples (e.g., changing list comprehensions to tuple comprehensions) when introducing `functools.lru_cache` to API fetch functions.
