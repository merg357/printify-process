#!/usr/bin/env python3
"""
Strike - Fetch product list and save compact JSON to DATA_DELIVERY.json.
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN   = os.getenv("PRINTIFY_TOKEN")
SHOP_ID = os.getenv("SHOP_ID", "5562421")

if not TOKEN:
    print("ERROR: PRINTIFY_TOKEN not set in .env")
    exit(1)

headers = {"Authorization": f"Bearer {TOKEN}"}
response = requests.get(
    f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json?limit=100",
    headers=headers
)

if response.status_code == 200:
    data = response.json()
    products = [{"id": p.get("id"), "title": p.get("title"), "is_draft": p.get("is_draft")}
                for p in data.get("data", [])]
    out_path = os.path.join(os.path.dirname(__file__), 'DATA_DELIVERY.json')
    with open(out_path, 'w') as f:
        json.dump({"products": products}, f, indent=2)
    print(f"Saved {len(products)} products to DATA_DELIVERY.json")
else:
    print(f"Error {response.status_code}: {response.text}")
