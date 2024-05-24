import os
import subprocess
from tqdm import tqdm

# Define the directory containing the PDB files
pdb_dir = "rna_only"

# Get the list of PDB files in the directory
pdb_files = [f for f in os.listdir(pdb_dir) if f.endswith(".pdb")]

# Function to run the command for a single PDB file
def run_mc_annotate(pdb_file):
    pdb_path = os.path.join(pdb_dir, pdb_file)
    output_file = pdb_path.replace(".pdb", ".info")
    command = f"./MC-Annotate {pdb_path} > {output_file}"
    subprocess.run(command, shell=True)

# Process each PDB file with progress tracking
for pdb_file in tqdm(pdb_files, desc="Processing PDB files"):
    run_mc_annotate(pdb_file)

print("All PDB files have been processed.")

