"""Upload markup/rendered/*.pdf to the Drive 'Rendered PDFs' folder.

Non-fatal: per-file upload errors are logged as workflow warnings; the
script always returns 0 so a Drive misconfiguration doesn't fail the
whole CI run. The rendered PDFs are already in the workflow artifact
and committed back to the branch by an earlier step.
"""
from __future__ import annotations

import json
import os
import sys
import traceback
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

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json),
            scopes=["https://www.googleapis.com/auth/drive"],
        )
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    except Exception as exc:
        print(f"::warning::Drive client init failed: {exc}", file=sys.stderr)
        traceback.print_exc()
        return 0

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

    ok = 0
    failed = 0
    for pdf in pdfs:
        try:
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
            ok += 1
        except Exception as exc:
            print(f"::warning::Failed to upload {pdf.name}: {exc}", file=sys.stderr)
            traceback.print_exc()
            failed += 1

    print(f"\nDrive upload: {ok} ok, {failed} failed (of {len(pdfs)} PDF(s))")
    if failed:
        print(
            "  → Likely causes:\n"
            "    1) 'Rendered PDFs/' folder shared with SA as Viewer instead of Editor\n"
            "    2) RENDERED_PDFS_FOLDER_ID points at the wrong folder\n"
            "    3) Drive API not enabled in the SA project"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
