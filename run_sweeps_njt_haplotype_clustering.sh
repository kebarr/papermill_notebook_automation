#!/usr/bin/env bash
#
# Notes on the notebooks that shape these sweeps:
# - Ag3 and Af1 calls need different contigs (3L vs 3RL), so their region
#   sweeps are paired value-by-value with --zip rather than combined.


CFG="python papermill_csv_config.py --notebooks-dir notebooks_fixed_parameters_cells create"
OUT=${OUT:-runners_and_csvs_new}

NJT_AG3='cell_4_call_1_ag3_njt,cell_[5-9]_call_1_ag3_plot_njt,cell_1[0-7]_call_1_ag3_plot_njt'
NJT_AF1='cell_*_call_1_af1_plot_njt'

# ---------------------------------------------------------------------------
# Neighbour-joining trees (plot_njt)
# ---------------------------------------------------------------------------

# n_snps: SNPs used for the distance matrix. Uses the 26 Mbp window so even
# 100k SNPs are available after thinning.
$CFG plot_njt \
    --set "$NJT_AG3.region=\"3L:15,000,000-41,000,000\"" \
    --set "$NJT_AF1.region=\"3RL:15,000,000-41,000,000\"" \
    --sweep "$NJT_AG3,$NJT_AF1.n_snps=[10000,25000,50000,100000]" \
    --output $OUT/plot_njt_n_snps.csv

# region: genome window the SNPs are drawn from (1, 10, 26 Mbp), Ag3 and Af1
# paired value-by-value.
$CFG plot_njt --zip \
    --sweep "$NJT_AG3.region=[\"3L:15,000,000-16,000,000\",\"3L:15,000,000-25,000,000\",\"3L:15,000,000-41,000,000\"]" \
    --sweep "$NJT_AF1.region=[\"3RL:15,000,000-16,000,000\",\"3RL:15,000,000-25,000,000\",\"3RL:15,000,000-41,000,000\"]" \
    --output $OUT/plot_njt_region.csv

# algorithm: the same neighbour-joining tree computed three ways; a pure
# compute comparison ('dynamic' is documented as fastest).
$CFG plot_njt \
    --sweep "$NJT_AG3,$NJT_AF1.algorithm=[\"dynamic\",\"rapid\",\"canonical\"]" \
    --output $OUT/plot_njt_algorithm.csv

# samples: tree size for the whole-release call (cell_18). Distance matrices
# grow with samples squared and tree building faster still.
# - plot_njt cell_18 runs the slow 'canonical' algorithm on the whole 3.0
#   release, so it is left out of the region / n_snps sweeps (patterns list the
#   other calls explicitly) and gets its own sample-size sweep instead.
$CFG plot_njt \
    --sweep 'cell_18_call_1_ag3_plot_njt.max_cohort_size=[100,250,500,1000]' \
    --output $OUT/plot_njt_samples.csv

#  region sweeps only touch the calls at one locus, so each example still studies its own gene.
# region: widen the window at the Vgsc locus (Ag3 cells 6-10, Ghana + Burkina
# Faso) and at the Af1 2RL:28.48 Mbp locus (cell_24), paired value-by-value.
$CFG plot_haplotype_clustering --zip \
    --sweep 'cell_[6-9]_call_1_ag3_plot_haplotype_clustering,cell_10_call_1_ag3_plot_haplotype_clustering.region=["2L:2,410,000-2,430,000","2L:2,410,000-2,460,000","2L:2,410,000-2,510,000"]' \
    --sweep 'cell_24_call_1_af1_plot_haplotype_clustering.region=["2RL:28,480,000-28,490,000","2RL:28,480,000-28,530,000","2RL:28,480,000-28,580,000"]' \
    --output $OUT/plot_haplotype_clustering_region.csv

# samples: the whole-release calls at the Cyp6 locus (cells 12-18). Pairwise
# distances grow with haplotypes squared, so this is the steepest lever.
$CFG plot_haplotype_clustering \
    --sweep 'cell_1[2-7]_call_1_ag3_plot_haplotype_clustering,cell_18_call_1_ag3_plot_haplotype_clustering_advanced.cohort_size=[100,250,500,1000]' \
    --output $OUT/plot_haplotype_clustering_samples.csv

# snp_filter_min_maf: SNPs kept for clustering in the advanced calls. Allele
# frequencies can't exceed 0.5, so values stay below that.
$CFG plot_haplotype_clustering \
    --sweep 'cell_18_call_1_ag3_plot_haplotype_clustering_advanced,cell_19_call_1_ag3_plot_haplotype_clustering_advanced.snp_filter_min_maf=[0.01,0.05,0.1]' \
    --output $OUT/plot_haplotype_clustering_min_maf.csv

# region: widen the window at the Vgsc locus (cells 7-9, Ghana + Burkina Faso).
$CFG plot_diplotype_clustering \
    --sweep 'cell_[7-9]_call_1_ag3_plot_diplotype_clustering.region=["2L:2,410,000-2,430,000","2L:2,410,000-2,460,000","2L:2,410,000-2,510,000"]' \
    --output $OUT/plot_diplotype_clustering_region.csv

# samples: Ghana + Burkina Faso at the Cyp6 locus (cell_6, ~280 samples).
$CFG plot_diplotype_clustering \
    --sweep 'cell_6_call_1_ag3_plot_diplotype_clustering_advanced.cohort_size=[50,100,200]' \
    --output $OUT/plot_diplotype_clustering_samples.csv
