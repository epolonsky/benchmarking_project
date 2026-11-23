import matplotlib.pyplot as plt
from pathlib import Path
#import necessary libraries


#store the relationship between proteome IDs and species names
proteome_species = {}

#open the QFO README file
with open("QFO_README.md") as file:

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
            species_name = parts[-1] 
            #get the full species name

            #store the proteome ID, taxonomy ID, and corresponding species name
            proteome_species[proteome_id + "_" + tax_id] = species_name

#store the relationship between protein accessions and species names
protein_species = {}

#go through all FASTA files in the dataset folder
fasta_folder = Path("datasets/QfO_release_2020_04_combined_all")
for fasta in fasta_folder.glob("*.fasta"):

    proteome_id = fasta.stem
     #get the proteome ID from the FASTA filename

    species_name = proteome_species[proteome_id]
    #find the corresponding species name using the proteome ID

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

#get the names and locations of the four TSV prediction files
files = {
    "OrthoFinder": "/home/epolonsky/benchmarking_project/QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv",

    "Proteinortho": "/home/epolonsky/benchmarking_project/QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv",

    "SonicParanoid2": "/home/epolonsky/benchmarking_project/QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv",

    "Orthologer": "/home/epolonsky/benchmarking_project/QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv"
}

#store the predicted protein pairs for each method and species comparison
predictions = {}

#read the TSV file for each method
for method in files:

    #store the protein pairs for each species comparison
    species_pairs = {}

    #open the TSV file
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

                #sort the species names and protein assession numbers so the comparison is stored consistently
                species_pair = tuple(sorted([species1, species2]))
                protein_pair = tuple(sorted([protein1, protein2]))

                #create an empty set for the species comparison if it does not exist yet
                if species_pair not in species_pairs:
                    species_pairs[species_pair] = set()

                #add the protein pair to the corresponding species comparison
                species_pairs[species_pair].add(protein_pair)

    #store all the species comparisons for the current method
    predictions[method] = species_pairs

jaccard_values = [] 
#store the Jaccard similarity values for each method comparison
labels = [] 
#store the labels for each method comparison

#get the names of the four prediction methods
methods = list(files.keys())

#compare each method with every method that comes after it
for i in range(len(methods)):

    for j in range(i + 1, len(methods)):

        method1 = methods[i] 
        #get the first method
        method2 = methods[j] 
        #get the second method
 
        values = [] 
        #store the Jaccard values for the current method comparison

        #get all the species comparisons found by either method
        all_species_pairs = set(predictions[method1]) | set(predictions[method2])

        #calculate the Jaccard similarity for each species comparison
        for species_pair in all_species_pairs:

            #get the predicted protein pairs from each method
            pairs1 = predictions[method1].get(species_pair, set())
            pairs2 = predictions[method2].get(species_pair, set())

            #find the protein pairs shared by both methods
            shared = pairs1 & pairs2

            #find all the unique protein pairs predicted by either method
            total = pairs1 | pairs2

            #only calculate the Jaccard similarity if at least one method predicted pairs
            if len(total) > 0:

                #calculate the proportion of shared pairs between the two methods
                jaccard = len(shared) / len(total)

                values.append(jaccard)

        #store the Jaccard values for the current method comparison
        jaccard_values.append(values)

        #create a label showing which two methods are being compared
        labels.append(method1 + "\nvs\n" + method2)

        #print out the number of species comparisons included
        print(method1, "vs", method2, ":", len(values), "comparisons")

#make one large plot to store the boxplots
plt.figure(figsize=(12, 6))

#draw a boxplot
plt.boxplot(
    jaccard_values,
    patch_artist=True,
    showfliers=True,

    boxprops=dict(facecolor="lightblue", color="black"),
    medianprops=dict(color="black", linewidth=1.5),
    whiskerprops=dict(color="black"),
    capprops=dict(color="black"),
    flierprops=dict(
        marker="o",
        markerfacecolor="black",
        markeredgecolor="black",
        markersize=3
    )
)

#add the method comparison labels to the x-axis
plt.xticks(range(1, 7), labels, fontsize=9)

#add labels to the x and y axes
plt.ylabel("Jaccard similarity")
plt.xlabel("Tool comparison")

#add a title to the boxplot
plt.title("Distribution of pairwise Jaccard similarity across species comparisons")

#set the y-axis range between zero and one
plt.ylim(0, 1)

#save and show the boxplot
plt.tight_layout()
plt.savefig("jaccard_boxplot.png", dpi=300, bbox_inches="tight")
plt.show()

#the jaccard boxplot provides another visualization of the commonalities between pairs produced
#by the 4 tools 