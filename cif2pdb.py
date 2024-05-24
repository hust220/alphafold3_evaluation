import os, sys, csv
from Bio.PDB import MMCIFParser, PDBIO, Select
from tqdm import tqdm

input_csv = sys.argv[1]
output_folder = sys.argv[2]

# Create the output_folder and 'chain_mappings' directories if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs("chain_mappings", exist_ok=True)

# Read the entry_ids from the CSV file
entry_ids = []
with open(input_csv, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        entry_ids.append(row["entry_id"])

# Initialize MMCIFParser and PDBIO
cif_parser = MMCIFParser(auth_residues=False, QUIET=True)
pdb_io = PDBIO()

class FirstAltLocSelect(Select):
    def accept_atom(self, atom):
        if atom.altloc not in ('', ' ', 'A'):
            return False
        atom.altloc = ' '  # Standardize altloc to the first option
        return True

# Function to rename chains and save the mapping
def rename_chains_and_save_mapping(structure):
    chain_map = {}
#    chain_id_gen = (chr(i) for i in range(ord('A'), ord('Z') + 100))
    chain_id_gen = (chr(i) for i in list(range(ord('A'), ord('Z') + 1)) + list(range(ord('a'), ord('z') + 1)))
    
    for chain in structure[0]:
        old_id = chain.id
        new_id = next(chain_id_gen)
        chain.id = 'TEMP_' + new_id
        chain_map[old_id] = new_id
#        for i, residue in enumerate(chain, start=1):
#            residue.id = (' ', i+10000, ' ')

    for chain in structure[0]:
        chain.id = chain.id[-1]
#        for i, residue in enumerate(chain, start=1):
#            residue.id = (' ', i, ' ')

    return chain_map

# Function to convert CIF to PDB with chain renaming
def convert_cif_to_pdb(entry_id):
    cif_file = f"cif_files/{entry_id}.cif"
    pdb_file = f"{output_folder}/{entry_id}.pdb"
    chain_map_file = f"chain_mappings/{entry_id}_chain_map.csv"
    
    try:
        # Parse the CIF file
        structure = cif_parser.get_structure(entry_id, cif_file)
        
        # Rename chains and get the mapping
        chain_map = rename_chains_and_save_mapping(structure)
        
        # Save the chain mapping to a CSV file
        with open(chain_map_file, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Old Chain ID", "New Chain ID"])
            for old_id, new_id in chain_map.items():
                writer.writerow([old_id, new_id])
        
        # Save the structure in PDB format
        pdb_io.set_structure(structure[0])
        pdb_io.save(pdb_file, select=FirstAltLocSelect())
#        print(f"Successfully converted {entry_id} to PDB format.")
    except Exception as e:
        print(f"Failed to convert {entry_id} to PDB format: {e}")

progress_bar = tqdm(total=len(entry_ids), desc="Converting", unit="structures")

# Convert each CIF file to PDB file
for entry_id in entry_ids:
    convert_cif_to_pdb(entry_id)
    progress_bar.update(1)


