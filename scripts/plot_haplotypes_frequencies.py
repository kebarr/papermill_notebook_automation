#!/usr/bin/env python3
"""plot_haplotypes_frequencies: the code from notebooks/plot_haplotypes_frequencies.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_haplotypes_frequencies.py                      # the notebook's defaults
    python scripts/plot_haplotypes_frequencies.py --config runs.csv    # one run per CSV row
    python scripts/plot_haplotypes_frequencies.py --list-parameters    # what a CSV can set

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
PERFORMANCE_CSV_PATH = 'plot_haplotypes_frequencies_performance.csv'
API_CALL_PARAMETERS = {'cell_3_call_1_ag3_haplotypes_frequencies': {'region': '2L:2,358,158-2,431,617',
                                              'cohorts': 'admin1_year',
                                              'sample_query': None,
                                              'sample_query_options': None,
                                              'min_cohort_size': 10,
                                              'sample_sets': ('AG1000G-BF-A',
                                                              'AG1000G-BF-B',
                                                              'AG1000G-BF-C'),
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_4_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
                                                'index': 'label',
                                                'max_len': 100,
                                                'col_width': 40,
                                                'row_height': 20,
                                                'x_label': 'Cohorts',
                                                'y_label': 'Variants',
                                                'colorbar': True,
                                                'width': None,
                                                'height': None,
                                                'text_auto': '.0%',
                                                'aspect': 'auto',
                                                'color_continuous_scale': 'Reds',
                                                'title': True,
                                                'show': True,
                                                'renderer': None,
                                                'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_5_call_1_ag3_haplotypes_frequencies_advanced': {'region': '2L:2,358,158-2,431,617',
                                                       'area_by': 'admin1_iso',
                                                       'period_by': 'year',
                                                       'sample_sets': ['AG1000G-BF-A',
                                                                       'AG1000G-BF-B'],
                                                       'sample_query': None,
                                                       'sample_query_options': None,
                                                       'min_cohort_size': 10,
                                                       'ci_method': 'wilson',
                                                       'chunks': 'native',
                                                       'inline_array': True,
                                                       'taxon_by': 'taxon',
                                                       'filter_unassigned': None},
 'cell_6_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                    'height': None,
                                                    'width': None,
                                                    'title': True,
                                                    'legend_sizing': 'constant',
                                                    'show': True,
                                                    'renderer': None,
                                                    'taxa': None,
                                                    'areas': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_9_call_1_af1_haplotypes_frequencies_advanced': {'region': '2RL:2,358,158-2,431,617',
                                                       'area_by': 'admin1_iso',
                                                       'period_by': 'year',
                                                       'sample_sets': ['1232-VO-KE-OCHOMO-VMF00044'],
                                                       'sample_query': None,
                                                       'sample_query_options': None,
                                                       'min_cohort_size': 10,
                                                       'ci_method': 'wilson',
                                                       'chunks': 'native',
                                                       'inline_array': True,
                                                       'taxon_by': 'taxon',
                                                       'filter_unassigned': None},
 'cell_9_call_2_af1_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                    'height': None,
                                                    'width': None,
                                                    'title': True,
                                                    'legend_sizing': 'constant',
                                                    'show': True,
                                                    'renderer': None,
                                                    'taxa': None,
                                                    'areas': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_haplotypes_frequencies'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_4_call_1_ag3_plot_frequencies_heatmap': '01_ag3_frequencies_heatmap',
 'cell_6_call_1_ag3_plot_frequencies_time_series': '02_ag3_frequencies_time_series',
 'cell_9_call_2_af1_plot_frequencies_time_series': '03_af1_frequencies_time_series'}


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
    # # Ag3
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    import malariagen_data

    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230516",
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    hap_df = _call_api_with_parameters(ag3.haplotypes_frequencies, 'cell_3_call_1_ag3_haplotypes_frequencies', "2L:2,358,158-2,431,617", "admin1_year", sample_sets=("AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-BF-C"))
    nbrt.display(hap_df)
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_4_call_1_ag3_plot_frequencies_heatmap', hap_df.query("max_af > .05")))
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    hap_xr = _call_api_with_parameters(ag3.haplotypes_frequencies_advanced, 'cell_5_call_1_ag3_haplotypes_frequencies_advanced', region="2L:2,358,158-2,431,617", area_by="admin1_iso", period_by="year", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"])
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_6_call_1_ag3_plot_frequencies_time_series', hap_xr))
    # # Af1
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
    )
    nbrt.display(af1)
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    hap_xr = _call_api_with_parameters(af1.haplotypes_frequencies_advanced, 'cell_9_call_1_af1_haplotypes_frequencies_advanced', region="2RL:2,358,158-2,431,617", area_by="admin1_iso", period_by="year", sample_sets=["1232-VO-KE-OCHOMO-VMF00044"], min_cohort_size=10)
    nbrt.display(_call_api_with_parameters(af1.plot_frequencies_time_series, 'cell_9_call_2_af1_plot_frequencies_time_series', hap_xr))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_haplotypes_frequencies.ipynb',
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
