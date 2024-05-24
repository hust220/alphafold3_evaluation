import os
import requests
from tqdm import tqdm

# Create the 'cif_files' directory if it doesn't exist
os.makedirs("cif_files", exist_ok=True)

# Read entry IDs from the file "rna.ls"
with open("rna.ls", "r") as file:
    entry_ids = [line.strip() for line in file.readlines()]

# Base URL for downloading CIF files
base_url = "https://files.rcsb.org/download/{}.cif"

# Function to download a CIF file
def download_cif(entry_id):
    url = base_url.format(entry_id)
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"cif_files/{entry_id}.cif", "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to download {entry_id}.cif")

# Download CIF files with progress bar
for entry_id in tqdm(entry_ids, desc="Downloading CIF files"):
    download_cif(entry_id)

print("Download completed.")

