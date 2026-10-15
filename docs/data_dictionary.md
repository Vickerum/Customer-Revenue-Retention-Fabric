# Data dictionary — source fields

The UCI Online Retail II workbook contains two worksheets covering separate historical periods. Keep the source workbook and its original column names unchanged. Confirm worksheet names and row counts by running the profiler after download.

| Source field | Meaning documented by UCI | Initial analytical notes |
|---|---|---|
| `Invoice` | Invoice number; an invoice number beginning with C indicates a cancellation. | Keep as text. Inspect cancellation patterns. One invoice can contain multiple item lines. |
| `StockCode` | Product/item code. | Keep as text to preserve code formatting. Check code consistency. |
| `Description` | Product/item description. | Inspect missing values and inconsistent descriptions for the same stock code. |
| `Quantity` | Quantity of each item per transaction line. | Numeric; investigate negative values before assigning business meaning. |
| `InvoiceDate` | Date and time the transaction was generated. | Parse to datetime and validate range. |
| `Price` | Unit price in British pounds sterling (£). | Numeric; inspect zero and negative prices before defining revenue. |
| `Customer ID` | Customer number. | Nullable identifier; customer-level analysis must disclose exclusions/unknown customers. |
| `Country` | Country where the customer resides. | Standardize only in Silver, retaining raw source values for audit. |

## Grain

Treat each source row as a transaction line until profiling establishes otherwise. Multiple rows can belong to the same invoice because an invoice may contain multiple products. Do not count rows as orders.

## Important derived fields (not source columns)

These will be created in the transformation/model layer and labelled as derived:

- `LineValue`: typically `Quantity * Price`, subject to validation and a documented cancellation/return treatment.
- `IsCancellationInvoice`: invoice number begins with C, based on UCI's documented convention.
- `HasCustomerID`: whether `Customer ID` is present.
- Calendar attributes derived from `InvoiceDate`.

These are not proof of net revenue or profit. A defensible net sales measure requires an explicit treatment of cancellations, returns, negative quantities and pricing conventions.
