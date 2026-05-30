#!/usr/bin/env python3
"""
Create Merch V2 - Bulk create 25 draft products with dynamic variant fetch.
"""
import requests
import json
import time
import os
import functools
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN   = os.getenv("PRINTIFY_TOKEN")
SHOP_ID = os.getenv("SHOP_ID", "5562421")
LOGO    = os.getenv("LOGO_URL", "https://via.placeholder.com/300x300.png?text=Reliable+Chaos")

if not TOKEN:
    print("ERROR: PRINTIFY_TOKEN not set in .env")
    exit(1)

HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# (blueprint_id, print_provider_id, label)
BLUEPRINTS = [
    (77,   29, "Bella Canvas Tee"),
    (69,   29, "Gildan Tee"),
    (107,  29, "All Cotton Tee"),
    (11,   29, "Hoodie"),
]

# Why: Prevents repeated N+1 network requests for blueprint variants in the loop.
# Impact: Eliminates redundant API calls, significantly speeding up bulk processing.
# Safety: We return an immutable tuple to prevent shared reference mutations.
@functools.lru_cache(maxsize=None)
def get_variants(bp_id: int, provider_id: int) -> tuple:
    var_url = f"https://api.printify.com/v1/catalog/blueprints/{bp_id}/print_providers/{provider_id}/variants.json"
    resp = requests.get(var_url, headers=HEADERS)
    if resp.status_code != 200:
        return None
    variants = resp.json().get("variants", [])
    if not variants:
        return tuple()
    return tuple(v["id"] for v in variants[:3])

created_products = []

for i in range(25):
    bp_id, provider_id, label = BLUEPRINTS[i % len(BLUEPRINTS)]

    # Fetch real variants
    variant_ids = get_variants(bp_id, provider_id)
    if variant_ids is None:
        print(f"[{i+1}] Could not get variants for {label}")
        continue
    if not variant_ids:
        print(f"[{i+1}] No variants for {label}, skipping")
        continue

    product_data = {
        "title": f"Reliable Chaos Industrial Logo {i+1} — {label}",
        "description": "Reliable Chaos Fire/EMS Dark Humor Gear",
        "blueprint_id": bp_id,
        "print_provider_id": provider_id,
        "variants": [{"id": vid, "price": 2499, "is_enabled": True} for vid in variant_ids],
        "print_areas": [{
            "variant_ids": variant_ids,
            "placeholders": [{
                "position": "front",
                "images": [{"id": None, "x": 0.5, "y": 0.5, "scale": 1.5, "angle": 0}]
            }]
        }],
        "is_draft": True
    }

    url = f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json"
    resp = requests.post(url, headers=HEADERS, json=product_data)
    if resp.status_code in (200, 201):
        pid = resp.json().get("id")
        created_products.append(pid)
        print(f"[{i+1}] Created: {pid}")
    else:
        print(f"[{i+1}] Failed {resp.status_code}: {resp.text[:120]}")
    time.sleep(0.5)

out = os.path.join(os.path.dirname(__file__), 'products_v2.json')
with open(out, 'w') as f:
    json.dump(created_products, f, indent=2)
print(f"\nDone: {len(created_products)}/25 products created.")
