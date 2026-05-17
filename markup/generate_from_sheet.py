"""Generate per-account pitch-card HTML files from Joe's Google Sheet.

Reads the 'account list' tab of the Pitch Card Spec spreadsheet, picks the
configured data rows (default: rows 3-7, 1-based), and writes one
markup/account-<slug>.html file per row by substituting placeholders in the
master template.

Three categories of placeholders get filled:
  1. {{PC_*}}      Direct from the matching sheet column (row 2 = header)
  2. Computed      title_prefix, title_region, p2_section_header, etc.
  3. Per-account   account_logo, hero_image_*, qr_*, product_N_icon, us_flag
                   Resolved against Drive folders by fuzzy name match. The
                   substituted value is a Mac CloudStorage file:/// URL so
                   markup/fetch_assets.py picks it up and downloads the file,
                   and markup/render.py rewrites it to a local assets/ path
                   at render time.

Non-fatal at every step — CI still produces whatever PDFs it can if the sheet
or a Drive folder is unreachable.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "pitch-card-template.html"

# Hardcoded to Joe's sheet — override via env if needed.
SPREADSHEET_ID = os.environ.get(
    "SHEETS_SPREADSHEET_ID",
    "1pH3FUc1PatPpgGBBXnyIsZH_UGwv6kdNQmXxdpJVO34",
)
ACCOUNT_LIST_GID = "922817776"

# Joe's "account list" tab uses TWO header rows:
#   row 1 = friendly names (SF Parent Account, Unique ID, …)
#   row 2 = PC_* code names that match {{placeholders}}
#   rows 3+ = actual account data
SHEET_HEADER_ROW = int(os.environ.get("SHEET_HEADER_ROW", "2"))
DATA_ROWS_START = int(os.environ.get("SHEET_DATA_ROWS_START", "3"))
DATA_ROWS_END = int(os.environ.get("SHEET_DATA_ROWS_END", "7"))

# Mac CloudStorage base used by every {{image}} substitution — render.py knows
# this same prefix and rewrites it to repo-local assets/ at render time.
MAC_BASE = (
    "file:///Users/kimrosenberg/Library/CloudStorage/"
    "GoogleDrive-kimrosenberg15@gmail.com/My%20Drive/Flock%20Collateral/"
)

# Drive folder IDs (source of truth: context/BRAND_ASSETS.md)
FOLDER_IDS = {
    "account_logo":        ("1PiwCEI43W9Cqr2lYJ6NU6tjf48ThArjy", "Images_Account Logos"),
    "hero_p1":             ("1mROZIgid4aIlNn4Vtm3rlkGSWOnHbdGd", "Images_Account_Location"),
    "hero_p2":             ("1rR3-lCkNFb4XrBszYnEtJGlhNMrjmxiV", "Images_Account_Agency Type"),
    "qr_codes":            ("1PtUhCHHeGq9fIoeKXOgeUP9UooBgMEri", "Images_Account_QR Codes"),
    "products":            ("1o29iYrriI5qx_cRm6mYh2KW-MkANt9BK", "Images_Products"),
    "fixed":               ("1dMiyw755bsl0jt1VCB2TsMuCLfPOaRVV", "Images_Fixed"),
}

# Two-letter state → display region used in the footer "Account Lead, <region>"
STATE_REGION_MAP = {
    "NY": "New York",
    "CT": "Connecticut",
}


def slugify(name: str) -> str:
    s = name.lower().strip()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "account"


def name_tokens(name: str) -> set[str]:
    """Tokenize a name for fuzzy matching: lowercase alphanumeric words,
    minus common filler words that don't disambiguate."""
    stop = {"the", "of", "and", "for", "a", "an", "in", "at"}
    tokens = re.findall(r"[a-z0-9]+", name.lower())
    return {t for t in tokens if t not in stop}


def best_file_match(account_name: str, files: list[dict]) -> dict | None:
    """Pick the Drive file whose name best matches the account.
    Prefers files whose tokens contain ALL the account's tokens; tie-breaks
    by the file with the fewest extra tokens (most specific match)."""
    if not account_name or not files:
        return None
    want = name_tokens(account_name)
    if not want:
        return None
    candidates = []
    for f in files:
        title = f.get("name") or f.get("title") or ""
        have = name_tokens(title)
        # Full match: every token in the account name appears in the filename
        if want.issubset(have):
            candidates.append((len(have - want), f))
    if candidates:
        candidates.sort(key=lambda c: c[0])
        return candidates[0][1]
    # Partial fallback: pick the file with the most token overlap
    best = None
    best_overlap = 0
    for f in files:
        title = f.get("name") or f.get("title") or ""
        have = name_tokens(title)
        overlap = len(want & have)
        if overlap > best_overlap:
            best_overlap = overlap
            best = f
    return best if best_overlap >= 2 else None


def mac_url(folder_label: str, filename: str) -> str:
    """Build the Mac CloudStorage URL fetch_assets.py expects."""
    rel = f"{folder_label}/{filename}"
    return MAC_BASE + urllib.parse.quote(rel)


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
            scopes=[
                "https://www.googleapis.com/auth/spreadsheets.readonly",
                "https://www.googleapis.com/auth/drive.readonly",
            ],
        )
        sheets = build("sheets", "v4", credentials=creds, cache_discovery=False)
        drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    except Exception as exc:
        print(f"API client init failed: {exc}", file=sys.stderr)
        return 0

    try:
        tab_name = _find_tab(sheets, SPREADSHEET_ID)
        if not tab_name:
            return 0
    except Exception as exc:
        print(f"Could not read spreadsheet metadata: {exc}", file=sys.stderr)
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
        return 0

    header_idx = SHEET_HEADER_ROW - 1
    if header_idx >= len(all_rows):
        return 0
    headers = all_rows[header_idx]
    print(f"Sheet '{tab_name}': {len(all_rows)} rows, {len(headers)} columns")
    pc_cols = [h for h in headers if h.startswith("PC_") or h.startswith("PC ")]
    print(f"  PC_* columns ({len(pc_cols)}): {pc_cols[:6]}{'…' if len(pc_cols) > 6 else ''}")

    start_idx = DATA_ROWS_START - 1
    data_rows = all_rows[start_idx:DATA_ROWS_END]
    if not data_rows:
        return 0

    # List every image folder once up front so per-account lookups are O(1) hash hits
    folder_files = _list_folders(drive)

    print(
        f"Generating HTML for {len(data_rows)} accounts "
        f"(sheet rows {DATA_ROWS_START}–{DATA_ROWS_END})…"
    )

    # Clear stale per-account HTML
    for stale in ROOT.glob("account-*.html"):
        stale.unlink()

    template_src = TEMPLATE.read_text(encoding="utf-8")
    generated = 0

    for sheet_row_num, row in enumerate(data_rows, start=DATA_ROWS_START):
        padded = row + [""] * max(0, len(headers) - len(row))
        values: dict[str, str] = dict(zip(headers, padded))

        account_long = values.get("PC_Account Name_Long", "").strip()
        account_short = values.get("PC_Account Name_Short", "").strip() or account_long
        account_name = account_long or account_short or f"row-{sheet_row_num}"
        state = values.get("SF BillingState", "").strip().upper()

        # 1. Direct sheet substitutions
        html = template_src
        for key, val in values.items():
            if key:
                html = html.replace("{{" + key + "}}", str(val or ""))

        # 2. Computed text fields
        computed = {
            "title_prefix": "Flock for the",
            "title_region": STATE_REGION_MAP.get(state, "New York"),
            "p2_section_header": f"Products for the {account_short}",
            "cta_account_ref": account_short,
            "Account Name_Long": account_long,
            "Account Name": account_short,
            "placeholder": "",
        }
        for key, val in computed.items():
            html = html.replace("{{" + key + "}}", str(val))

        # 3. Per-account images → Mac CloudStorage URLs (fetch_assets.py will
        # download them; render.py will rewrite to local assets/ paths)
        images_filled, images_missing = _fill_images(
            values=values,
            account_long=account_long,
            account_short=account_short,
            folder_files=folder_files,
        )
        for placeholder, url in images_filled.items():
            html = html.replace("{{" + placeholder + "}}", url)

        slug = slugify(account_name)
        out_path = ROOT / f"account-{slug}.html"
        out_path.write_text(html, encoding="utf-8")

        filled_count = len(images_filled)
        missing_count = len(images_missing)
        print(
            f"  ✓ row {sheet_row_num}: {account_name!r} → {out_path.name}  "
            f"({filled_count} images resolved, {missing_count} missing)"
        )
        for m in images_missing:
            print(f"      - missing: {m}")
        generated += 1

    print(f"\nGenerated {generated} account HTML file(s) in markup/")
    return 0


def _find_tab(sheets_client, spreadsheet_id: str) -> str | None:
    meta = sheets_client.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    for sheet in meta.get("sheets", []):
        props = sheet.get("properties", {})
        if str(props.get("sheetId", "")) == ACCOUNT_LIST_GID:
            return props["title"]
    for sheet in meta.get("sheets", []):
        title = sheet["properties"]["title"]
        if title.lower() == "account list":
            return title
    return None


def _list_folders(drive) -> dict[str, list[dict]]:
    """One Drive query per image folder, cached for the rest of the run."""
    out: dict[str, list[dict]] = {}
    for key, (folder_id, label) in FOLDER_IDS.items():
        try:
            resp = drive.files().list(
                q=f"'{folder_id}' in parents and trashed = false",
                fields="files(id, name, mimeType)",
                pageSize=200,
                supportsAllDrives=True,
                includeItemsFromAllDrives=True,
            ).execute()
            files = [f for f in resp.get("files", []) if f.get("mimeType", "").startswith("image/")]
            out[key] = files
            print(f"  Listed {len(files)} images in {label}/")
        except Exception as exc:
            print(f"  ::warning::Could not list {label}/: {exc}", file=sys.stderr)
            out[key] = []
    return out


def _fill_images(
    values: dict[str, str],
    account_long: str,
    account_short: str,
    folder_files: dict[str, list[dict]],
) -> tuple[dict[str, str], list[str]]:
    """Map each per-account image placeholder to a Mac CloudStorage URL.
    Returns (placeholder -> url, list of missing placeholders)."""
    filled: dict[str, str] = {}
    missing: list[str] = []

    # P1 / P2 per-account images. Try long name then short name.
    for placeholder, folder_key in [
        ("account_logo",        "account_logo"),
        ("hero_image_cover",    "hero_p1"),
        ("hero_image_products", "hero_p2"),
    ]:
        files = folder_files.get(folder_key, [])
        match = best_file_match(account_long, files) or best_file_match(account_short, files)
        if match:
            _, label = FOLDER_IDS[folder_key]
            filled[placeholder] = mac_url(label, match["name"])
        else:
            missing.append(placeholder)

    # QR codes — Drive only has PLACEHOLDER files right now; use them as fallback
    qr_files = folder_files.get("qr_codes", [])
    fixed_files = folder_files.get("fixed", [])
    # Try per-account first; otherwise fall back to the PLACEHOLDER file
    qr_footer = best_file_match(account_long, qr_files) or best_file_match("footer placeholder", qr_files)
    if qr_footer:
        _, label = FOLDER_IDS["qr_codes"]
        filled["qr_footer"] = mac_url(label, qr_footer["name"])
    else:
        missing.append("qr_footer")
    qr_booking = (
        best_file_match(account_long, qr_files)
        or best_file_match("book meeting", fixed_files)
        or best_file_match("booking placeholder", qr_files)
    )
    if qr_booking:
        # could live in either folder — figure out which
        for folder_key, files in (("qr_codes", qr_files), ("fixed", fixed_files)):
            if qr_booking in files:
                _, label = FOLDER_IDS[folder_key]
                filled["qr_booking"] = mac_url(label, qr_booking["name"])
                break
    else:
        missing.append("qr_booking")

    # US flag — single fixed asset
    us_flag = best_file_match("ndaa us flag", fixed_files) or best_file_match("us flag", fixed_files)
    if us_flag:
        _, label = FOLDER_IDS["fixed"]
        filled["us_flag"] = mac_url(label, us_flag["name"])
    else:
        missing.append("us_flag")

    # Product icons (8 slots)
    product_files = folder_files.get("products", [])
    for i in range(1, 9):
        placeholder = f"product_{i}_icon"
        prod_name = values.get(f"PC_Product {i} — Name", "").strip()
        if not prod_name:
            missing.append(f"{placeholder} (no product name in sheet)")
            continue
        # Strip "PROD_IMAGE_" prefix from filenames before matching
        candidates = []
        for f in product_files:
            name = f.get("name", "")
            stripped = re.sub(r"(?i)^prod_image_", "", name)
            stripped = re.sub(r"\.(jpg|jpeg|png|svg|webp|avif)$", "", stripped, flags=re.I)
            candidates.append({**f, "_match": stripped})
        # Best match on the stripped name
        match = best_file_match(prod_name, [{"name": c["_match"], "_orig": c} for c in candidates])
        if match:
            orig = match["_orig"]
            _, label = FOLDER_IDS["products"]
            filled[placeholder] = mac_url(label, orig["name"])
        else:
            missing.append(f"{placeholder} ({prod_name!r})")

    return filled, missing


if __name__ == "__main__":
    sys.exit(main())
