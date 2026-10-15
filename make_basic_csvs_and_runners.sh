for notebook in ./notebooks/*ipynb
do 
    notebook_name=$(basename $notebook)
    echo "Generating runner and CSV for notebook: $notebook_name"
    python papermill_meta.py ${notebook_name} --notebooks-dir ./notebooks   --output-dir runners_and_csvs/generated_runners
    python papermill_csv_config.py create ${notebook_name}   --validate-metadata --output runners_and_csvs/${notebook_name}_config.csv
done

python runners_and_csvs/generated_runners/papermill_${notebook_name%.ipynb}.py --config runners_and_csvs/${notebook_name%.ipynb}_config.csv --output-dir executed_runs
sed 's,"PERFORMANCE_CSV_PATH = '\'',"PERFORMANCE_CSV_PATH = '\''../executed_runs/,' notebooks/extra_metadata.ipynb | less
sed 's,PERFORMANCE_CSV_PATH = '\'',PERFORMANCE_CSV_PATH = '\''../executed_runs/,' notebooks/extra_metadata.ipynb | less

PERFORMANCE_CSV_PATH = 'extra_metadata_performance.csv