#!/usr/bin/env python3
"""
Merch Bridge - Full pipeline: upload designs, fetch blueprints, create products.
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
AUTH     = {"Authorization": f"Bearer {API_KEY}"}
HEADERS  = {**AUTH, "Content-Type": "application/json"}

def get_blueprints() -> list:
    url = f"{BASE_URL}/catalog/blueprints.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

# 💡 What: Cache static blueprint variants from Printify
# 🎯 Why: Solves N+1 API bottleneck in product creation loop
# 📊 Impact: Eliminates redundant network requests
# 🛡️ Safety: Returns immutable tuple for cache safety
@functools.lru_cache(maxsize=None)
def get_blueprint_variants(blueprint_id: int, provider_id: int) -> tuple:
    url = f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers/{provider_id}/variants.json"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return tuple(resp.json().get("variants", []))

def upload_image(image_path: str) -> str:
    url = f"{BASE_URL}/uploads/images.json"
    with open(image_path, 'rb') as f:
        resp = requests.post(url, headers=AUTH,
                             files={"file": (os.path.basename(image_path), f, "image/png")})
    resp.raise_for_status()
    image_id = resp.json().get("id")
    if not image_id:
        raise ValueError(f"Upload returned no ID: {resp.text}")
    return image_id

def create_product(blueprint_id: int, provider_id: int, image_id: str,
                   title: str, variant_prices: dict = None) -> dict:
    variants = get_blueprint_variants(blueprint_id, provider_id)
    if not variants:
        raise ValueError(f"No variants for blueprint {blueprint_id}")
    variant_list = []
    for v in variants[:4]:
        vid = v["id"]
        price = variant_prices.get(vid, v.get("price", 2999)) if variant_prices else v.get("price", 2999)
        variant_list.append({"id": vid, "price": price, "is_enabled": True})
    variant_ids = [v["id"] for v in variant_list]

    payload = {
        "title": title,
        "description": "Reliable Chaos brand merchandise.",
        "blueprint_id": blueprint_id,
        "print_provider_id": provider_id,
        "variants": variant_list,
        "print_areas": [{
            "variant_ids": variant_ids,
            "placeholders": [{
                "position": "front",
                "images": [{"id": image_id, "x": 0.5, "y": 0.5, "scale": 1.5, "angle": 0}]
            }]
        }],
        "is_draft": True
    }
    url = f"{BASE_URL}/shops/{SHOP_ID}/products.json"
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code not in (200, 201):
        raise ValueError(f"Create failed {resp.status_code}: {resp.text}")
    return resp.json()

def find_blueprints_by_keyword(blueprints: list, keywords: list) -> list:
    return [bp for bp in blueprints if any(kw in bp.get("title", "").lower() for kw in keywords)]

def main():
    if not API_KEY:
        print("ERROR: PRINTIFY_TOKEN not set in .env")
        return 1

    designs_dir = Path(os.path.dirname(__file__)) / "designs"
    image_files = sorted(designs_dir.glob("*.png"))
    if not image_files:
        print("No PNG designs found in ./designs/ — add images and re-run")
        return 1

    print("Fetching catalog...")
    blueprints = get_blueprints()
    hoodies = find_blueprints_by_keyword(blueprints, ["hoodie"])
    tees    = find_blueprints_by_keyword(blueprints, ["t-shirt", "tee", "unisex"])
    mugs    = find_blueprints_by_keyword(blueprints, ["mug"])
    print(f"Found {len(hoodies)} hoodies, {len(tees)} tees, {len(mugs)} mugs in catalog")

    targets = {"hoodie": (hoodies, 10), "tee": (tees, 10), "mug": (mugs, 5)}
    remaining = {k: v[1] for k, v in targets.items()}
    product_ids = []
    created = 0

    for img_path in image_files:
        if sum(remaining.values()) == 0:
            break
        print(f"\nUploading {img_path.name}...")
        try:
            image_id = upload_image(str(img_path))
            print(f"  -> image ID: {image_id}")
        except Exception as e:
            print(f"  Upload error: {e}")
            continue

        for ptype, (candidates, _) in targets.items():
            if remaining[ptype] <= 0 or not candidates:
                continue
            bp = candidates[0]
            provider_id = bp.get("print_providers", [{}])[0].get("id", 29) if bp.get("print_providers") else 29
            title = f"Reliable Chaos {img_path.stem.replace('_', ' ').title()} {ptype.title()}"
            try:
                product = create_product(bp["id"], provider_id, image_id, title)
                pid = product.get("id")
                product_ids.append(pid)
                remaining[ptype] -= 1
                created += 1
                print(f"  Created {ptype}: {title} (ID: {pid})")
                time.sleep(0.4)
            except Exception as e:
                print(f"  Error: {e}")

    out = os.path.join(os.path.dirname(__file__), 'bridge_products.json')
    with open(out, 'w') as f:
        json.dump(product_ids, f, indent=2)
    print(f"\nBridge done: {created} products. IDs in bridge_products.json")
    return 0

if __name__ == "__main__":
    exit(main())
