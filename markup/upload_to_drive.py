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

    diag_lines: list[str] = []

    def diag(msg: str) -> None:
        print(msg)
        diag_lines.append(msg)

    def write_diag() -> None:
        diag_path = PDFS_DIR / "_upload_diag.txt"
        diag_path.write_text("\n".join(diag_lines) + "\n", encoding="utf-8")

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        sa_info = json.loads(sa_json)
        diag(f"SA email: {sa_info.get('client_email', '<missing>')}")
        diag(f"SA project: {sa_info.get('project_id', '<missing>')}")
        diag(f"Target folder ID: {folder_id}")
        creds = service_account.Credentials.from_service_account_info(
            sa_info,
            scopes=["https://www.googleapis.com/auth/drive"],
        )
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
            diag(
                "::warning::SA cannot add files to this folder. "
                "Share 'Rendered PDFs' with the SA email above as Editor."
            )
    except Exception as exc:
        diag(f"::warning::Could not read folder metadata: {exc}")
        diag("  → Folder ID may be wrong, or SA has no access at all.")
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
    if failed:
        diag(
            "  → Likely causes:\n"
            "    1) 'Rendered PDFs/' folder shared with SA as Viewer instead of Editor\n"
            "    2) RENDERED_PDFS_FOLDER_ID points at the wrong folder\n"
            "    3) Drive API not enabled in the SA project"
        )
    write_diag()
    return 0


if __name__ == "__main__":
    sys.exit(main())
