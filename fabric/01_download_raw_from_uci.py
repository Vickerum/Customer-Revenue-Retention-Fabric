import requests
import zipfile

url = "https://archive.ics.uci.edu/static/public/502/online+retail+ii.zip"

open("/tmp/data.zip", "wb").write(requests.get(url).content)

with zipfile.ZipFile("/tmp/data.zip") as z:
    z.extract("online_retail_II.xlsx", "/tmp")

notebookutils.fs.mkdirs("Files/raw")
notebookutils.fs.cp("file:/tmp/online_retail_II.xlsx", "Files/raw/online_retail_II.xlsx", True)

print("Done!")
