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
mkdir datasets
#make a new directory within the benchmarking_project directory for the datasets

nohup wget -P datasets https://ftp.ebi.ac.uk/pub/databases/reference_proteomes/previous_releases/qfo_release-2020_04/QfO_release_2020_04.tar.gz &
#retrieves the dataset using wget from the orthology benchmarking service webpage
#the 2020_04 dataset was chosen because it allows comparisons with the most tools
```

Extract contents of QfO_release_2020_04.tar.gz

```bash
mkdir QfO_release_2020_04

cd QfO_release_2020_04

tar -xzf ~/benchmarking_project/datasets/QfO_release_2020_04.tar.gz -C .
```

combine all the protein fasta files for the main benchmarking input

```bash
mkdir QfO_release_2020_04_combined_all

cp QfO_release_2020_04/*/*.fasta QfO_release_2020_04_combined_all

rm QfO_release_2020_04_combined_all/*_DNA.fasta # remove DNA fasta files to keep just the protein fasta files
rm QfO_release_2020_04_combined_all/*_additional.fasta # remove protein isoform fasta files to keep just the protein fasta files
```

extract species for the subdatasets

```bash
mkdir distant_species
#makes a new directory within the datasets directory for distant species
mkdir close_species
#makes a new directory within the datasets directory for close species

# copy the close species into one folder
cp QfO_release_2020_04/Eukaryota/UP000005640_9606.fasta QfO_release_2020_04/Eukaryota/UP000002277_9598.fasta QfO_release_2020_04/Eukaryota/UP000000589_10090.fasta QfO_release_2020_04/Eukaryota/UP000002494_10116.fasta QfO_release_2020_04/Eukaryota/UP000002254_9615.fasta QfO_release_2020_04/Eukaryota/UP000009136_9913.fasta close_species/

# copy the distant species into one folder
cp QfO_release_2020_04/Eukaryota/UP000005640_9606.fasta QfO_release_2020_04/Eukaryota/UP000000437_7955.fasta QfO_release_2020_04/Eukaryota/UP000000803_7227.fasta QfO_release_2020_04/Eukaryota/UP000001940_6239.fasta QfO_release_2020_04/Eukaryota/UP000002311_559292.fasta QfO_release_2020_04/Eukaryota/UP000006548_3702.fasta distant_species/
```

## SonicParanoid2

```bash
mkdir datasets/sonicparanoid_fasta_only
cp datasets/QfO_release_2020_04_combined_all/*.fasta datasets/sonicparanoid_fasta_only/

nohup /usr/bin/time --verbose -o sonicparanoid_resource_usage.txt pixi run sonicparanoid -i datasets/sonicparanoid_fasta_only -o sonicparanoid_results --project-id sonicparanoid_main_benchmark --graph-only &
```

## Proteinortho

```bash
mkdir proteinortho_results
conda activate proteinortho_env

nohup /usr/bin/time --verbose -o proteinortho_resource_usage.txt perl proteinortho6.pl -project=proteinortho_main_benchmark datasets/QfO_release_2020_04_combined_all/*.fasta &

# move the files to the proteinortho results directory after run finished
mv proteinortho_main_benchmark.blast-graph proteinortho_results
mv proteinortho_main_benchmark.info proteinortho_results
mv proteinortho_main_benchmark.proteinortho-graph proteinortho_results
mv proteinortho_main_benchmark.proteinortho.tsv proteinortho_results
```

## Orthofinder

```bash
conda activate of3_env

nohup /usr/bin/time --verbose -o orthofinder_resource_usage.txt orthofinder -f datasets/QfO_release_2020_04_combined_all -o orthofinder_results &
```

## OrthoLoger

```bash
mkdir orthologer_results

pixi run bash -c '
export PATH="$CONDA_PREFIX/bin:$PATH"
export ODBAPI_URL_VERSION="v12-2"
cd /home/epolonsky/benchmarking_project/orthologer_results
orthologer -c create
'

cp orthologer_test_data/orthomapper_conf.sh orthologer_results/orthomapper_conf.sh
cd orthologer_results

pixi run bash -c '
export PATH="$CONDA_PREFIX/bin:$PATH"
export ODBAPI_URL_VERSION="v12-2"
orthologer -c import -d /home/epolonsky/benchmarking_project/datasets/QfO_release_2020_04_combined_all -p orthologer_main_benchmark
'

nohup /usr/bin/time --verbose -o orthologer_resource_usage.txt pixi run bash -c '
export PATH="$CONDA_PREFIX/bin:$PATH"
export ODBAPI_URL_VERSION="v12-2"
orthologer -c run -p orthologer_main_benchmark
' &
```
