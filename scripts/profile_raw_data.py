#!/usr/bin/env python3
"""Create a basic, non-destructive profile of the original Online Retail II workbook."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "data" / "raw" / "online_retail_II.xlsx"
OUT = ROOT / "data" / "raw" / "profile_summary.json"


def find_column(frame: pd.DataFrame, *candidates: str) -> str | None:
    """Find a source column using case-insensitive, whitespace-normalized names."""
    normalized = {str(c).strip().casefold(): str(c) for c in frame.columns}
    for candidate in candidates:
        actual = normalized.get(candidate.strip().casefold())
        if actual is not None:
            return actual
    return None


def main() -> None:
    if not WORKBOOK.exists():
        raise SystemExit("Raw workbook not found. Run python scripts/download_data.py first.")

    sheets = pd.read_excel(
        WORKBOOK,
        sheet_name=None,
        dtype={
            "Invoice": "string",
            "InvoiceNo": "string",
            "StockCode": "string",
            "Customer ID": "string",
            "CustomerID": "string",
        },
    )
    summary = {"source_file": WORKBOOK.name, "sheets": {}}

    for sheet_name, frame in sheets.items():
        invoice_col = find_column(frame, "Invoice", "InvoiceNo")
        customer_col = find_column(frame, "Customer ID", "CustomerID")
        qty_col = find_column(frame, "Quantity")
        price_col = find_column(frame, "Price", "UnitPrice")
        date_col = find_column(frame, "InvoiceDate")

        sheet_summary = {
            "row_count": int(len(frame)),
            "columns": [str(c) for c in frame.columns],
            "missing_values_by_column": {
                str(c): int(v) for c, v in frame.isna().sum().items()
            },
            "exact_duplicate_rows": int(frame.duplicated().sum()),
        }
        if invoice_col:
            invoice = frame[invoice_col].astype("string").str.strip()
            sheet_summary["unique_invoice_numbers_including_cancellations"] = int(
                invoice.nunique(dropna=True)
            )
            sheet_summary["invoice_numbers_starting_with_C_rows"] = int(
                invoice.str.upper().str.startswith("C", na=False).sum()
            )
        if customer_col:
            sheet_summary["missing_customer_id_rows"] = int(
                frame[customer_col].isna().sum()
            )
        if qty_col:
            quantity = pd.to_numeric(frame[qty_col], errors="coerce")
            sheet_summary["negative_quantity_rows"] = int((quantity < 0).sum())
            sheet_summary["zero_quantity_rows"] = int((quantity == 0).sum())
        if price_col:
            price = pd.to_numeric(frame[price_col], errors="coerce")
            sheet_summary["zero_price_rows"] = int((price == 0).sum())
            sheet_summary["negative_price_rows"] = int((price < 0).sum())
        if date_col:
            dates = pd.to_datetime(frame[date_col], errors="coerce")
            sheet_summary["invalid_invoice_datetime_rows"] = int(dates.isna().sum())
            sheet_summary["min_invoice_datetime"] = (
                None if dates.isna().all() else str(dates.min())
            )
            sheet_summary["max_invoice_datetime"] = (
                None if dates.isna().all() else str(dates.max())
            )

        summary["sheets"][str(sheet_name)] = sheet_summary

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))
    print(f"\nProfile written to {OUT}")


if __name__ == "__main__":
    main()
