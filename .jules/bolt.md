## 2024-06-01 - Avoid N+1 Network Bottlenecks with Safe Memoization
**Learning:** Memoizing external API queries (like fetching product variants) inside iterative loops prevents severe N+1 network bottlenecks. However, caching mutable objects (like lists) risks downstream mutations. Python's json.dumps() natively serializes tuples to JSON arrays.
**Action:** Always use @functools.lru_cache(maxsize=None) combined with casting returned lists to immutable tuples to safely memoize static third-party API data without risking state mutations.
