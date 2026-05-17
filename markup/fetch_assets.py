"""Download brand assets (logos, hero images, product icons, fonts) from the
Flock Collateral Drive folder into markup/assets/ for the CI render.

No-op if DRIVE_SA_JSON is unset or FLOCK_COLLATERAL_FOLDER_ID is unset —
this lets the workflow run end-to-end before Kim wires up the service account.

Folder layout mirrored locally:
  markup/assets/BRAND_Logos/...
  markup/assets/BRAND_Images/...
  markup/assets/Account Logos/...
  markup/assets/Images_Fixed/...
  markup/assets/LPR & ALPR/...
  ...etc.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS_DIR = ROOT / "assets"

# Top-level subfolders we want to mirror. Keep this list small — pitch cards
# only reference these directories. Folder names must match Drive exactly
# (see context/BRAND_ASSETS.md for the canonical SSOT).
WANTED_SUBFOLDERS = [
    "BRAND_Flock Logo",
    "BRAND_Images",
    "BRAND_Font - Denton OTF",
    "BRAND_Font - Sohne OTF",
    "Images_Fixed",
    "Images_Account Logos",
    "Images_Account_QR Codes",
    "Images_Account_Location",
    "Images_Account_Agency Type",
    "Images_Products",
    "LPR & ALPR",
    "Video Cameras",
    "Audio Detection",
    "DFR - Drone as First Responder",
    "Mobile Security Trailers",
    "Nova OSINT",
    "FlockOS & Platform",
    "Traffic Analytics & Transportation",
    "Community & Advocacy",
    "Industry Verticals",
    "Legal & Compliance",
]


def main() -> int:
    sa_json = os.environ.get("DRIVE_SA_JSON", "").strip()
    folder_id = os.environ.get("FLOCK_COLLATERAL_FOLDER_ID", "").strip()
    if not sa_json or not folder_id:
        print("DRIVE_SA_JSON or FLOCK_COLLATERAL_FOLDER_ID not set — skipping asset fetch.")
        return 0

    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaIoBaseDownload
    import io

    creds = service_account.Credentials.from_service_account_info(
        json.loads(sa_json),
        scopes=["https://www.googleapis.com/auth/drive.readonly"],
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    def list_children(parent_id: str) -> list[dict]:
        items = []
        token = None
        while True:
            resp = drive.files().list(
                q=f"'{parent_id}' in parents and trashed = false",
                fields="nextPageToken, files(id, name, mimeType)",
                pageSize=1000,
                pageToken=token,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()
            items.extend(resp.get("files", []))
            token = resp.get("nextPageToken")
            if not token:
                break
        return items

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

    def walk(folder_id: str, local: Path) -> int:
        count = 0
        for entry in list_children(folder_id):
            if entry["mimeType"] == "application/vnd.google-apps.folder":
                count += walk(entry["id"], local / entry["name"])
            elif entry["mimeType"].startswith("application/vnd.google-apps."):
                # Skip Google native types (Docs/Sheets/etc.) — not used in templates.
                continue
            else:
                try:
                    download(entry["id"], local / entry["name"])
                    count += 1
                except Exception as exc:
                    print(f"  ✗ {entry['name']}: {exc}", file=sys.stderr)
        return count

    print(f"Listing children of Flock Collateral folder {folder_id}...")
    top = list_children(folder_id)
    by_name = {f["name"]: f for f in top if f["mimeType"] == "application/vnd.google-apps.folder"}

    total = 0
    for name in WANTED_SUBFOLDERS:
        sub = by_name.get(name)
        if not sub:
            print(f"  (no folder named '{name}' in Drive — skipping)")
            continue
        n = walk(sub["id"], ASSETS_DIR / name)
        print(f"  ↓ {name}: {n} files")
        total += n

    print(f"Downloaded {total} asset files into {ASSETS_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
