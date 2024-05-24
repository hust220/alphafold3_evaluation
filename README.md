
# Download RNA IDs.

    python download_rna_id.py

Release date is later than 9/30/2021.
At least one RNA is included in the structure.

# Download the information about these RNAs.

    python download_rna_info.py

Information about the RNAs are saved in the `rna_info.json` file.

# Download RNA cif files.

    python download_cif.py

cif files rather than pdb file are downloaded because some RNAs have no pdb structure files.

# Extract structures with only RNA.

    python get_rna_only.py

Information about these RNA are saved in the `rna_only.csv` file.

# Convert cif files to pdb files.

    python cif2pdb.py rna_only.csv rna_only

Only the first model is retained.
Chain names are reset from A-Z and then a-z.
Residue numbers are reset from 1.

# Run MC-Annotate

    python annotate.py

# Convert MC-Annotate output to dot-bracket form

    python mc2db.py

# Compile the Dataset

First, collect all the secondary structure information.

    for i in $(cat in); do echo $i; cat rna_only/${i}.db; echo; done >rna_only.db

Next, compile the `rna_only.db` file by:

1. Remove helices like `(((((((())))))))`
2. Remove duplicates
3. Remove structures like `..........`

The compiled dataset for RNA-only prediction is the file `rna_only_compiled.db`.
