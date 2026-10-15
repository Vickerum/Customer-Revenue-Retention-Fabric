# Customer Revenue & Retention Intelligence — Microsoft Fabric

An end-to-end portfolio project using **real historical retail transactions** to investigate revenue trends, customer purchasing behaviour, repeat purchases and cancellations. The goal is to demonstrate reliable data engineering, dimensional modelling, advanced DAX and evidence-based business analysis.

> **Data integrity:** This project uses the original Online Retail II dataset published by the UCI Machine Learning Repository. The original workbook is included in this repository at `data/raw/online_retail_II.xlsx` for direct access. It is not replaced with synthetic data or silently edited.

## Data source

- **Dataset:** Online Retail II
- **Publisher:** UCI Machine Learning Repository
- **Citation:** Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D
- **Official page:** https://archive.ics.uci.edu/dataset/502/online+retail+ii
- **Licence:** CC BY 4.0 — attribution required
- **Documented period:** 1 December 2009–9 December 2011
- **Documented records:** 1,067,371 transaction lines
- **Business context:** Historical transactions from a UK-based, non-store online retailer selling giftware; the source notes that many customers are wholesalers.

The source workbook has eight fields: `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer ID`, and `Country`. Preserve these source names in the raw layer; any renamed columns belong in documented transformation layers. See [the data dictionary](docs/data_dictionary.md).

The dataset is historical. It is suitable for demonstrating analytics methods, not for claiming that its behaviour represents the 2026 retail market. We have not independently audited the retailer's original transaction system; provenance is based on UCI's documentation.

## Raw workbook links

- **Direct raw Excel file:** https://raw.githubusercontent.com/Vickerum/Customer-Revenue-Retention-Fabric/main/data/raw/online_retail_II.xlsx
- **GitHub file page:** https://github.com/Vickerum/Customer-Revenue-Retention-Fabric/blob/main/data/raw/online_retail_II.xlsx
- **Checksum and source manifest:** [`data/raw/manifest.json`](data/raw/manifest.json)

In Microsoft Fabric, try the direct raw URL with a URL-based source/ingestion method. If the connector cannot read the workbook directly from that URL, download the file and upload it into your Lakehouse under `Files/raw/`. The repository-hosted workbook is approximately 45.6 MB.

## Download and verify locally

Requirements: Python 3.10+.

```bash
python scripts/download_data.py
python scripts/download_data.py --verify-only
```

The script downloads the dataset archive from UCI, extracts the original workbook to `data/raw/online_retail_II.xlsx`, calculates its SHA-256 checksum, and writes a manifest. It does not transform the workbook. The checksum verifies file integrity relative to the recorded manifest; it does not independently prove that every transaction is authentic.

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
- How do cancellations and negative-quantity lines affect transaction value?
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
│       ├── online_retail_II.xlsx
│       └── manifest.json
├── docs/
│   ├── data_dictionary.md
│   └── data_provenance.md
├── fabric/
│   └── 01_download_raw_from_uci.py
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
