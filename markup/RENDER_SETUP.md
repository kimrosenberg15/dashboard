# Pitch-card render pipeline — one-time setup

This is a 10-minute, one-time setup. Once it's done, every push that touches
`markup/*.html` will render PDFs in CI and drop them into Drive's
`Rendered PDFs/` folder.

Without these secrets, the workflow still runs — it renders PDFs with Google
Fonts substitutes (Playfair Display + Inter instead of Denton + Söhne), no
brand images, and skips the Drive upload. So you can set things up
incrementally.

## What you need to create

| GitHub secret | Where it comes from | Required? |
|---|---|---|
| `DRIVE_SA_JSON` | Google Cloud service account JSON key | Yes (for images + Drive upload) |
| `FLOCK_COLLATERAL_FOLDER_ID` | `1gAw6R_N6EW24Yd0t2U12sxI5ESXMbjSa` | Yes (already known) |
| `RENDERED_PDFS_FOLDER_ID` | Drive folder ID of `Rendered PDFs/` | Yes (find via Drive URL) |

## Step 1 — Create the Google Cloud service account

1. Open <https://console.cloud.google.com/iam-admin/serviceaccounts>.
2. Pick a project (or create one called `flock-collateral`).
3. **Create service account**:
   - Name: `flock-pdf-renderer`
   - Description: "Renders pitch card PDFs in GitHub Actions; reads brand assets, writes rendered PDFs"
   - Click **Create and continue** → **Done** (no role needed at the project level — Drive permissions come from sharing the folder in step 3).
4. On the service-account row, click the three-dot menu → **Manage keys** → **Add key** → **Create new key** → **JSON** → **Create**.
5. A `.json` file downloads. Keep it secret. You'll paste its contents into GitHub in step 4.
6. Copy the service account's email — it looks like
   `flock-pdf-renderer@flock-collateral.iam.gserviceaccount.com`. You'll use it in step 2.

## Step 2 — Enable the Drive API for this project

1. Open <https://console.cloud.google.com/apis/library/drive.googleapis.com>.
2. Make sure the project from step 1 is selected (top-left).
3. Click **Enable**.

## Step 3 — Share the Drive folders with the service account

The service account is just an email address from Drive's perspective.

1. Open <https://drive.google.com/drive/u/0/folders/1gAw6R_N6EW24Yd0t2U12sxI5ESXMbjSa>
   — this is the `Flock Collateral` folder.
2. Right-click the folder → **Share**.
3. Paste the service-account email from step 1.6.
4. Set permission to **Viewer**. Uncheck "Notify people". **Share**.
5. Open the `Rendered PDFs` subfolder (inside Flock Collateral).
6. Right-click → **Share**. Paste the same email. Set permission to **Editor**
   (it needs write access to upload PDFs). **Share**.
7. Grab the `Rendered PDFs` folder ID — it's the long string after `/folders/`
   in the URL when you're inside the folder. Save it for step 4.

## Step 4 — Add the GitHub secrets

1. Open <https://github.com/kimrosenberg15/dashboard/settings/secrets/actions>.
2. **New repository secret**:
   - Name: `DRIVE_SA_JSON`
   - Secret: paste the entire contents of the `.json` file from step 1.4 (the
     whole `{ ... }` blob).
   - **Add secret**.
3. **New repository secret**:
   - Name: `FLOCK_COLLATERAL_FOLDER_ID`
   - Secret: `1gAw6R_N6EW24Yd0t2U12sxI5ESXMbjSa`
   - **Add secret**.
4. **New repository secret**:
   - Name: `RENDERED_PDFS_FOLDER_ID`
   - Secret: the folder ID from step 3.7.
   - **Add secret**.

## Step 5 — Kick off the first render

Either:

- Push any change to a `markup/*.html` file, or
- Open <https://github.com/kimrosenberg15/dashboard/actions/workflows/render-pdfs.yml>
  and click **Run workflow** → pick the branch → **Run workflow**.

Once it's green:

- PDFs are committed back to the branch under `markup/rendered/<name>.pdf`.
- PDFs are uploaded to Drive's `Rendered PDFs/` folder, overwriting any
  same-named file.
- You can also download them as a workflow artifact from the Actions run page.

## How the rendered output behaves without the SA

Until step 4 is done:

- Fonts will fall back to **Playfair Display** (≈ Denton) and **Inter**
  (≈ Söhne) loaded from Google Fonts CDN. Layouts will be close but not
  pixel-identical to Kim's Mac renders.
- Brand images (logos, hero photos, product icons) will show as broken-image
  placeholders, because the Mac `file:///Users/kimrosenberg/...` paths don't
  resolve in CI.
- Drive upload is skipped silently.
- PDFs still commit back to the branch under `markup/rendered/`.

## Rotating the key

If the SA key leaks or you want to rotate it: in Cloud Console, **Manage keys**
→ delete the old key → **Add key** → JSON → paste the new contents into the
`DRIVE_SA_JSON` GitHub secret.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Render step succeeds, fonts look wrong | `DRIVE_SA_JSON` set but Drive API not enabled | Step 2. |
| Render step succeeds, images broken | Brand folder not shared with SA email | Step 3.1–4. |
| `403: insufficientPermissions` on upload | `Rendered PDFs/` shared as Viewer not Editor | Step 3.5–6, change role to Editor. |
| `Forbidden: Drive API has not been used` | API disabled in project | Step 2. |
| Workflow doesn't trigger on push | The file you changed wasn't under `markup/*.html` | Touch any `.html` in markup/ and re-push, or click **Run workflow**. |
