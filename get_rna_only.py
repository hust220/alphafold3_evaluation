import json
import csv

# Load the JSON data from the file
with open("rna_info.json", "r") as file:
    data = json.load(file)

# Filter entries based on the specified conditions
filtered_entries = []
for entry in data["data"]["entries"]:
    entry_info = entry["rcsb_entry_info"]
    if (entry_info["polymer_entity_count_DNA"] == 0 and
        entry_info["polymer_entity_count_nucleic_acid_hybrid"] == 0 and
        entry_info["polymer_entity_count_protein"] == 0 and
        entry_info["polymer_entity_count_RNA"] > 0):
        filtered_entries.append(entry)

# Define the CSV file headers
headers = [
    "entry_id",
    "deposited_model_count",
    "polymer_entity_count_RNA",
    "resolution_combined",
    "chains",
    "sequence"
]

# Save the filtered results to a CSV file
with open("rna_only.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for entry in filtered_entries:
        entry_info = entry["rcsb_entry_info"]
        entities = entry["polymer_entities"]
        sequence = []
        chains = []
        for entity in entities:
            instances = entity["polymer_entity_instances"]
            seq1 = entity["entity_poly"]["pdbx_seq_one_letter_code_can"]
            n = len(instances)
            sequence.append(' '.join(seq1 for i in range(n)))
            chains.append(' '.join(instance["rcsb_polymer_entity_instance_container_identifiers"]["auth_asym_id"] for instance in instances))

        row = {
            "entry_id": entry["rcsb_entry_container_identifiers"]["entry_id"],
            "deposited_model_count": entry_info["deposited_model_count"],
            "polymer_entity_count_RNA": entry_info["polymer_entity_count_RNA"],
            "resolution_combined": entry_info["resolution_combined"][0] if entry_info["resolution_combined"] else None,
            "chains": ' '.join(chains),
            "sequence": ' '.join(sequence)
        }
        writer.writerow(row)

print("Filtered data has been saved to rna_only.csv")

