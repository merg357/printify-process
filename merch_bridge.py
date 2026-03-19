#!/usr/bin/env python3
"""
Merch Bridge (stub) - Sync designs from ./designs/ folder to Printify.
Calls merg_bridge.py logic. Run merg_bridge.py for full pipeline.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

API_KEY = os.getenv("PRINTIFY_TOKEN")
SHOP_ID = os.getenv("SHOP_ID", "5562421")

def sync_designs(folder="./designs"):
    path = Path(folder)
    images = sorted(path.glob("*.png"))
    if not images:
        print("No PNG designs found. Add images to ./designs/ first.")
        return
    print(f"Found {len(images)} designs to sync:")
    for img in images:
        print(f"  {img.name}")
    print("\nRun merg_bridge.py for the full upload + product creation pipeline.")

if __name__ == "__main__":
    sync_designs(os.path.join(os.path.dirname(__file__), "designs"))
