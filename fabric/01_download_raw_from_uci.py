# Download the UCI dataset and store the original workbook in the Fabric Lakehouse.

import requests
import zipfile

# Source dataset and file locations
url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
zip_path = "/tmp/retail.zip"  # Temporary workspace used during this run.
excel_name = "online_retail_II.xlsx"

# Download the ZIP archive and save its contents as a local file.
response = requests.get(url)
data = response.content  # Raw bytes returned by the download request.
open(zip_path, "wb").write(data)  # "wb" writes binary data.

# Extract the original Excel workbook from the archive.
with zipfile.ZipFile(zip_path) as zip_file:
    zip_file.extract(excel_name, "/tmp")

# Create the destination folder in the attached Lakehouse, if needed.
notebookutils.fs.mkdirs("Files/raw")

# Copy the workbook from temporary storage to the Lakehouse.
notebookutils.fs.cp(
    "file:/tmp/" + excel_name,  # Source file in the notebook environment.
    "Files/raw/" + excel_name,  # Destination inside the Lakehouse.
    True                        # Overwrite an existing copy.
)

print("Dataset saved in the Lakehouse!")
