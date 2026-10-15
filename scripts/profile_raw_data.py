#!/usr/bin/env python3
"""Create a basic, non-destructive profile of the original Online Retail II workbook."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "data" / "raw" / "online_retail_II.xlsx"
OUT = ROOT / "data" / "raw" / "profile_summary.json"


def main() -> None:
    if not WORKBOOK.exists():
        raise SystemExit("Raw workbook not found. Run python scripts/download_data.py first.")

    sheets = pd.read_excel(WORKBOOK, sheet_name=None, dtype={"InvoiceNo": "string", "StockCode": "string", "CustomerID": "string"})
    summary = {"source_file": WORKBOOK.name, "sheets": {}}

    for sheet_name, frame in sheets.items():
        invoice = frame.get("Invoice")
        invoice_col = "InvoiceNo" if "InvoiceNo" in frame.columns else None
        customer_col = "CustomerID" if "CustomerID" in frame.columns else None
        qty_col = "Quantity" if "Quantity" in frame.columns else None
        price_col = "Price" if "Price" in frame.columns else ("UnitPrice" if "UnitPrice" in frame.columns else None)
        date_col = "InvoiceDate" if "InvoiceDate" in frame.columns else None

        sheet_summary = {
            "row_count": int(len(frame)),
            "columns": list(frame.columns),
            "missing_values_by_column": {str(k): int(v) for k, v in frame.isna().sum().items()},
            "exact_duplicate_rows": int(frame.duplicated().sum()),
        }
        if invoice_col:
            inv = frame[invoice_col].astype("string").str.strip()
            sheet_summary["unique_invoice_numbers_including_cancellations"] = int(inv.nunique(dropna=True))
            sheet_summary["invoice_numbers_starting_with_C_rows"] = int(inv.str.upper().str.startswith("C", na=False).sum())
        if customer_col:
            sheet_summary["missing_customer_id_rows"] = int(frame[customer_col].isna().sum())
        if qty_col:
            qty = pd.to_numeric(frame[qty_col], errors="coerce")
            sheet_summary["negative_quantity_rows"] = int((qty < 0).sum())
            sheet_summary["zero_quantity_rows"] = int((qty == 0).sum())
        if price_col:
            price = pd.to_numeric(frame[price_col], errors="coerce")
            sheet_summary["zero_price_rows"] = int((price == 0).sum())
            sheet_summary["negative_price_rows"] = int((price < 0).sum())
        if date_col:
            dates = pd.to_datetime(frame[date_col], errors="coerce")
            sheet_summary["min_invoice_datetime"] = None if dates.isna().all() else str(dates.min())
            sheet_summary["max_invoice_datetime"] = None if dates.isna().all() else str(dates.max())

        summary["sheets"][str(sheet_name)] = sheet_summary

    OUT.write_text(json.dumps(summary, indent=2, default=str) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))
    print(f"\nProfile written to {OUT}")


if __name__ == "__main__":
    main()
