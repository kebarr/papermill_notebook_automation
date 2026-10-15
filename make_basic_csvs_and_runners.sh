for notebook in ./notebooks/*ipynb
do 
    # Prefix ../executed_runs/ only while the path is a bare file name (no "/"),
    # so rerunning leaves already-prefixed paths alone. -i.bak works with both
    # macOS and GNU sed.
    sed -i.bak -E "s,\"PERFORMANCE_CSV_PATH = '([^'/]*)',\"PERFORMANCE_CSV_PATH = '../executed_runs/\1'," "$notebook" && rm "$notebook.bak"
    notebook_name=$(basename ${notebook%.ipynb})
    echo "Generating runner and CSV for notebook: $notebook_name"
    python papermill_meta.py ${notebook_name} --notebooks-dir ./notebooks   --output-dir runners_and_csvs/generated_runners
    python papermill_csv_config.py create ${notebook_name}   --validate-metadata --output runners_and_csvs/${notebook_name}_config.csv
    python runners_and_csvs/generated_runners/papermill_${notebook_name}.py --config runners_and_csvs/${notebook_name}_config.csv --output-dir executed_runs
done

python runners_and_csvs/generated_runners/papermill_${notebook_name%.ipynb}.py --config runners_and_csvs/${notebook_name%.ipynb}_config.csv --output-dir executed_runs
sed 's,"PERFORMANCE_CSV_PATH = '\'',"PERFORMANCE_CSV_PATH = '\''../executed_runs/,' notebooks/extra_metadata.ipynb | less
sed 's,PERFORMANCE_CSV_PATH = '\'',PERFORMANCE_CSV_PATH = '\''../executed_runs/,' notebooks/extra_metadata.ipynb | less

PERFORMANCE_CSV_PATH = 'extra_metadata_performance.csv'

for script in ./*.py
do
    script_name=$(basename ${script%.py})
    echo "Generating runner and CSV for notebook: $script_name"
    python ${script} --output-csv ${script_name}_default_config.csv
done

# think karyoptype crashed it
python ld_pruning.py --output-csv ld_pruning_default_config.csv > ld_pruning_default_config_stdout.txt 2> ld_pruning_default_config_stderr.txt
python phenotype_data_demo.py --output-csv phenotype_data_demo_default_config.csv > phenotype_data_demo_default_config_stdout.txt 2> phenotype_data_demo_default_config_stderr.txt
python plink_convert.py --output-csv plink_convert_default_config.csv > plink_convert_default_config_stdout.txt 2> plink_convert_default_config_stderr.txt
python plot_aims.py --output-csv plot_aims.csv > plot_aims_stdout.txt 2> plot_aims_stderr.txt
python plot_cnv.py --output-csv plot_cnv.csv > plot_cnv_stdout.txt 2> plot_cnv_stderr.txt
python plot_diplotype_clustering.py --output-csv plot_diplotype_clustering.csv > plot_diplotype_clustering_stdout.txt 2> plot_diplotype_clustering_stderr.txt
python plot_diversity.py --output-csv plot_diversity.csv > plot_diversity_stdout.txt 2> plot_diversity_stderr.txt
# went over memory
python plot_frequencies_heatmap.py --output-csv plot_frequencies_heatmap.csv > plot_frequencies_heatmap_stdout.txt 2> plot_frequencies_heatmap_stderr.txt
python plot_frequencies_space_time.py --output-csv plot_frequencies_space_time.csv > plot_frequencies_space_time_stdout.txt 2> plot_frequencies_space_time_stderr.txt
# went over memory
python plot_fst_gwss.py --output-csv plot_fst_gwss.csv > plot_fst_gwss_stdout.txt 2> plot_fst_gwss_stderr.txt
python plot_g123_gwss.py --output-csv plot_g123_gwss.csv > plot_g123_gwss_stdout.txt 2> plot_g123_gwss_stderr.txt
python plot_genes.py --output-csv plot_genes.csv > plot_genes_stdout.txt 2> plot_genes_stderr.txt
# went over memory
python plot_h12_h1x.py --output-csv plot_h12_h1x.csv > plot_h12_h1x_stdout.txt 2> plot_h12_h1x_stderr.txt
python plot_haplotype_clustering.py --output-csv plot_haplotype_clustering.csv > plot_haplotype_clustering_stdout.txt 2> plot_haplotype_clustering_stderr.txt
python plot_haplotype_networks.py --output-csv plot_haplotype_networks.csv > plot_haplotype_networks_stdout.txt 2> plot_haplotype_networks_stderr.txt
python plot_haplotype_frequencies.py --output-csv plot_haplotype_frequencies.csv > plot_haplotype_frequencies_stdout.txt 2> plot_haplotype_frequencies_stderr.txt
python plot_heterozygosity.py --output-csv plot_heterozygosity.csv > plot_heterozygosity_stdout.txt 2> plot_heterozygosity_stderr.txt
python plot_ihs_gwss.py --output-csv plot_ihs_gwss.csv > plot_ihs_gwss_stdout.txt 2> plot_ihs_gwss_stderr.txt
python plot_njt.py --output-csv plot_njt.csv > plot_njt_stdout.txt 2> plot_njt_stderr.txt
python plot_pairwise_average_fst.py --output-csv plot_pairwise_average_fst.csv > plot_pairwise_average_fst_stdout.txt 2> plot_pairwise_average_fst_stderr.txt
python plot_pca.py --output-csv plot_pca.csv > plot_pca_stdout.txt 2> plot_pca_stderr.txt
python plot_samples.py --output-csv plot_samples.csv > plot_samples_stdout.txt 2> plot_samples_stderr.txt
python plot_snps.py --output-csv plot_snps.csv > plot_snps_stdout.txt 2> plot_snps_stderr.txt
python plot_xpehh_gwss.py --output-csv plot_xpehh_gwss.csv > plot_xpehh_gwss_stdout.txt 2> plot_xpehh_gwss_stderr.txt
python repr.py --output-csv repr.csv > repr_stdout.txt 2> repr_stderr.txt
python spike_sim_test_data.py --output-csv spike_sim_test_data.csv > spike_sim_test_data_stdout.txt 2> spike_sim_test_data_stderr.txt
