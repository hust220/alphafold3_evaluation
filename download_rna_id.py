import requests
import os

# Define the search query
search_url = "https://search.rcsb.org/rcsbsearch/v2/query?json="
query = {
    "query":{
        "type":"group",
        "logical_operator":"and",
        "nodes":[
            {
                "type":"terminal",
                "service":"text",
                "parameters":{
                    "attribute":"rcsb_accession_info.initial_release_date",
                    "operator":"greater",
                    "negation":False,
                    "value":"2021-09-30"
                }
            },
            {
                "type":"terminal",
                "service":"text",
                "parameters":{
                    "attribute":"rcsb_entry_info.polymer_entity_count_RNA",
                    "operator":"greater_or_equal",
                    "negation":False,
                    "value":1
                }
            }
        ],
        "label":"text"
    },
    "return_type":"entry",
    "request_options":{
        "paginate":{
            "start":0,
            "rows":10000
        },
        "results_content_type":[
            "experimental"
        ],
        "sort":[
            {
                "sort_by":"score","direction":"desc"
            }
        ],
        "scoring_strategy":"combined"
    }
}
# Convert query to JSON string
import json
query_json = json.dumps(query)

# Send the request to the RCSB PDB API
response = requests.get(search_url + query_json)
response.raise_for_status()  # Raise an error if the request fails

# Parse the response to get a list of PDB IDs
pdb_ids = [entry["identifier"] for entry in response.json()["result_set"]]

# Define a function to download a PDB file
def download_pdb(pdb_id):
    pdb_url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(pdb_url)
    if response.status_code == 200:
        with open(f"{pdb_id}.pdb", "wb") as file:
            file.write(response.content)
        print(f"Downloaded {pdb_id}.pdb")
    else:
        print(f"Failed to download {pdb_id}.pdb")

# Create a directory to save the PDB files
#os.makedirs("pdb_files", exist_ok=True)
#os.chdir("pdb_files")

# Download all the PDB files
f = open('rna.ls', 'w+')
for pdb_id in pdb_ids:
#    download_pdb(pdb_id)
    f.write(f'{pdb_id}\n')
#    print(pdb_id)
f.close()

print("Download completed.")

