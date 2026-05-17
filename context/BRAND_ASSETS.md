# Brand assets — single source of truth

_Living manifest. Every asset we use in any Flock collateral lives here with its Drive folder, filename, and the templates/fields that reference it. Update on every session that touches a brand asset._

> **How to use this doc:** When adding a new asset, drop a row in the right table. When swapping an asset in a template, update the "Used in" column. Future sessions read this first before touching brand visuals.

---

## 1. Drive folder reference

**Root:** `Flock Collateral` — `1QwRN0wAFYB9QUETttAOT5LTj6D1hCXWW`
🔗 <https://drive.google.com/drive/folders/1QwRN0wAFYB9QUETttAOT5LTj6D1hCXWW>

| Folder | ID | What it holds |
|---|---|---|
| `BRAND_Flock Logo` | `1wyStT8EvJv_hivPvd3id_5pufk6GiGws` | Wordmark + bird symbol, 4 color variants each |
| `BRAND_Images` | `1KoRssnkY-Xp3KsxSg1N31UqbWEtpneut` | Brand-approved hero imagery |
| `BRAND_Font - Denton OTF` | `18lHsKDa7oF65sziCN_d1194oMjFpt9qR` | Denton font family (serif) |
| `BRAND_Font - Sohne OTF` | `1wewOF4sFdI5hdt47C8OWefHiOlUSdQ1y` | Söhne font family (sans) |
| `Images_Fixed` | `1dMiyw755bsl0jt1VCB2TsMuCLfPOaRVV` | Shared template assets (diagram, US flag) |
| `Images_Account Logos` | `1PiwCEI43W9Cqr2lYJ6NU6tjf48ThArjy` | Per-account logos, keyed by account |
| `Images_Account_QR Codes` | `1PtUhCHHeGq9fIoeKXOgeUP9UooBgMEri` | Per-account QR codes (footer + booking) |
| `Images_Account_Location` | `1mROZIgid4aIlNn4Vtm3rlkGSWOnHbdGd` | Per-account location/hero photos |
| `Images_Account_Agency Type` | `1rR3-lCkNFb4XrBszYnEtJGlhNMrjmxiV` | Hero imagery grouped by agency type |
| `Images_Products` | `1o29iYrriI5qx_cRm6mYh2KW-MkANt9BK` | Product card thumbnails |
| `Rendered PDFs` | `1gAw6R_N6EW24Yd0t2U12sxI5ESXMbjSa` | Output destination for rendered PDFs |
| `LPR & ALPR` | `1JdeN1yonssexQKYCS62FVcaGCKsYA1Mb` | Product imagery |
| `Video Cameras` | `1Gs_njqY-znH_zxyDrC3WmZCXqY-rMUxz` | Product imagery |
| `Audio Detection` | `1FSrx7ErfIg_MHUXuGTMqGsRbOmc9IYyD` | Product imagery |
| `DFR - Drone as First Responder` | `18q2K5GbHfSkY8FksQXdQUhBQ9SSORQp8` | Product imagery |
| `Mobile Security Trailers` | `1wJdsCCPQ8KVKW2iW66gbp67KYdNVD7D_` | Product imagery |
| `Nova OSINT` | `1SM5WMQ7XP4ZyH5lizuCF3d7rC97w1CAT` | Product imagery |
| `FlockOS & Platform` | `11_inTagfsSvgBg51HeyTSDDx-Ag5W24S` | Product imagery |
| `Traffic Analytics & Transportation` | `1m8CIE9fW_u9WxGIzNlb3sZ61gK8htlmZ` | Product/vertical imagery |
| `Community & Advocacy` | `1ZCa7Ezngos2-Igo_AnfTWMCEAfowVvkf` | Supporting imagery |
| `Industry Verticals` | `1ea1w5TfaZJc5yJIoQXFZe8BQvj7M7tps` | Per-vertical imagery |
| `Legal & Compliance` | `172KtmDbFSW-BTDODo3bY5tujac4fy1dy` | Compliance icons (NDAA flag, etc.) |

---

## 2. Flock logos (`BRAND_Flock Logo/`)

Two marks (wordmark `Logo` + bird-only `Symbol`), each in 4 colors.

| Filename | Mark | Color | Used in |
|---|---|---|---|
| `Flock_Logo_Cream.svg` | Wordmark + bird | Cream `#F7F7F4` | **Pitch card P1 banner header** (`.p1-logo-bird`, 23px tall, on dark green banner) |
| `Flock_Logo_Black.svg` | Wordmark + bird | Black | _Available, not yet used_ |
| `Flock_Logo_Green.svg` | Wordmark + bird | Brand green `#034435` | _Available, not yet used_ |
| `Flock_Logo_White.svg` | Wordmark + bird | White | _Available, not yet used_ |
| `Flock_Symbol_Black.svg` | Bird only | Black | **Pitch card footer on all 3 pages** (`.footer-bird`, 28px wide, on off-white footer card) |
| `Flock_Symbol_Cream.svg` | Bird only | Cream | _Available, not yet used_ |
| `Flock_Symbol_Green.svg` | Bird only | Brand green | _Available, not yet used_ |
| `Flock_Symbol_White.svg` | Bird only | White | _Available, not yet used_ |

**Rule of thumb:** Wordmark for primary brand placement on dark backgrounds → Cream. Bird-only for secondary placements on light backgrounds → Black. Other variants are options when we add new templates with different backgrounds.

---

## 3. Fonts

| Family | Folder | Weights available | Used in |
|---|---|---|---|
| **Denton** | `BRAND_Font - Denton OTF` | 400 Regular, 700 Bold, 900 Black, 400 italic | Pitch card headings (`.p1-h1`, `.adv-section-head`, `.stats-head`, `.p2-products-hd`, `.p3-title`, `.feat-lc`, `.p3-cta-quote`, `.p3-cta-book-head`) and the lime tagline (`.p1-tagline`) |
| **Söhne** | `BRAND_Font - Sohne OTF` | 400 Buch, 400 Buch Kursiv (italic), 600 Halbfett, 700 Kräftig | Pitch card body (`.p1-body-text`, `.adv-body`, `.stats-list li`, `.pdesc`, `.feat-rc`, `.footer-info`, etc.) |

**Fallback in CI** (when fonts not yet wired through SA): Denton → Playfair Display, Söhne → Inter, both from Google Fonts CDN. See `markup/render.py`.

---

## 4. Fixed template assets (`Images_Fixed/`)

| Filename | Used in |
|---|---|
| `Image_Page1_Flock Product Diagram.png` | P1 proven-at-scale panel, FlockOS sensor network diagram |
| _US flag (NDAA)_ | P3 compliance row — filename TBD, currently a placeholder |

---

## 5. Per-account assets (per-piece)

These follow naming conventions keyed off Account ID. Filenames TBD as Joe + sheet finalize:

| Asset type | Folder | Naming convention (proposed) | Pitch card field |
|---|---|---|---|
| Account logo | `Images_Account Logos/` | `<AccountID>-logo.png` (or SVG) | P2 header, account logo lockup |
| Account hero (P1) | `Images_Account_Location/` | `<AccountID>-hero-p1.jpg` | P1 banner right photo |
| Account hero (P2) | `Images_Account_Location/` | `<AccountID>-hero-p2.jpg` | P2 top hero photo |
| Account QR — footer | `Images_Account_QR Codes/` | `<AccountID>-qr-footer.png` | All 3 page footers |
| Account QR — booking | `Images_Account_QR Codes/` | `<AccountID>-qr-booking.png` | P3 CTA right panel |

---

## 6. Product imagery (per pitch card mix)

P2 product cards reference 8 product images. Each Flock product has its own folder under Flock Collateral root.

| Product | Folder | Notes |
|---|---|---|
| LPR & ALPR | `LPR & ALPR/` | License-plate readers |
| Video Cameras | `Video Cameras/` | Camera lineup |
| Audio Detection | `Audio Detection/` | Raven / gunshot detection |
| DFR | `DFR - Drone as First Responder/` | Drone product |
| Mobile Security Trailers | `Mobile Security Trailers/` | Trailers |
| Nova OSINT | `Nova OSINT/` | Open-source intel platform |
| FlockOS & Platform | `FlockOS & Platform/` | Platform/UI screenshots |
| Traffic Analytics & Transportation | `Traffic Analytics & Transportation/` | Analytics product |

Per-vertical product mixes will be defined in the Vertical Library table (see `context/WORKFLOW.md` §3).

---

## 7. Update protocol

When making changes that touch any brand asset, update this doc in the same commit:

- **Adding a new asset** → add a row to the appropriate table, note the file's used location even if not in a template yet.
- **Swapping an asset in a template** → update the "Used in" column for both the old (mark as available) and the new (mark as in use).
- **Renaming a Drive folder** → update the folder ID table AND grep for the old name in `markup/`, `context/`, and `.github/` to update all references.
- **New asset family** (e.g., a new product, a new vertical) → add a section.

This doc is the SSOT. If it disagrees with code, the code is wrong and gets fixed.

---

_Last updated: 2026-05-16 — Initial creation. Captured logo variants in `BRAND_Flock Logo/`, folder ID inventory for Flock Collateral, font references, per-account naming convention proposals._
