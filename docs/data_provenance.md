# Data provenance and integrity

## Source of record

- **Dataset:** Online Retail II
- **Publisher:** UCI Machine Learning Repository
- **Official landing page:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **DOI:** https://doi.org/10.24432/C5CG6D
- **Citation:** Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository.
- **Licence:** Creative Commons Attribution 4.0 International (CC BY 4.0)
- **Source-described period:** 2009-12-01 through 2011-12-09
- **Source-described record count:** 1,067,371

## What “real” means in this project

UCI describes the data as transactions from a UK-based, registered, non-store online retailer. We use that published provenance and do not fabricate transactions. We have not independently audited the retailer's point-of-sale or ERP system, so do not claim independent verification of every transaction.

## Download and integrity procedure

1. Run `python scripts/download_data.py`.
2. The script downloads the archive from the official UCI static download endpoint and extracts the original workbook without modifying it.
3. The script calculates SHA-256 and writes `data/raw/manifest.json` containing the source URL, retrieval timestamp, filename, file size and checksum.
4. Keep the manifest with your local raw file. The raw workbook and manifest are excluded from Git by `.gitignore`.
5. Run `python scripts/download_data.py --verify-only` to recalculate the hash and compare it to the locally recorded value.

A checksum detects changes relative to the recorded checksum. It does not prove the source publisher's claims or transaction authenticity.

## Raw-data handling rules

- Never overwrite the downloaded workbook with cleaned data.
- Do not manually edit the raw file.
- Store transformations and cleaned outputs separately.
- Log row counts before and after every transformation.
- Treat duplicate rows as candidates for investigation, not automatic deletions.
- Treat negative quantities and invoice numbers beginning with C according to documented source conventions; do not automatically label every negative quantity as a confirmed return.
- Do not infer profit without cost data or causality without supporting evidence.

## Interview-ready explanation

“I used the Online Retail II dataset published by the UCI Machine Learning Repository. I preserved the original workbook, documented its source and licence, and recorded a SHA-256 checksum so the file's integrity can be checked. My cleaning and modelling steps are separate and reproducible. I rely on UCI's documentation for the dataset's real-world origin; I have not independently audited the retailer's original transaction system.”
