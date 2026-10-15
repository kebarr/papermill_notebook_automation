#!/usr/bin/env python3
"""plot_g123_gwss: the code from notebooks/plot_g123_gwss.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_g123_gwss.py                      # the notebook's defaults
    python scripts/plot_g123_gwss.py --config runs.csv    # one run per CSV row
    python scripts/plot_g123_gwss.py --list-parameters    # what a CSV can set

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
PERFORMANCE_CSV_PATH = 'plot_g123_gwss_performance.csv'
API_CALL_PARAMETERS = {'cell_5_call_1_ag3_plot_g123_calibration': {'contig': '__KEEP_CALLSITE_VALUE__',
                                             'sites': '__KEEP_CALLSITE_VALUE__',
                                             'site_mask': 'default',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'sample_sets': None,
                                             'min_cohort_size': 20,
                                             'max_cohort_size': 50,
                                             'window_sizes': (100, 200, 500, 1000, 2000, 5000),
                                             'random_seed': 42,
                                             'title': None,
                                             'show': True,
                                             'inline_array': True,
                                             'chunks': 'native'},
 'cell_6_call_1_ag3_plot_g123_calibration': {'contig': '__KEEP_CALLSITE_VALUE__',
                                             'sites': '__KEEP_CALLSITE_VALUE__',
                                             'site_mask': 'default',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'sample_sets': None,
                                             'min_cohort_size': 20,
                                             'max_cohort_size': 50,
                                             'window_sizes': (100, 200, 500, 1000, 2000, 5000),
                                             'random_seed': 42,
                                             'title': None,
                                             'show': True,
                                             'inline_array': True,
                                             'chunks': 'native'},
 'cell_7_call_1_ag3_plot_g123_gwss_track': {'contig': '2L',
                                            'window_size': 1000,
                                            'sites': 'segregating',
                                            'site_mask': 'default',
                                            'sample_sets': None,
                                            'sample_query': None,
                                            'sample_query_options': None,
                                            'min_cohort_size': 20,
                                            'max_cohort_size': 10,
                                            'random_seed': 42,
                                            'title': None,
                                            'sizing_mode': 'stretch_width',
                                            'width': None,
                                            'height': 200,
                                            'show': True,
                                            'x_range': None,
                                            'output_backend': 'webgl',
                                            'inline_array': True,
                                            'chunks': 'native'},
 'cell_8_call_1_ag3_plot_g123_gwss_track': {'contig': '2L',
                                            'window_size': 1000,
                                            'sites': 'segregating',
                                            'site_mask': 'default',
                                            'sample_sets': None,
                                            'sample_query': None,
                                            'sample_query_options': None,
                                            'min_cohort_size': 20,
                                            'max_cohort_size': 10,
                                            'random_seed': 42,
                                            'title': None,
                                            'sizing_mode': 'stretch_width',
                                            'width': None,
                                            'height': 200,
                                            'show': True,
                                            'x_range': None,
                                            'output_backend': 'webgl',
                                            'inline_array': True,
                                            'chunks': 'native'},
 'cell_9_call_1_ag3_plot_g123_gwss_track': {'contig': '2L',
                                            'window_size': 1000,
                                            'sites': 'segregating',
                                            'site_mask': 'default',
                                            'sample_sets': None,
                                            'sample_query': None,
                                            'sample_query_options': None,
                                            'min_cohort_size': 20,
                                            'max_cohort_size': 30,
                                            'random_seed': 42,
                                            'title': None,
                                            'sizing_mode': 'fixed',
                                            'width': 700,
                                            'height': 200,
                                            'show': True,
                                            'x_range': None,
                                            'output_backend': 'webgl',
                                            'inline_array': True,
                                            'chunks': 'native'},
 'cell_10_call_1_ag3_plot_g123_gwss': {'contig': '2L',
                                       'window_size': 1000,
                                       'sites': 'all',
                                       'site_mask': 'default',
                                       'sample_sets': None,
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'min_cohort_size': 10,
                                       'max_cohort_size': 20,
                                       'random_seed': 42,
                                       'title': None,
                                       'sizing_mode': 'stretch_width',
                                       'width': None,
                                       'track_height': 170,
                                       'genes_height': 90,
                                       'show': True,
                                       'output_backend': 'webgl',
                                       'inline_array': True,
                                       'chunks': 'native',
                                       'gene_labels': None,
                                       'gene_labelset': None},
 'cell_11_call_1_ag3_plot_g123_gwss': {'contig': '2L',
                                       'window_size': 1000,
                                       'sites': 'segregating',
                                       'site_mask': 'default',
                                       'sample_sets': None,
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'min_cohort_size': 20,
                                       'max_cohort_size': None,
                                       'random_seed': 42,
                                       'title': None,
                                       'sizing_mode': 'stretch_width',
                                       'width': None,
                                       'track_height': 170,
                                       'genes_height': 90,
                                       'show': True,
                                       'output_backend': 'webgl',
                                       'inline_array': True,
                                       'chunks': 'native',
                                       'gene_labels': None,
                                       'gene_labelset': None},
 'cell_12_call_1_af1_sample_sets': {'release': '1.0'},
 'cell_13_call_1_af1_sample_metadata': {'sample_sets': '1.0',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_14_call_1_af1_plot_g123_gwss': {'contig': 'X',
                                       'window_size': 2000,
                                       'sites': 'segregating',
                                       'site_mask': 'funestus',
                                       'sample_sets': '1232-VO-KE-OCHOMO-VMF00044',
                                       'sample_query': "cohort_admin1_year == 'KE-03_fune_2016'",
                                       'sample_query_options': None,
                                       'min_cohort_size': 20,
                                       'max_cohort_size': 20,
                                       'random_seed': 42,
                                       'title': None,
                                       'sizing_mode': 'stretch_width',
                                       'width': None,
                                       'track_height': 170,
                                       'genes_height': 90,
                                       'show': True,
                                       'output_backend': 'webgl',
                                       'inline_array': True,
                                       'chunks': 'native',
                                       'gene_labels': None,
                                       'gene_labelset': None},
 'cell_15_call_1_af1_plot_g123_gwss': {'contig': 'X',
                                       'window_size': 2000,
                                       'sites': 'funestus',
                                       'site_mask': 'funestus',
                                       'sample_sets': '1232-VO-KE-OCHOMO-VMF00044',
                                       'sample_query': "cohort_admin1_year == 'KE-03_fune_2016'",
                                       'sample_query_options': None,
                                       'min_cohort_size': 20,
                                       'max_cohort_size': None,
                                       'random_seed': 42,
                                       'title': None,
                                       'sizing_mode': 'stretch_width',
                                       'width': None,
                                       'track_height': 170,
                                       'genes_height': 90,
                                       'show': True,
                                       'output_backend': 'webgl',
                                       'inline_array': True,
                                       'chunks': 'native',
                                       'gene_labels': None,
                                       'gene_labelset': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_g123_gwss'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_5_call_1_ag3_plot_g123_calibration': '01_ag3_g123_calibration',
 'cell_6_call_1_ag3_plot_g123_calibration': '02_ag3_g123_calibration',
 'cell_7_call_1_ag3_plot_g123_gwss_track': '03_ag3_g123_gwss_track_2L',
 'cell_8_call_1_ag3_plot_g123_gwss_track': '04_ag3_g123_gwss_track_2L',
 'cell_9_call_1_ag3_plot_g123_gwss_track': '05_ag3_g123_gwss_track_2L',
 'cell_10_call_1_ag3_plot_g123_gwss': '06_ag3_g123_gwss_2L',
 'cell_11_call_1_ag3_plot_g123_gwss': '07_ag3_g123_gwss_2L',
 'cell_14_call_1_af1_plot_g123_gwss': '08_af1_g123_gwss_X',
 'cell_15_call_1_af1_plot_g123_gwss': '09_af1_g123_gwss_X'}


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

    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230516",
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    import malariagen_data

    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230823",
        results_cache="results_cache",
    )
    nbrt.display(af1)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.shell('rm -rf results_cache')
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    contig = "3L"
    sample_set = "AG1000G-BF-A"
    sample_query = 'taxon == "gambiae"'
    site_mask = "gamb_colu"
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_calibration, 'cell_5_call_1_ag3_plot_g123_calibration', contig=contig, sites=site_mask, sample_sets=sample_set, sample_query=sample_query, site_mask=site_mask))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_calibration, 'cell_6_call_1_ag3_plot_g123_calibration', contig=contig, sites=site_mask, sample_sets=sample_set, sample_query=sample_query, site_mask=site_mask))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_gwss_track, 'cell_7_call_1_ag3_plot_g123_gwss_track', contig="2L", window_size=1_000, site_mask=site_mask, sites=site_mask, sample_query=sample_query, sample_sets=sample_set, max_cohort_size=10))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_gwss_track, 'cell_8_call_1_ag3_plot_g123_gwss_track', contig="2L", window_size=1_000, site_mask=site_mask, sites=site_mask, sample_query=sample_query, sample_sets=sample_set, max_cohort_size=10))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_gwss_track, 'cell_9_call_1_ag3_plot_g123_gwss_track', contig="2L", window_size=1_000, site_mask=site_mask, sites="segregating", sample_query=sample_query, sample_sets=sample_set, max_cohort_size=30, width=700, sizing_mode="fixed"))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_gwss, 'cell_10_call_1_ag3_plot_g123_gwss', contig="2L", window_size=1_000, site_mask=site_mask, sites="all", sample_query=sample_query, sample_sets=sample_set, min_cohort_size=10, max_cohort_size=20))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(_call_api_with_parameters(ag3.plot_g123_gwss, 'cell_11_call_1_ag3_plot_g123_gwss', contig="2L", window_size=1_000, site_mask=site_mask, sites=site_mask, sample_query=sample_query, sample_sets=sample_set, max_cohort_size=None))
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(af1.sample_sets, 'cell_12_call_1_af1_sample_sets', release="1.0"))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(af1.sample_metadata, 'cell_13_call_1_af1_sample_metadata', sample_sets="1.0").groupby(
        ["sample_set", "cohort_admin1_year"]
    ).size())
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(af1.plot_g123_gwss, 'cell_14_call_1_af1_plot_g123_gwss', contig="X", window_size=2_000, sites="segregating", site_mask="funestus", sample_query="cohort_admin1_year == 'KE-03_fune_2016'", sample_sets="1232-VO-KE-OCHOMO-VMF00044", max_cohort_size=20))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(af1.plot_g123_gwss, 'cell_15_call_1_af1_plot_g123_gwss', contig="X", window_size=2000, site_mask="funestus", sites="funestus", sample_query="cohort_admin1_year == 'KE-03_fune_2016'", sample_sets="1232-VO-KE-OCHOMO-VMF00044", max_cohort_size=None))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_g123_gwss.ipynb',
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
