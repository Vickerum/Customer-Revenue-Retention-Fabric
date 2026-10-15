# Microsoft Fabric notebook code — download the original UCI workbook
# Copy this into a Fabric notebook and run it in a Lakehouse-attached workspace.
# It stores the original workbook unchanged under Files/raw/ and does not require
# the workbook to be hosted in GitHub.

import io
import zipfile
import requests
from pathlib import Path

SOURCE_URL = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
ARCHIVE_PATH = Path("/tmp/online_retail_ii.zip")
EXTRACT_DIR = Path("/tmp/uci_online_retail_ii")

response = requests.get(SOURCE_URL, timeout=120)
response.raise_for_status()
ARCHIVE_PATH.write_bytes(response.content)

if not zipfile.is_zipfile(ARCHIVE_PATH):
    raise ValueError("UCI response was not a ZIP archive. Check the official dataset page.")

EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(ARCHIVE_PATH) as archive:
    workbook_member = next(
        (name for name in archive.namelist()
         if Path(name).name.lower() == "online_retail_ii.xlsx"),
        None,
    )
    if workbook_member is None:
        raise FileNotFoundError(
            "Could not find online_retail_II.xlsx in the downloaded UCI archive. "
            f"Archive members: {archive.namelist()}"
        )
    workbook_bytes = archive.read(workbook_member)

local_workbook = EXTRACT_DIR / "online_retail_II.xlsx"
local_workbook.write_bytes(workbook_bytes)

# Save the original workbook bytes unchanged in the attached Fabric Lakehouse.
# In a Lakehouse-attached notebook, Files/ maps to the default Lakehouse Files area.
target_dir = "Files/raw"
notebookutils.fs.mkdirs(target_dir)
notebookutils.fs.cp(
    f"file:{local_workbook}",
    f"{target_dir}/online_retail_II.xlsx",
    True,
)

import hashlib
checksum = hashlib.sha256(workbook_bytes).hexdigest()
print(f"Saved original workbook to {target_dir}/online_retail_II.xlsx")
print(f"Workbook size: {len(workbook_bytes):,} bytes")
print(f"SHA-256: {checksum}")
print("Source: https://archive.ics.uci.edu/dataset/502/online+retail+ii")
print("The workbook was not transformed. Keep this as the raw/bronze source artifact.")

# Optional next step, after confirming the workbook is present:
# import pandas as pd
# sheets = pd.read_excel(local_workbook, sheet_name=None)
# for sheet_name, frame in sheets.items():
#     print(sheet_name, frame.shape, list(frame.columns))
