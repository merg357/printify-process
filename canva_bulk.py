#!/usr/bin/env python3
"""
canva_bulk.py — Bulk upload images to Canva and/or export designs at high resolution.

SETUP:
  1. Go to https://www.canva.com/developers/
  2. Create an app → get a Client ID and Client Secret
  3. Add a redirect URI: http://localhost:8080/callback
  4. Run this script with --auth to complete OAuth once, saves token to canva_token.json
  5. Then use --upload, --list-designs, --export as needed

USAGE:
  python3 canva_bulk.py --auth                          # One-time OAuth login
  python3 canva_bulk.py --upload ./designs/             # Upload all PNGs in a folder
  python3 canva_bulk.py --list-designs                  # List all your Canva designs
  python3 canva_bulk.py --export output/                # Export all designs as high-res PDFs
  python3 canva_bulk.py --export output/ --format PNG   # Export as PNG instead
  python3 canva_bulk.py --upload ./designs/ --export output/  # Upload + export in one go

REQUIREMENTS:
  pip install requests python-dotenv
"""

import argparse
import json
import os
import sys
import time
import threading
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

CLIENT_ID     = os.getenv("CANVA_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("CANVA_CLIENT_SECRET", "")
REDIRECT_URI  = "http://localhost:8080/callback"
TOKEN_FILE    = Path("canva_token.json")
EXPORT_CACHE  = Path("canva_exports.json")
ASSET_CACHE   = Path("canva_assets.json")

BASE_URL      = "https://api.canva.com/rest/v1"

SCOPES = " ".join([
    "asset:read",
    "asset:write",
    "design:content:read",
    "design:meta:read",
    "design:content:write",
])

# ── Token helpers ─────────────────────────────────────────────────────────────

def save_token(token_data: dict):
    token_data["saved_at"] = time.time()
    TOKEN_FILE.write_text(json.dumps(token_data, indent=2))

def load_token() -> dict:
    if not TOKEN_FILE.exists():
        sys.exit("No token found. Run:  python3 canva_bulk.py --auth")
    return json.loads(TOKEN_FILE.read_text())

def maybe_refresh(token_data: dict) -> dict:
    """Refresh the access token if it's expiring within 5 minutes."""
    expires_in  = token_data.get("expires_in", 3600)
    saved_at    = token_data.get("saved_at", 0)
    age         = time.time() - saved_at
    if age < expires_in - 300:
        return token_data  # still valid

    print("Refreshing access token...")
    r = requests.post("https://api.canva.com/rest/v1/oauth/token", data={
        "grant_type":    "refresh_token",
        "refresh_token": token_data["refresh_token"],
        "client_id":     CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    r.raise_for_status()
    new_token = r.json()
    save_token(new_token)
    print("Token refreshed.")
    return new_token

def get_headers() -> dict:
    token = maybe_refresh(load_token())
    return {"Authorization": f"Bearer {token['access_token']}"}

# ── OAuth flow ────────────────────────────────────────────────────────────────

def do_auth():
    if not CLIENT_ID or not CLIENT_SECRET:
        sys.exit(
            "Set CANVA_CLIENT_ID and CANVA_CLIENT_SECRET in your .env file first.\n"
            "Get them at https://www.canva.com/developers/"
        )

    auth_code_holder = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            params = urllib.parse.parse_qs(parsed.query)
            if "code" in params:
                auth_code_holder["code"] = params["code"][0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Auth complete! You can close this tab.")
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing code parameter.")
        def log_message(self, *_):
            pass  # suppress request logs

    server = HTTPServer(("localhost", 8080), Handler)
    thread = threading.Thread(target=server.handle_request)
    thread.start()

    params = urllib.parse.urlencode({
        "response_type": "code",
        "client_id":     CLIENT_ID,
        "redirect_uri":  REDIRECT_URI,
        "scope":         SCOPES,
    })
    url = f"https://www.canva.com/api/oauth/authorize?{params}"
    print(f"Opening browser for Canva login...\n{url}\n")
    webbrowser.open(url)
    thread.join(timeout=120)

    code = auth_code_holder.get("code")
    if not code:
        sys.exit("Auth timed out or failed.")

    r = requests.post("https://api.canva.com/rest/v1/oauth/token", data={
        "grant_type":   "authorization_code",
        "code":         code,
        "redirect_uri": REDIRECT_URI,
        "client_id":    CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    })
    r.raise_for_status()
    save_token(r.json())
    print(f"Authenticated! Token saved to {TOKEN_FILE}")

# ── Asset upload ──────────────────────────────────────────────────────────────

def load_asset_cache() -> dict:
    if ASSET_CACHE.exists():
        return json.loads(ASSET_CACHE.read_text())
    return {}

def save_asset_cache(data: dict):
    ASSET_CACHE.write_text(json.dumps(data, indent=2))

def upload_asset(filepath: Path) -> str:
    """Upload one image file to Canva assets. Returns asset ID."""
    headers = get_headers()
    # Canva requires the name in a special header (URL-encoded)
    name_encoded = urllib.parse.quote(filepath.name)
    headers["Asset-Name"] = name_encoded

    with open(filepath, "rb") as f:
        r = requests.post(
            f"{BASE_URL}/asset-uploads",
            headers=headers,
            files={"file": (filepath.name, f, "image/png")},
        )

    if r.status_code == 409:
        # Asset already exists — try to find its ID from cache
        print(f"   (already exists on Canva, skipping upload)")
        return None

    try:
        r.raise_for_status()
    except requests.HTTPError:
        print(f"   Upload failed {r.status_code}: {r.text[:200]}")
        return None

    data = r.json()
    # Response has job/asset reference — poll if needed
    asset = data.get("asset") or data.get("job", {}).get("asset")
    if asset:
        return asset.get("id")

    # Some responses return a job ID to poll
    job_id = data.get("job", {}).get("id")
    if job_id:
        return poll_upload_job(job_id)

    print(f"   Unexpected response: {data}")
    return None

def poll_upload_job(job_id: str, timeout: int = 60) -> str | None:
    """Poll an asset upload job until it completes."""
    headers = get_headers()
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"{BASE_URL}/asset-uploads/{job_id}", headers=headers)
        r.raise_for_status()
        job = r.json().get("job", {})
        status = job.get("status")
        if status == "success":
            return job["asset"]["id"]
        if status in ("failed", "cancelled"):
            print(f"   Upload job {job_id} {status}")
            return None
        time.sleep(2)
    print(f"   Upload job {job_id} timed out")
    return None

def cmd_upload(folder: str):
    folder_path = Path(folder)
    pngs = sorted(folder_path.glob("*.png")) + sorted(folder_path.glob("*.jpg"))
    if not pngs:
        sys.exit(f"No PNG/JPG files found in {folder}")

    cache = load_asset_cache()
    already = set(cache.keys())
    to_do = [p for p in pngs if p.name not in already]

    print(f"Found {len(pngs)} images — {len(already)} cached, {len(to_do)} to upload.")

    for i, p in enumerate(to_do, 1):
        print(f"  [{i}/{len(to_do)}] {p.name}", end="", flush=True)
        for attempt in range(3):
            asset_id = upload_asset(p)
            if asset_id:
                cache[p.name] = asset_id
                save_asset_cache(cache)
                print(f" -> {asset_id}")
                break
            if attempt < 2:
                print(f" retry {attempt+1}...", end="", flush=True)
                time.sleep(3)
        else:
            print(f" FAILED after 3 attempts")
        time.sleep(1)

    print(f"\nDone. {len(cache)} assets in {ASSET_CACHE}")
    return cache

# ── Design listing ────────────────────────────────────────────────────────────

def list_designs(continuation: str = None) -> list:
    """Fetch all user designs (handles pagination)."""
    headers = get_headers()
    designs = []
    params  = {"limit": 100}
    if continuation:
        params["continuation"] = continuation

    while True:
        r = requests.get(f"{BASE_URL}/designs", headers=headers, params=params)
        r.raise_for_status()
        data     = r.json()
        page     = data.get("items", [])
        designs += page
        cont     = data.get("continuation")
        if not cont:
            break
        params["continuation"] = cont
        time.sleep(0.3)

    return designs

def cmd_list_designs():
    print("Fetching designs from Canva...")
    designs = list_designs()
    if not designs:
        print("No designs found.")
        return []
    print(f"\n{'ID':<30} {'Title'}")
    print("-" * 60)
    for d in designs:
        print(f"{d['id']:<30} {d.get('title', '(untitled)')}")
    print(f"\nTotal: {len(designs)}")
    return designs

# ── Export / download ─────────────────────────────────────────────────────────

def load_export_cache() -> dict:
    if EXPORT_CACHE.exists():
        return json.loads(EXPORT_CACHE.read_text())
    return {}

def create_export_job(design_id: str, fmt: str = "PDF_PRINT") -> str | None:
    """
    Supported formats:
      PDF_PRINT  — 300 DPI, highest quality, best for print-ready files
      PNG        — raster, good for web/transparent
      JPG        — raster, compressed
    """
    headers = get_headers()
    payload = {
        "design_id": design_id,
        "format":    fmt,
    }
    if fmt == "PDF_PRINT":
        payload["export_quality"] = "pro"  # highest available

    r = requests.post(f"{BASE_URL}/exports", headers=headers, json=payload)
    if r.status_code == 400:
        print(f"   Export error: {r.json()}")
        return None
    r.raise_for_status()
    return r.json().get("job", {}).get("id")

def poll_export_job(job_id: str, timeout: int = 120) -> list[str] | None:
    """Returns list of download URLs once export is ready."""
    headers  = get_headers()
    deadline = time.time() + timeout
    while time.time() < deadline:
        r = requests.get(f"{BASE_URL}/exports/{job_id}", headers=headers)
        r.raise_for_status()
        job    = r.json().get("job", {})
        status = job.get("status")
        if status == "success":
            urls = job.get("urls", [])
            return urls
        if status in ("failed", "cancelled"):
            print(f"   Export job {status}: {job.get('error', {})}")
            return None
        time.sleep(3)
    print(f"   Export job {job_id} timed out")
    return None

def download_file(url: str, dest: Path):
    r = requests.get(url, stream=True, timeout=60)
    r.raise_for_status()
    with open(dest, "wb") as f:
        for chunk in r.iter_content(chunk_size=65536):
            f.write(chunk)

def cmd_export(output_dir: str, fmt: str = "PDF_PRINT", design_ids: list = None):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    if not design_ids:
        print("Fetching design list...")
        designs    = list_designs()
        design_ids = [(d["id"], d.get("title", d["id"])) for d in designs]
    else:
        design_ids = [(did, did) for did in design_ids]

    if not design_ids:
        print("No designs to export.")
        return

    ext_map  = {"PDF_PRINT": "pdf", "PNG": "png", "JPG": "jpg"}
    ext      = ext_map.get(fmt, "pdf")
    cache    = load_export_cache()

    print(f"Exporting {len(design_ids)} designs as {fmt}...\n")
    for i, (did, title) in enumerate(design_ids, 1):
        safe_title = "".join(c if c.isalnum() or c in " -_" else "_" for c in title).strip()
        out_file   = out_path / f"{safe_title}_{did[:8]}.{ext}"

        if did in cache and Path(cache[did]).exists():
            print(f"  [{i}/{len(design_ids)}] {title} (already exported, skipping)")
            continue

        print(f"  [{i}/{len(design_ids)}] {title}", end="", flush=True)
        job_id = create_export_job(did, fmt)
        if not job_id:
            print(" SKIP (export job failed)")
            continue

        print(" waiting...", end="", flush=True)
        urls = poll_export_job(job_id)
        if not urls:
            print(" FAILED")
            continue

        # Download all pages (PDF can be multi-page)
        for j, url in enumerate(urls):
            dest = out_file if len(urls) == 1 else out_path / f"{safe_title}_{did[:8]}_p{j+1}.{ext}"
            download_file(url, dest)

        cache[did] = str(out_file)
        EXPORT_CACHE.write_text(json.dumps(cache, indent=2))
        size_kb = out_file.stat().st_size // 1024
        print(f" -> {out_file.name} ({size_kb} KB)")
        time.sleep(1)

    print(f"\nExports saved to {out_path}/")

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Bulk upload images to Canva and/or export designs at high resolution."
    )
    parser.add_argument("--auth",         action="store_true",  help="Run OAuth login (one-time)")
    parser.add_argument("--upload",       metavar="FOLDER",     help="Upload all PNGs/JPGs in FOLDER to Canva assets")
    parser.add_argument("--list-designs", action="store_true",  help="List all Canva designs")
    parser.add_argument("--export",       metavar="OUTPUT_DIR", help="Export all Canva designs to OUTPUT_DIR")
    parser.add_argument("--format",       default="PDF_PRINT",  choices=["PDF_PRINT", "PNG", "JPG"],
                        help="Export format (default: PDF_PRINT = 300 DPI)")
    parser.add_argument("--design-ids",   nargs="+",            help="Only export specific design IDs")

    args = parser.parse_args()

    if args.auth:
        do_auth()
        return

    if not args.upload and not args.list_designs and not args.export:
        parser.print_help()
        return

    if args.upload:
        cmd_upload(args.upload)

    if args.list_designs:
        cmd_list_designs()

    if args.export:
        cmd_export(args.export, fmt=args.format, design_ids=args.design_ids)


if __name__ == "__main__":
    main()
