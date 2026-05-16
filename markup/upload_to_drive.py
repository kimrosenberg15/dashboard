"""Upload markup/rendered/*.pdf to the Drive 'Rendered PDFs' folder.

No-op if DRIVE_SA_JSON or RENDERED_PDFS_FOLDER_ID is unset, so the workflow
can run before Kim sets the secret.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PDFS_DIR = ROOT / "rendered"


def main() -> int:
    sa_json = os.environ.get("DRIVE_SA_JSON", "").strip()
    folder_id = os.environ.get("RENDERED_PDFS_FOLDER_ID", "").strip()
    if not sa_json or not folder_id:
        print("DRIVE_SA_JSON or RENDERED_PDFS_FOLDER_ID not set — skipping Drive upload.")
        return 0

    pdfs = sorted(PDFS_DIR.glob("*.pdf"))
    if not pdfs:
        print("No PDFs to upload.")
        return 0

    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload

    creds = service_account.Credentials.from_service_account_info(
        json.loads(sa_json),
        scopes=["https://www.googleapis.com/auth/drive"],
    )
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)

    def find_existing(name: str) -> str | None:
        safe = name.replace("'", "\\'")
        resp = drive.files().list(
            q=f"'{folder_id}' in parents and name = '{safe}' and trashed = false",
            fields="files(id, name)",
            pageSize=10,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        files = resp.get("files", [])
        return files[0]["id"] if files else None

    for pdf in pdfs:
        media = MediaFileUpload(str(pdf), mimetype="application/pdf", resumable=False)
        existing = find_existing(pdf.name)
        if existing:
            drive.files().update(
                fileId=existing,
                media_body=media,
                supportsAllDrives=True,
            ).execute()
            print(f"  ↻ updated {pdf.name}")
        else:
            drive.files().create(
                body={"name": pdf.name, "parents": [folder_id]},
                media_body=media,
                fields="id",
                supportsAllDrives=True,
            ).execute()
            print(f"  ↑ uploaded {pdf.name}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
