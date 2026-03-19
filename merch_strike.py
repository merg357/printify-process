#!/usr/bin/env python3
"""
Merch Strike - Fetch all products and save to DATA_DELIVERY.json (no auth version was broken).
"""
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

API_KEY = os.getenv("PRINTIFY_TOKEN")
SHOP_ID = os.getenv("SHOP_ID", "5562421")

if not API_KEY:
    print("ERROR: PRINTIFY_TOKEN not set in .env")
    exit(1)

headers = {"Authorization": f"Bearer {API_KEY}"}
response = requests.get(
    f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json?limit=100",
    headers=headers
)
if response.status_code == 200:
    with open('DATA_DELIVERY.json', 'w') as f:
        json.dump(response.json(), f, indent=2)
    data = response.json()
    count = len(data.get("data", []))
    print(f"Saved {count} products to DATA_DELIVERY.json")
else:
    print(f"Failed: {response.status_code} - {response.text}")
