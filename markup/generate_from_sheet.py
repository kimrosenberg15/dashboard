"""Generate per-account pitch-card HTML files from Joe's Google Sheet.

Reads the 'account list' tab of the Pitch Card Spec spreadsheet, picks the
configured data rows (default: rows 3-7, 1-based), and writes one
markup/account-<slug>.html file per row by substituting {{Field Name}}
placeholders in the master template.

No-op if DRIVE_SA_JSON is unset (same SA used for Drive also calls Sheets API).
Non-fatal if the sheet is unreachable — CI still renders whatever HTML exists.

First-time setup (one-time, in addition to the Drive SA setup):
  1. Enable Sheets API in your GCP project:
     https://console.cloud.google.com/apis/library/sheets.googleapis.com
  2. Share the spreadsheet with the SA email (Viewer is enough):
     https://docs.google.com/spreadsheets/d/1pH3FUc1PatPpgGBBXnyIsZH_UGwv6kdNQmXxdpJVO34
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "pitch-card-template.html"

# Hardcoded to Joe's sheet — override via env if needed.
SPREADSHEET_ID = os.environ.get(
    "SHEETS_SPREADSHEET_ID",
    "1pH3FUc1PatPpgGBBXnyIsZH_UGwv6kdNQmXxdpJVO34",
)
ACCOUNT_LIST_GID = "922817776"

# Row numbers are 1-based (Google Sheets convention).
# Joe's "account list" tab uses TWO header rows:
#   Row 1 = friendly column names (SF Parent Account, Unique ID, …)
#   Row 2 = the PC_* code names that match {{placeholders}} in the template
#   Rows 3+ = actual account data
SHEET_HEADER_ROW = int(os.environ.get("SHEET_HEADER_ROW", "2"))
DATA_ROWS_START = int(os.environ.get("SHEET_DATA_ROWS_START", "3"))
DATA_ROWS_END = int(os.environ.get("SHEET_DATA_ROWS_END", "7"))


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "account"


def find_account_list_tab(sheets_client, spreadsheet_id: str) -> str | None:
    """Return the tab name for the account list sheet, matched by gid or name."""
    meta = sheets_client.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in meta.get("sheets", []):
        props = sheet.get("properties", {})
        if str(props.get("sheetId", "")) == ACCOUNT_LIST_GID:
            return props["title"]
    # Fallback: case-insensitive name match
    for sheet in meta.get("sheets", []):
        title = sheet["properties"]["title"]
        if title.lower() == "account list":
            return title
    all_tabs = [s["properties"]["title"] for s in meta.get("sheets", [])]
    print(f"Could not find 'account list' tab (gid {ACCOUNT_LIST_GID}).")
    print(f"  Available tabs: {all_tabs}")
    return None


def main() -> int:
    sa_json = os.environ.get("DRIVE_SA_JSON", "").strip()
    if not sa_json:
        print("DRIVE_SA_JSON not set — skipping sheet-based HTML generation.")
        return 0

    if not TEMPLATE.exists():
        print(f"Template not found: {TEMPLATE}", file=sys.stderr)
        return 1

    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build

        creds = service_account.Credentials.from_service_account_info(
            json.loads(sa_json),
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        )
        sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
    except Exception as exc:
        print(f"Sheets client init failed: {exc}", file=sys.stderr)
        return 0

    try:
        tab_name = find_account_list_tab(sheets, SPREADSHEET_ID)
        if not tab_name:
            return 0
    except Exception as exc:
        print(f"Could not read spreadsheet metadata: {exc}", file=sys.stderr)
        print(
            "  → Check: 1) Sheets API enabled in GCP  "
            "2) Spreadsheet shared with SA email  "
            "3) DRIVE_SA_JSON is correct"
        )
        return 0

    try:
        result = (
            sheets.spreadsheets()
            .values()
            .get(spreadsheetId=SPREADSHEET_ID, range=f"'{tab_name}'")
            .execute()
        )
        all_rows = result.get("values", [])
    except Exception as exc:
        print(f"Could not read '{tab_name}' tab: {exc}", file=sys.stderr)
        return 0

    if not all_rows:
        print(f"'{tab_name}' tab is empty.")
        return 0

    header_idx = SHEET_HEADER_ROW - 1
    if header_idx >= len(all_rows):
        print(
            f"Header row {SHEET_HEADER_ROW} out of range "
            f"(sheet has {len(all_rows)} rows). Aborting."
        )
        return 0
    headers = all_rows[header_idx]
    print(f"Sheet '{tab_name}': {len(all_rows)} rows, {len(headers)} columns")
    pc_cols = [h for h in headers if h.startswith("PC_") or h.startswith("PC ")]
    print(f"  PC_* header columns ({len(pc_cols)}): {pc_cols[:8]}{'…' if len(pc_cols) > 8 else ''}")

    # Convert 1-based row numbers to 0-based indices in all_rows.
    start_idx = DATA_ROWS_START - 1
    end_idx = DATA_ROWS_END      # exclusive slice
    data_rows = all_rows[start_idx:end_idx]

    if not data_rows:
        print(
            f"No rows at positions {DATA_ROWS_START}–{DATA_ROWS_END} "
            f"(sheet has {len(all_rows)} rows total)."
        )
        return 0

    print(
        f"Generating HTML for {len(data_rows)} accounts "
        f"(sheet rows {DATA_ROWS_START}–{DATA_ROWS_END})…"
    )

    # Clear any account-*.html from a previous run so renamed/removed accounts
    # don't linger and get rendered to stale PDFs.
    for stale in ROOT.glob("account-*.html"):
        stale.unlink()

    template_src = TEMPLATE.read_text(encoding="utf-8")
    generated = 0

    for sheet_row_num, row in enumerate(data_rows, start=DATA_ROWS_START):
        # Pad short rows (Google Sheets strips trailing blanks)
        padded = row + [""] * max(0, len(headers) - len(row))
        values: dict[str, str] = dict(zip(headers, padded))

        # Determine account name for slug / filename
        account_name = (
            values.get("PC_Account Name_Long")
            or values.get("Account Name_Long")
            or values.get("Account Name")
            or f"row-{sheet_row_num}"
        )
        slug = slugify(account_name)
        out_path = ROOT / f"account-{slug}.html"

        # Substitute all {{key}} patterns present in both template and this row
        html = template_src
        for key, val in values.items():
            if key and val is not None:
                html = html.replace("{{" + key + "}}", str(val))

        # Also write Account Name_Long / Account Name aliases from PC_ columns
        alias_map = {
            "Account Name_Long": values.get("PC_Account Name_Long", ""),
            "Account Name": values.get("PC_Account Name_Long", "").split(",")[0].strip(),
        }
        for alias, val in alias_map.items():
            if val:
                html = html.replace("{{" + alias + "}}", val)

        out_path.write_text(html, encoding="utf-8")
        print(f"  ✓ row {sheet_row_num}: {account_name!r} → {out_path.name}")
        generated += 1

    print(f"\nGenerated {generated} account HTML file(s) in markup/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
