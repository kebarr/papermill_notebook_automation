#!/usr/bin/env python3
"""plot_h12_h1x: the code from notebooks/plot_h12_h1x.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_h12_h1x.py                      # the notebook's defaults
    python scripts/plot_h12_h1x.py --config runs.csv    # one run per CSV row
    python scripts/plot_h12_h1x.py --list-parameters    # what a CSV can set

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
PERFORMANCE_CSV_PATH = 'plot_h12_h1x_performance.csv'
API_CALL_PARAMETERS = {'cell_7_call_1_ag3_plot_h12_calibration': {'contig': '__KEEP_CALLSITE_VALUE__',
                                            'analysis': 'gamb_colu',
                                            'sample_query': None,
                                            'sample_query_options': None,
                                            'sample_sets': '3.0',
                                            'cohort_size': None,
                                            'min_cohort_size': 15,
                                            'max_cohort_size': 50,
                                            'window_sizes': (100,
                                                             200,
                                                             500,
                                                             1000,
                                                             2000,
                                                             5000,
                                                             10000,
                                                             20000),
                                            'random_seed': 42,
                                            'title': None,
                                            'show': True,
                                            'chunks': 'native',
                                            'inline_array': True},
 'cell_8_call_1_ag3_plot_h12_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                     'window_size': 2000,
                                     'analysis': 'gamb_colu',
                                     'sample_sets': '3.0',
                                     'sample_query': None,
                                     'sample_query_options': None,
                                     'cohort_size': 20,
                                     'min_cohort_size': 15,
                                     'max_cohort_size': 50,
                                     'random_seed': 42,
                                     'title': None,
                                     'sizing_mode': 'stretch_width',
                                     'width': None,
                                     'track_height': 170,
                                     'contig_colors': ['#393b79',
                                                       '#5254a3',
                                                       '#6b6ecf',
                                                       '#9c9ede',
                                                       '#637939'],
                                     'genes_height': 90,
                                     'show': True,
                                     'output_backend': 'webgl',
                                     'chunks': 'native',
                                     'inline_array': True,
                                     'gene_labels': None,
                                     'gene_labelset': None},
 'cell_9_call_1_ag3_plot_h12_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                     'window_size': 2000,
                                     'analysis': 'gamb_colu',
                                     'sample_sets': '3.0',
                                     'sample_query': None,
                                     'sample_query_options': None,
                                     'cohort_size': 20,
                                     'min_cohort_size': 15,
                                     'max_cohort_size': 50,
                                     'random_seed': 42,
                                     'title': None,
                                     'sizing_mode': 'stretch_width',
                                     'width': None,
                                     'track_height': 170,
                                     'contig_colors': ['#393b79',
                                                       '#5254a3',
                                                       '#6b6ecf',
                                                       '#9c9ede',
                                                       '#637939'],
                                     'genes_height': 90,
                                     'show': True,
                                     'output_backend': 'webgl',
                                     'chunks': 'native',
                                     'inline_array': True,
                                     'gene_labels': None,
                                     'gene_labelset': None},
 'cell_10_call_1_ag3_plot_h12_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'analysis': 'gamb_colu',
                                      'sample_sets': '3.0',
                                      'sample_query': None,
                                      'sample_query_options': None,
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 170,
                                      'contig_colors': ['#393b79',
                                                        '#5254a3',
                                                        '#6b6ecf',
                                                        '#9c9ede',
                                                        '#637939'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'canvas',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None},
 'cell_11_call_1_ag3_plot_h12_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'analysis': 'gamb_colu',
                                      'sample_sets': '3.0',
                                      'sample_query': None,
                                      'sample_query_options': None,
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 170,
                                      'contig_colors': ['#393b79',
                                                        '#5254a3',
                                                        '#6b6ecf',
                                                        '#9c9ede',
                                                        '#637939'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'webgl',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None},
 'cell_12_call_1_ag3_plot_h1x_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'cohort1_query': '__KEEP_CALLSITE_VALUE__',
                                      'cohort2_query': '__KEEP_CALLSITE_VALUE__',
                                      'sample_query_options': None,
                                      'analysis': 'gamb_colu',
                                      'sample_sets': '3.0',
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 190,
                                      'contig_colors': ['#393b79',
                                                        '#5254a3',
                                                        '#6b6ecf',
                                                        '#9c9ede',
                                                        '#637939'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'webgl',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None},
 'cell_13_call_1_ag3_plot_h1x_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'cohort1_query': '__KEEP_CALLSITE_VALUE__',
                                      'cohort2_query': '__KEEP_CALLSITE_VALUE__',
                                      'sample_query_options': None,
                                      'analysis': 'gamb_colu',
                                      'sample_sets': '3.0',
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 190,
                                      'contig_colors': ['red', 'green'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'webgl',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None},
 'cell_14_call_1_ag3_count_samples': {'sample_sets': 'AG1000G-ML-A',
                                      'sample_query': None,
                                      'sample_query_options': None,
                                      'sample_indices': None,
                                      'index': ('country',
                                                'admin1_iso',
                                                'admin1_name',
                                                'admin2_name',
                                                'year'),
                                      'columns': 'taxon'},
 'cell_15_call_1_ag3_plot_h12_gwss_multi_overlay': {'contig': '__KEEP_CALLSITE_VALUE__',
                                                    'cohorts': 'admin2_year',
                                                    'window_size': 2000,
                                                    'cohort_size': 20,
                                                    'sample_query': None,
                                                    'analysis': 'gamb_colu',
                                                    'min_cohort_size': 15,
                                                    'max_cohort_size': 50,
                                                    'sample_query_options': None,
                                                    'sample_sets': 'AG1000G-ML-A',
                                                    'colors': ('#1f77b4',
                                                               '#ff7f0e',
                                                               '#2ca02c',
                                                               '#d62728',
                                                               '#9467bd',
                                                               '#8c564b',
                                                               '#e377c2',
                                                               '#7f7f7f',
                                                               '#bcbd22',
                                                               '#17becf'),
                                                    'random_seed': 42,
                                                    'title': None,
                                                    'sizing_mode': 'stretch_width',
                                                    'width': None,
                                                    'track_height': 170,
                                                    'genes_height': 90,
                                                    'show': True,
                                                    'output_backend': 'webgl',
                                                    'gene_labels': None,
                                                    'gene_labelset': None,
                                                    'chunks': 'native',
                                                    'inline_array': True},
 'cell_16_call_1_ag3_plot_h12_gwss_multi_panel': {'contig': '__KEEP_CALLSITE_VALUE__',
                                                  'cohorts': 'admin2_year',
                                                  'window_size': 2000,
                                                  'cohort_size': 20,
                                                  'sample_query': None,
                                                  'analysis': 'gamb_colu',
                                                  'min_cohort_size': 15,
                                                  'max_cohort_size': 50,
                                                  'sample_query_options': None,
                                                  'sample_sets': 'AG1000G-ML-A',
                                                  'random_seed': 42,
                                                  'sizing_mode': 'stretch_width',
                                                  'width': None,
                                                  'track_height': 170,
                                                  'genes_height': 90,
                                                  'show': True,
                                                  'output_backend': 'webgl',
                                                  'gene_labels': None,
                                                  'gene_labelset': None,
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_22_call_1_af1_plot_h12_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'analysis': 'default',
                                      'sample_sets': '1.0',
                                      'sample_query': None,
                                      'sample_query_options': None,
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 170,
                                      'contig_colors': ['#393b79',
                                                        '#5254a3',
                                                        '#6b6ecf',
                                                        '#9c9ede',
                                                        '#637939'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'webgl',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None},
 'cell_23_call_1_af1_plot_h12_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'analysis': 'default',
                                      'sample_sets': '1.0',
                                      'sample_query': None,
                                      'sample_query_options': None,
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 170,
                                      'contig_colors': ['#393b79',
                                                        '#5254a3',
                                                        '#6b6ecf',
                                                        '#9c9ede',
                                                        '#637939'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'webgl',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None},
 'cell_25_call_1_af1_plot_h12_gwss_multi_overlay': {'contig': '__KEEP_CALLSITE_VALUE__',
                                                    'cohorts': '__KEEP_CALLSITE_VALUE__',
                                                    'window_size': '__KEEP_CALLSITE_VALUE__',
                                                    'cohort_size': 20,
                                                    'sample_query': None,
                                                    'analysis': 'default',
                                                    'min_cohort_size': 15,
                                                    'max_cohort_size': 50,
                                                    'sample_query_options': None,
                                                    'sample_sets': '1.0',
                                                    'colors': ('#1f77b4',
                                                               '#ff7f0e',
                                                               '#2ca02c',
                                                               '#d62728',
                                                               '#9467bd',
                                                               '#8c564b',
                                                               '#e377c2',
                                                               '#7f7f7f',
                                                               '#bcbd22',
                                                               '#17becf'),
                                                    'random_seed': 42,
                                                    'title': None,
                                                    'sizing_mode': 'stretch_width',
                                                    'width': None,
                                                    'track_height': 170,
                                                    'genes_height': 90,
                                                    'show': True,
                                                    'output_backend': 'webgl',
                                                    'gene_labels': None,
                                                    'gene_labelset': None,
                                                    'chunks': 'native',
                                                    'inline_array': True},
 'cell_26_call_1_af1_plot_h12_gwss_multi_panel': {'contig': '__KEEP_CALLSITE_VALUE__',
                                                  'cohorts': '__KEEP_CALLSITE_VALUE__',
                                                  'window_size': '__KEEP_CALLSITE_VALUE__',
                                                  'cohort_size': 20,
                                                  'sample_query': None,
                                                  'analysis': 'default',
                                                  'min_cohort_size': 15,
                                                  'max_cohort_size': 50,
                                                  'sample_query_options': None,
                                                  'sample_sets': '1.0',
                                                  'random_seed': 42,
                                                  'sizing_mode': 'stretch_width',
                                                  'width': None,
                                                  'track_height': 170,
                                                  'genes_height': 90,
                                                  'show': True,
                                                  'output_backend': 'webgl',
                                                  'gene_labels': None,
                                                  'gene_labelset': None,
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_27_call_1_af1_plot_h1x_gwss': {'contig': '__KEEP_CALLSITE_VALUE__',
                                      'window_size': 2000,
                                      'cohort1_query': '__KEEP_CALLSITE_VALUE__',
                                      'cohort2_query': '__KEEP_CALLSITE_VALUE__',
                                      'sample_query_options': None,
                                      'analysis': 'default',
                                      'sample_sets': '1.0',
                                      'cohort_size': 20,
                                      'min_cohort_size': 15,
                                      'max_cohort_size': 50,
                                      'random_seed': 42,
                                      'title': None,
                                      'sizing_mode': 'stretch_width',
                                      'width': None,
                                      'track_height': 190,
                                      'contig_colors': ['#393b79',
                                                        '#5254a3',
                                                        '#6b6ecf',
                                                        '#9c9ede',
                                                        '#637939'],
                                      'genes_height': 90,
                                      'show': True,
                                      'output_backend': 'webgl',
                                      'chunks': 'native',
                                      'inline_array': True,
                                      'gene_labels': None,
                                      'gene_labelset': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_h12_h1x'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_7_call_1_ag3_plot_h12_calibration': '01_ag3_h12_calibration',
 'cell_8_call_1_ag3_plot_h12_gwss': '02_ag3_h12_gwss',
 'cell_9_call_1_ag3_plot_h12_gwss': '03_ag3_h12_gwss',
 'cell_10_call_1_ag3_plot_h12_gwss': '04_ag3_h12_gwss',
 'cell_11_call_1_ag3_plot_h12_gwss': '05_ag3_h12_gwss',
 'cell_12_call_1_ag3_plot_h1x_gwss': '06_ag3_h1x_gwss',
 'cell_13_call_1_ag3_plot_h1x_gwss': '07_ag3_h1x_gwss',
 'cell_15_call_1_ag3_plot_h12_gwss_multi_overlay': '08_ag3_h12_gwss_multi_overlay',
 'cell_16_call_1_ag3_plot_h12_gwss_multi_panel': '09_ag3_h12_gwss_multi_panel',
 'cell_22_call_1_af1_plot_h12_gwss': '10_af1_h12_gwss',
 'cell_23_call_1_af1_plot_h12_gwss': '11_af1_h12_gwss',
 'cell_25_call_1_af1_plot_h12_gwss_multi_overlay': '12_af1_h12_gwss_multi_overlay',
 'cell_26_call_1_af1_plot_h12_gwss_multi_panel': '13_af1_h12_gwss_multi_panel',
 'cell_27_call_1_af1_plot_h1x_gwss': '14_af1_h1x_gwss'}


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
    import numpy as np
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    import malariagen_data
    # ## Ag3
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230516",
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.shell('rm -rf results_cache')
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    coh1 = "ML-2_Kati_colu_2014"
    coh2 = "ML-2_Kati_gamb_2014"
    coh1_query = f"cohort_admin2_year == '{coh1}'"
    coh2_query = f"cohort_admin2_year == '{coh2}'"
    contig = "2L"
    contigs = "2RL"
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_calibration, 'cell_7_call_1_ag3_plot_h12_calibration', contig=contig, analysis="gamb_colu", sample_query=coh1_query, sample_sets="3.0"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_gwss, 'cell_8_call_1_ag3_plot_h12_gwss', contig=contig, analysis="gamb_colu", window_size=2000, sample_query=coh1_query, sample_sets="3.0", cohort_size=20))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_gwss, 'cell_9_call_1_ag3_plot_h12_gwss', contig=contigs, analysis="gamb_colu", window_size=2000, sample_query=coh1_query, sample_sets="3.0", cohort_size=20))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_gwss, 'cell_10_call_1_ag3_plot_h12_gwss', contig=contig, analysis="gamb_colu", window_size=2000, sample_query=coh1_query, sample_sets="3.0", cohort_size=20, output_backend="canvas"))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_gwss, 'cell_11_call_1_ag3_plot_h12_gwss', contig=contig, analysis="gamb_colu", window_size=2000, sample_query=coh2_query, sample_sets="3.0", cohort_size=20))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.plot_h1x_gwss, 'cell_12_call_1_ag3_plot_h1x_gwss', contig=contig, window_size=2000, cohort1_query=coh1_query, cohort2_query=coh2_query, sample_sets="3.0", analysis="gamb_colu", cohort_size=20))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_h1x_gwss, 'cell_13_call_1_ag3_plot_h1x_gwss', contig=contigs, window_size=2000, cohort1_query=coh1_query, cohort2_query=coh2_query, sample_sets="3.0", analysis="gamb_colu", cohort_size=20, contig_colors=["red", "green"]))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(ag3.count_samples, 'cell_14_call_1_ag3_count_samples', sample_sets="AG1000G-ML-A"))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_gwss_multi_overlay, 'cell_15_call_1_ag3_plot_h12_gwss_multi_overlay', contig=contig, window_size=2000, cohorts="admin2_year", sample_sets="AG1000G-ML-A", analysis="gamb_colu", cohort_size=20))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(ag3.plot_h12_gwss_multi_panel, 'cell_16_call_1_ag3_plot_h12_gwss_multi_panel', contig=contig, window_size=2000, cohorts="admin2_year", sample_sets="AG1000G-ML-A", analysis="gamb_colu", cohort_size=20))
    # ## Af1
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230823",
        results_cache="results_cache",
    )
    nbrt.display(af1)
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    coh1 = "GH-NP_Kumbungu_fune_2017"
    coh2 = "GH-AH_Adansi-Akrofuom_fune_2014"
    coh1_query = f"cohort_admin2_year == '{coh1}'"
    coh2_query = f"cohort_admin2_year == '{coh2}'"
    contig = "2RL"
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(_call_api_with_parameters(af1.plot_h12_gwss, 'cell_22_call_1_af1_plot_h12_gwss', contig=contig, window_size=2000, sample_query=coh1_query, sample_sets="1.0", cohort_size=20))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(af1.plot_h12_gwss, 'cell_23_call_1_af1_plot_h12_gwss', contig=contig, window_size=2000, sample_query=coh2_query, sample_sets="1.0", cohort_size=20))
    # --- Notebook cell 25 ---
    nbrt.start_cell("notebook_cell_25")
    cohorts = {
        "cohort1": coh1_query,
        "cohort2": coh2_query,
    }
    window_size = {
        "cohort1": 2000,
        "cohort2": 1500,
    }
    # --- Notebook cell 26 ---
    nbrt.start_cell("notebook_cell_26")
    nbrt.display(_call_api_with_parameters(af1.plot_h12_gwss_multi_overlay, 'cell_25_call_1_af1_plot_h12_gwss_multi_overlay', contig=contig, window_size=window_size, cohorts=cohorts, sample_sets="1.0", cohort_size=20))
    # --- Notebook cell 27 ---
    nbrt.start_cell("notebook_cell_27")
    nbrt.display(_call_api_with_parameters(af1.plot_h12_gwss_multi_panel, 'cell_26_call_1_af1_plot_h12_gwss_multi_panel', contig=contig, window_size=window_size, cohorts=cohorts, sample_sets="1.0", cohort_size=20))
    # --- Notebook cell 28 ---
    nbrt.start_cell("notebook_cell_28")
    nbrt.display(_call_api_with_parameters(af1.plot_h1x_gwss, 'cell_27_call_1_af1_plot_h1x_gwss', contig=contig, window_size=2000, cohort1_query=coh1_query, cohort2_query=coh2_query, sample_sets="1.0", cohort_size=20))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_h12_h1x.ipynb',
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
