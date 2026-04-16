"""
============================================================
NCBI Sequence Fetcher for Phylogenetic Pipeline
============================================================

Description:
This script retrieves nucleotide sequences from NCBI based on
a user-defined organism (genus/species) and gene name.
It ensures:
- No duplicate sequences
- One representative sequence per species
- Phylogeny-safe sequence identifiers

Output:
FASTA file with unique species sequences, ready for pipeline use.

Requirements:
- Biopython
- Internet connection (NCBI Entrez access)

============================================================
"""

from Bio import Entrez, SeqIO
from io import StringIO
import time
import re

# ------------------------------------------------------------
# User Input
# ------------------------------------------------------------

Entrez.email = input("Enter your email address: ").strip()

main_species = input("Enter main genus/species name: ").strip()
gene_name = input("Enter gene name: ").strip()
target_species_count = int(input("How many DISTINCT species do you want?: ").strip())

# Construct NCBI query
query = f'{main_species}[Organism] AND {gene_name}[Gene]'

# ------------------------------------------------------------
# Data Structures
# ------------------------------------------------------------

species_dict = {}          # Stores best sequence per species
unique_sequences = set()   # Avoid duplicate sequences

batch_size = 200
retstart = 0

print("\n🔍 Collecting distinct species...\n")

# ------------------------------------------------------------
# Fetch sequences from NCBI
# ------------------------------------------------------------

while len(species_dict) < target_species_count:

    # Search NCBI
    handle = Entrez.esearch(
        db="nucleotide",
        term=query,
        retstart=retstart,
        retmax=batch_size
    )
    record = Entrez.read(handle)
    handle.close()

    ids = record.get("IdList", [])
    if not ids:
        break

    # Fetch sequences in FASTA format
    fetch_handle = Entrez.efetch(
        db="nucleotide",
        id=",".join(ids),
        rettype="fasta",
        retmode="text"
    )

    fasta_data = fetch_handle.read()
    fetch_handle.close()

    records = list(SeqIO.parse(StringIO(fasta_data), "fasta"))

    for rec in records:
        if len(species_dict) >= target_species_count:
            break

        sequence = str(rec.seq)

        # Skip duplicate sequences
        if sequence in unique_sequences:
            continue
        unique_sequences.add(sequence)

        # Extract species name (Genus + species)
        words = rec.description.split()
        if len(words) < 2:
            continue

        if words[0][0].isupper():
            genus = words[0]
            species = words[1]
        else:
            continue

        species_name = f"{genus}_{species}"

        # Clean ID (phylogeny-safe)
        species_name = re.sub(r'[^A-Za-z0-9_]', '', species_name)

        # Keep longest sequence if duplicate species found
        if species_name not in species_dict:
            species_dict[species_name] = rec
        else:
            if len(rec.seq) > len(species_dict[species_name].seq):
                species_dict[species_name] = rec

    retstart += batch_size
    time.sleep(0.4)  # Respect NCBI rate limits

# ------------------------------------------------------------
# Output results
# ------------------------------------------------------------

print(f"\n✅ Collected {len(species_dict)} distinct species.")

if len(species_dict) < target_species_count:
    print("⚠ Warning: Fewer species found than requested.")

output_file = f"{main_species}_{gene_name}_{len(species_dict)}species_phyloSafe.fasta"

with open(output_file, "w") as f:
    for i, (species, rec) in enumerate(list(species_dict.items())[:target_species_count], 1):
        safe_id = f"{species}_{i}"  # Ensure unique IDs
        f.write(f">{safe_id}\n")
        f.write(str(rec.seq) + "\n")

print(f"\n🎉 Saved to: {output_file}")
print("✔ Output is phylogeny-safe (no duplicate IDs).")