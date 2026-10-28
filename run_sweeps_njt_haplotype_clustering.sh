
CFG="python papermill_csv_config.py --notebooks-dir notebooks_fixed_parameters_cells create"
OUT=runners_and_csvs_new

# for neighbour joining tree, notebook varies region, n_snps
$CFG plot_njt --set 'cell_*_call_*_ag3_njt.region=["3L:15,000,000-41,000,000"]' --sweep 'cell_*_call_*_ag3_njt.n_snps=[10000,25000,50000,100000]' --output $OUT/plot_njt_n_snps.csv
$CFG plot_njt --set 'cell_*_call_*_ag3_plot_njt.region=["3L:15,000,000-41,000,000"]' --sweep 'cell_*_call_*_ag3_plot_njt.n_snps=[10000,25000,50000,100000]' --output $OUT/plot_njt_n_snps.csv
$CFG plot_njt --set 'cell_*_call_*_af1_plot_njt.region=["3L:15,000,000-41,000,000"]' --sweep 'cell_*_call_*_af1_plot_njt.n_snps=[10000,25000,50000,100000]' --output $OUT/plot_njt_n_snps.csv

$CFG plot_njt --sweep 'cell_*_call_*_ag3_plot_njt.region=["3L:15,000,000-16,000,000","3L:15,000,000-25,000,000","3L:15,000,000-41,000,000"]' --output $OUT/plot_njt_region.csv
$CFG plot_njt --sweep 'cell_*_call_*_ag3_njt.region=["3L:15,000,000-16,000,000","3L:15,000,000-25,000,000","3L:15,000,000-41,000,000"]' --output $OUT/plot_njt_region.csv
$CFG plot_njt --sweep 'cell_*_call_*_af1_plot_njt.region=["3RL:15,000,000-16,000,000","3RL:15,000,000-25,000,000","3RL:15,000,000-41,000,000"]' --output $OUT/plot_njt_region.csv