#!/usr/bin/env python3
"""
Merch Factory - Creates products from local ./designs/*.png files.
Uploads each image to Printify then creates hoodie/tee/mug drafts.
"""
import requests
import json
import time
import os
import functools
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

API_KEY  = os.getenv("PRINTIFY_TOKEN")
SHOP_ID  = os.getenv("SHOP_ID", "5562421")
BASE_URL = "https://api.printify.com/v1"
HEADERS  = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

# blueprint_id -> (title_keyword, print_provider_id)
BLUEPRINT_MAP = {
    "hoodie": (77,  29),  # Bella Canvas unisex hoodie via Monster Digital
    "tee":    (69,  29),  # Gildan 5000 via Monster Digital
    "mug":    (1039, 29), # 11oz white mug
}
TARGET = {"hoodie": 10, "tee": 10, "mug": 5}

def upload_image(image_path: str) -> str:
    url = f"{BASE_URL}/uploads/images.json"
    with open(image_path, 'rb') as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"file": (os.path.basename(image_path), f, "image/png")}
        )
    resp.raise_for_status()
    image_id = resp.json().get("id")
    if not image_id:
        raise ValueError(f"No image ID returned: {resp.text}")
    return image_id

# 💡 What: Memoize Printify variants API queries and use immutable return types.
# 🎯 Why: Blueprint variants are static. Caching prevents N+1 network requests during bulk creation.
# 📊 Impact: Eliminates redundant API calls, significantly speeding up product creation loops.
# 🛡️ Safety: Returning a tuple prevents unintended mutable state bugs with cached objects.
@functools.lru_cache(maxsize=None)
def get_variants(blueprint_id: int, provider_id: int) -> tuple:
    url = f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers/{provider_id}/variants.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return tuple([v["id"] for v in resp.json().get("variants", [])[:4]])

def create_product(title: str, blueprint_id: int, provider_id: int,
                   variant_ids: list, image_id: str) -> dict:
    url = f"{BASE_URL}/shops/{SHOP_ID}/products.json"
    payload = {
        "title": title,
        "description": "Custom Fire/EMS Dark Humor Gear — Reliable Chaos",
        "blueprint_id": blueprint_id,
        "print_provider_id": provider_id,
        "variants": [{"id": vid, "price": 2999, "is_enabled": True} for vid in variant_ids],
        "print_areas": [{
            "variant_ids": variant_ids,
            "placeholders": [{
                "position": "front",
                "images": [{"id": image_id, "x": 0.5, "y": 0.5, "scale": 1.0, "angle": 0}]
            }]
        }],
        "is_draft": True
    }
    resp = requests.post(url, headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()

def main():
    if not API_KEY:
        print("ERROR: PRINTIFY_TOKEN not set in .env")
        return 1

    designs_dir = Path(os.path.dirname(__file__)) / "designs"
    image_files = sorted(designs_dir.glob("*.png"))
    if not image_files:
        print("No PNG designs found in ./designs/")
        return 1

    remaining = dict(TARGET)
    created = 0
    product_ids = []

    for img_path in image_files:
        if sum(remaining.values()) == 0:
            break

        print(f"\nUploading {img_path.name}...")
        try:
            image_id = upload_image(str(img_path))
            print(f"  Uploaded -> image ID: {image_id}")
        except Exception as e:
            print(f"  Upload failed: {e}")
            continue

        for ptype, (blueprint_id, provider_id) in BLUEPRINT_MAP.items():
            if remaining.get(ptype, 0) <= 0:
                continue
            try:
                variant_ids = get_variants(blueprint_id, provider_id)
                if not variant_ids:
                    print(f"  No variants for {ptype}, skipping")
                    continue
                title = f"Reliable Chaos {img_path.stem.replace('_', ' ').title()} {ptype.title()}"
                product = create_product(title, blueprint_id, provider_id, variant_ids, image_id)
                pid = product.get("id")
                product_ids.append(pid)
                remaining[ptype] -= 1
                created += 1
                print(f"  Created {ptype}: {title} (ID: {pid})")
                time.sleep(0.4)
            except Exception as e:
                print(f"  Error creating {ptype}: {e}")

    with open(os.path.join(os.path.dirname(__file__), 'factory_products.json'), 'w') as f:
        json.dump(product_ids, f, indent=2)
    print(f"\nFactory done: {created} products created. IDs in factory_products.json")
    return 0

if __name__ == "__main__":
    exit(main())
