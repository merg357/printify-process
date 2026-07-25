## 2026-07-25 - Memoization of 3rd Party API Calls in Iteration Loops
**Learning:** Using lru_cache in iterative product creation loops on third-party APIs (like Printify) avoids N+1 network bottlenecks, but must return immutable types like tuples to prevent unintended downstream mutations.
**Action:** Always memoize static or infrequently changing third-party API queries within iterative loops using @functools.lru_cache, and explicitly convert parsed JSON lists to immutable tuples.
