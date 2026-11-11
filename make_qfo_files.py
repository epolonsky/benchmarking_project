from pathlib import Path


# Create the output folder
output = Path("QfO_2020_04_benchmarking_service_files")
output.mkdir(exist_ok=True)


# Convert full FASTA IDs into UniProt accessions
def get_accession(protein):
    parts = protein.split("|")

    if len(parts) == 3 and parts[0] in ["sp", "tr"]:
        return parts[1]

    return protein


# Save pairs into a new TSV file
def save_pairs(pairs, filename):
    with open(output / filename, "w") as f:
        for a, b in sorted(pairs):
            f.write(a + "\t" + b + "\n")

    print(filename, ":", len(pairs), "pairs")

# Proteinortho

pairs = set()

file = Path(
    "proteinortho_results/"
    "proteinortho_main_benchmark.proteinortho-graph"
)

with open(file) as f:
    for line in f:

        if not line.startswith("#") and line.strip():

            fields = line.split()

            if len(fields) >= 6:

                a = get_accession(fields[0])
                b = get_accession(fields[1])

                if a != b:
                    pairs.add(tuple(sorted((a, b))))


save_pairs(pairs, "proteinortho_QfO_2020_04.tsv")

# OrthoFinder

pairs = set()

folder = Path("orthofinder_results/Results_Oct18/Orthologues")

for file in folder.rglob("*.tsv"):

    if not file.parent.name.startswith("Orthologues_"):
        continue

    with open(file) as f:

        next(f, None)  # Skip the header

        for line in f:

            fields = line.strip().split("\t")

            if len(fields) < 3:
                continue

            proteins_a = fields[1].split(",")
            proteins_b = fields[2].split(",")

            for a in proteins_a:

                for b in proteins_b:

                    a = get_accession(a.strip())
                    b = get_accession(b.strip())

                    if a != b:
                        pairs.add(tuple(sorted((a, b))))


save_pairs(pairs, "orthofinder_QfO_2020_04.tsv")


# SonicParanoid2

pairs = set()
problems = []

folder = Path(
    "sonicparanoid_results/runs/"
    "sonicparanoid_main_benchmark/"
    "species_to_species_orthologs"
)

for file in folder.rglob("*.fasta"):

    if not file.is_file():
        continue

    with open(file) as f:

        for line in f:

            if line.startswith("Size") or not line.strip():
                continue

            fields = line.strip().split("\t")

            if len(fields) != 4:
                problems.append(str(file))
                continue

            proteins_a = fields[2].split()
            proteins_b = fields[3].split()

            if len(proteins_a) % 2 != 0 or len(proteins_b) % 2 != 0:
                problems.append(str(file))
                continue

            proteins_a = [
                get_accession(proteins_a[i])
                for i in range(0, len(proteins_a), 2)
            ]

            proteins_b = [
                get_accession(proteins_b[i])
                for i in range(0, len(proteins_b), 2)
            ]

            if int(fields[0]) != len(proteins_a) + len(proteins_b):
                problems.append(str(file))
                continue

            if int(fields[1]) != len(proteins_a) * len(proteins_b):
                problems.append(str(file))
                continue

            for a in proteins_a:

                for b in proteins_b:

                    if a != b:
                        pairs.add(tuple(sorted((a, b))))


if problems:

    print("SonicParanoid needs checking. No file created.")
    print("Problem files:", len(set(problems)))

else:

    save_pairs(pairs, "sonicparanoid_QfO_2020_04.tsv")

# OrthoLoger

pairs = set()

# Create internal ID to UniProt mapping

id_to_accession = {}

folder = Path("orthologer_results/Rawdata")

for file in folder.glob("*.fs.maptxt"):

    with open(file) as f:

        for line in f:

            fields = line.strip().split()

            if len(fields) >= 2:

                internal_id = fields[0]
                protein = fields[1]

                accession = get_accession(protein)

                id_to_accession[internal_id] = accession


print("Orthologer proteins mapped:", len(id_to_accession))



# Read the BRH files


folder = Path("orthologer_results/PWC")

missing_ids = 0

for file in folder.rglob("*.brh"):

    with open(file) as f:

        for line in f:

            if line.startswith("#") or not line.strip():
                continue

            fields = line.split()

            if len(fields) < 2:
                continue

            a = id_to_accession.get(fields[0])
            b = id_to_accession.get(fields[1])

            if a is None or b is None:

                missing_ids += 1
                continue

            if a != b:
                pairs.add(tuple(sorted((a, b))))


# Read the INPAR files

for file in folder.rglob("*.inpar"):

    with open(file) as f:

        for line in f:

            if line.startswith("#") or not line.strip():
                continue

            fields = line.split()

            if len(fields) < 2:
                continue

            # The first two proteins are the seed pair
            seed_a = fields[0]
            seed_b = fields[1]

            species_a = seed_a.split(":")[0]
            species_b = seed_b.split(":")[0]

            group_a = {seed_a}
            group_b = {seed_b}

            # Read additional in-paralogs
            for field in fields[3:]:

                internal_id = field.split(";")[0]

                if internal_id.startswith(species_a + ":"):

                    group_a.add(internal_id)

                elif internal_id.startswith(species_b + ":"):

                    group_b.add(internal_id)

            # Create pairs between the two groups
            for protein_a in group_a:

                for protein_b in group_b:

                    a = id_to_accession.get(protein_a)
                    b = id_to_accession.get(protein_b)

                    if a is None or b is None:

                        missing_ids += 1
                        continue

                    if a != b:
                        pairs.add(tuple(sorted((a, b))))


# D. Save Orthologer results

print("Orthologer missing ID mappings:", missing_ids)

if missing_ids == 0:

    save_pairs(pairs, "orthologer_QfO_2020_04.tsv")

else:

    print("Orthologer file was NOT created.")
    print("Some protein IDs could not be mapped. Check the mapping files.")
