#!/usr/bin/env python3
"""plot_haplotype_networks: the code from notebooks/plot_haplotype_networks.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_haplotype_networks.py                      # the notebook's defaults
    python scripts/plot_haplotype_networks.py --config runs.csv    # one run per CSV row
    python scripts/plot_haplotype_networks.py --list-parameters    # what a CSV can set
    python scripts/plot_haplotype_networks.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_haplotype_networks_performance.csv'
API_CALL_PARAMETERS = {'cell_7_call_1_ag3_plot_haplotype_network': {'region': '2L:2,358,158-2,431,617',
                                              'analysis': 'gamb_colu',
                                              'sample_sets': '3.0',
                                              'sample_query': "taxon == 'coluzzii'",
                                              'sample_query_options': None,
                                              'max_dist': 2,
                                              'color': 'country',
                                              'color_discrete_sequence': None,
                                              'color_discrete_map': None,
                                              'category_orders': None,
                                              'node_size_factor': 50,
                                              'layout': 'cose',
                                              'layout_params': None,
                                              'server_port': None,
                                              'server_mode': 'inline',
                                              'height': 600,
                                              'width': '100%',
                                              'serve_scripts_locally': True,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_9_call_1_ag3_plot_haplotype_network': {'region': '2L:2,358,158-2,431,617',
                                              'analysis': 'gamb_colu',
                                              'sample_sets': '3.0',
                                              'sample_query': "taxon == 'coluzzii'",
                                              'sample_query_options': None,
                                              'max_dist': 2,
                                              'color': 'admin1_iso',
                                              'color_discrete_sequence': None,
                                              'color_discrete_map': None,
                                              'category_orders': None,
                                              'node_size_factor': 50,
                                              'layout': 'cose',
                                              'layout_params': None,
                                              'server_port': None,
                                              'server_mode': 'inline',
                                              'height': 600,
                                              'width': '100%',
                                              'serve_scripts_locally': True,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_11_call_1_ag3_plot_haplotype_network': {'region': '2L:2,358,158-2,431,617',
                                               'analysis': 'gamb_colu',
                                               'sample_sets': '3.0',
                                               'sample_query': "taxon == 'coluzzii'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': None,
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'inline',
                                               'height': 600,
                                               'width': '100%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_13_call_1_ag3_plot_haplotype_network': {'region': '2L:2,358,158-2,431,617',
                                               'analysis': 'gamb_colu',
                                               'sample_sets': '3.0',
                                               'sample_query': "taxon == 'coluzzii'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': None,
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'inline',
                                               'height': 600,
                                               'width': '100%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_15_call_1_ag3_plot_haplotype_network': {'region': '2L:2,358,158-2,431,617',
                                               'analysis': 'gamb_colu',
                                               'sample_sets': '3.0',
                                               'sample_query': "taxon == 'coluzzii'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': 'country',
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'external',
                                               'height': 600,
                                               'width': '100%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_19_call_1_af1_plot_haplotype_network': {'region': '2RL:2,358,158-2,431,617',
                                               'analysis': 'default',
                                               'sample_sets': '1.0',
                                               'sample_query': "country == 'Ghana'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': 'sample_set',
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'inline',
                                               'height': 500,
                                               'width': '90%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_21_call_1_af1_plot_haplotype_network': {'region': '2RL:2,358,158-2,431,617',
                                               'analysis': 'default',
                                               'sample_sets': '1.0',
                                               'sample_query': "country == 'Ghana'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': 'year',
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'inline',
                                               'height': 600,
                                               'width': '100%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_23_call_1_af1_plot_haplotype_network': {'region': '2RL:2,358,158-2,431,617',
                                               'analysis': 'default',
                                               'sample_sets': '1.0',
                                               'sample_query': "country == 'Ghana'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': None,
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'inline',
                                               'height': 600,
                                               'width': '100%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_25_call_1_af1_plot_haplotype_network': {'region': '2RL:2,358,158-2,431,617',
                                               'analysis': 'default',
                                               'sample_sets': '1.0',
                                               'sample_query': "country == 'Ghana'",
                                               'sample_query_options': None,
                                               'max_dist': 2,
                                               'color': None,
                                               'color_discrete_sequence': None,
                                               'color_discrete_map': None,
                                               'category_orders': None,
                                               'node_size_factor': 50,
                                               'layout': 'cose',
                                               'layout_params': None,
                                               'server_port': None,
                                               'server_mode': 'inline',
                                               'height': 600,
                                               'width': '100%',
                                               'serve_scripts_locally': True,
                                               'chunks': 'native',
                                               'inline_array': True}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_haplotype_networks'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_7_call_1_ag3_plot_haplotype_network': '01_ag3_haplotype_network_by_country',
 'cell_9_call_1_ag3_plot_haplotype_network': '02_ag3_haplotype_network_by_admin1_iso',
 'cell_11_call_1_ag3_plot_haplotype_network': '03_ag3_haplotype_network',
 'cell_13_call_1_ag3_plot_haplotype_network': '04_ag3_haplotype_network',
 'cell_15_call_1_ag3_plot_haplotype_network': '05_ag3_haplotype_network_by_country',
 'cell_19_call_1_af1_plot_haplotype_network': '06_af1_haplotype_network_by_sample_set',
 'cell_21_call_1_af1_plot_haplotype_network': '07_af1_haplotype_network_by_year',
 'cell_23_call_1_af1_plot_haplotype_network': '08_af1_haplotype_network',
 'cell_25_call_1_af1_plot_haplotype_network': '09_af1_haplotype_network'}


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
    # # Haplotype Network Plotting Examples
    # This notebook demonstrates the `plot_haplotype_network` function from the `malariagen_data` package, showcasing different ways to use the `color` parameter to visualize haplotype networks.
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    import malariagen_data
    # ## Ag3
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    # Initialize Ag3 instance
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
    )
    nbrt.display(ag3)
    # N.B., manually specifying the server_port parameter doesn't seem to be necessary on colab, but is needed when running locally via Jupyter notebook, otherwise get "Address already in use" error and cannot run multiple plots in same notebook.
    # ## Example 1: Direct Column Name (String)
    # Use a direct column name like 'country' to color nodes by country.
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    # Plot haplotype network with country coloring
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_network, 'cell_7_call_1_ag3_plot_haplotype_network', region="2L:2,358,158-2,431,617", analysis="gamb_colu", sample_sets="3.0", sample_query="taxon == 'coluzzii'", color="country", max_dist=2))
    # ## Example 2: Cohorts Prefix (String)
    # In this example, `"admin1_iso"` is used, which the function interprets as `"cohorts_admin1_iso"`, a column typically available in cohort-annotated metadata.
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_network, 'cell_9_call_1_ag3_plot_haplotype_network', region="2L:2,358,158-2,431,617", analysis="gamb_colu", sample_query="taxon == 'coluzzii'", sample_sets="3.0", color="admin1_iso", max_dist=2))
    # This example uses a dictionary to define custom color groups based on conditions applied to the `"country"` column.
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    color_mapping = {"Ghana": "country == 'Ghana'", "Other": "country != 'Ghana'"}
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_network, 'cell_11_call_1_ag3_plot_haplotype_network', region="2L:2,358,158-2,431,617", analysis="gamb_colu", sample_query="taxon == 'coluzzii'", sample_sets="3.0", color=color_mapping, max_dist=2))
    # Setting `color=None` applies the default coloring scheme, typically uniform across all nodes.
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_network, 'cell_13_call_1_ag3_plot_haplotype_network', region="2L:2,358,158-2,431,617", analysis="gamb_colu", sample_query="taxon == 'coluzzii'", sample_sets="3.0", color=None, max_dist=2))
    # This replicates Example 1 but uses `server_mode="external"`, useful for rendering plots in certain environments.
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_network, 'cell_15_call_1_ag3_plot_haplotype_network', region="2L:2,358,158-2,431,617", analysis="gamb_colu", sample_query="taxon == 'coluzzii'", sample_sets="3.0", color="country", max_dist=2, server_mode="external"))
    # ## Af1
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    # Initialize Af1 instance
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
    )
    nbrt.display(af1)
    # Here, nodes are colored based on the `"sample_set"` column.
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_network, 'cell_19_call_1_af1_plot_haplotype_network', region="2RL:2,358,158-2,431,617", sample_query="country == 'Ghana'", sample_sets="1.0", color="sample_set", max_dist=2, height=500, width="90%"))
    # Using `"year"` implies the function looks for `"cohorts_year"` in the metadata.
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_network, 'cell_21_call_1_af1_plot_haplotype_network', region="2RL:2,358,158-2,431,617", sample_query="country == 'Ghana'", sample_sets="1.0", color="year", max_dist=2))
    # A dictionary defines custom groups based on the `"year"` column (assuming year data is available).
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    color_mapping = {"2012": "year == 2012", "2014": "year == 2014"}
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_network, 'cell_23_call_1_af1_plot_haplotype_network', region="2RL:2,358,158-2,431,617", sample_query="country == 'Ghana'", sample_sets="1.0", color=color_mapping, max_dist=2))
    # With `color=None`, the default coloring is applied.
    # --- Notebook cell 26 ---
    nbrt.start_cell("notebook_cell_26")
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_network, 'cell_25_call_1_af1_plot_haplotype_network', region="2RL:2,358,158-2,431,617", sample_query="country == 'Ghana'", sample_sets="1.0", color=None, max_dist=2))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_haplotype_networks.ipynb',
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
