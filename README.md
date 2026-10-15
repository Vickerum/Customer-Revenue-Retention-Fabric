# Customer Revenue & Retention Intelligence — Microsoft Fabric

An end-to-end portfolio project using **real historical retail transactions** to investigate revenue trends, customer purchasing behaviour, repeat purchases and cancellations. The goal is to demonstrate reliable data engineering, dimensional modelling, advanced DAX and evidence-based business analysis.

> **Data integrity:** This project uses the original Online Retail II dataset from the UCI Machine Learning Repository. The raw workbook is downloaded from UCI by the script in this repository; it is not replaced with synthetic data or silently edited. The source workbook is intentionally not committed to Git.

## Data source

- **Dataset:** Online Retail II
- **Publisher:** UCI Machine Learning Repository
- **Creator/citation:** Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D
- **Official page:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **Licence:** CC BY 4.0 — attribution required
- **Documented period:** 1 December 2009–9 December 2011
- **Documented records:** 1,067,371 transaction lines
- **Business context:** Historical transactions from a UK-based, non-store online retailer selling giftware; the source notes that many customers are wholesalers.

The source workbook has eight fields: `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, and `Country`. Preserve these source names in the raw layer; any renamed columns belong in documented transformation layers. See [the data dictionary](docs/data_dictionary.md).\n\nThe dataset is historical. It is suitable for demonstrating analytics methods, not for claiming that its behaviour represents the 2026 retail market. We have not independently audited the retailer's original transaction system; provenance is based on UCI's documentation.

## Get the original raw data

Requirements: Python 3.10+.

```bash
python scripts/download_data.py
```

The script downloads the dataset archive from UCI, extracts the original Excel workbook to `data/raw/online_retail_II.xlsx`, calculates its SHA-256 checksum, and writes a local manifest. It does not alter the workbook. The raw workbook and manifest are ignored by Git to keep large data files out of source control.

Verify the workbook later by rerunning:

```bash
python scripts/download_data.py --verify-only
```

The verification compares the file against the checksum recorded locally when it was downloaded. This proves file integrity relative to that recorded checksum; it does not independently prove that every transaction is authentic.

## Planned architecture

```text
UCI source workbook (unchanged)
          |
          v
Bronze — preserve source / ingestion metadata
          |
          v
Silver — data types, quality checks, documented cleaning
          |
          v
Gold — customer, product, date and transaction analytical tables
          |
          v
Power BI semantic model — star schema + DAX measures
          |
          v
Business insights — revenue, repeat purchase, cancellations, concentration
```

Bronze/Silver/Gold are logical data layers. Their implementation will be documented as the Fabric solution is built.

## Questions to investigate (not assumed conclusions)

- How does revenue vary over time and across countries/products?
- How concentrated is revenue among customers?
- What share of identifiable customers make repeat purchases?
- How do cancellations and negative-quantity lines affect gross transaction value?
- Which products and customer groups show meaningful changes over time?
- Which data-quality limitations could bias each metric?

We will discover findings from the data rather than invent results in advance. We will not claim profit, acquisition cost, marketing ROI, delivery causes or customer churn causes unless suitable evidence exists.

## Repository layout

```text
.
├── README.md
├── .gitignore
├── requirements.txt
├── data/
│   └── raw/
│       └── .gitkeep
├── docs/
│   ├── data_dictionary.md
│   └── data_provenance.md
└── scripts/
    ├── download_data.py
    └── profile_raw_data.py
```

## Planned deliverables

- Reproducible raw-data acquisition and provenance
- Data profiling and quality issue log
- Microsoft Fabric ingestion and Bronze/Silver/Gold processing
- SQL transformations and documented data-quality rules
- Star-schema semantic model
- Advanced DAX: time intelligence, customer ranking, repeat purchase/cohorts and cancellation analysis
- Power BI report with executive summary and drill-through
- Evidence-backed recommendations with assumptions and limitations clearly stated

## Attribution

Please retain this attribution when reusing or adapting the dataset:

Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D. Licensed under CC BY 4.0.
