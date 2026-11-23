
from pathlib import Path
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_contents
#import necessary libraries


#get the location of the directory containing the 4 TSV prediction files
folder = Path("QfO_2020_04_benchmarking_service_files")

#get the names and locations of the 4 TSV prediction files
files = {
    "OrthoFinder": folder / "orthofinder_QfO_2020_04.sorted.tsv",
    "Proteinortho": folder / "proteinortho_QfO_2020_04.sorted.tsv",
    "SonicParanoid2": folder / "sonicparanoid_QfO_2020_04.sorted.tsv",
    "OrthoLoger": folder / "orthologer_QfO_2020_04.sorted.tsv"
}

#store the protein pairs from each method
predictions = {}
#creates an empty list to store the pairs in

#read each prediction file
for method, filename in files.items():

    #stores all unique protein pairs for the current method within a set
    protein_pairs = set()

     #open the file
    with open(filename) as file:

        #read the file one line at a time
        for line in file:

            
            #extract the two protein accessions from each line
            protein1, protein2 = line.strip().split("\t")

             #sort the accessions so that the same protein pair is always stored in the same order
            pair = tuple(sorted([protein1, protein2]))

            #add the protein pair to the set
            protein_pairs.add(pair)

    #store all protein pairs for the current method
    predictions[method] = protein_pairs

#print the total number of unique protein pairs predicted by each method
for method, pairs in predictions.items():
    print(method, len(pairs))

#convert the prediction sets into the format required for the upset plot
data = from_contents(predictions)

#cake one large plot to store the upset plot
plt.figure(figsize=(14, 8))

#create the upset plot 
upset = UpSet(
    data,
    subset_size="count",
    show_counts=False,
    sort_by="cardinality",
    sort_categories_by="input",
    facecolor="cornflowerblue"
)

#draw the plot
upset.plot()

#add a title to the figure
plt.suptitle(
    "Shared and Unique Orthologous Protein Pairs Across Four Methods",
    fontsize=14
)

#save and show the UpSet plot
plt.savefig(
    "upset_plot.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()
#the upset plot will show the intersections of the pairs from the 4 tools
#this will visualize what pairs the tools found in common