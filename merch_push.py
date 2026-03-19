#!/usr/bin/env python3
"""
Merch Push - List all products in the shop.
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN   = os.getenv("PRINTIFY_TOKEN")
SHOP_ID = os.getenv("SHOP_ID", "5562421")

if not TOKEN:
    print("ERROR: PRINTIFY_TOKEN not set in .env")
    exit(1)

def get_products():
    url = f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json?limit=100"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        products = data.get("data", [])
        print(f"Found {len(products)} products:\n")
        for p in products:
            status = "DRAFT" if p.get("is_draft") else "LIVE"
            print(f"  [{status}] {p.get('id')} — {p.get('title')}")
        return products
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

if __name__ == "__main__":
    get_products()
