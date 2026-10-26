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

# these are missing because the CSVs weren't generated for some reason
notebook_name="cohort_geometries"
python papermill_meta.py ${notebook_name} --output-csv executed_runs_local_papermill/ --notebooks-dir ./notebooks   --output-dir runners_and_csvs/generated_runners
python papermill_csv_config.py create cohort_geometries   --validate-metadata --output runners_and_csvs/cohort_geometries_config.csv
python runners_and_csvs/generated_runners/papermill_cohort_geometries.py --config runners_and_csvs/cohort_geometries_config.csv --output-dir executed_runs_local_papermill
python papermill_csv_config.py create phenotype_data_demo   --validate-metadata --output runners_and_csvs/phenotype_data_demo_config.csv
python runners_and_csvs/generated_runners/papermill_phenotype_data_demo.py --config runners_and_csvs/phenotype_data_demo_config.csv --output-dir executed_runs_local_papermill
python papermill_csv_config.py create plot_genes   --validate-metadata --output runners_and_csvs/plot_genes_config.csv
python runners_and_csvs/generated_runners/papermill_plot_genes.py --config runners_and_csvs/plot_genes_config.csv --output-dir executed_runs_local_papermill
python papermill_csv_config.py create plot_h12_h1x   --validate-metadata --output runners_and_csvs/plot_h12_h1x_config.csv
python runners_and_csvs/generated_runners/papermill_plot_h12_h1x.py --config runners_and_csvs/plot_h12_h1x_config.csv --output-dir executed_runs_local_papermill
python papermill_csv_config.py create plot_ihs_gwss   --validate-metadata --output runners_and_csvs/plot_ihs_gwss_config.csv
python runners_and_csvs/generated_runners/papermill_plot_ihs_gwss.py --config runners_and_csvs/plot_ihs_gwss_config.csv --output-dir executed_runs_local_papermill
python papermill_csv_config.py create plot_pairwise_average_fst   --validate-metadata --output runners_and_csvs/plot_pairwise_average_fst_config.csv
python runners_and_csvs/generated_runners/papermill_plot_pairwise_average_fst.py --config runners_and_csvs/plot_pairwise_average_fst_config.csv --output-dir executed_runs_local_papermill
python papermill_csv_config.py create plot_xpehh_gwss   --validate-metadata --output runners_and_csvs/plot_xpehh_gwss_config.csv
python runners_and_csvs/generated_runners/papermill_plot_xpehh_gwss.py --config runners_and_csvs/plot_xpehh_gwss_config.csv --output-dir executed_runs_local_papermill

python papermill_csv_config.py create karyotype   --validate-metadata --output runners_and_csvs/karyotype_config.csv
python runners_and_csvs/generated_runners/papermill_karyotype.py --config runners_and_csvs/karyotype_config.csv --output-dir executed_runs_local_papermill


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

python karyotype.py --output-csv karyotype.csv > karyotype_stdout_6_GB.txt 2> karyotype_stderr_6_GB.txt

# think karyoptype crashed it
python ld_pruning.py --output-csv ld_pruning_default_config.csv > ld_pruning_default_config_stdout.txt 2> ld_pruning_default_config_stderr.txt
python phenotype_data_demo.py --output-csv phenotype_data_demo_default_config.csv > phenotype_data_demo_default_config_stdout.txt 2> phenotype_data_demo_default_config_stderr.txt
python plink_convert.py --output-csv plink_convert_default_config.csv > plink_convert_default_config_stdout.txt 2> plink_convert_default_config_stderr.txt
python plot_aims.py --output-csv plot_aims.csv > plot_aims_stdout.txt 2> plot_aims_stderr.txt
python plot_cnv.py --output-csv plot_cnv.csv > plot_cnv_stdout.txt 2> plot_cnv_stderr.txt
python plot_diplotype_clustering.py --output-csv plot_diplotype_clustering.csv > plot_diplotype_clustering_stdout.txt 2> plot_diplotype_clustering_stderr.txt
python plot_diversity.py --output-csv plot_diversity.csv > plot_diversity_stdout.txt 2> plot_diversity_stderr.txt
# went over memory
python plot_frequencies_heatmap.py --output-csv plot_frequencies_heatmap.csv > plot_frequencies_heatmap_stdout_6_GB.txt 2> plot_frequencies_heatmap_stderr_6_GB.txt
python plot_frequencies_space_time.py --output-csv plot_frequencies_space_time.csv > plot_frequencies_space_time_stdout.txt 2> plot_frequencies_space_time_stderr.txt
# went over memory
python plot_fst_gwss.py --output-csv plot_fst_gwss.csv > plot_fst_gwss_stdout_6_GB.txt 2> plot_fst_gwss_stderr_6_GB.txt
python plot_g123_gwss.py --output-csv plot_g123_gwss.csv > plot_g123_gwss_stdout.txt 2> plot_g123_gwss_stderr.txt
python plot_genes.py --output-csv plot_genes.csv > plot_genes_stdout.txt 2> plot_genes_stderr.txt
# went over memory
python plot_h12_h1x.py --output-csv plot_h12_h1x.csv > plot_h12_h1x_stdout_6_GB.txt 2> plot_h12_h1x_stderr_6_GB.txt
# went over memory, I think, tab randomly closed
python plot_haplotype_clustering.py --output-csv plot_haplotype_clustering.csv > plot_haplotype_clustering_stdout.txt 2> plot_haplotype_clustering_stderr.txt
# went over memory, I think, tab randomly closed, no stdout or stderr
python plot_haplotype_networks.py --output-csv plot_haplotype_networks.csv > plot_haplotype_networks_stdout.txt 2> plot_haplotype_networks_stderr.txt
python plot_haplotypes_frequencies.py --output-csv plot_haplotypes_frequencies.csv > plot_haplotypes_frequencies_stdout.txt 2> plot_haplotypes_frequencies_stderr.txt
python plot_heterozygosity.py --output-csv plot_heterozygosity.csv > plot_heterozygosity_stdout.txt 2> plot_heterozygosity_stderr.txt
python plot_ihs_gwss.py --output-csv plot_ihs_gwss.csv > plot_ihs_gwss_stdout.txt 2> plot_ihs_gwss_stderr.txt
python plot_njt.py --output-csv plot_njt.csv > plot_njt_stdout.txt 2> plot_njt_stderr.txt
python plot_pairwise_average_fst.py --output-csv plot_pairwise_average_fst.csv > plot_pairwise_average_fst_stdout.txt 2> plot_pairwise_average_fst_stderr.txt
python plot_pca.py --output-csv plot_pca.csv > plot_pca_stdout.txt 2> plot_pca_stderr.txt
python plot_samples.py --output-csv plot_samples.csv > plot_samples_stdout.txt 2> plot_samples_stderr.txt
python plot_snps.py --output-csv plot_snps.csv > plot_snps_stdout.txt 2> plot_snps_stderr.txt
# went over memory, worked on g^GB
python plot_xpehh_gwss.py --output-csv plot_xpehh_gwss.csv > plot_xpehh_gwss_stdout.txt 2> plot_xpehh_gwss_stderr.txt
python repr.py --output-csv repr.csv > repr_stdout.txt 2> repr_stderr.txt
# server went down, worked on 6GB
python spike_sim_test_data.py --output-csv spike_sim_test_data.csv > spike_sim_test_data_stdout.txt 2> spike_sim_test_data_stderr.txt

# console comments
# crashes on igv cell 10: call_api_with_parameters(af1.snp_calls_to_vcf, 'cell_19_call_2_af1_snp_calls_to_vcf', output_path=str(local_vcf_path), region=region, sample_sets=[sample_set], sample_query=f"sample_id == '{sample_id}'", overwrite=True)
# saying no relevant alignments found, which is false
# leaving ones likely to crash 3GB server to last
# plot frequencies space time errors on
ds = _call_api_with_parameters(ag3.gene_cnv_frequencies_advanced, 'cell_5_call_1_ag3_gene_cnv_frequencies_advanced', region="2R:28,450,000-28,510,000", area_by="admin1_iso", period_by="year", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"], sample_query="taxon in ['coluzzii', 'gambiae']", min_cohort_size=10)
# with I/O operation on a closed file
# plot g123_gwss webt over memory
# haplotype frequencies errors with I/O operation on a closed file
# nbrt.display(_call_api_with_parameters(ag3.plot_roh, 'cell_3_call_1_ag3_plot_roh', sample="AK0050-C", region="3R", site_mask="gamb_colu", window_size=20_000))
# ditto ihs_gwss
# nbrt.display(_call_api_with_parameters(ag3.plot_ihs_gwss, 'cell_5_call_1_ag3_plot_ihs_gwss', contig="2L", window_size=100, sample_query="cohort_admin2_year == 'ML-2_Kati_colu_2014'", sample_sets="3.0", analysis="gamb_colu", min_cohort_size=10, max_cohort_size=20))
# plot ihs_gwss
# plot ihs_gwss runs out of memoy
# plot_snps - dataset object not callble

# run with 6GB server:
# spike_sim_test_data
# xpehh_gwss - got I/O operation on a closed file
# same with ihs_gwss, plot_haplotype_networks, plot_h12_h1x

# haplotype_network errored with port connection, then port in use, then no attribute x- saved
# karyotype went above 6GB, trying againin case it was due to leftover momry from another console

# papermill performance notebooks to run on 6GB
#plot_g123_gwss.ipynb
# plot_frequencies_heatmap
# plot_frequencies_space_time
# plot_fst_gwss
# plot_h12_h1x
# plot_haplotype_clustering
# plot njt has assesrtion error

# karyotype failed in 6GB notebook not sure if due to going idle or memory
# g123_gwss failed in 6GB notebook not sure if due to going idle or memory
# plot haplotype_networks errored with address already in use

python view_performance.py executed_runs_notebooks_fixed console/executed_runs_datalab scripts/executed_runs_datalab notebooks/executed_runs_datalab --output view_performance_each_run.html --open > view_performance_stdout.txt 2> view_performance_stderr.txt

for notebook in ./notebooks_fixed_parameters_cells/*ipynb
do 
    notebook_name=$(basename ${notebook%.ipynb})
    echo "Generating runner and CSV for notebook: $notebook_name"
    echo ${notebook}
    python papermill_meta.py ${notebook_name} --notebooks-dir ./notebooks_fixed_parameters_cells   --output-dir runners_and_csvs_new/generated_runners --output-csv executed_runs_notebooks_fixed/${notebook_name}_parameters_fixed.csv
    python papermill_csv_config.py --notebooks-dir ./notebooks_fixed_parameters_cells create ${notebook_name}   --validate-metadata --output runners_and_csvs_new/${notebook_name}_config.csv
    python notebook_to_script.py ${notebook} # will use default notebook params
    python runners_and_csvs_new/generated_runners/papermill_${notebook_name}.py --output-csv executed_runs_notebooks_fixed/${notebook_name}_parameters_fixed.csv --config runners_and_csvs_new/${notebook_name}_config.csv --output-dir executed_runs_notebooks_fixed
done


for notebook in ./notebooks_fixed_parameters_cells/*ipynb
do 
    notebook_name=$(basename ${notebook%.ipynb})
    echo "Generating runner and CSV for notebook: $notebook_name"
    echo ${notebook}
    python papermill_meta.py ${notebook_name} --notebooks-dir ./notebooks_fixed_parameters_cells --output-dir runners_and_csvs_new/generated_runners > fixed_parameters_stdout/${notebook_name}_papermill_meta.txt 2> fixed_parameters_stderr/${notebook_name}_papermill_meta.txt
    python papermill_csv_config.py --notebooks-dir ./notebooks_fixed_parameters_cells create ${notebook_name} --validate-metadata --output runners_and_csvs_new/${notebook_name}_config.csv > fixed_parameters_stdout/${notebook_name}_papermill_csv_maker.txt 2> fixed_parameters_stderr/${notebook_name}_papermill_csv_maker.txt
    python notebook_to_script.py ${notebook_name} --notebooks-dir ./notebooks_fixed_parameters_cells > fixed_parameters_stdout/${notebook_name}_to_script.txt 2> fixed_parameters_stderr/${notebook_name}_to_script.txt # will use default notebook params
    python runners_and_csvs_new/generated_runners/papermill_${notebook_name}.py --output-csv executed_runs_notebooks_fixed/${notebook_name}_parameters_fixed.csv --config runners_and_csvs_new/${notebook_name}_config.csv --output-dir executed_runs_notebooks_fixed > fixed_parameters_stdout/${notebook_name}_papermill_run.txt 2> fixed_parameters_stderr_${notebook_name}_papermill_run.txt 
done

python extra_metadata.py --output-csv extra_metadata.csv --workdir > extra_metadata_stdout.txt 2> extra_metadata_stderr.txt
python igv.py --output-csv igv.csv > igv_stdout.txt 2> igv_stderr.txt
python karyotype.py --output-csv karyotype.csv > karyotype_stdout.txt 2> karyotype_stderr.txt
python plot_h12_h1x.py --output-csv plot_h12_h1x.csv > plot_h12_h1x_stdout.txt 2> plot_h12_h1x_stderr.txt
python plot_g123_gwss.py --output-csv plot_g123_gwss.csv > plot_g123_gwss_stdout.txt 2> plot_g123_gwss_stderr.txt
python phenotype_data_demo.py --output-csv phenotype_data_demo.csv > phenotype_data_demo_stdout.txt 2> phenotype_data_demo_stderr.txt
python plot_pairwise_average_fst.py --output-csv plot_pairwise_average_fst.csv > plot_pairwise_average_fst_stdout.txt 2> plot_pairwise_average_fst_stderr.txt
python plot_pca.py --output-csv plot_pca.csv > plot_pca_average_fst_stdout.txt 2> plot_pca_average_fst_stderr.txt

# still missing, notebooks: haplotype_clustering, haplotype networks, xpehh, repr, spike_test_dat
#  script: local_cluster, fst_gwss, haplotype networks, pairwise fst, repr, spike_sim_data
# console: frequencies_space_time, g123_gwss, heterozygosity

# notebooks and scripts g12_gwss broke at cell 14 of 16 

# Something that affects your runtime estimates: memory_profiler.memory_usage reruns the measured call until it has at least 5 memory samples, taken every 0.1 s. Any call faster than about half a second is executed 2–3 times, and the helper's runtime_sec includes all the repeats. Slow calls aren't affected, but the times for fast calls are inflated. In the hand-edited old plot_snps, where memory_usage wraps the helper itself, the repeats also write extra rows. I can fix the helper to time just one execution if you want.


for notebook in /Users/katie.barr/malariagen-data-python/notebooks/*ipynb
do 
    notebook_name=$(basename ${notebook%.ipynb})
    echo "Generating memit for notebook: $notebook_name"
    echo ${notebook}
    python ../add_memit.py $notebook -o ${notebook_name}_memit.ipynb
done

