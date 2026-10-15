# GOAL: Download the dataset and save it in Fabric.

# 1. These are ready-made Python tools.
import requests   # Downloads things from the internet.
import zipfile    # Opens ZIP files.

# 2. Variables are named boxes that store information.
url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
zip_path = "/tmp/retail.zip"  # /tmp is a temporary folder while code runs.
excel_name = "online_retail_II.xlsx"

# 3. Download the ZIP file.
response = requests.get(url)  # Ask the website for the file.
data = response.content      # The downloaded file's actual bytes.
open(zip_path, "wb").write(data)  # "wb" means save bytes as a file.

# 4. Take the Excel file out of the ZIP file.
with zipfile.ZipFile(zip_path) as zip_file:
    zip_file.extract(excel_name, "/tmp")

# 5. Make a folder in the Fabric Lakehouse.
notebookutils.fs.mkdirs("Files/raw")  # mkdirs means "make folders".
# notebookutils.fs is Fabric's tool for working with Lakehouse files.

# 6. Copy the Excel file from the temporary folder into the Lakehouse.
notebookutils.fs.cp(
    "file:/tmp/" + excel_name,       # Where the file is now.
    "Files/raw/" + excel_name,       # Where we want the file to go.
    True                             # Allow replacing it if it already exists.
)

print("Dataset saved in the Lakehouse!")
