# benchmarking_project

# Project Overview

This project aims to benchmark four orthology prediction tools to investigate their accuracy, computational performance, and the effect of evolutionary distance on ortholog prediction.

The four tools benchmarked are:

| Tool | Version | Execution Method | Source |
|------|---------|------------------|--------|
| SonicParanoid2 | 2.0.9 | Pixi environment (pixi) | [SonicParanoid2 GitLab](https://gitlab.com/salvo981/sonicparanoid2) |
| Proteinortho   | 6.3.6  | Conda environment (proteinortho_env) | [Proteinortho GitLab](https://gitlab.com/paulklemm_PHD/proteinortho/-/tree/master?ref_type=heads)   |
| OrthoFinder    | 2.5.5 | Conda environment (of3_env) | [OrthoFinder GitHub](https://orthofinder.github.io/OrthoFinder/) |
| OrthoLoger     | 3.9.1 | Pixi environment (pixi) | [OrthoLoger WebPage](https://orthologer.ezlab.org/) |


The tools will be evaluated using  reference datasets from closely related and distantly related species. We will also investigate whether dataset size affects tool performance.

## Research Questions

Our project will address three main questions:

1. **Accuracy:** Which tool most accurately identifies orthologous genes?
2. **Efficiency:** Which tool has the shortest runtime and lowest memory usage?
3. **Evolutionary distance:** Does evolutionary distance between species affect the accuracy of orthology predictions?

## Background

Orthologs are genes in different species that evolved from a common ancestral gene. Orthologous genes often retain similar biological functions, making them useful for transferring functional annotations between species and studying evolutionary relationships.

Computational tools identify orthologs using different combinations of sequence similarity searches, reciprocal best-hit approaches, graph clustering, and phylogenetic analysis. Because these methods differ, they may produce different orthology predictions and computational requirements.

# Tool Installation

## Perequisites

Before running the benchmark, complete the following steps:

- Clone the project repository.
- Install Pixi, for the SonicParanoid2 and OrthoLoger environments.
- Install Conda, for the Proteinortho and OrthoFinder environments.
- The software dependencies required by each tool.

Clone the repository and enter the project directory:

git clone <https://github.com/epolonsky/benchmarking_project>

cd benchmarking_project


## Pixi

Pixi version 0.81.0 was used to install Sonicparanoid2 and OrthoLoger.

Install Pixi using the [official installation instructions](https://pixi.prefix.dev/latest/installation/).

Verify the Pixi installation:

```bash
pixi --version
```

## Sonicparanoid2

Sonicparanoid2 was installed using pixi.

```bash
pixi install -e sonicparanoid
```

Verify the installation:

```bash
pixi run -e sonicparanoid sonicparanoid --help 
```

We used the --graph-only flag because the mmseqs2 functionality required AVX2 support, while the server only supported AVX1. Therefore, we did not use the mmseqs2 functionality.

Run on test data:

The test data was obtained from SonicParanoid using the `sonicparanoid-get-test-data` command.

```bash
# Retrieve the test data from SonicParanoid
pixi run -e sonicparanoid sonicparanoid-get-test-data -o sonicparanoid_test_data

# Run SonicParanoid on the test data
pixi run -e sonicparanoid sonicparanoid -i ./sonicparanoid_test_data/sonicparanoid_test/test_input -o ./sonicparanoid_test_data/sonicparanoid_test/test_output --project-id my_first_run --graph-only
```

### Expected output:

SonicParanoid2 ouputs its results into the output directory specified in the run command. The results directory contains three subdirectories.

These include:
- **alignments:** Contains intermediate sequence alignment files generated during the protein comparison step.
- **orthologs_db:** Contains pairwise ortholog tables stored in a database structure. These tables can be reused during subsequent or updated runs.
- **runs**: Contains results organized by individual analysis runs. Each run has its own directory containing run information, pairwise ortholog relationships, and multi-species ortholog groups.

The results directory contains two additional files:

- **last_run_info.txt:** Records details about the most recent SonicParanoid2 run, including the run ID, input and output directories, number of input proteomes, analysis settings, alignment tool and parameters, memory and thread settings, and software environment information.
- **snapshot.tsv:** Records information about each input proteome used in the analysis. The file includes a numerical identifier, species name, number of protein sequences, and total number of amino acids. This information helps identify and track the input proteomes used across analyses.

problem we were having before:
[Forum About Error](https://gitlab.com/salvo981/sonicparanoid2/-/work_items/54)

## OrthoFinder

OrthoFinder was installed through a Conda environment.

```bash
conda env create -f orthofinder.yaml
```

Run on test data:

Test data for OrthoFinder was obtain from the OrthoFinder GitHub page.

```bash
# Activate the Conda environment for OrthoFinder
conda activate of3_env

# Run OrthoFinder on the test data
orthofinder -f orthofinder_test_data/
```

### Expected output:

OrthoFinder ouputs its results into a dirctory called `Resuts_Date`, with the "Date"  being the date the analysis was run. This results directory contains 13 subdirectories that organize the output files according to their purpose. 

These include:

- **Comparative_Genomics_Statistics:** Contains statistical summaries of orthogroups, ortholog relationships, gene duplications, and species overlaps.
- **Gene_Duplication_Events:** Contains information about inferred gene duplication events.
- **Gene_Trees:** Contains inferred gene trees for orthogroups.
- **Orthogroup_Sequences:** Contains FASTA files with the protein sequences assigned to each orthogroup.
- **Orthologues:** Contains files describing orthologous relationships between genes from different species.
- **Phylogenetic_Hierarchical_Orthogroups:** Contains hierarchical orthogroups (HOGs) inferred at different levels of the species tree.
- **Phylogenetically_Misplaced_Genes:** Contains genes identified as potentially misplaced within their gene trees.
- **Putarive_Xenologs:** Contains genes identified as potential xenologs, which may have originated through horizontal gene transfer.
- **Resolved_Gene_Trees:** Contains rooted and resolved gene trees for orthogroups.
- **Single_Copy_Orthologue_Sequences:** Contains FASTA files of sequences belonging to single-copy orthogroups.
- **Species_Tree:** Contains the inferred species phylogenetic tree and related files.
- **Working Directory:** Contains intermediate files generated during the OrthoFinder analysis.

The results directory contains two additional files:

- **Citation.txt:** Provides the citation information for OrthoFinder.
- **Log.txt:** Contains information about the analysis execution, including processing steps and progress messages.

For more detailed descriptions of the individual output files, refer to the [Official OrthoFinder Guide to Results](https://orthofinder.github.io/OrthoFinder/tutorials/guide-to-results/). 


## OrthoLoger
OrthoLoger was installed using pixi.
 
```bash
pixi install -e orthologer
```

Verify the installation:

```bash
pixi run -e orthologer orthologer -v
```

run on test data:

The test data for OrthoLoger is obtained through running the `run_test.sh` script within OrhtoLoger's installation.

```bash
# Run OrthoLoger with the test script
pixi run -e orthologer bash -c 'export PATH="$CONDA_PREFIX/bin:$PATH"; "$CONDA_PREFIX/ORTHOLOGER-3.9.1/test/run_test.sh" prot/main'
```

### Expected output:

OrthoLoger writes the test output to the following directory:

```bash
$CONDA_PREFIX/ORTHOLOGER-3.9.1/test/tests/prot/
```

The run log is stored in:

```bash
$CONDA_PREFIX/ORTHOLOGER-3.9.1/test/tests/prot/RunLogs/
```

The results directory contains 15 subdirectories.

These include:

- **bin:** Contains executable programs and utility scripts required by OrthoLoger.
- **busco:** Contains files associated with BUSCO, which is used to assess the completeness of genome or protein datasets.
- **Cluster:** Contains files related to the clustering of protein sequences into groups.
- **import:** Contains imported input data and files used during the data preparation stage.
- **JobLog:** Contains logs associated with individual computational jobs.
- **logs:** Contains general log files generated during execution.
- **orthologer_test:** Contains files and results associated with the OrthoLoger test pipeline.
- **PWC:** Contains files associated with pairwise comparisons.
- **Rawdata:** Contains the raw input data used for the analysis.
- **refs:** Contains reference files used during the analysis.
- **Results:** Contains the results generated by the OrthoLoger analysis.
- **RunLogs:** Contains execution logs documenting the analysis runs.
- **sbin:** Contains system-level executable scripts and utilities.
- **Sequences:** Contains protein sequence files used in the analysis.
- **todo:** Contains files associated with pending tasks or processing steps.

The results directory contains 14 additional files:
- **cleanup.sh:** Shell script used to remove temporary files and clean up the working directory.
- **orthologer_conf.sh:** Configuration file containing settings for the OrthoLoger pipeline.
- **ortholofer_conf.sh.bck_pipeline:** Backup configuration file associated with the pipeline.
- **orthologer.sh:** Main shell script used to execute the OrthoLoger pipeline.
- **orthomapper_conf.sh:** Configuration file containing settings for the OrthoMapper pipeline.
- **orthomapper.sh:** Shell script used to execute the OrthoMapper pipeline.
- **prot_main.txt:** Text file containing protein-related information or settings for the main test.
- **prot_short.txt:** Text file containing protein-related information or settings for the shorter test.
- **README:** Provides documentation and instructions related to the OrthoLoger test installation.
- **run_test0_main.sh:** Shell script used to execute the main test.
- **run_test0_short.sh:** Shell script used to execute the shorter test.
- **run_test1_localmap.sh:** Shell script used to execute the local mapping test.
- **setup.log:** Log file documenting the setup process.
- **setup.sh:** Shell script used to configure and prepare the test environment.

To copy the generated test data into your own project directory:

Run the following commands from the root directory of the cloned benchmarking project:

```bash
# make the OrthoLoger test data directory
mkdir orthologer_test_data

# Copy the OrthoLoger results into the OrthoLoger test data directory
cp -r $CONDA_PREFIX/ORTHOLOGER-3.9.1/test/tests/prot/* orthologer_test_data/
```

From the project root, you can check the location of the OrthoLoger test script with:

```bash
pixi run -e orthologer bash -c 'echo "$CONDA_PREFIX"; find "$CONDA_PREFIX" -type f -name run_test.sh'
```

## Proteinortho
Proteinortho was installed through a Conda environment.

```bash
conda env create -f proteinortho.yaml
```

run on test data:

Test data for Proteinortho was obtain from the Proteinortho GitLab page.

```bash
# activate the proteinortho Conda environment
conda activate proteinortho_env

# run the perl script on the test data
perl proteinortho6.pl -project=proteinortho_test_data proteinortho_test_data/C.faa proteinortho_test_data/E.faa proteinortho_test_data/L.faa proteinortho_test_data/M.faa
```

The Proteinortho command assumes that proteinortho6.pl is available from the current directory, otherwise it can be downloaded into the directory from the Proteinortho GitLab page.

### Expected output:

Proteinortho outputs its results into the directory you run it from. The results contain six files. The -project option identifies the project name used for the run and the prefix names for the output files.

These include:

- **proteinortho_test_data.blast-graph:** Contains pairwise sequence similarity results generated during the all-against-all comparison step, before ortholog clustering.
- **proteinortho_test_data.info:** Records information about the Proteinortho execution, including the date and time of the run, command used, software version, input FASTA files, and analysis parameters and settings.
- **proteinortho_test_data.proteinortho-graph:** Contains pairwise ortholog relationships retained after clustering. It represents the connections between genes assigned to orthologous groups.
- **proteinortho_test_data.proteinortho-graph.summary:** Provides summary statistics for the orthology graph, including the number of groups containing different proportions of the input species and the number of groups associated with each species.
- **proteinortho_test_data.proteinortho.html:** Provides an HTML version of the orthologous group results that can be viewed in a web browser.
- **proteinortho_test_data.proteinortho.tsv:** Contains the predicted orthologous groups in tab-separated format, including the number of species and genes in each group and the gene identifiers assigned to each species.


# Data Selection

The data for this project is selected from the European Bioinformatics Institute (EBI) Quest for Orthologs (QfO) reference proteome collection. The collection of datasets can be found using the link below.

[QfO previous reference proteome releases](https://ftp.ebi.ac.uk/pub/databases/reference_proteomes/previous_releases/)

The dataset we are using: 

[QfO release 2020_04](https://ftp.ebi.ac.uk/pub/databases/reference_proteomes/previous_releases/qfo_release-2020_04/)

Reference proteomes provide protein sequences for different species and can be used as input for orthology inference tools. This dataset was chosen because it is compatible with the most tools, allowing for a more seamless process. 

## Dataset Categories

The types of datasets used in this project:

| Dataset | Species | Purpose |
|---------|---------|---------|
| Full | All 78 QfO species | Main benchmark |
| Close | 6 related species | Closely related species |
| Distant | 6 distant species | More distantly related species |

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
