# Download the Excel dataset from GitHub into the Fabric Lakehouse.

import requests

url = "https://raw.githubusercontent.com/Vickerum/Customer-Revenue-Retention-Fabric/main/data/raw/online_retail_II.xlsx"
local_file = "/tmp/online_retail_II.xlsx"

# Download the Excel file.
response = requests.get(url)
response.raise_for_status()
open(local_file, "wb").write(response.content)

# Copy it into the Lakehouse.
notebookutils.fs.mkdirs("Files/raw")
notebookutils.fs.cp(
    "file:" + local_file,
    "Files/raw/online_retail_II.xlsx",
    True
)

print("Dataset saved in Files/raw!")
