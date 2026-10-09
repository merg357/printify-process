#!/usr/bin/env python3
"""
Printify Manager - Unified CLI for all Printify operations.

Usage:
  python3 printify_manager.py list                   # List all products
  python3 printify_manager.py upload                 # Upload all PNGs in ./designs/ (resumes on re-run)
  python3 printify_manager.py upload-url <url> <name>  # Upload image from URL
  python3 printify_manager.py create                 # Create products from uploaded designs
  python3 printify_manager.py run                    # Full pipeline: upload + create
  python3 printify_manager.py sync-github <owner/repo> [branch] [folder]  # Upload PNGs from GitHub repo
  python3 printify_manager.py run-github <owner/repo> [branch] [folder]   # Sync from GitHub + create products
  python3 printify_manager.py dump                   # Save product list to DATA_DELIVERY.json
  python3 printify_manager.py delete <id> [<id>...]  # Delete products by ID
  python3 printify_manager.py delete-all-drafts      # Delete all draft products
  python3 printify_manager.py check                  # Check API token is valid
"""
import sys
import os
import functools
import json
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

TOKEN    = os.getenv("PRINTIFY_TOKEN")
SHOP_ID  = os.getenv("SHOP_ID", "5562421")
BASE_URL = "https://api.printify.com/v1"
AUTH_H   = {"Authorization": f"Bearer {TOKEN}"}
JSON_H   = {**AUTH_H, "Content-Type": "application/json"}
UPLOAD_CACHE = os.path.join(os.path.dirname(__file__), "uploaded_images.json")

# Product blueprints: (blueprint_id, print_provider_id, label)
BLUEPRINTS = [
    (77,   29, "Bella Canvas Tee"),
    (69,   29, "Gildan Tee"),
    (11,   29, "Hoodie"),
    (1039, 29, "11oz Mug"),
]

# How many of each type to create per run
TARGETS = {"Bella Canvas Tee": 8, "Gildan Tee": 8, "Hoodie": 6, "11oz Mug": 3}

# Image spec guidance (not enforced, just printed as warning)
MIN_SIZES = {
    "tee": (4500, 5400),
    "hoodie": (4500, 5400),
    "mug": (3300, 2600),
    "hat": (3000, 1800),
    "tote": (4800, 4800),
}

# ─── Helpers ────────────────────────────────────────────────────────────────

def check_token():
    if not TOKEN:
        print("ERROR: PRINTIFY_TOKEN not set in .env")
        print("  Get a token at: https://printify.com/app/settings/api")
        sys.exit(1)

def load_upload_cache() -> dict:
    if os.path.exists(UPLOAD_CACHE):
        with open(UPLOAD_CACHE) as f:
            return json.load(f)
    return {}

def save_upload_cache(data: dict):
    with open(UPLOAD_CACHE, "w") as f:
        json.dump(data, f, indent=2)

# 💡 What: Memoize Printify variant lookups to prevent N+1 API calls during bulk creation
# 🎯 Why: Repeatedly hitting the variants API for the same blueprint slows down bulk processes
# 📊 Impact: Significantly reduces network overhead and speeds up the product creation loop
# 🛡️ Safety: Converted return type to immutable tuple to guarantee thread-safety of cached objects
@functools.lru_cache(maxsize=None)
def get_variants(blueprint_id: int, provider_id: int) -> tuple[int, ...]:
    url = f"{BASE_URL}/catalog/blueprints/{blueprint_id}/print_providers/{provider_id}/variants.json"
    r = requests.get(url, headers=AUTH_H, timeout=15)
    r.raise_for_status()
    return tuple(v["id"] for v in r.json().get("variants", [])[:4])

def upload_image_file(path: str) -> str:
    """Upload a local PNG file to Printify. Returns image ID."""
    url = f"{BASE_URL}/uploads/images.json"
    with open(path, "rb") as f:
        r = requests.post(url, headers=AUTH_H,
                          files={"file": (os.path.basename(path), f, "image/png")},
                          timeout=120)
    r.raise_for_status()
    image_id = r.json().get("id")
    if not image_id:
        raise ValueError(f"No image ID in response: {r.text}")
    return image_id

def upload_image_url(url_src: str, filename: str) -> str:
    """Upload an image by URL to Printify (faster for hosted images). Returns image ID."""
    url = f"{BASE_URL}/uploads/images.json"
    r = requests.post(url, headers=JSON_H,
                      json={"file_name": filename, "url": url_src},
                      timeout=60)
    r.raise_for_status()
    image_id = r.json().get("id")
    if not image_id:
        raise ValueError(f"No image ID in response: {r.text}")
    return image_id

def check_image_size(path: str):
    """Warn if image may be too small for print quality."""
    try:
        import struct, zlib
        with open(path, 'rb') as f:
            f.read(8)  # PNG signature
            f.read(4)  # chunk length
            f.read(4)  # IHDR
            w = struct.unpack('>I', f.read(4))[0]
            h = struct.unpack('>I', f.read(4))[0]
        if w < 3000 or h < 3000:
            print(f"  WARNING: {os.path.basename(path)} is {w}x{h}px — may be too small for quality print (recommend 4500x5400 for apparel)")
    except Exception:
        pass  # Non-critical

def create_product(blueprint_id: int, provider_id: int, label: str,
                   image_id: str, title: str) -> dict:
    variant_ids = get_variants(blueprint_id, provider_id)
    if not variant_ids:
        raise ValueError(f"No variants for blueprint {blueprint_id}")
    payload = {
        "title": title,
        "description": "Reliable Chaos — Fire/EMS Dark Humor Gear",
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
    r = requests.post(f"{BASE_URL}/shops/{SHOP_ID}/products.json",
                      headers=JSON_H, json=payload, timeout=30)
    if r.status_code not in (200, 201):
        raise ValueError(f"Create failed {r.status_code}: {r.text[:300]}")
    return r.json()

def get_all_products() -> list:
    r = requests.get(f"{BASE_URL}/shops/{SHOP_ID}/products.json?limit=100",
                     headers=AUTH_H, timeout=15)
    r.raise_for_status()
    return r.json().get("data", [])

# ─── Commands ───────────────────────────────────────────────────────────────

def cmd_check():
    """Verify token and show shop info."""
    r = requests.get(f"{BASE_URL}/shops.json", headers=AUTH_H, timeout=10)
    if r.status_code == 200:
        shops = r.json()
        print("Token valid. Shops:")
        for s in shops:
            print(f"  ID: {s['id']}  Name: {s['title']}")
    else:
        print(f"Token INVALID ({r.status_code}): {r.text}")
        print("\nGet a new token at: https://printify.com/app/settings/api")
        print("Then update PRINTIFY_TOKEN in /tmp/jim-fix/.env")
        sys.exit(1)

def cmd_list():
    products = get_all_products()
    if not products:
        print("No products found.")
        return
    print(f"{'ID':<30} {'STATUS':<8} TITLE")
    print("-" * 80)
    for p in products:
        status = "DRAFT" if p.get("is_draft") else "LIVE "
        print(f"{p['id']:<30} {status:<8} {p['title']}")
    print(f"\nTotal: {len(products)}")

def cmd_upload() -> dict:
    """Upload all PNGs in ./designs/ — skips already-uploaded files (resume safe)."""
    designs_dir = Path(os.path.dirname(__file__)) / "designs"
    images = sorted(designs_dir.glob("*.png"))
    if not images:
        print("No PNG files in ./designs/")
        print("  Add your print-ready PNGs (4500x5400px, transparent bg, RGB) and re-run.")
        return {}

    # Load existing cache to resume if interrupted
    uploaded = load_upload_cache()
    already_done = set(uploaded.keys())
    to_upload = [img for img in images if img.stem not in already_done]

    if already_done:
        print(f"Resuming: {len(already_done)} already uploaded, {len(to_upload)} remaining.")
    else:
        print(f"Uploading {len(images)} images from ./designs/...")

    if not to_upload:
        print("All images already uploaded. Run 'create' to make products.")
        return uploaded

    for i, img in enumerate(to_upload, 1):
        print(f"  [{i}/{len(to_upload)}] {img.name}", end="", flush=True)
        check_image_size(str(img))
        for attempt in range(3):
            try:
                image_id = upload_image_file(str(img))
                uploaded[img.stem] = image_id
                save_upload_cache(uploaded)
                print(f" -> {image_id}")
                break
            except Exception as e:
                if attempt < 2:
                    print(f" retry {attempt+1}...", end="", flush=True)
                    time.sleep(2)
                else:
                    print(f" FAILED: {e}")
        time.sleep(0.5)

    print(f"\nDone: {len(uploaded)} total images in cache. IDs in uploaded_images.json")
    return uploaded

def cmd_upload_url(url_src: str, name: str):
    """Upload a single image from a URL."""
    uploaded = load_upload_cache()
    print(f"Uploading from URL: {url_src}")
    try:
        image_id = upload_image_url(url_src, name if name.endswith('.png') else name + '.png')
        uploaded[name] = image_id
        save_upload_cache(uploaded)
        print(f"Uploaded: {name} -> {image_id}")
    except Exception as e:
        print(f"Failed: {e}")

def cmd_create(uploaded: dict = None):
    """Create draft products from uploaded images."""
    if uploaded is None:
        uploaded = load_upload_cache()
    if not uploaded:
        print("No uploaded images found. Run 'upload' first.")
        return

    remaining = dict(TARGETS)
    product_ids = []
    created = 0

    for img_name, image_id in uploaded.items():
        if sum(remaining.values()) == 0:
            break
        for bp_id, provider_id, label in BLUEPRINTS:
            if remaining.get(label, 0) <= 0:
                continue
            title = f"Reliable Chaos {img_name.replace('_', ' ').title()} — {label}"
            print(f"  Creating: {title}", end="", flush=True)
            for attempt in range(3):
                try:
                    product = create_product(bp_id, provider_id, label, image_id, title)
                    pid = product.get("id")
                    product_ids.append(pid)
                    remaining[label] -= 1
                    created += 1
                    print(f" -> {pid}")
                    time.sleep(0.5)
                    break
                except Exception as e:
                    if attempt < 2:
                        print(f" retry...", end="", flush=True)
                        time.sleep(2)
                    else:
                        print(f" FAILED: {e}")

    out = os.path.join(os.path.dirname(__file__), "created_products.json")
    existing = []
    if os.path.exists(out):
        with open(out) as f:
            existing = json.load(f)
    with open(out, "w") as f:
        json.dump(existing + product_ids, f, indent=2)
    print(f"\nCreated {created} draft products. All IDs in created_products.json")

def cmd_sync_github(repo: str, branch: str = "main", folder: str = ""):
    """
    Fetch all .png files from a public GitHub repo and upload them to Printify via URL.
    repo   : 'owner/repo-name'
    branch : branch name (default: main)
    folder : subfolder in repo, e.g. 'designs' (optional)
    """
    api_base = f"https://api.github.com/repos/{repo}/contents/{folder}"
    params = {"ref": branch}
    print(f"Fetching file list from github.com/{repo} [{branch}]{'/'+folder if folder else ''}...")
    r = requests.get(api_base, params=params, timeout=15)
    if r.status_code == 404:
        print(f"Repo or folder not found: {repo}/{folder}")
        print("Make sure the repo is PUBLIC and the path is correct.")
        return
    r.raise_for_status()
    files = r.json()
    pngs = [f for f in files if isinstance(f, dict) and f.get("name", "").lower().endswith(".png")]
    if not pngs:
        print(f"No PNG files found in {repo}/{folder}")
        return

    uploaded = load_upload_cache()
    already_done = set(uploaded.keys())
    to_upload = [f for f in pngs if f["name"].rsplit(".", 1)[0] not in already_done]

    print(f"Found {len(pngs)} PNGs — {len(already_done)} already uploaded, {len(to_upload)} to upload.")
    for i, f in enumerate(to_upload, 1):
        name = f["name"].rsplit(".", 1)[0]
        raw_url = f"https://raw.githubusercontent.com/{repo}/{branch}/{folder+'/' if folder else ''}{f['name']}"
        print(f"  [{i}/{len(to_upload)}] {f['name']}", end="", flush=True)
        for attempt in range(3):
            try:
                image_id = upload_image_url(raw_url, f["name"])
                uploaded[name] = image_id
                save_upload_cache(uploaded)
                print(f" -> {image_id}")
                break
            except Exception as e:
                if attempt < 2:
                    print(f" retry {attempt+1}...", end="", flush=True)
                    time.sleep(2)
                else:
                    print(f" FAILED: {e}")
        time.sleep(0.5)

    print(f"\nSync done: {len(uploaded)} total images cached.")
    return uploaded

def cmd_run():
    """Full pipeline: upload all designs then create products."""
    print("=== Step 1: Upload images ===")
    uploaded = cmd_upload()
    if not uploaded:
        return
    print("\n=== Step 2: Create products ===")
    cmd_create(uploaded)

def cmd_run_github(repo: str, branch: str = "main", folder: str = ""):
    """Full pipeline from GitHub: sync images then create products."""
    print("=== Step 1: Sync images from GitHub ===")
    uploaded = cmd_sync_github(repo, branch, folder)
    if not uploaded:
        return
    print("\n=== Step 2: Create products ===")
    cmd_create(uploaded)

def cmd_dump():
    products = get_all_products()
    out = os.path.join(os.path.dirname(__file__), "DATA_DELIVERY.json")
    with open(out, "w") as f:
        json.dump({"products": [{"id": p["id"], "title": p["title"], "is_draft": p.get("is_draft")}
                                for p in products]}, f, indent=2)
    print(f"Saved {len(products)} products to DATA_DELIVERY.json")

def cmd_delete(ids: list):
    for pid in ids:
        r = requests.delete(f"{BASE_URL}/shops/{SHOP_ID}/products/{pid}.json",
                            headers=AUTH_H, timeout=15)
        if r.status_code in (200, 204):
            print(f"Deleted: {pid}")
        else:
            print(f"Failed {pid}: {r.status_code} {r.text[:80]}")
        time.sleep(0.3)

def cmd_delete_all_drafts():
    products = get_all_products()
    drafts = [p["id"] for p in products if p.get("is_draft")]
    if not drafts:
        print("No draft products found.")
        return
    confirm = input(f"Delete {len(drafts)} draft products? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return
    print(f"Deleting {len(drafts)} drafts...")
    cmd_delete(drafts)

# ─── Main ───────────────────────────────────────────────────────────────────

def main():
    check_token()
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    cmd = args[0].lower()
    if cmd == "check":
        cmd_check()
    elif cmd == "list":
        cmd_list()
    elif cmd == "upload":
        cmd_upload()
    elif cmd == "upload-url":
        if len(args) < 3:
            print("Usage: upload-url <url> <name>")
        else:
            cmd_upload_url(args[1], args[2])
    elif cmd == "create":
        cmd_create()
    elif cmd == "run":
        cmd_run()
    elif cmd == "sync-github":
        # Usage: sync-github owner/repo [branch] [folder]
        if len(args) < 2:
            print("Usage: sync-github <owner/repo> [branch] [folder]")
            print("  e.g. sync-github merg357/reliable-chaos-designs main designs")
        else:
            repo   = args[1]
            branch = args[2] if len(args) > 2 else "main"
            folder = args[3] if len(args) > 3 else ""
            cmd_sync_github(repo, branch, folder)
    elif cmd == "run-github":
        if len(args) < 2:
            print("Usage: run-github <owner/repo> [branch] [folder]")
        else:
            repo   = args[1]
            branch = args[2] if len(args) > 2 else "main"
            folder = args[3] if len(args) > 3 else ""
            cmd_run_github(repo, branch, folder)
    elif cmd == "dump":
        cmd_dump()
    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: delete <id> [<id>...]")
        else:
            cmd_delete(args[1:])
    elif cmd == "delete-all-drafts":
        cmd_delete_all_drafts()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == "__main__":
    main()
