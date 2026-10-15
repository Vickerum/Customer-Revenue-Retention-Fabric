# Step 1: Import the tools we need
import requests
import zipfile

# Step 2: Set the file names and download link
url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"
zip_file = "/tmp/retail.zip"
excel_file = "online_retail_II.xlsx"

# Step 3: Download the ZIP file
response = requests.get(url)
with open(zip_file, "wb") as file:
    file.write(response.content)

# Step 4: Extract the Excel file
with zipfile.ZipFile(zip_file) as file:
    file.extract(excel_file, "/tmp")

# Step 5: Save the Excel file in the Lakehouse
notebookutils.fs.mkdirs("Files/raw")
notebookutils.fs.cp(
    "file:/tmp/" + excel_file,
    "Files/raw/" + excel_file,
    True
)

print("Dataset saved!")
