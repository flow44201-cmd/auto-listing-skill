---
name: auto-listing-skill
description: Use when the user explicitly invokes auto-listing-skill or asks to process Ozon automatic listing work: locate the current shop root dynamically, read the shop rules and category notes, process product info and finished images, fill the price workbook and category listing workbook, build the image zip, fill the task summary workbook, and backfill the auto-listing tool paths, row ranges, and Ozon task_id without missing details.
---

# Auto Listing Skill

## Encoding-safe entry

This `SKILL.md` is intentionally ASCII-only so it remains readable on Windows computers where PowerShell defaults to a legacy code page.

Do not read Chinese rule files with default PowerShell `Get-Content`.

Required rule:

```powershell
python .\scripts\read_utf8_references.py --all
```

If running from another directory, use the absolute path to this skill folder:

```powershell
python "PATH_TO_SKILL\scripts\read_utf8_references.py" --all
```

This script reads every required reference file with UTF-8, validates that no mojibake was produced, and prints the complete rule text. It avoids the common Windows problem where PowerShell default decoding turns Chinese into unreadable text.

Forbidden for Chinese rule files:

```powershell
Get-Content .\references\*.md
Get-Content .\SKILL.md
type .\references\*.md
```

Allowed only when explicit UTF-8 is used:

```powershell
Get-Content -Encoding UTF8 .\references\verbatim-user-requirements.md
```

If any output contains mojibake, replacement characters, question-mark Chinese, or unreadable Chinese, stop immediately and rerun `scripts/read_utf8_references.py`. Do not execute from garbled rules.

## Mandatory references

Before doing any Ozon listing work, load the following files completely through `scripts/read_utf8_references.py --all`:

- `references/verbatim-user-requirements.md`
- `references/full-original-instructions.md`
- `references/ozon-listing-rules.md`
- `references/original-requirements-coverage.md`
- `references/final-audit-checklist.md`

Do not use `-TotalCount`, `head`, preview, or partial reads instead of full reads.

## Execution contract

Treat this as production data processing, not ordinary copywriting.

The task is complete only when all applicable items in `references/original-requirements-coverage.md` and `references/final-audit-checklist.md` are checked and satisfied. If any item cannot be completed or verified, report it as unfinished or blocked with the reason.

Important constraints that must never be skipped:

- Dynamically locate the current shop root. Do not hardcode a path.
- Prefer paths mentioned later in the user prompt or in lower notes.
- Strip Chinese locative suffixes such as trailing `li` meaning "in/inside" from user-provided paths when appropriate; for example, `...\shop li` in Chinese text may mean the path is `...\shop`.
- Determine the product-number prefix dynamically from the user message, shop config, init script, or old workbooks. Do not hardcode `1`, `21`, or any other prefix without a source.
- `Finished images` / `system finished images` determine what products must be listed.
- Product selling points and parameters come from corresponding product info folders, txt files, and selling-point images.
- Product info txt files may use the new filled template described in the UTF-8 references. Parse every line of that template; do not ignore freight, product weight, color count, link count, repacking dimensions, repacking weight, pasted attributes, pasted package info, or the "estimate the rest yourself" instruction.
- If pasted product attributes/package info conflict with the user's own repacking section, the user's own repacking section wins.
- Fill the price workbook without overwriting old data or formulas.
- Preserve formulas and formatting; do not hide or overwrite formulas.
- Fill numeric values as numbers where required; keep long IDs as direct text, never scientific notation.
- Prices and relevant amounts are RMB when the user says so; do not calculate from rubles.
- Respect all unit conversions.
- Choose the category workbook from the category line in the product txt file.
- Also judge product category yourself when required. Products with different categories must not be written into the same category listing workbook.
- If products have different categories, each category must have its own listing workbook output and its own separate row in the task summary workbook.
- Listing titles, descriptions, and tags must be Russian and suitable for direct Ozon upload.
- Titles, descriptions, intros, and tags must not contain brand information unless allowed, forbidden words, color terms where prohibited, or manufacturer/factory/wholesale/origin/place-of-origin/year/supplier wording.
- Even if the user-provided source text contains manufacturer, factory, wholesale, origin/place-of-origin, year, or manufacturer-info wording, ignore those parts. The seller page should mainly display product information and must not mention manufacturer information.
- Tags must be based on product data and Ozon/search analysis.
- Before generating titles or attributes, analyze the actual product from images, 1688/source links, product name, category, spec data, competitor data, and Ozon/RU search habits. Do not merely translate the Chinese name, invent a title, or reuse a fixed template.
- Avoid Ozon duplicate-card or forced-merge problems. For offers that should not merge into one card, keep model-name, similar-product grouping, color-name, seller-code, title structure, specs, weight, dimensions, use case, and scenario distinguishable by offer_id or real product specs, for example `model-{offer_id}` and `series-{offer_id}`.
- Category attributes must follow "fill everything that can reasonably be filled".
- Fields with dictionary/dropdown/enum values must use valid dictionary values or old-table dictionary patterns. Do not invent dictionary values and do not replace dictionary values with free text.
- Brand is the special exception: fill a brand only when the user explicitly provides `brand: XXX` or the Chinese equivalent. Otherwise use the Russian no-brand dictionary value specified in the UTF-8 references.
- `main images and video` is one folder name. Do not create separate `main images` and `video` folders. Inside it, create only product-number folders, and put the corresponding images inside those folders.
- Put image zip files in the required image-zip folder.
- Fill `task summary workbook` every time. New rows must not be yellow. If copying row formatting, clear any yellow fill from newly added rows.
- Do not process more than 100 products in one batch; split batches when needed.
- Put all intermediate files only in the required temporary folder.
- Backfill the auto-listing tool paths, row ranges, zip path, workbook paths, and Ozon task_id from the latest task-summary row. Do not leave this for the user.
- If lower notes conflict with upper rules, lower notes win.

## Recommended workflow

1. Run `scripts/read_utf8_references.py --all`.
2. Identify the shop root and product-number prefix.
3. Read shop-specific total rules and category notes.
4. Identify products from finished images and map them to product info folders.
5. Read txt and image-based product data.
6. Analyze Ozon/search data when creating titles, descriptions, and tags.
7. Fill the price workbook.
8. Fill the category listing workbook.
9. Build the `main images and video` product-number folders and image zip.
10. Fill the task summary workbook with no yellow fill on new rows.
11. Backfill the auto-listing tool.
12. Run the final checklist and report exactly what was completed.
