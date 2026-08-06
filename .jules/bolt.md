## 2026-08-06 - Cache Third-Party API Iteration Calls
**Learning:** Using `@functools.lru_cache(maxsize=None)` on third-party API queries inside product iteration loops drastically minimizes N+1 bottlenecks for identical payload constraints like blueprint variants.
**Action:** When returning memoized list comprehensions, wrap the data into an immutable tuple ensuring shared cached state stays untampered by downstream list operations and maintains thread safety.
