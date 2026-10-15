#!/usr/bin/env python3
"""plot_pairwise_average_fst: the code from notebooks/plot_pairwise_average_fst.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_pairwise_average_fst.py                      # the notebook's defaults
    python scripts/plot_pairwise_average_fst.py --config runs.csv    # one run per CSV row
    python scripts/plot_pairwise_average_fst.py --list-parameters    # what a CSV can set
    python scripts/plot_pairwise_average_fst.py --output-csv my_run.csv
                                    # performance CSV -> executed_runs_scripts/my_run.csv

CSV columns are parameter names (API_KEEP_CALLSITE_VALUE, PERFORMANCE_CSV_PATH, API_CALL_PARAMETERS, FIGURE_DIR, FIGURE_FORMAT, FIGURE_NAMES).
Values are JSON; empty cells keep the default. API_CALL_PARAMETERS and
FIGURE_NAMES only need the entries you want to change.

Generated from the notebook by notebook_to_script.py.
"""

import notebook_runtime as nbrt

# ---------------------------------------------------------------------------
# Parameters (the notebook's "parameters" cell)
# ---------------------------------------------------------------------------

# Malariagen API arguments for each call below.
# Replace a value to override it; keep the marker to use the call-site
# value or the method's default.
API_KEEP_CALLSITE_VALUE = '__KEEP_CALLSITE_VALUE__'
# Relative to where the script is run from.
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_pairwise_average_fst_performance.csv'
API_CALL_PARAMETERS = {'cell_5_call_1_ag3_average_fst': {'region': '__KEEP_CALLSITE_VALUE__',
                                   'cohort1_query': "cohort_admin2_year == 'ML-2_Kati_colu_2014'",
                                   'cohort2_query': "cohort_admin2_year == 'ML-2_Kati_gamb_2014'",
                                   'sample_query_options': None,
                                   'sample_sets': '3.0',
                                   'cohort_size': None,
                                   'min_cohort_size': 15,
                                   'max_cohort_size': 50,
                                   'n_jack': 200,
                                   'site_mask': 'default',
                                   'site_class': None,
                                   'random_seed': 42},
 'cell_6_call_1_ag3_pairwise_average_fst': {'region': '__KEEP_CALLSITE_VALUE__',
                                            'cohorts': 'cohort_admin1_year',
                                            'sample_sets': '3.0',
                                            'sample_query': "country == 'Mali' and taxon == "
                                                            "'gambiae'",
                                            'sample_query_options': None,
                                            'cohort_size': None,
                                            'min_cohort_size': 15,
                                            'max_cohort_size': 50,
                                            'n_jack': 200,
                                            'site_mask': 'default',
                                            'site_class': None,
                                            'random_seed': 42},
 'cell_7_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                 'annotation': None,
                                                 'zmin': 0.0,
                                                 'zmax': None,
                                                 'text_auto': '.3f',
                                                 'color_continuous_scale': 'gray_r',
                                                 'width': None,
                                                 'height': None,
                                                 'row_height': 40,
                                                 'col_width': 50,
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_8_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                 'annotation': 'standard error',
                                                 'zmin': 0.0,
                                                 'zmax': None,
                                                 'text_auto': '.3f',
                                                 'color_continuous_scale': 'gray_r',
                                                 'width': None,
                                                 'height': None,
                                                 'row_height': 40,
                                                 'col_width': 50,
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_9_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                 'annotation': 'Z score',
                                                 'zmin': 0.0,
                                                 'zmax': None,
                                                 'text_auto': '.3f',
                                                 'color_continuous_scale': 'gray_r',
                                                 'width': None,
                                                 'height': None,
                                                 'row_height': 40,
                                                 'col_width': 50,
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_10_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                  'annotation': None,
                                                  'zmin': 0.0,
                                                  'zmax': 0.1,
                                                  'text_auto': '.3f',
                                                  'color_continuous_scale': 'gray_r',
                                                  'width': 400,
                                                  'height': 300,
                                                  'row_height': 40,
                                                  'col_width': 50,
                                                  'show': True,
                                                  'renderer': None,
                                                  'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_12_call_1_ag3_pairwise_average_fst': {'region': '__KEEP_CALLSITE_VALUE__',
                                             'cohorts': 'cohort_admin1_year',
                                             'sample_sets': ['AG1000G-KE',
                                                             '1274-VO-KE-KAMAU-VMF00246'],
                                             'sample_query': "country == 'Kenya' and taxon == "
                                                             "'arabiensis'",
                                             'sample_query_options': None,
                                             'cohort_size': None,
                                             'min_cohort_size': 10,
                                             'max_cohort_size': 50,
                                             'n_jack': 200,
                                             'site_mask': 'default',
                                             'site_class': None,
                                             'random_seed': 42},
 'cell_13_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                  'annotation': None,
                                                  'zmin': 0.0,
                                                  'zmax': None,
                                                  'text_auto': '.3f',
                                                  'color_continuous_scale': 'gray_r',
                                                  'width': None,
                                                  'height': None,
                                                  'row_height': 40,
                                                  'col_width': 50,
                                                  'show': True,
                                                  'renderer': None,
                                                  'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_14_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                  'annotation': 'standard error',
                                                  'zmin': 0.0,
                                                  'zmax': None,
                                                  'text_auto': '.3f',
                                                  'color_continuous_scale': 'gray_r',
                                                  'width': None,
                                                  'height': None,
                                                  'row_height': 40,
                                                  'col_width': 50,
                                                  'show': True,
                                                  'renderer': None,
                                                  'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_15_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                  'annotation': 'Z score',
                                                  'zmin': 0.0,
                                                  'zmax': 0.03,
                                                  'text_auto': '.3f',
                                                  'color_continuous_scale': 'gray_r',
                                                  'width': None,
                                                  'height': None,
                                                  'row_height': 40,
                                                  'col_width': 50,
                                                  'show': True,
                                                  'renderer': None,
                                                  'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_16_call_1_ag3_pairwise_average_fst': {'region': '3L:15,000,000-16,000,000',
                                             'cohorts': '__KEEP_CALLSITE_VALUE__',
                                             'sample_sets': None,
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'cohort_size': None,
                                             'min_cohort_size': 10,
                                             'max_cohort_size': 50,
                                             'n_jack': 200,
                                             'site_mask': 'arab',
                                             'site_class': None,
                                             'random_seed': 42},
 'cell_17_call_1_ag3_plot_pairwise_average_fst': {'fst_df': '__KEEP_CALLSITE_VALUE__',
                                                  'annotation': 'Z score',
                                                  'zmin': 0.0,
                                                  'zmax': 0.4,
                                                  'text_auto': '.3f',
                                                  'color_continuous_scale': 'gray_r',
                                                  'width': None,
                                                  'height': None,
                                                  'row_height': 40,
                                                  'col_width': 50,
                                                  'show': True,
                                                  'renderer': None,
                                                  'kwargs': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_pairwise_average_fst'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_7_call_1_ag3_plot_pairwise_average_fst': '01_ag3_pairwise_average_fst',
 'cell_8_call_1_ag3_plot_pairwise_average_fst': '02_ag3_pairwise_average_fst',
 'cell_9_call_1_ag3_plot_pairwise_average_fst': '03_ag3_pairwise_average_fst',
 'cell_10_call_1_ag3_plot_pairwise_average_fst': '04_ag3_pairwise_average_fst',
 'cell_13_call_1_ag3_plot_pairwise_average_fst': '05_ag3_pairwise_average_fst',
 'cell_14_call_1_ag3_plot_pairwise_average_fst': '06_ag3_pairwise_average_fst',
 'cell_15_call_1_ag3_plot_pairwise_average_fst': '07_ag3_pairwise_average_fst',
 'cell_17_call_1_ag3_plot_pairwise_average_fst': '08_ag3_pairwise_average_fst'}


def run(API_KEEP_CALLSITE_VALUE, PERFORMANCE_CSV_PATH, API_CALL_PARAMETERS):
    # --- Notebook cell 1 ---
    nbrt.start_cell("notebook_cell_1")
    import inspect
    from memory_profiler import memory_usage
    import time
    import json
    import csv
    from pathlib import Path

    def _parameter_value_for_csv(value):
        if value is None or isinstance(value, (str, int, float, bool)):
            return value
        if isinstance(value, dict):
            return {str(key): _parameter_value_for_csv(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [_parameter_value_for_csv(item) for item in value]
        shape = getattr(value, "shape", None)
        if shape is not None:
            return {
                "type": f"{type(value).__module__}.{type(value).__qualname__}",
                "shape": list(shape),
            }
        return repr(value)


    def _call_api_with_parameters(method, call_key, *args, **kwargs):
        signature = inspect.signature(method)
        bound = signature.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        for name, value in API_CALL_PARAMETERS[call_key].items():
            if not (isinstance(value, str) and value == API_KEEP_CALLSITE_VALUE):
                bound.arguments[name] = value

        positional = []
        keyword = {}
        for parameter in signature.parameters.values():
            if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
                if parameter.name in bound.arguments:
                    positional.append(bound.arguments[parameter.name])
            elif parameter.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD:
                if parameter.name in bound.arguments:
                    keyword[parameter.name] = bound.arguments[parameter.name]
            elif parameter.kind is inspect.Parameter.VAR_POSITIONAL:
                positional.extend(bound.arguments.get(parameter.name, ()))
            elif parameter.kind is inspect.Parameter.KEYWORD_ONLY:
                if parameter.name in bound.arguments:
                    keyword[parameter.name] = bound.arguments[parameter.name]
            elif parameter.kind is inspect.Parameter.VAR_KEYWORD:
                keyword.update(bound.arguments.get(parameter.name, {}))
        result = {}

        def operation():
            result["value"] = method(*positional, **keyword)

        start_time = time.perf_counter()
        peak_memory_mib = memory_usage((operation, ()), max_usage=True)
        runtime_sec = time.perf_counter() - start_time

        output_path = Path(PERFORMANCE_CSV_PATH)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [
            "call_key",
            "method",
            "parameters_json",
            "runtime_sec",
            "peak_memory_mib",
        ]
        record = {
            "call_key": call_key,
            "method": getattr(method, "__qualname__", getattr(method, "__name__", repr(method))),
            "parameters_json": json.dumps(
                {
                    name: _parameter_value_for_csv(value)
                    for name, value in bound.arguments.items()
                },
                sort_keys=True,
            ),
            "runtime_sec": round(runtime_sec, 4),
            "peak_memory_mib": round(peak_memory_mib, 2),
        }
        file_exists = output_path.exists() and output_path.stat().st_size > 0
        with output_path.open("a", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(record)

        return result["value"]
    # Name figures after the API call that produced them.
    _call_api_with_parameters = nbrt.track_api_calls(_call_api_with_parameters)
    # --- Notebook cell 2 ---
    nbrt.start_cell("notebook_cell_2")
    import malariagen_data
    import allel
    import pandas as pd
    import numpy as np
    import plotly.express as px
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20240717",
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.shell('rm -rf results_cache')
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    region = "3L:15,000,000-16,000,000"
    site_mask = "gamb_colu"
    n_jack = 200
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    fst_hudson, se_hudson = _call_api_with_parameters(ag3.average_fst, 'cell_5_call_1_ag3_average_fst', region=region, cohort1_query="cohort_admin2_year == 'ML-2_Kati_colu_2014'", cohort2_query="cohort_admin2_year == 'ML-2_Kati_gamb_2014'", sample_sets="3.0", n_jack=n_jack, site_mask=site_mask)
    nbrt.display(fst_hudson, se_hudson)
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    pairwise_fst_df = _call_api_with_parameters(ag3.pairwise_average_fst, 'cell_6_call_1_ag3_pairwise_average_fst', region=region, cohorts="cohort_admin1_year", sample_query="country == 'Mali' and taxon == 'gambiae'", sample_sets="3.0", n_jack=n_jack, site_mask=site_mask)
    nbrt.display(pairwise_fst_df)
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_7_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_8_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df, annotation="standard error"))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_9_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df, annotation="Z score"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_10_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df, zmax=0.1, width=400, height=300))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    region = "3L:15,000,000-16,000,000"
    site_mask = "arab"
    n_jack = 200
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    pairwise_fst_df = _call_api_with_parameters(ag3.pairwise_average_fst, 'cell_12_call_1_ag3_pairwise_average_fst', region=region, cohorts="cohort_admin1_year", sample_query="country == 'Kenya' and taxon == 'arabiensis'", sample_sets=["AG1000G-KE", "1274-VO-KE-KAMAU-VMF00246"], n_jack=n_jack, site_mask=site_mask, min_cohort_size=10)
    nbrt.display(pairwise_fst_df)
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_13_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_14_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df, annotation="standard error"))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_15_call_1_ag3_plot_pairwise_average_fst', pairwise_fst_df, annotation="Z score", zmax=0.03))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    wild_cohorts = {
        "Mwea_2007": "taxon == 'arabiensis' and location == 'Mwea' and year == 2007",
        "Mwea_2014": "taxon == 'arabiensis' and location == 'Mwea' and year == 2014",
        "Teso_2013": "taxon == 'arabiensis' and location == 'Teso'",
        "Turkana_2006": "taxon == 'arabiensis' and location == 'Turkana'",
        "Kilifi_2012": "taxon == 'arabiensis' and location == 'Kilifi' and year == 2012",
    }
    fst_df = _call_api_with_parameters(ag3.pairwise_average_fst, 'cell_16_call_1_ag3_pairwise_average_fst', region="3L:15,000,000-16,000,000", cohorts=wild_cohorts, min_cohort_size=10, site_mask="arab")
    nbrt.display(fst_df)
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(ag3.plot_pairwise_average_fst, 'cell_17_call_1_ag3_plot_pairwise_average_fst', fst_df, annotation="Z score", zmax=0.4))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_pairwise_average_fst.ipynb',
        run=run,
        parameters={
            'API_KEEP_CALLSITE_VALUE': API_KEEP_CALLSITE_VALUE,
            'PERFORMANCE_CSV_PATH': PERFORMANCE_CSV_PATH,
            'API_CALL_PARAMETERS': API_CALL_PARAMETERS,
            'FIGURE_DIR': FIGURE_DIR,
            'FIGURE_FORMAT': FIGURE_FORMAT,
            'FIGURE_NAMES': FIGURE_NAMES,
        },
    )
