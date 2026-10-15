# Data dictionary — source fields

The Online Retail II source contains eight fields. The workbook has two historical sheets/periods; confirm the exact sheet names and per-sheet row counts after downloading. Do not rename or transform columns in the raw workbook.

| Source field | Meaning documented by UCI | Initial analytical notes |
|---|---|---|
| `InvoiceNo` | Invoice number; an invoice number beginning with C indicates a cancellation. | Keep as text. Inspect cancellation patterns. Do not assume each invoice equals one row; invoices can have multiple line items. |
| `StockCode` | Product/item code. | Keep as text to preserve codes and leading zeros if present. Check code consistency. |
| `Description` | Product/item description. | Text field; inspect missing values and inconsistent descriptions per stock code. |
| `Quantity` | Quantity of each item per transaction line. | Numeric; negative values need investigation and source-aware interpretation. |
| `InvoiceDate` | Date and time the transaction was generated. | Parse to datetime; validate range and locale/time interpretation. |
| `UnitPrice` | Unit price in British pounds sterling (£). | Numeric; inspect zero and negative prices before defining revenue. |
| `CustomerID` | Customer number. | Nullable identifier; customer-level analysis must disclose exclusions/unknown customers. |
| `Country` | Country where the customer resides. | Text; standardize only in Silver, retaining raw source values for audit. |

## Grain

Treat each source row as a transaction line until profiling establishes otherwise. Multiple rows can belong to the same invoice because one invoice may contain multiple products. Do not count rows as orders.

## Important derived fields (not source columns)

These will be created in the transformation/model layer and labelled as derived:

- `LineGrossValue`: typically `Quantity * UnitPrice`, subject to validation and a documented cancellation/return treatment.
- `IsCancellationInvoice`: invoice number begins with C, based on UCI's documented convention.
- `HasCustomerID`: whether CustomerID is present.
- Calendar attributes derived from InvoiceDate.

These are not proof of net revenue or profit. A defensible net sales measure requires an explicit treatment of cancellations, returns, negative quantities and pricing conventions.
