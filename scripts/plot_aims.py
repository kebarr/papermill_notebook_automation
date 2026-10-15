#!/usr/bin/env python3
"""plot_aims: the code from notebooks/plot_aims.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_aims.py                      # the notebook's defaults
    python scripts/plot_aims.py --config runs.csv    # one run per CSV row
    python scripts/plot_aims.py --list-parameters    # what a CSV can set

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
PERFORMANCE_CSV_PATH = 'plot_aims_performance.csv'
API_CALL_PARAMETERS = {'cell_3_call_1_ag3_plot_aim_heatmap': {'aims': 'gambcolu_vs_arab',
                                        'sample_sets': 'AG1000G-UG',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sort': True,
                                        'row_height': 4,
                                        'xgap': 0,
                                        'ygap': 0.5,
                                        'palette': None,
                                        'show': True,
                                        'renderer': None},
 'cell_4_call_1_ag3_plot_aim_heatmap': {'aims': 'gamb_vs_colu',
                                        'sample_sets': ['AG1000G-BF-A', 'AG1000G-BF-B'],
                                        'sample_query': "aim_species != 'arabiensis'",
                                        'sample_query_options': None,
                                        'sort': True,
                                        'row_height': 4,
                                        'xgap': 0,
                                        'ygap': 0.5,
                                        'palette': None,
                                        'show': True,
                                        'renderer': None},
 'cell_5_call_1_ag3_plot_aim_heatmap': {'aims': 'gamb_vs_colu',
                                        'sample_sets': 'AG1000G-GW',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sort': True,
                                        'row_height': 4,
                                        'xgap': 0,
                                        'ygap': 0.5,
                                        'palette': None,
                                        'show': True,
                                        'renderer': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_aims'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_3_call_1_ag3_plot_aim_heatmap': '01_ag3_aim_heatmap',
 'cell_4_call_1_ag3_plot_aim_heatmap': '02_ag3_aim_heatmap',
 'cell_5_call_1_ag3_plot_aim_heatmap': '03_ag3_aim_heatmap'}


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
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.display(_call_api_with_parameters(ag3.plot_aim_heatmap, 'cell_3_call_1_ag3_plot_aim_heatmap', aims="gambcolu_vs_arab", sample_sets="AG1000G-UG"))
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    nbrt.display(_call_api_with_parameters(ag3.plot_aim_heatmap, 'cell_4_call_1_ag3_plot_aim_heatmap', aims="gamb_vs_colu", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"], sample_query="aim_species != 'arabiensis'"))
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.display(_call_api_with_parameters(ag3.plot_aim_heatmap, 'cell_5_call_1_ag3_plot_aim_heatmap', aims="gamb_vs_colu", sample_sets="AG1000G-GW"))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_aims.ipynb',
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
