#!/usr/bin/env python3
"""
upscale_pipeline.py — Full pipeline:
  1. Fetch PNG images from a public GitHub repo
  2. AI-upscale them to Printify print-ready resolution (Real-ESRGAN)
  3. Save to production/ folder
  4. Optionally push straight to Printify

INSTALL (one-time):
  pip install basicsr facexlib gfpgan realesrgan Pillow requests python-dotenv

  Real-ESRGAN model is auto-downloaded on first run (~64 MB).
  On a CPU-only VPS each image takes ~1-3 minutes. GPU is much faster.

USAGE:
  # Upscale from GitHub repo
  python3 upscale_pipeline.py --github owner/repo --branch main --folder designs

  # Upscale local folder of images
  python3 upscale_pipeline.py --local ./raw_designs/

  # Upscale + push straight to Printify
  python3 upscale_pipeline.py --github owner/repo --push

  # Just check what's already in the production folder
  python3 upscale_pipeline.py --list

TARGET SIZES (Printify requirements):
  Shirts / Hoodies : 4500 x 5400 px  (15" x 18" @ 300 DPI)
  Mugs (11oz)      : 3300 x 2400 px  (11" x 8" @ 300 DPI)
  Phone cases      : 1800 x 2760 px  (6" x 9.2" @ 300 DPI)

Default target is shirt/hoodie size. Use --product to override.
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# ── Target sizes per product type ─────────────────────────────────────────────

PRODUCT_SIZES = {
    "shirt":  (4500, 5400),  # width x height
    "hoodie": (4500, 5400),
    "mug":    (3300, 2400),
    "phone":  (1800, 2760),
}

PRODUCTION_DIR = Path("production")
RAW_DIR        = Path("raw_designs")
CACHE_FILE     = Path("upscale_cache.json")

# ── Cache helpers ─────────────────────────────────────────────────────────────

def load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}

def save_cache(data: dict):
    CACHE_FILE.write_text(json.dumps(data, indent=2))

# ── GitHub fetch ──────────────────────────────────────────────────────────────

def fetch_from_github(repo: str, branch: str = "main", folder: str = ""):
    api_url = f"https://api.github.com/repos/{repo}/contents/{folder}"
    params  = {"ref": branch}

    # Support private repos via GITHUB_TOKEN env var
    headers = {}
    gh_token = os.getenv("GITHUB_TOKEN")
    if gh_token:
        headers["Authorization"] = f"Bearer {gh_token}"

    print(f"Fetching file list from github.com/{repo} [{branch}]{'/'+folder if folder else ''}...")
    r = requests.get(api_url, headers=headers, params=params, timeout=15)
    if r.status_code == 404:
        sys.exit(f"Not found: {repo}/{folder} on branch {branch}.\nMake sure the repo is public or set GITHUB_TOKEN in .env for private repos.")
    r.raise_for_status()

    files = r.json()
    pngs  = [f for f in files if isinstance(f, dict) and f["name"].lower().endswith((".png", ".jpg", ".jpeg"))]
    if not pngs:
        sys.exit(f"No PNG/JPG files found in {repo}/{folder}")

    RAW_DIR.mkdir(exist_ok=True)
    cache    = load_cache()
    to_fetch = [f for f in pngs if f["name"] not in cache.get("fetched", [])]

    print(f"Found {len(pngs)} images — {len(pngs)-len(to_fetch)} cached, {len(to_fetch)} to download.")

    for i, f in enumerate(to_fetch, 1):
        dest    = RAW_DIR / f["name"]
        raw_url = f["download_url"]  # raw.githubusercontent.com URL
        print(f"  [{i}/{len(to_fetch)}] Downloading {f['name']}...", end="", flush=True)
        r2 = requests.get(raw_url, headers=headers, timeout=60, stream=True)
        r2.raise_for_status()
        with open(dest, "wb") as out:
            for chunk in r2.iter_content(65536):
                out.write(chunk)
        kb = dest.stat().st_size // 1024
        print(f" {kb} KB")
        cache.setdefault("fetched", []).append(f["name"])
        save_cache(cache)

    return list(RAW_DIR.glob("*.png")) + list(RAW_DIR.glob("*.jpg")) + list(RAW_DIR.glob("*.jpeg"))

# ── Upscaling ─────────────────────────────────────────────────────────────────

def upscale_realesrgan(input_path: Path, output_path: Path, target_w: int, target_h: int):
    """
    Upscale using Real-ESRGAN (the engine behind Upscayl).
    Model auto-downloads on first use to ~/.cache/realesrgan/
    """
    try:
        import numpy as np
        from PIL import Image
        from realesrgan import RealESRGANer
        from basicsr.archs.rrdbnet_arch import RRDBNet
    except ImportError:
        return False, "realesrgan package not installed"

    try:
        import torch
        use_half = torch.cuda.is_available()
    except ImportError:
        use_half = False

    model_name = "RealESRGAN_x4plus"
    model_path = Path.home() / ".cache" / "realesrgan" / f"{model_name}.pth"
    model_url  = "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"

    # Auto-download model weights if needed
    if not model_path.exists():
        print(f"    Downloading Real-ESRGAN model (~64 MB)...")
        model_path.parent.mkdir(parents=True, exist_ok=True)
        r = requests.get(model_url, stream=True, timeout=300)
        r.raise_for_status()
        with open(model_path, "wb") as f:
            for chunk in r.iter_content(65536):
                f.write(chunk)
        print(f"    Model saved to {model_path}")

    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64,
                    num_block=23, num_grow_ch=32, scale=4)

    upsampler = RealESRGANer(
        scale=4,
        model_path=str(model_path),
        model=model,
        tile=512,        # tile processing — safe for low-RAM VPS
        tile_pad=10,
        pre_pad=0,
        half=use_half,
    )

    img = Image.open(input_path).convert("RGB")
    img_np = __import__("numpy").array(img)

    print(f"    Running Real-ESRGAN (this may take 1-3 min on CPU)...", end="", flush=True)
    output_np, _ = upsampler.enhance(img_np, outscale=4)
    print(" done.")

    result = Image.fromarray(output_np)

    # Fit to exact target size (letterbox with transparent padding if PNG)
    result = fit_to_target(result, target_w, target_h, input_path.suffix.lower() == ".png")
    result.save(output_path, dpi=(300, 300))
    return True, None


def upscale_pillow(input_path: Path, output_path: Path, target_w: int, target_h: int):
    """
    Fallback: high-quality Lanczos resize via Pillow.
    Not AI — but fast and always available. Good if source is already ≥1500px wide.
    """
    from PIL import Image
    img = Image.open(input_path)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")

    src_w, src_h = img.size
    scale_needed = max(target_w / src_w, target_h / src_h)

    if scale_needed > 4:
        print(f"    WARNING: source is only {src_w}x{src_h} — needs {scale_needed:.1f}x scale, quality will degrade.")
    elif scale_needed > 2:
        print(f"    NOTE: source is {src_w}x{src_h}, upscaling {scale_needed:.1f}x with Lanczos.")
    else:
        print(f"    Source is {src_w}x{src_h}, resizing down or small upscale.")

    resized = img.resize((int(src_w * scale_needed), int(src_h * scale_needed)), Image.LANCZOS)
    final   = fit_to_target(resized, target_w, target_h, img.mode == "RGBA")
    final.save(output_path, dpi=(300, 300))
    return True, None


def fit_to_target(img, target_w: int, target_h: int, transparent: bool = True):
    """
    Centre the image on a canvas of exactly (target_w x target_h).
    If transparent=True, background is transparent (for apparel).
    If transparent=False, background is white.
    """
    from PIL import Image

    src_w, src_h = img.size

    # Scale to fit within target while preserving aspect ratio
    scale = min(target_w / src_w, target_h / src_h)
    new_w = int(src_w * scale)
    new_h = int(src_h * scale)
    img   = img.resize((new_w, new_h), Image.LANCZOS)

    mode   = "RGBA" if transparent else "RGB"
    canvas = Image.new(mode, (target_w, target_h), (0, 0, 0, 0) if transparent else (255, 255, 255))
    offset = ((target_w - new_w) // 2, (target_h - new_h) // 2)

    if transparent and img.mode != "RGBA":
        img = img.convert("RGBA")
    canvas.paste(img, offset, img if img.mode == "RGBA" else None)
    return canvas


def upscale_image(input_path: Path, output_path: Path, target_w: int, target_h: int, force_pillow: bool = False):
    """Try Real-ESRGAN first, fall back to Pillow Lanczos."""
    if not force_pillow:
        ok, err = upscale_realesrgan(input_path, output_path, target_w, target_h)
        if ok:
            return "realesrgan"
        print(f"    Real-ESRGAN unavailable ({err}), falling back to Pillow Lanczos.")

    upscale_pillow(input_path, output_path, target_w, target_h)
    return "pillow"

# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_upscale(image_files: list, product: str = "shirt", force_pillow: bool = False):
    from PIL import Image  # ensure it's available

    target_w, target_h = PRODUCT_SIZES[product]
    PRODUCTION_DIR.mkdir(exist_ok=True)

    cache    = load_cache()
    done     = set(cache.get("upscaled", []))
    to_do    = [p for p in image_files if p.name not in done]

    print(f"\nTarget: {target_w}x{target_h}px ({product}) — {len(image_files)} images, {len(done)} cached, {len(to_do)} to upscale.\n")

    for i, src in enumerate(to_do, 1):
        stem    = src.stem
        out     = PRODUCTION_DIR / f"{stem}.png"
        print(f"  [{i}/{len(to_do)}] {src.name} -> {out.name}")

        if out.exists():
            w, h = Image.open(out).size
            if w == target_w and h == target_h:
                print(f"    Already correct size, skipping.")
                cache.setdefault("upscaled", []).append(src.name)
                save_cache(cache)
                continue

        start  = time.time()
        method = upscale_image(src, out, target_w, target_h, force_pillow)
        elapsed = time.time() - start
        kb      = out.stat().st_size // 1024
        print(f"    Saved {out.name} ({kb} KB) via {method} in {elapsed:.0f}s")
        cache.setdefault("upscaled", []).append(src.name)
        save_cache(cache)

    print(f"\nAll done. Production files in {PRODUCTION_DIR}/")
    return list(PRODUCTION_DIR.glob("*.png"))


def cmd_list():
    files = list(PRODUCTION_DIR.glob("*.png")) if PRODUCTION_DIR.exists() else []
    if not files:
        print("Production folder is empty.")
        return
    try:
        from PIL import Image
        print(f"\n{'File':<40} {'Size':>12} {'Dimensions'}")
        print("-" * 70)
        for f in sorted(files):
            w, h = Image.open(f).size
            kb   = f.stat().st_size // 1024
            print(f"  {f.name:<38} {kb:>8} KB    {w}x{h}")
    except ImportError:
        for f in sorted(files):
            print(f"  {f.name}  ({f.stat().st_size//1024} KB)")
    print(f"\nTotal: {len(files)} files in {PRODUCTION_DIR}/")


def cmd_push_to_printify():
    """Hand off to printify_manager.py for upload + product creation."""
    manager = Path(__file__).parent / "printify_manager.py"
    if not manager.exists():
        print("printify_manager.py not found — run upload manually.")
        return
    print("\nHanding off to printify_manager.py...\n")
    prod_files = list(PRODUCTION_DIR.glob("*.png"))
    if not prod_files:
        print("No files in production/ to upload.")
        return

    # printify_manager reads from designs/ by default — symlink or copy production/ files
    designs_dir = Path("designs")
    designs_dir.mkdir(exist_ok=True)
    for f in prod_files:
        link = designs_dir / f.name
        if not link.exists():
            link.symlink_to(f.resolve())

    result = subprocess.run([sys.executable, str(manager), "run"], check=False)
    return result.returncode == 0

# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Fetch images from GitHub → AI upscale → Printify production folder",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full run from GitHub
  python3 upscale_pipeline.py --github merg357/merch-designs --branch main --folder designs

  # Local folder
  python3 upscale_pipeline.py --local ./raw_designs/

  # Upscale for mugs instead of shirts
  python3 upscale_pipeline.py --github owner/repo --product mug

  # Skip AI upscaling (use fast Pillow resize instead)
  python3 upscale_pipeline.py --github owner/repo --fast

  # Full pipeline: fetch + upscale + push to Printify
  python3 upscale_pipeline.py --github owner/repo --push

  # List what's in the production folder
  python3 upscale_pipeline.py --list
        """
    )
    parser.add_argument("--github",  metavar="OWNER/REPO",  help="GitHub repo to pull images from")
    parser.add_argument("--branch",  default="main",         help="Branch (default: main)")
    parser.add_argument("--folder",  default="",             help="Subfolder in repo (e.g. 'designs')")
    parser.add_argument("--local",   metavar="FOLDER",       help="Local folder of images to upscale")
    parser.add_argument("--product", default="shirt",        choices=list(PRODUCT_SIZES),
                        help="Product type for target size (default: shirt = 4500x5400)")
    parser.add_argument("--fast",    action="store_true",    help="Skip AI — use Pillow Lanczos (fast, lower quality)")
    parser.add_argument("--push",    action="store_true",    help="Push upscaled images to Printify after upscaling")
    parser.add_argument("--list",    action="store_true",    help="List files in production folder")

    args = parser.parse_args()

    if args.list:
        cmd_list()
        return

    if not args.github and not args.local:
        parser.print_help()
        return

    # Step 1: Gather source images
    if args.github:
        image_files = fetch_from_github(args.github, args.branch, args.folder)
    else:
        local_path  = Path(args.local)
        if not local_path.is_dir():
            sys.exit(f"Not a directory: {args.local}")
        image_files = (list(local_path.glob("*.png")) +
                       list(local_path.glob("*.jpg")) +
                       list(local_path.glob("*.jpeg")))
        if not image_files:
            sys.exit(f"No images found in {args.local}")
        print(f"Found {len(image_files)} local images in {args.local}")

    # Step 2: Upscale
    prod_files = cmd_upscale(image_files, product=args.product, force_pillow=args.fast)

    # Step 3 (optional): push to Printify
    if args.push:
        cmd_push_to_printify()
    else:
        print("\nNext step:")
        print("  python3 printify_manager.py run   # upload + create Printify products")
        print("  — or —")
        print(f"  python3 upscale_pipeline.py --push   # do it now")


if __name__ == "__main__":
    main()
