#!/usr/bin/env python3
"""plot_cnv: the code from notebooks/plot_cnv.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_cnv.py                      # the notebook's defaults
    python scripts/plot_cnv.py --config runs.csv    # one run per CSV row
    python scripts/plot_cnv.py --list-parameters    # what a CSV can set
    python scripts/plot_cnv.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_cnv_performance.csv'
API_CALL_PARAMETERS = {'cell_6_call_1_ag3_plot_cnv_hmm_coverage_track': {'sample': 'AP0021-C',
                                                   'region': '2R:28,460,000-28,580,000',
                                                   'sample_set': None,
                                                   'y_max': 'auto',
                                                   'sizing_mode': 'stretch_width',
                                                   'width': None,
                                                   'height': 200,
                                                   'circle_kwargs': None,
                                                   'line_kwargs': None,
                                                   'show': True,
                                                   'x_range': None,
                                                   'output_backend': 'webgl'},
 'cell_7_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0091-C',
                                             'region': '2R:28,460,000-28,580,000',
                                             'sample_set': None,
                                             'y_max': 'auto',
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'track_height': 170,
                                             'genes_height': 90,
                                             'circle_kwargs': None,
                                             'line_kwargs': None,
                                             'show': True,
                                             'output_backend': 'webgl',
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_8_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0072-C',
                                             'region': '2R:28,460,000-28,580,000',
                                             'sample_set': None,
                                             'y_max': 'auto',
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'track_height': 170,
                                             'genes_height': 90,
                                             'circle_kwargs': None,
                                             'line_kwargs': None,
                                             'show': True,
                                             'output_backend': 'webgl',
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_9_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0062-C',
                                             'region': '2R:28,460,000-28,580,000',
                                             'sample_set': None,
                                             'y_max': 'auto',
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'track_height': 170,
                                             'genes_height': 90,
                                             'circle_kwargs': None,
                                             'line_kwargs': None,
                                             'show': True,
                                             'output_backend': 'webgl',
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_10_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0039-C',
                                              'region': '2R:28,460,000-28,580,000',
                                              'sample_set': None,
                                              'y_max': 'auto',
                                              'sizing_mode': 'stretch_width',
                                              'width': None,
                                              'track_height': 170,
                                              'genes_height': 90,
                                              'circle_kwargs': None,
                                              'line_kwargs': None,
                                              'show': True,
                                              'output_backend': 'webgl',
                                              'gene_labels': None,
                                              'gene_labelset': None},
 'cell_11_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AG0382-CW',
                                              'region': '2R:28,460,000-28,580,000',
                                              'sample_set': None,
                                              'y_max': 'auto',
                                              'sizing_mode': 'stretch_width',
                                              'width': None,
                                              'track_height': 170,
                                              'genes_height': 90,
                                              'circle_kwargs': None,
                                              'line_kwargs': None,
                                              'show': True,
                                              'output_backend': 'webgl',
                                              'gene_labels': None,
                                              'gene_labelset': None},
 'cell_13_call_1_af1_plot_cnv_hmm_coverage_track': {'sample': 'VBS24196',
                                                    'region': '2RL:28,460,000-28,580,000',
                                                    'sample_set': None,
                                                    'y_max': 'auto',
                                                    'sizing_mode': 'stretch_width',
                                                    'width': None,
                                                    'height': 200,
                                                    'circle_kwargs': None,
                                                    'line_kwargs': None,
                                                    'show': True,
                                                    'x_range': None,
                                                    'output_backend': 'webgl'},
 'cell_16_call_1_ag3_plot_cnv_hmm_heatmap_track': {'region': '2R:28,460,000-28,580,000',
                                                   'sample_sets': 'AG1000G-FR',
                                                   'sample_query': None,
                                                   'sample_query_options': None,
                                                   'max_coverage_variance': 0.2,
                                                   'sizing_mode': 'stretch_width',
                                                   'width': None,
                                                   'row_height': 7,
                                                   'height': None,
                                                   'palette': None,
                                                   'show': True,
                                                   'output_backend': 'webgl'},
 'cell_17_call_1_ag3_plot_cnv_hmm_heatmap_track': {'region': '2R:28,460,000-28,580,000',
                                                   'sample_sets': ['AG1000G-FR', 'AG1000G-GQ'],
                                                   'sample_query': None,
                                                   'sample_query_options': None,
                                                   'max_coverage_variance': 0.2,
                                                   'sizing_mode': 'stretch_width',
                                                   'width': None,
                                                   'row_height': 7,
                                                   'height': None,
                                                   'palette': None,
                                                   'show': True,
                                                   'output_backend': 'webgl'},
 'cell_18_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-BF-A',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_19_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-BF-A',
                                             'sample_query': "taxon == 'gambiae'",
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_20_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-BF-A',
                                             'sample_query': "taxon == 'coluzzii'",
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_21_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-CI',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_22_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-CI',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': None,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_23_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-GM-B',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': None,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_25_call_1_af1_plot_cnv_hmm_heatmap': {'region': '2RL:28,520,000-28,570,000',
                                             'sample_sets': '1230-VO-GA-CF-AYALA-VMF00045',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': None,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_cnv'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_6_call_1_ag3_plot_cnv_hmm_coverage_track': '01_ag3_cnv_hmm_coverage_track_AP0021-C',
 'cell_7_call_1_ag3_plot_cnv_hmm_coverage': '02_ag3_cnv_hmm_coverage_AY0091-C',
 'cell_8_call_1_ag3_plot_cnv_hmm_coverage': '03_ag3_cnv_hmm_coverage_AY0072-C',
 'cell_9_call_1_ag3_plot_cnv_hmm_coverage': '04_ag3_cnv_hmm_coverage_AY0062-C',
 'cell_10_call_1_ag3_plot_cnv_hmm_coverage': '05_ag3_cnv_hmm_coverage_AY0039-C',
 'cell_11_call_1_ag3_plot_cnv_hmm_coverage': '06_ag3_cnv_hmm_coverage_AG0382-CW',
 'cell_13_call_1_af1_plot_cnv_hmm_coverage_track': '07_af1_cnv_hmm_coverage_track_VBS24196',
 'cell_16_call_1_ag3_plot_cnv_hmm_heatmap_track': '08_ag3_cnv_hmm_heatmap_track',
 'cell_17_call_1_ag3_plot_cnv_hmm_heatmap_track': '09_ag3_cnv_hmm_heatmap_track',
 'cell_18_call_1_ag3_plot_cnv_hmm_heatmap': '10_ag3_cnv_hmm_heatmap',
 'cell_19_call_1_ag3_plot_cnv_hmm_heatmap': '11_ag3_cnv_hmm_heatmap',
 'cell_20_call_1_ag3_plot_cnv_hmm_heatmap': '12_ag3_cnv_hmm_heatmap',
 'cell_21_call_1_ag3_plot_cnv_hmm_heatmap': '13_ag3_cnv_hmm_heatmap',
 'cell_22_call_1_ag3_plot_cnv_hmm_heatmap': '14_ag3_cnv_hmm_heatmap',
 'cell_23_call_1_ag3_plot_cnv_hmm_heatmap': '15_ag3_cnv_hmm_heatmap',
 'cell_25_call_1_af1_plot_cnv_hmm_heatmap': '16_af1_cnv_hmm_heatmap'}


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
    import dask
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
    )
    nbrt.display(af1)
    # ## CNV HMM coverage
    # ### Ag3
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    # sample with no CNV
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage_track, 'cell_6_call_1_ag3_plot_cnv_hmm_coverage_track', sample="AP0021-C", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    # sample with a small CNV
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_7_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0091-C", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    # sample with a big CNV
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_8_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0072-C", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    # sample with a complex CNV
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_9_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0062-C", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    # sample with a complex CNV
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_10_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0039-C", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    # sample with high coverage variance
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_11_call_1_ag3_plot_cnv_hmm_coverage', sample="AG0382-CW", region="2R:28,460,000-28,580,000"))
    # ### Af1
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    # sample with a small CNV
    nbrt.display(_call_api_with_parameters(af1.plot_cnv_hmm_coverage_track, 'cell_13_call_1_af1_plot_cnv_hmm_coverage_track', sample="VBS24196", region="2RL:28,460,000-28,580,000"))
    # ## CNV HMM heatmap
    # ### Ag3
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap_track, 'cell_16_call_1_ag3_plot_cnv_hmm_heatmap_track', sample_sets="AG1000G-FR", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap_track, 'cell_17_call_1_ag3_plot_cnv_hmm_heatmap_track', sample_sets=["AG1000G-FR", "AG1000G-GQ"], region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_18_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-BF-A", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_19_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-BF-A", sample_query="taxon == 'gambiae'", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_20_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-BF-A", sample_query="taxon == 'coluzzii'", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_21_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-CI", region="2R:28,460,000-28,580,000"))
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_22_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-CI", region="2R:28,460,000-28,580,000", max_coverage_variance=None))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_23_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-GM-B", region="2R:28,460,000-28,580,000", max_coverage_variance=None))
    # ### Af1
    # --- Notebook cell 26 ---
    nbrt.start_cell("notebook_cell_26")
    nbrt.display(_call_api_with_parameters(af1.plot_cnv_hmm_heatmap, 'cell_25_call_1_af1_plot_cnv_hmm_heatmap', sample_sets="1230-VO-GA-CF-AYALA-VMF00045", region="2RL:28,520,000-28,570,000", max_coverage_variance=None))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_cnv.ipynb',
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
