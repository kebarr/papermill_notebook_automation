#!/usr/bin/env python3
"""plot_diversity: the code from notebooks/plot_diversity.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_diversity.py                      # the notebook's defaults
    python scripts/plot_diversity.py --config runs.csv    # one run per CSV row
    python scripts/plot_diversity.py --list-parameters    # what a CSV can set
    python scripts/plot_diversity.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_diversity_performance.csv'
API_CALL_PARAMETERS = {'cell_4_call_1_ag3_diversity_stats': {'cohorts': 'admin2_year',
                                       'cohort_size': 10,
                                       'region': '3L:15,000,000-16,000,000',
                                       'site_mask': 'gamb_colu_arab',
                                       'site_class': 'CDS_DEG_4',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_sets': 'AG1000G-TZ',
                                       'random_seed': 42,
                                       'n_jack': 200,
                                       'confidence_level': 0.95,
                                       'chunks': 'native',
                                       'inline_array': True},
 'cell_5_call_1_ag3_diversity_stats': {'cohorts': 'admin2_year',
                                       'cohort_size': 10,
                                       'region': '3L:15,000,000-16,000,000',
                                       'site_mask': 'gamb_colu_arab',
                                       'site_class': 'CDS_DEG_4',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_sets': 'AG1000G-TZ',
                                       'random_seed': 42,
                                       'n_jack': 200,
                                       'confidence_level': 0.95,
                                       'chunks': 'native',
                                       'inline_array': True},
 'cell_6_call_1_ag3_plot_diversity_stats': {'df_stats': '__KEEP_CALLSITE_VALUE__',
                                            'color': None,
                                            'bar_plot_height': 450,
                                            'bar_width': 30,
                                            'scatter_plot_height': 500,
                                            'scatter_plot_width': 500,
                                            'template': 'plotly_white',
                                            'color_discrete_sequence': None,
                                            'color_discrete_map': None,
                                            'category_orders': None,
                                            'plot_kwargs': None,
                                            'show': True,
                                            'renderer': None},
 'cell_7_call_1_ag3_plot_diversity_stats': {'df_stats': '__KEEP_CALLSITE_VALUE__',
                                            'color': 'taxon',
                                            'bar_plot_height': 450,
                                            'bar_width': 30,
                                            'scatter_plot_height': 500,
                                            'scatter_plot_width': 500,
                                            'template': 'plotly_white',
                                            'color_discrete_sequence': None,
                                            'color_discrete_map': None,
                                            'category_orders': None,
                                            'plot_kwargs': None,
                                            'show': True,
                                            'renderer': None},
 'cell_8_call_1_ag3_plot_diversity_stats': {'df_stats': '__KEEP_CALLSITE_VALUE__',
                                            'color': 'admin2_name',
                                            'bar_plot_height': 450,
                                            'bar_width': 30,
                                            'scatter_plot_height': 500,
                                            'scatter_plot_width': 500,
                                            'template': 'plotly_white',
                                            'color_discrete_sequence': None,
                                            'color_discrete_map': None,
                                            'category_orders': None,
                                            'plot_kwargs': None,
                                            'show': False,
                                            'renderer': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_diversity'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_6_call_1_ag3_plot_diversity_stats': '01_ag3_diversity_stats',
 'cell_7_call_1_ag3_plot_diversity_stats': '02_ag3_diversity_stats_by_taxon'}


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


    import collections.abc
    import types
    import typing


    def _tuple_if_expected(annotation, value):
        """Turn a list back into a tuple where the API accepts a tuple but not a
    list, e.g. percentiles. CSV configs store values as JSON, which has no
    tuples, so (50, 75, 100) arrives as [50, 75, 100]."""
        if not isinstance(value, list):
            return value
        if typing.get_origin(annotation) is typing.Annotated:
            annotation = typing.get_args(annotation)[0]
        if typing.get_origin(annotation) in (typing.Union, types.UnionType):
            options = typing.get_args(annotation)
        else:
            options = (annotation,)
        accepted = {typing.get_origin(option) or option for option in options}
        accepts_list = accepted & {
            list, typing.Any, collections.abc.Sequence, collections.abc.Iterable,
            collections.abc.Collection, collections.abc.MutableSequence,
        }
        if tuple in accepted and not accepts_list:
            return tuple(value)
        return value


    def _call_api_with_parameters(method, call_key, *args, **kwargs):
        signature = inspect.signature(method)
        bound = signature.bind_partial(*args, **kwargs)
        bound.apply_defaults()
        for name, value in API_CALL_PARAMETERS[call_key].items():
            if not (isinstance(value, str) and value == API_KEEP_CALLSITE_VALUE):
                parameter = signature.parameters.get(name)
                if parameter is not None:
                    value = _tuple_if_expected(parameter.annotation, value)
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
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.shell('rm -rf results_cache')
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    df_stats = _call_api_with_parameters(ag3.diversity_stats, 'cell_4_call_1_ag3_diversity_stats', sample_sets="AG1000G-TZ", cohorts="admin2_year", cohort_size=10, region="3L:15,000,000-16,000,000", site_mask="gamb_colu_arab", site_class="CDS_DEG_4")
    nbrt.display(df_stats)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    df_stats = _call_api_with_parameters(ag3.diversity_stats, 'cell_5_call_1_ag3_diversity_stats', sample_sets="AG1000G-TZ", cohorts="admin2_year", cohort_size=10, region="3L:15,000,000-16,000,000", site_mask="gamb_colu_arab", site_class="CDS_DEG_4")
    nbrt.display(df_stats)
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_diversity_stats, 'cell_6_call_1_ag3_plot_diversity_stats', df_stats))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_diversity_stats, 'cell_7_call_1_ag3_plot_diversity_stats', df_stats, color="taxon"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    figs = _call_api_with_parameters(ag3.plot_diversity_stats, 'cell_8_call_1_ag3_plot_diversity_stats', df_stats, color="admin2_name", show=False)
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(figs[0])
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(figs[1])
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(figs[2])
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(figs[3])


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_diversity.ipynb',
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
