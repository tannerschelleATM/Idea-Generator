#!/usr/bin/env python3
"""Check local downloads against Canto to avoid duplicates and upload new files.

This script scans a download directory, computes a SHA-256 hash for each file,
queries the Canto API to see if that hash already exists, and uploads the file
if it is missing.

Environment variables:
    CANTO_API_BASE   Base URL for Canto API, e.g. https://your.canto.com/api/v1
    CANTO_API_TOKEN  API token or OAuth bearer token
    DOWNLOAD_DIR     Path to folder containing downloaded videos
"""
import hashlib
import os
from pathlib import Path
from typing import Iterator
import requests

API_BASE = os.environ.get("CANTO_API_BASE")
TOKEN = os.environ.get("CANTO_API_TOKEN")
DOWNLOAD_DIR = Path(os.environ.get("DOWNLOAD_DIR", "."))

HEADERS = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}


def file_hash(path: Path) -> str:
    """Return SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def exists_in_canto(hash_value: str) -> bool:
    """Check whether an asset with the given hash exists in Canto."""
    url = f"{API_BASE}/assets"
    params = {"filter": f"hash:{hash_value}"}
    r = requests.get(url, headers=HEADERS, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    return len(data.get("results", [])) > 0


def upload_to_canto(path: Path, hash_value: str) -> None:
    """Upload a file to Canto with the given hash as metadata."""
    url = f"{API_BASE}/assets"
    files = {"file": path.open("rb")}
    data = {"name": path.name, "hash": hash_value}
    r = requests.post(url, headers=HEADERS, files=files, data=data, timeout=300)
    r.raise_for_status()


def iter_files(root: Path) -> Iterator[Path]:
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            yield Path(dirpath) / name


def main() -> None:
    for file_path in iter_files(DOWNLOAD_DIR):
        digest = file_hash(file_path)
        if exists_in_canto(digest):
            print(f"Skipping existing file: {file_path}")
            continue
        print(f"Uploading new file: {file_path}")
        upload_to_canto(file_path, digest)


if __name__ == "__main__":
    main()
