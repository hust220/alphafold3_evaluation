import requests
import json
from tqdm import tqdm

# Function to perform a GraphQL query
def perform_query(entry_ids):
    query = """
    {
      entries(entry_ids: ["{ids}"]) {
        rcsb_id
        rcsb_accession_info {
          initial_release_date
        }
        rcsb_entry_container_identifiers {
          entry_id
        }
        rcsb_entry_info {
          deposited_model_count
          deposited_polymer_entity_instance_count
          deposited_polymer_monomer_count
          polymer_entity_count_DNA
          polymer_entity_count_nucleic_acid_hybrid
          polymer_entity_count_protein
          polymer_entity_count_RNA
          resolution_combined
        }
        polymer_entities {
          entity_poly {
            pdbx_seq_one_letter_code_can
            rcsb_entity_polymer_type
            rcsb_sample_sequence_length
          }
          polymer_entity_instances {
            rcsb_polymer_entity_instance_container_identifiers {
              auth_asym_id
            }
          }
          rcsb_polymer_entity_container_identifiers {
            entity_id
          }
        }
      }
    }
    """.replace("{ids}", '","'.join(entry_ids))

    url = "https://data.rcsb.org/graphql"
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps({"query": query}))

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Query failed with status code {response.status_code}")
        print(response.text)
        return None

# Read entry IDs from the file "rna.ls"
with open("rna.ls", "r") as file:
    entry_ids = [line.strip() for line in file.readlines()]

# Split the IDs into batches of 50
batch_size = 50
batches = [entry_ids[i:i + batch_size] for i in range(0, len(entry_ids), batch_size)]

# Perform queries for each batch and collect results
all_results = []
for batch in tqdm(batches, desc="Processing batches"):
    result = perform_query(batch)
    if result:
        all_results.append(result)

# Combine all results
combined_results = {
    "data": {
        "entries": []
    }
}
for result in all_results:
    combined_results["data"]["entries"].extend(result["data"]["entries"])

# Save the combined results to a JSON file
with open("rna_info.json", "w") as file:
    json.dump(combined_results, file, indent=4)

print("Data has been saved to rna_info.json")

