"""Download only the brand assets referenced by the templates in markup/*.html.

Scans every HTML file for Mac CloudStorage file:/// URLs, extracts the
relative paths, and downloads each one from Drive into markup/assets/
preserving the relative structure.

No-op if DRIVE_SA_JSON is unset or FLOCK_COLLATERAL_FOLDER_ID is unset —
this lets the workflow run end-to-end before the service account is wired up.

Future per-account work: render-time placeholder substitution can produce
the full resolved HTML first, then this fetcher pulls whatever paths
appear in the resolved files.
"""
from __future__ import annotations

import io
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"

MAC_BASE = (
    "file:///Users/kimrosenberg/Library/CloudStorage/"
    "GoogleDrive-kimrosenberg15@gmail.com/My%20Drive/Flock%20Collateral/"
)
MAC_PATH_RE = re.compile(re.escape(MAC_BASE) + r"[^'\"\s)]+")


def extract_referenced_paths() -> list[str]:
    """Return the unique decoded relative paths (e.g. 'BRAND_Flock Logo/Flock_Logo_Cream.svg')
    that appear in any markup/*.html file."""
    paths: set[str] = set()
    for html_file in ROOT.glob("*.html"):
        content = html_file.read_text(encoding="utf-8")
        for m in MAC_PATH_RE.finditer(content):
            rel_encoded = m.group(0)[len(MAC_BASE):]
            rel = urllib.parse.unquote(rel_encoded)
            paths.add(rel)
    return sorted(paths)


def main() -> int:
    sa_json = os.environ.get("DRIVE_SA_JSON", "").strip()
    folder_id = os.environ.get("FLOCK_COLLATERAL_FOLDER_ID", "").strip()
    if not sa_json or not folder_id:
        print("DRIVE_SA_JSON or FLOCK_COLLATERAL_FOLDER_ID not set — skipping asset fetch.")
        return 0

    wanted = extract_referenced_paths()
    if not wanted:
        print("No Mac CloudStorage paths referenced by any markup/*.html — nothing to fetch.")
        return 0

    print(f"Templates reference {len(wanted)} unique assets:")
    for w in wanted:
        print(f"  · {w}")

    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload

    creds = service_account.Credentials.from_service_account_info(
        json.loads(sa_json),
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    folder_id_cache: dict[tuple[str, str], str | None] = {}

    def find_child(parent_id: str, name: str, want_folder: bool) -> dict | None:
        """Look up a child of parent_id by exact name. Cached."""
        key = (parent_id, name)
        if key in folder_id_cache:
            return None  # cached as not found; full lookups are below
        # Escape single quotes for the Drive query string
        safe = name.replace("'", "\\'")
        mime_filter = "= 'application/vnd.google-apps.folder'" if want_folder else "!= 'application/vnd.google-apps.folder'"
        q = f"'{parent_id}' in parents and name = '{safe}' and mimeType {mime_filter} and trashed = false"
        resp = drive.files().list(
            q=q,
            fields="files(id, name, mimeType)",
            pageSize=10,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        files = resp.get("files", [])
        return files[0] if files else None

    def resolve_path(rel_path: str) -> str | None:
        """Walk the rel_path under the root folder, return the file ID at the leaf."""
        parts = rel_path.split("/")
        cur = folder_id
        for part in parts[:-1]:
            key = (cur, part)
            cached = folder_id_cache.get(key)
            if cached == "__MISS__":
                return None
            if cached:
                cur = cached
                continue
            entry = find_child(cur, part, want_folder=True)
            if not entry:
                folder_id_cache[key] = "__MISS__"
                return None
            folder_id_cache[key] = entry["id"]
            cur = entry["id"]
        leaf = find_child(cur, parts[-1], want_folder=False)
        return leaf["id"] if leaf else None

    def download(file_id: str, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            return
        request = drive.files().get_media(fileId=file_id, supportsAllDrives=True)
        with io.FileIO(dest, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    found = 0
    missing = []
    for rel in wanted:
        file_id = resolve_path(rel)
        if not file_id:
            missing.append(rel)
            continue
        try:
            download(file_id, ASSETS_DIR / rel)
            found += 1
        except Exception as exc:
            print(f"  ✗ {rel}: {exc}", file=sys.stderr)
            missing.append(rel)

    print(f"\nDownloaded {found}/{len(wanted)} referenced assets into {ASSETS_DIR}")
    if missing:
        print(f"Missing in Drive ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
