# papermill_notebook_automation

#Purpose of this repo

Many repos use Jupyter notebooks to demonstrate their APIs, these are usually configurd specifically to run quickly as simple demonstrations. However, many of the APIs demonstrated can quickly blow up- in terms of time and compute resources. IT is therefore important to understand how varying the arguments to methods exposed by APIs impacts running time and resource usage. These scripts enable you to create papermill runners for arbitrary ipython notebooks, create configurable CSVs, convert the notebooks into scripts to be run from the command line, and records the time and peak memory usage for each configuration run. This enables you to learn how parameters impact performance, an important consideration when planning large-scale analyses.

The notebooks were first converted into a papermill compatible formats and wrapped with the performance analysis capability in the second cell using an LLM.

# Dependencies
- papermill
- jupyter
- memory_profiler
- malariagen_data 


# Basic usage

This is a set of utilities for converting the notebooks in malariagen_data, which have been edited sych that they can be run through papaermill with user specified parameterisation via an input CSV. In principle, this should be useable for any suitably formated Jupyter notebook

To generate a runner for a notebook, use:
```python papermill_meta.py ${notebook_name} --notebooks-dir ./notebooks   --output-dir runners_and_csvs/generated_runners```

Where notebook_name is the basename, i.e. without the ".ipynb" extension

You can configure a CSV that edits the API_CALL_PARAMETERS section of the parameters cell (required for papermill runs) asf ollows:

```python papermill_csv_config.py create ${notebook_name%.ipynb}   --validate-metadata --output runners_and_csvs/${notebook_name%.ipynb}_config.ch```

You can then run the resulting papermill runner for your notebook with the CSV you have configured as follows::
```python runners_and_csvs/generated_runners/papermill_${notebook_name}.py --config runners_and_csvs/${notebook_name}_config.csv --output-dir executed_runs```

# Converting notebooks into scripts
There is also funcitonality to convert notebooks into scripts, using notebook_to_script.py 
For this to run, the notebooks must meet the following criteria:

-One parameters cell: exactly one cell tagged parameters, containing only simple literal assignments (NAME = value). Your new PERFORMANCE_CSV_PATH is fine and automatically becomes a CSV column.
-Helper signature: _call_api_with_parameters(method, call_key, ...). This is what links each graph to its call key for naming. If it changes, graphs still get saved, but named after the cell instead of the call.
-Magics: only %%time (as the first line of a cell), %timeit, %memit, %load_ext and !command. Anything else, such as %%capture or %matplotlib, is rejected. Each is a small addition to _translate_magics in notebook_to_script.py. 

This can be run as follows:
```python notebook_to_script.py              # all notebooks```
```python notebook_to_script.py plot_pca     # just one```

The generated scripts are then run as follows, the CSVs are in the same format, and geenrated in the same was, as the ones used for the papermill runners::
```python scripts/plot_pca.py                                        # notebook defaults```
```python scripts/plot_pca.py --config runners_and_csvs/plot_pca_config.csv```
```python scripts/plot_pca.py --list-parameters                      # what a CSV can set``

A default output CSV name is used unless otherwise specified, meaning if you have run the script in the past, then run it again, it will overwrite the old CSV. You can avoid this by specifying the nae of the output CSV as follows: 
```python scripts/plot_pca.py --output-csv my_run.csv        # -> executed_runs_scripts/my_run.csv```
```python scripts/plot_pca.py --output-csv results/pca.csv   # -> results/pca.csv (relative to where you run it```)
`



