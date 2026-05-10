#!/usr/bin/env python3
"""
Printify Product Bulk Creator
Creates draft products for a Printify shop using hardcoded blueprints.
"""
import requests
import json
import time
import os
import functools
from typing import List, Dict, Any, Tuple
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SHOP_ID = os.getenv("SHOP_ID", "5562421")
API_TOKEN = os.getenv("PRINTIFY_TOKEN")
BASE_URL = "https://api.printify.com/v1"

def get_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

def get_product_blueprints() -> List[Dict[str, Any]]:
    return [
        # Hoodies - Gildan 18500
        {"product_name": "Gildan 18500 Hoodie", "blueprint_id": 1048, "variant_id": None, "color": "Charcoal",       "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Gildan 18500 Hoodie", "blueprint_id": 1048, "variant_id": None, "color": "Navy",           "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Gildan 18500 Hoodie", "blueprint_id": 1048, "variant_id": None, "color": "Safety Orange",  "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Gildan 18500 Hoodie", "blueprint_id": 1048, "variant_id": None, "color": "Military Green", "placement": {"position": "front", "size": 1.5}},
        # Tees - Comfort Colors 1717
        {"product_name": "Comfort Colors 1717 Tee", "blueprint_id": 650, "variant_id": None, "color": "Charcoal",       "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Comfort Colors 1717 Tee", "blueprint_id": 650, "variant_id": None, "color": "Navy",           "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Comfort Colors 1717 Tee", "blueprint_id": 650, "variant_id": None, "color": "Safety Orange",  "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Comfort Colors 1717 Tee", "blueprint_id": 650, "variant_id": None, "color": "Military Green", "placement": {"position": "front", "size": 1.5}},
        # Tees - Bella+Canvas 3001
        {"product_name": "Bella+Canvas 3001 Tee", "blueprint_id": 472, "variant_id": None, "color": "Charcoal",       "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Bella+Canvas 3001 Tee", "blueprint_id": 472, "variant_id": None, "color": "Navy",           "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Bella+Canvas 3001 Tee", "blueprint_id": 472, "variant_id": None, "color": "Safety Orange",  "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Bella+Canvas 3001 Tee", "blueprint_id": 472, "variant_id": None, "color": "Military Green", "placement": {"position": "front", "size": 1.5}},
        # Mugs
        {"product_name": "11oz Mug", "blueprint_id": 1039, "variant_id": None, "color": "White", "placement": {"position": "center_chest", "size": 1.5}},
        {"product_name": "15oz Mug", "blueprint_id": 1040, "variant_id": None, "color": "White", "placement": {"position": "center_chest", "size": 1.5}},
        # Trucker Hats
        {"product_name": "Trucker Hat", "blueprint_id": 1123, "variant_id": None, "color": "Charcoal",       "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Trucker Hat", "blueprint_id": 1123, "variant_id": None, "color": "Navy",           "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Trucker Hat", "blueprint_id": 1123, "variant_id": None, "color": "Safety Orange",  "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Trucker Hat", "blueprint_id": 1123, "variant_id": None, "color": "Military Green", "placement": {"position": "front", "size": 1.5}},
        # Totes
        {"product_name": "Tote Bag", "blueprint_id": 1234, "variant_id": None, "color": "Natural", "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Tote Bag", "blueprint_id": 1234, "variant_id": None, "color": "Black",   "placement": {"position": "front", "size": 1.5}},
        {"product_name": "Tote Bag", "blueprint_id": 1234, "variant_id": None, "color": "Navy",    "placement": {"position": "front", "size": 1.5}},
    ]

# Cache expensive API call results to prevent N+1 network bottlenecks
# Returning a tuple ensures the cached value is immutable to prevent downstream state mutations.
@functools.lru_cache(maxsize=None)
def get_variants(blueprint_id: int, print_provider_id: int = 29) -> Tuple[int, ...]:
    url = f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers/{print_provider_id}/variants.json"
    resp = requests.get(url, headers=get_headers())
    resp.raise_for_status()
    data = resp.json()
    variants = data.get("variants", [])
    return tuple([v["id"] for v in variants[:3]]) if variants else tuple()

def create_product(blueprint_id: int, variant_ids: Tuple[int, ...], product_name: str,
                   color: str, placement: Dict[str, Any]) -> Dict[str, Any]:
    logo_url = os.getenv("LOGO_URL", "https://via.placeholder.com/300x300.png?text=Reliable+Chaos")
    url = f"{BASE_URL}/shops/{SHOP_ID}/products.json"
    product_data = {
        "title": f"Reliable Chaos {product_name} - {color}",
        "description": f"Reliable Chaos branded {product_name}",
        "tags": ["Reliable Chaos", product_name, color],
        "blueprint_id": blueprint_id,
        "print_provider_id": 29,
        "variants": [{"id": vid, "price": 2500, "is_enabled": True} for vid in variant_ids],
        "print_areas": [{
            "variant_ids": variant_ids,
            "placeholders": [{
                "position": placement.get("position", "front"),
                "images": [{"id": None, "x": 0.5, "y": 0.5, "scale": placement.get("size", 1.5), "angle": 0}]
            }]
        }],
        "print_on_side": "off",
        "is_draft": True
    }
    resp = requests.post(url, headers=get_headers(), json=product_data)
    resp.raise_for_status()
    return resp.json()

def main():
    if not API_TOKEN:
        print("ERROR: PRINTIFY_TOKEN not set in .env")
        return 1

    blueprints = get_product_blueprints()
    product_ids = []
    total = len(blueprints)

    for idx, product in enumerate(blueprints, 1):
        print(f"[{idx}/{total}] Creating: {product['product_name']} - {product['color']}")
        try:
            variant_ids = get_variants(product['blueprint_id'])
            if not variant_ids:
                print(f"  ! No variants found for blueprint {product['blueprint_id']}, skipping")
                continue
            result = create_product(
                blueprint_id=product['blueprint_id'],
                variant_ids=variant_ids,
                product_name=product['product_name'],
                color=product['color'],
                placement=product['placement']
            )
            pid = result.get('id')
            if pid:
                product_ids.append(pid)
                print(f"  OK product ID: {pid}")
            time.sleep(0.5)
        except requests.exceptions.RequestException as e:
            print(f"  ERR: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"       {e.response.text}")
            continue

    with open('product_ids.json', 'w') as f:
        json.dump(product_ids, f, indent=2)
    print(f"\nDone: {len(product_ids)}/{total} products created. IDs in product_ids.json")
    return 0

if __name__ == "__main__":
    exit(main())
