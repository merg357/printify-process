## 2026-09-09 - N+1 bottlenecks in Printify variant fetching
**Learning:** The application causes severe N+1 query bottlenecks during its bulk merchandise creation loops (e.g., in printify_manager.py, create_merch.py, and merch_factory.py) by repeatedly fetching the exact same static Printify blueprint variants for every product variation.
**Action:** Always memoize static external data dependencies (like blueprint variants) inside tight creation loops to prevent redundant network requests and drastically improve overall bulk processing time.
