# benchmarking_project

# Project Overview

This project aims to benchmark four orthology prediction tools to investigate their accuracy, computational performance, and the effect of evolutionary distance on ortholog prediction.

The four tools benchmarked are:

| Tool | Version | Execution Method | Source |
|------|---------|------------------|--------|
| SonicParanoid2 | 2.0.9 | Pixi environment (pixi) | https://gitlab.com/salvo981/sonicparanoid2 |
| Proteinortho   | 6.3.6  | Conda environment (proteinortho_env) | https://gitlab.com/paulklemm_PHD/proteinortho/-/tree/master?ref_type=heads   |
| OrthoFinder    | 2.5.5 | Conda environment (of3_env) | https://orthofinder.github.io/OrthoFinder/ |
| OrthoLoger     | 3.9.1 | Pixi environment (pixi) | https://orthologer.ezlab.org/ |


The tools will be evaluated using protein reference datasets from closely related and distantly related species. We will also investigate whether dataset size affects tool performance.

## Research Questions

Our project will address three main questions:

1. **Accuracy:** Which tool most accurately identifies orthologous genes?
2. **Efficiency:** Which tool has the shortest runtime and lowest memory usage?
3. **Evolutionary distance:** Does evolutionary distance between species affect the accuracy of orthology predictions?

## Background

Orthologs are genes in different species that evolved from a common ancestral gene. Orthologous genes often retain similar biological functions, making them useful for transferring functional annotations between species and studying evolutionary relationships.

Computational tools identify orthologs using different combinations of sequence similarity searches, reciprocal best-hit approaches, graph clustering, and phylogenetic analysis. Because these methods differ, they may produce different orthology predictions and computational requirements.

# Tool Installation

## Pixi

Pixi was used to install Sonicparanoid2 and OrthoLoger

The Pixi version used was 0.81.0

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Install Pixi
wget -qO- https://pixi.sh/install.sh | sh

# Reload Bash configuration
source ~/.bashrc

# Verify Pixi installation
pixi --version

# Go into the benchmarking project directory
cd ~/benchmarking_project

# Initialize Pixi project
pixi init

# Add package channels to the Pixi project
pixi workspace channel add conda-forge
pixi workspace channel add bioconda
```


## Sonicparanoid2
https://gitlab.com/salvo981/sonicparanoid2
https://bioconda.github.io/recipes/sonicparanoid/README.html

Sonicparanoid2 was installed using pixi

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Add Python 3.10 to the Pixi project
pixi add python=3.10

# Install SonicParanoid
pixi add --pypi sonicparanoid
```

we did not use the mmsqs2 function of this tool as it was incompatible with the CPU on the server it required AVX2 and we only had AVX1. This was done using the --graph-only flag.
run on test data:

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Retrieve the test data from SonicParanoid
pixi run sonicparanoid-get-test-data -o sonicparanoid_test_data

# Go into the SonicParanoid test data directory
cd sonicparanoid_test_data/sonicparanoid_test/

# Run SonicParanoid on the test data
pixi run sonicparanoid -i ./test_input -o ./test_output --project-id my_first_run -t 4 --graph-only
```

problem we were having before (in case we want to try to fix it again)
https://gitlab.com/salvo981/sonicparanoid2/-/work_items/54

## OrthoFinder
https://orthofinder.github.io/OrthoFinder/

OrthoFinder was installed through a conda environment

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Create conda environment 
conda create -n of3_env python=3.12

# Activate the conda environment
conda activate of3_env

# Install OrthoFinder through conda
conda install -c conda-forge -c bioconda orthofinder

# Install numpy through conda
conda install numpy=1.26.4
```

run on test data:

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Activate the conda environment for OrthoFinder
conda activate of3_env

# Run OrthoFinder on the test data
orthofinder -f orthofinder_test_data/
```

## OrthoLoger
https://orthologer.ezlab.org/

https://bioconda.github.io/recipes/orthologer/README.html
 
OrthoLoger was installed using pixi
 
```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Add the right dependencies and install OrthoLoger
pixi add python=3.12 "numpy<2" "scipy<1.13" "orthologer=3.9.1"

# Install the requests Python library 
pixi add requests
```

run on test data:

change the paths below to match the location of your OrthoLoger installation and project directory

In the command below, replace:

- **`/home/epolonsky/benchmarking_project`** with the path to your own project directory
- **`.pixi/envs/default/ORTHOLOGER-3.9.1`** with the location of your OrthoLoger installation, if different

```bash
# Run OrthoLoger with the test script
pixi run bash -c 'export PATH="$CONDA_PREFIX/bin:$PATH"; /home/epolonsky/benchmarking_project/.pixi/envs/default/ORTHOLOGER-3.9.1/test/run_test.sh prot/main'
#if the same directory names have been used, all that would need to changed within the path above is the username
```


OrthoLoger writes the test output to the test installation directory:

```bash
/home/epolonsky/benchmarking_project/.pixi/envs/default/ORTHOLOGER-3.9.1/test/tests/prot/
#in the path above insert your own username and directory names to get to the test installation directory
```

The run log is stored in:

```bash
/home/epolonsky/benchmarking_project/.pixi/envs/default/ORTHOLOGER-3.9.1/test/tests/prot/RunLogs/
#replace with your username and directory names(if different than the ones above)
```

To copy the generated test data into the project directory:

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# make the orthologer test data directory
mkdir orthologer_test_data

# Copy the OrthoLoger results into the orthologer test data directory
cp -r /home/epolonsky/benchmarking_project/.pixi/envs/default/ORTHOLOGER-3.9.1/test/tests/prot/* orthologer_test_data/
#replace with your username and directory names(if different than the ones above)
```


## proteinortho
https://gitlab.com/paulklemm_PHD/proteinortho/-/tree/master?ref_type=heads

proteinortho was installed through a conda environment

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# Make environment and install proteinortho with conda
conda create -n proteinortho_env -c conda-forge -c bioconda python=3.7 proteinortho
```

run on test data:

```bash
# Go into the benchmarking project directory
cd ~/benchmarking_project

# activate the proteinortho conda environment
conda activate proteinortho_env

# run the perl script on the test data
perl proteinortho6.pl -project=proteinortho_test_data proteinortho_test_data/C.faa proteinortho_test_data/E.faa proteinortho_test_data/L.faa proteinortho_test_data/M.faa

# Make the proteinortho test data directory
mkdir proteinortho_test_data

# Move the output files into the proteinortho test data directory
mv ~/benchmarking_project/proteinortho_test_data/proteinortho_test_data.blast-graph
mv ~/benchmarking_project/proteinortho_test_data/proteinortho_test_data.info
mv ~/benchmarking_project/proteinortho_test_data/proteinortho_test_data.proteinortho-graph
mv ~/benchmarking_project/proteinortho_test_data/proteinortho_test_data.proteinortho-graph.summary
mv ~/benchmarking_project/proteinortho_test_data/proteinortho_test_data.proteinortho.html
mv ~/benchmarking_project/proteinortho_test_data/proteinortho_test_data.proteinortho.tsv
```

# Data Selection

The data for this project is selected from the European Bioinformatics Institute (EBI) Quest for Orthologs (QfO) reference proteome collection. The collection of datasets can be found using the link below.

**QfO reference proteome releases:** `https://ftp.ebi.ac.uk/pub/databases/reference_proteomes/previous_releases/`

The dataset we are using: 

**QfO release 2020_04:** `https://ftp.ebi.ac.uk/pub/databases/reference_proteomes/previous_releases/qfo_release-2020_04/`

Reference proteomes provide protein sequences for different species and can be used as input for orthology inference tools. This dataset was chosen because it is compatible with the most tools, allowing for a more seamless process. 

## Dataset Categories

The types of datasets used in this project:

| Dataset | Species | Purpose |
|---------|---------|---------|
| Full | All 78 QfO species | Main benchmark |
| Close | list species used | Closely related species |
| Distant | list species used | More distantly related species |

Species were selected based on their evolutionary relationships and the availability of suitable proteomes and reference orthology data.

## Species

| Proteome_ID | Species | Common Name | NCBI Taxonomy ID | Subset |
|-------------|---------|-------------|---|---|
| `UP000005640` | *Homo sapiens* | Human | 9606 | Close and distant |
| `UP000002277` | *Pan troglodytes* | Chimpanzee | 9598 | Close |
| `UP000000589` | *Mus musculus* | Mouse | 10090 | Close |
| `UP000002494` | *Rattus norvegicus* | Rat | 10116 | Close |
| `UP000002254` | *Canis lupus familiaris* | Dog | 9615 | Close |
| `UP000009136` | *Bos taurus* | Bovine | 9913 | Close |
| `UP000000437` | *Danio rerio* | Zebrafish | 7955 | Distant |
| `UP000000803` | *Drosophila melanogaster* | Fruit fly | 7227 | Distant |
| `UP000001940` | *Caenorhabditis elegans* | Roundworm | 6239 | Distant |
| `UP000002311` | *Saccharomyces cerevisiae* | Baker's yeast | 559292 | Distant |
| `UP000006548` | *Arabidopsis thaliana* | Mouse-ear cress | 3702 | Distant |

**Dataset summary:** The dataset contains 11 eukaryotic species. The close subset includes six mammalian species, and the distant subset includes six species representing diverse eukaryotic lineages. Human is shared between both subsets.

# Comparing the Tools

The tools are compare using the following measures:

| Category | Measurement |
|----------|-------------|
| Accuracy | Precision, recall, and F1 score |
| Runtime and Memory | *`/usr/bin/time —verbose`* |
| Agreement | Overlap and differences between predicted ortholog relationships |
| Evolutionary distance | Changes in accuracy between closely related and distantly related species |
| Dataset size | Changes in runtime, memory, and accuracy across dataset sizes |

# Code for project

All the code used for this project is in the `benchmarking_commands.md` file.
