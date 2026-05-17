"""Upload markup/rendered/*.pdf to the Drive 'Rendered PDFs' folder.

Two auth modes, picked at runtime:

  • OAuth user delegation (preferred) — uses
      DRIVE_OAUTH_CLIENT_ID
      DRIVE_OAUTH_CLIENT_SECRET
      DRIVE_OAUTH_REFRESH_TOKEN
    All three must be set. Uploads as Kim's user account, which works for
    personal Drive folders (the service-account path does not, because
    service accounts have no personal storage quota).

  • Service account (fallback) — uses DRIVE_SA_JSON. Only works if the
    target folder lives inside a Shared Drive.

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
    folder_id = os.environ.get("RENDERED_PDFS_FOLDER_ID", "").strip()
    if not folder_id:
        print("RENDERED_PDFS_FOLDER_ID not set — skipping Drive upload.")
        return 0

    oauth_client_id = os.environ.get("DRIVE_OAUTH_CLIENT_ID", "").strip()
    oauth_client_secret = os.environ.get("DRIVE_OAUTH_CLIENT_SECRET", "").strip()
    oauth_refresh_token = os.environ.get("DRIVE_OAUTH_REFRESH_TOKEN", "").strip()
    sa_json = os.environ.get("DRIVE_SA_JSON", "").strip()

    have_oauth = bool(oauth_client_id and oauth_client_secret and oauth_refresh_token)
    have_sa = bool(sa_json)

    if not have_oauth and not have_sa:
        print("No DRIVE_OAUTH_* or DRIVE_SA_JSON env vars — skipping Drive upload.")
        return 0

    pdfs = sorted(PDFS_DIR.glob("*.pdf"))
    if not pdfs:
        print("No PDFs to upload.")
        return 0

    diag_lines: list[str] = []

    def diag(msg: str) -> None:
        print(msg)
        diag_lines.append(msg)

    def write_diag() -> None:
        (PDFS_DIR / "_upload_diag.txt").write_text(
            "\n".join(diag_lines) + "\n", encoding="utf-8"
        )

    try:
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        if have_oauth:
            from google.oauth2.credentials import Credentials
            creds = Credentials(
                token=None,
                refresh_token=oauth_refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=oauth_client_id,
                client_secret=oauth_client_secret,
                scopes=["https://www.googleapis.com/auth/drive"],
            )
            diag("Auth mode: OAuth user delegation (refresh token)")
        else:
            from google.oauth2 import service_account
            sa_info = json.loads(sa_json)
            diag(f"Auth mode: Service account ({sa_info.get('client_email', '<missing>')})")
            diag("  NOTE: SAs cannot create files in personal Drive — only Shared Drives.")
            creds = service_account.Credentials.from_service_account_info(
                sa_info,
                scopes=["https://www.googleapis.com/auth/drive"],
            )

        diag(f"Target folder ID: {folder_id}")
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    except Exception as exc:
        diag(f"::warning::Drive client init failed: {exc}")
        traceback.print_exc()
        write_diag()
        return 0

    # Probe folder reachability + write capability before touching the PDFs.
    try:
        meta = drive.files().get(
            fileId=folder_id,
            fields="id, name, mimeType, capabilities(canEdit, canAddChildren)",
            supportsAllDrives=True,
        ).execute()
        diag(f"Folder: {meta.get('name')!r}  type={meta.get('mimeType')}")
        caps = meta.get("capabilities", {})
        diag(f"  canEdit={caps.get('canEdit')}  canAddChildren={caps.get('canAddChildren')}")
        if not caps.get("canAddChildren"):
            diag("::warning::Auth principal cannot add files to this folder.")
    except Exception as exc:
        diag(f"::warning::Could not read folder metadata: {exc}")
        traceback.print_exc()
        write_diag()
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
                diag(f"  ↻ updated {pdf.name}")
            else:
                drive.files().create(
                    body={"name": pdf.name, "parents": [folder_id]},
                    media_body=media,
                    fields="id",
                    supportsAllDrives=True,
                ).execute()
                diag(f"  ↑ uploaded {pdf.name}")
            ok += 1
        except Exception as exc:
            diag(f"::warning::Failed to upload {pdf.name}: {exc}")
            traceback.print_exc()
            failed += 1

    diag(f"\nDrive upload: {ok} ok, {failed} failed (of {len(pdfs)} PDF(s))")
    if failed and have_sa and not have_oauth:
        diag(
            "  → SA mode hit 'storage quota' because the folder is in personal\n"
            "    Drive. Switch to OAuth (DRIVE_OAUTH_* secrets) or move the folder\n"
            "    into a Shared Drive."
        )
    write_diag()
    return 0


if __name__ == "__main__":
    sys.exit(main())
