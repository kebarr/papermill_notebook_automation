# papermill_notebook_automation

# Basic usage

This is a set of utilities for converting the notebooks in malariagen_data, which have been edited sych that they can be run through papaermill with user specified parameterisation via an input CSV. In principle, this should be useable for any suitably formated Jupyter notebook

To generate a runner for a notebook, use:
```python papermill_meta.py ${notebook_name} --notebooks-dir ./notebooks   --output-dir runners_and_csvs/generated_runners```

Where notebook_name is the basename, i.e. without the ".ipynb" extension

You can configure a CSV that edits the API_CALL_PARAMETERS section of the parameters cell (required for papermill runs) asf ollows:

```python papermill_csv_config.py create ${notebook_name%.ipynb}   --validate-metadata --output runners_and_csvs/${notebook_name%.ipynb}_config.ch```

You can then run the resulting papermill runner for your notebook with the CSV you have configured as follows::
```python runners_and_csvs/generated_runners/papermill_${notebook_name}.py --config runners_and_csvs/${notebook_name}_config.csv --output-dir executed_runs```




