import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
#import necessary libraries

#get the names and locations of the input files
readme = Path("QFO_README.md")
fasta_dir = Path("datasets") / "QfO_release_2020_04_combined_all"
folder = Path("QfO_2020_04_benchmarking_service_files")

#store the relationship between proteome IDs and species names
proteome_species = {}

#open the QFO README file
with open(readme) as file:

    #read the file one line at a time
    for line in file:

        #only read lines containing proteome information
        if line.startswith("UP"):

            #split the line into columns
            parts = line.strip().split("\t")

            proteome_id = parts[0] 
            #get the proteome ID
            tax_id = parts[1] 
            #get the taxonomy ID

            #get the scientific name of the species
            species_name = " ".join(parts[-1].split()[:2])

            #store the proteome ID, taxonomy ID, and corresponding species name
            proteome_species[proteome_id + "_" + tax_id] = species_name

#store the relationship between protein accessions and species names
protein_species = {}

#go through all FASTA files in the dataset folder
for fasta in fasta_dir.glob("*.fasta"):

    #get the proteome ID from the FASTA filename
    proteome_id = fasta.stem

    #find the corresponding species name using the proteome ID
    species_name = proteome_species[proteome_id]

    #open the file
    with open(fasta) as file:

        #read the file one line at a time
        for line in file:

            #only read the protein header lines
            if line.startswith(">"):

                #remove the ">" symbol from the header
                header = line[1:].strip()

                #extract the UniProt accession from the protein ID
                accession = header.split("|")[1]

                #store the protein accession and its corresponding species
                protein_species[accession] = species_name


#print the total number of species and proteins identified
print("Species identified:", len(set(protein_species.values())))
print("Proteins mapped:", len(protein_species))

#get the names and locations of the four TSV prediction files
files = {
    "OrthoFinder":    folder / "orthofinder_QfO_2020_04.sorted.tsv",
    "Proteinortho":   folder / "proteinortho_QfO_2020_04.sorted.tsv",
    "SonicParanoid2": folder / "sonicparanoid_QfO_2020_04.sorted.tsv",
    "OrthoLoger":     folder / "orthologer_QfO_2020_04.sorted.tsv",
}

#get all the unique species names and sort them alphabetically
species = sorted(set(protein_species.values()))

#store the index assigned to each species
species_index = {}

#set the initial species index to 0
index = 0

#assign an index to each species
for name in species:
    species_index[name] = index
    index += 1 
    #move to the next index

#make one large plot to store the four heatmap subplots
plt.figure(figsize=(22, 22))

#start with the first subplot
number = 1

#read the TSV file for each method
for method in files:

    #make an empty matrix
    matrix = np.zeros((len(species), len(species)))

    #read the TSV file
    with open(files[method]) as file:

        #read the file one line at a time
        for line in file:

            #extract the two protein accessions from each line
            protein1, protein2 = line.strip().split("\t")

            #get the species that each protein belongs to
            species1 = protein_species[protein1]
            species2 = protein_species[protein2]

            #only add if the protein pairs are not the same
            if species1 != species2:

                #get the matrix position for each species
                i = species_index[species1]
                j = species_index[species2]

                #add one to the count for both species positions
                matrix[i, j] += 1
                matrix[j, i] += 1

    #draw the heatmap in the next subplot
    plt.subplot(2, 2, number)

    #display the matrix as a heatmap
    plt.imshow(matrix, cmap="viridis")

    #add the prediction method as the heatmap title
    plt.title(method)

    #add the species names to the axes
    plt.xticks(range(len(species)), species, rotation=90, fontsize=5)
    plt.yticks(range(len(species)), species, fontsize=5)

    #add labels to both axes
    plt.xlabel("Species")
    plt.ylabel("Species")

    #add a colorbar showing the number of ortholog pairs
    plt.colorbar(label="Number of ortholog pairs")

    #move to the next subplot
    number += 1

#save and show the heatmap
plt.tight_layout()
plt.savefig("species_comparison_heatmap.png",  dpi=300, bbox_inches="tight")
plt.show()

#the heatmap will visualize which pairs the tools had in common and which ones were unique for 
#each tool