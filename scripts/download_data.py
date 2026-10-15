#!/usr/bin/env python3
"""Download the original UCI Online Retail II workbook and record its checksum.

The source workbook is preserved unchanged. The local manifest is intentionally
not committed to Git because it records the local retrieval timestamp/hash.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
import zipfile
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = REPO_ROOT / "data" / "raw"
WORKBOOK = RAW_DIR / "online_retail_II.xlsx"
MANIFEST = RAW_DIR / "manifest.json"
SOURCE_URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
ARCHIVE = RAW_DIR / "online_retail_ii.zip"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Customer-Revenue-Retention-Fabric-portfolio/1.0"},
    )
    with urllib.request.urlopen(request, timeout=120) as response, destination.open("wb") as out:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            out.write(chunk)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Verify the existing workbook against data/raw/manifest.json; do not download.",
    )
    args = parser.parse_args()
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if args.verify_only:
        if not WORKBOOK.exists() or not MANIFEST.exists():
            print("Workbook or manifest missing. Run python scripts/download_data.py first.", file=sys.stderr)
            return 1
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        actual = sha256_file(WORKBOOK)
        expected = manifest.get("sha256")
        print(f"File: {WORKBOOK}")
        print(f"Expected SHA-256: {expected}")
        print(f"Actual SHA-256:   {actual}")
        if actual != expected:
            print("FAIL: checksum mismatch; the file differs from the locally recorded version.", file=sys.stderr)
            return 2
        print("PASS: checksum matches the local manifest.")
        return 0

    print(f"Downloading original UCI archive: {SOURCE_URL}")
    try:
        download(SOURCE_URL, ARCHIVE)
    except Exception as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        print("Open the official dataset page and use its Download option:", file=sys.stderr)
        print("https://archive.ics.uci.edu/dataset/502/online+retail+ii", file=sys.stderr)
        return 1

    if not zipfile.is_zipfile(ARCHIVE):
        print("The downloaded response is not a ZIP archive. No workbook was changed.", file=sys.stderr)
        return 1

    try:
        with zipfile.ZipFile(ARCHIVE) as archive:
            candidates = [
                name for name in archive.namelist()
                if Path(name).name.lower() == "online_retail_ii.xlsx"
            ]
            if not candidates:
                print("Could not find online_retail_II.xlsx in the UCI archive.", file=sys.stderr)
                print("Archive members:", archive.namelist(), file=sys.stderr)
                return 1
            # Extract only the expected workbook and write its bytes unchanged.
            with archive.open(candidates[0]) as src, WORKBOOK.open("wb") as dst:
                while True:
                    chunk = src.read(1024 * 1024)
                    if not chunk:
                        break
                    dst.write(chunk)
    except (OSError, zipfile.BadZipFile) as exc:
        print(f"Could not extract workbook: {exc}", file=sys.stderr)
        return 1

    manifest = {
        "dataset": "Online Retail II",
        "publisher": "UCI Machine Learning Repository",
        "citation": "Chen, D. (2012). Online Retail II [Dataset]. UCI Machine Learning Repository.",
        "doi": "https://doi.org/10.24432/C5CG6D",
        "source_page": "https://archive.ics.uci.edu/dataset/502/online+retail+ii",
        "download_url": SOURCE_URL,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "filename": WORKBOOK.name,
        "size_bytes": WORKBOOK.stat().st_size,
        "sha256": sha256_file(WORKBOOK),
        "note": "Checksum establishes integrity relative to this manifest; it does not independently authenticate the source transactions.",
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Saved original workbook: {WORKBOOK}")
    print(f"Size: {manifest['size_bytes']:,} bytes")
    print(f"SHA-256: {manifest['sha256']}")
    print(f"Local manifest: {MANIFEST}")
    print("The workbook was not transformed. Do not commit the raw workbook or local manifest to Git.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
