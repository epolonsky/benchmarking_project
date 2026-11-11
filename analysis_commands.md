## Sort the tsv files for comparison

```bash
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv
```

## Number of ortholog pairs

```bash
wc -l QfO_2020_04_benchmarking_service_files/*.tsv
```

## Pairwise overlap

```bash
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv | wc -l
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv | wc -l
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv | wc -l
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv | wc -l
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv | wc -l
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv | wc -l
LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv | wc -l
```

## Number of ortholog pairs

```bash
wc -l QfO_2020_04_benchmarking_service_files/*.tsv
```

## Shared ortholog pairs
```bash
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv
LC_ALL=C sort -u QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.tsv -o QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv
LC_ALL=C comm -12 <(LC_ALL=C comm -12 <(LC_ALL=C comm -12 QfO_2020_04_benchmarking_service_files/proteinortho_QfO_2020_04.sorted.tsv QfO_2020_04_benchmarking_service_files/orthofinder_QfO_2020_04.sorted.tsv) QfO_2020_04_benchmarking_service_files/sonicparanoid_QfO_2020_04.sorted.tsv) QfO_2020_04_benchmarking_service_files/orthologer_QfO_2020_04.sorted.tsv | wc -l
```

## Percent similarity

```bash
awk 'BEGIN {
print "Proteinortho - OrthoFinder:", 100*3935148/(4575714+11207043-3935148), "%"
print "Proteinortho - SonicParanoid:", 100*4295812/(4575714+11771331-4295812), "%"
print "Proteinortho - OrthoLoger:", 100*3467065/(4575714+9420835-3467065), "%"
print "OrthoFinder - SonicParanoid:", 100*6686606/(11207043+11771331-6686606), "%"
print "OrthoFinder - OrthoLoger:", 100*5154892/(11207043+9420835-5154892), "%"
print "SonicParanoid - OrthoLoger:", 100*5673331/(11771331+9420835-5673331), "%"
}'
```

