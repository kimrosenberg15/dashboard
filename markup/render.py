"""Render every markup/*.html (except the master template) to PDF via Playwright.

Rewrites Kim's local Mac asset paths
  file:///Users/kimrosenberg/Library/CloudStorage/.../Flock Collateral/
to two repo-side sources:
  1. Fonts -> Google Fonts CDN (Denton -> Playfair Display, Sohne -> Inter)
  2. Images -> markup/assets/<original-relative-path>, if fetched by fetch_assets.py

Missing images are tolerated (kept as the original path; Chromium just shows a broken
image, but Kim wanted CI to render even before the SA is hooked up).
"""
from __future__ import annotations

import os
import re
import sys
import shutil
import urllib.parse
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
ASSETS_DIR = ROOT / "assets"
OUT_DIR = ROOT / "rendered"
OUT_DIR.mkdir(exist_ok=True)

MAC_BASE = (
    "file:///Users/kimrosenberg/Library/CloudStorage/"
    "GoogleDrive-kimrosenberg15@gmail.com/My%20Drive/Flock%20Collateral/"
)

GOOGLE_FONTS_CSS = """
<style id="render-fonts-fallback">
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=Inter:wght@400;500;600;700&display=swap');
/* Map Denton -> Playfair Display, Sohne -> Inter, so the Mac @font-face URLs
   that 404 at file:/// in CI fall through to these aliases. */
@font-face { font-family: 'Denton'; src: local('Playfair Display'); font-weight: 400; }
@font-face { font-family: 'Denton'; src: local('Playfair Display Bold'); font-weight: 700; }
@font-face { font-family: 'Denton'; src: local('Playfair Display Black'); font-weight: 900; }
@font-face { font-family: 'Sohne'; src: local('Inter'); font-weight: 400; }
@font-face { font-family: 'Sohne'; src: local('Inter Medium'); font-weight: 500; }
@font-face { font-family: 'Sohne'; src: local('Inter SemiBold'); font-weight: 600; }
@font-face { font-family: 'Sohne'; src: local('Inter Bold'); font-weight: 700; }
</style>
"""


def rewrite_asset_paths(html: str, staging: Path) -> tuple[str, dict]:
    """Rewrite Mac CloudStorage file:/// URLs to repo-side file:/// URLs.

    For each absolute Mac path, decode the relative part, look for it under
    markup/assets/, and if present, rewrite to that local file:// URL.
    If absent, leave the original path (will 404 silently).

    Returns the rewritten HTML and a stats dict so we can see in CI logs
    which assets resolved and which didn't.
    """
    stats = {"rewritten": [], "missing": []}

    def _replace(match: re.Match) -> str:
        full = match.group(0)
        rel_encoded = full[len(MAC_BASE):]
        rel = urllib.parse.unquote(rel_encoded)
        local = ASSETS_DIR / rel
        if local.exists():
            staged = staging / "assets" / rel
            staged.parent.mkdir(parents=True, exist_ok=True)
            if not staged.exists():
                shutil.copy2(local, staged)
            stats["rewritten"].append(rel)
            return "assets/" + urllib.parse.quote(rel)
        stats["missing"].append(rel)
        return full

    pattern = re.compile(re.escape(MAC_BASE) + r"[^'\"\s)]+")
    out = pattern.sub(_replace, html)

    # Inject the Google Fonts fallback right before </head>
    if "</head>" in out and "render-fonts-fallback" not in out:
        out = out.replace("</head>", GOOGLE_FONTS_CSS + "</head>", 1)
    return out, stats


def html_files() -> list[Path]:
    """Every markup/*.html that's a real per-account variant or the template."""
    return sorted(p for p in ROOT.glob("*.html") if p.is_file())


def render_one(page, html_path: Path, staging: Path) -> Path:
    src = html_path.read_text(encoding="utf-8")
    rewritten, stats = rewrite_asset_paths(src, staging)
    staged_html = staging / html_path.name
    staged_html.write_text(rewritten, encoding="utf-8")

    unique_missing = sorted(set(stats["missing"]))
    print(f"    {len(set(stats['rewritten']))} unique assets resolved, "
          f"{len(unique_missing)} missing")
    for m in unique_missing[:10]:
        print(f"      - missing: {m}")
    if len(unique_missing) > 10:
        print(f"      ... and {len(unique_missing) - 10} more")

    out_pdf = OUT_DIR / f"{html_path.stem}.pdf"
    page.goto(staged_html.as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")
    page.pdf(
        path=str(out_pdf),
        width="8.5in",
        height="11in",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        prefer_css_page_size=False,
    )
    return out_pdf


def main() -> int:
    files = html_files()
    if not files:
        print("No HTML files found in markup/ — nothing to render.")
        return 0

    # Drop stale PDFs whose source HTML no longer exists (e.g. an account
    # that was removed from Joe's sheet, or row-N.pdf orphans from before
    # the header-row fix).
    expected_stems = {f.stem for f in files}
    for pdf in OUT_DIR.glob("*.pdf"):
        if pdf.stem not in expected_stems:
            print(f"  ⌫ removing stale {pdf.name}")
            pdf.unlink()

    staging = ROOT / "_staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir()
    (staging / "assets").mkdir(exist_ok=True)

    print(f"Rendering {len(files)} HTML file(s)...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 816, "height": 1056})
        page = ctx.new_page()
        for f in files:
            try:
                out = render_one(page, f, staging)
                print(f"  ✓ {f.name} -> {out.relative_to(REPO)}")
            except Exception as exc:
                print(f"  ✗ {f.name}: {exc}", file=sys.stderr)
                return 1
        browser.close()

    shutil.rmtree(staging, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
