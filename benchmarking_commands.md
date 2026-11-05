# Benchmarking Commands and Workflow

## Overview
This document contains the commands and code used to run and benchmark the four orthology inference tools evaluated in this project: SonicParanoid2, Proteinortho, OrthoFinder, and OrthoLoger.

The commands are organized by tool and task to make the benchmarking process reproducible. 

Before running the following commands make sure you are in the cloned benchmarking project directory:

```bash
cd benchmarking_project
```

## Dataset Download

The main benchmarking dataset was downloaded using `wget`

```bash
# Make a new directory within the benchmarking_project directory for the datasets
mkdir datasets

# Retrieve the dataset using wget from the orthology benchmarking service webpage
# The 2020_04 dataset was chosen because it allows comparisons with the most methods
nohup wget -P datasets https://ftp.ebi.ac.uk/pub/databases/reference_proteomes/previous_releases/qfo_release-2020_04/QfO_release_2020_04.tar.gz &
```

Extract contents of QfO_release_2020_04.tar.gz:

```bash
# Make a new directory within the datasets directory to extract the contents of the gzipped file
mkdir datasets/QfO_release_2020_04

# Extract the contents of the file into the new directory
tar -xzf path/to/benchmarking_project/datasets/QfO_release_2020_04.tar.gz -C QfO_release_2020_04
```

combine all the protein fasta files for the main benchmarking input

```bash
# Make a new directory within the datasets directory to store just the protein fasta files for input
mkdir QfO_release_2020_04_combined_all

# Copy all the fasta files into the new directory
cp QfO_release_2020_04/*/*.fasta QfO_release_2020_04_combined_all

# Remove DNA and protein isoform fasta files to keep just the protein fasta files
rm QfO_release_2020_04_combined_all/*_DNA.fasta 
rm QfO_release_2020_04_combined_all/*_additional.fasta
```

extract species for the subdatasets

```bash
# Make a new directory within the datasets directory for distant species
mkdir distant_species

# Make a new directory within the datasets directory for close species
mkdir close_species

# Copy the close species into one folder
cp QfO_release_2020_04/Eukaryota/UP000005640_9606.fasta QfO_release_2020_04/Eukaryota/UP000002277_9598.fasta QfO_release_2020_04/Eukaryota/UP000000589_10090.fasta QfO_release_2020_04/Eukaryota/UP000002494_10116.fasta QfO_release_2020_04/Eukaryota/UP000002254_9615.fasta QfO_release_2020_04/Eukaryota/UP000009136_9913.fasta close_species/

# Copy the distant species into one folder
cp QfO_release_2020_04/Eukaryota/UP000005640_9606.fasta QfO_release_2020_04/Eukaryota/UP000000437_7955.fasta QfO_release_2020_04/Eukaryota/UP000000803_7227.fasta QfO_release_2020_04/Eukaryota/UP000001940_6239.fasta QfO_release_2020_04/Eukaryota/UP000002311_559292.fasta QfO_release_2020_04/Eukaryota/UP000006548_3702.fasta distant_species/
```

## Orthofinder

```bash
# Activate the conda environment for OrthoFinder
conda activate of3_env

# Run OrthoFinder
nohup /usr/bin/time --verbose -o orthofinder_resource_usage.txt orthofinder -f datasets/QfO_release_2020_04_combined_all -o orthofinder_results &
```

## Proteinortho

```bash
# Activate the conda environment for Proteinortho
conda activate proteinortho_env

# Run Proteinortho
nohup /usr/bin/time --verbose -o proteinortho_resource_usage.txt perl proteinortho6.pl -project=proteinortho_main_benchmark datasets/QfO_release_2020_04_combined_all/*.fasta &
```

## SonicParanoid2

```bash
# Make a new directory within the datasets directory to have just fasta files for SonicParanoid2
# (it would not run if there were intermediate files left over in the input dataset directory from other tools
# so we had to create a clean directory to have just fasta files in it minus the intermediate files)
mkdir datasets/sonicparanoid_fasta_only
cp datasets/QfO_release_2020_04_combined_all/*.fasta datasets/sonicparanoid_fasta_only/

# Run SonicParanoid2
nohup /usr/bin/time --verbose -o sonicparanoid_resource_usage.txt pixi run -e sonicparanoid  sonicparanoid -i datasets/sonicparanoid_fasta_only -o sonicparanoid_results --project-id sonicparanoid_main_benchmark --graph-only &
```

## OrthoLoger

```bash
# Make a new directory within the benchmarking_project directory for the Orhtologer results
mkdir orthologer_results

# Initialize the orthologer environment and generate the baseline configuration files
pixi run -e orthologer bash -c '
export PATH="$CONDA_PREFIX/bin:$PATH"
export ODBAPI_URL_VERSION="v12-2"
cd /home/epolonsky/benchmarking_project/orthologer_results
orthologer -c create
'

# Copy the OrthoMapper configuration script and move into the results directory
cp orthologer_test_data/orthomapper_conf.sh orthologer_results/orthomapper_conf.sh
cd orthologer_results

# Import the Quest for Orthologs (QfO) benchmark dataset into orthologer
pixi run -e orthologer bash -c '
export PATH="$CONDA_PREFIX/bin:$PATH"
export ODBAPI_URL_VERSION="v12-2"
orthologer -c import -d /home/epolonsky/benchmarking_project/datasets/QfO_release_2020_04_combined_all -p orthologer_main_benchmark
'

# Run Orthologer
nohup /usr/bin/time --verbose -o orthologer_resource_usage.txt pixi run -e orthologer bash -c '
export PATH="$CONDA_PREFIX/bin:$PATH"
export ODBAPI_URL_VERSION="v12-2"
orthologer -c run -p orthologer_main_benchmark
' &
```
