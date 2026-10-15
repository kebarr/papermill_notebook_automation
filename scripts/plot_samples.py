#!/usr/bin/env python3
"""plot_samples: the code from notebooks/plot_samples.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_samples.py                      # the notebook's defaults
    python scripts/plot_samples.py --config runs.csv    # one run per CSV row
    python scripts/plot_samples.py --list-parameters    # what a CSV can set
    python scripts/plot_samples.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_samples_performance.csv'
API_CALL_PARAMETERS = {'cell_4_call_1_ag3_plot_samples_bar': {'x': 'country',
                                        'color': None,
                                        'sort': True,
                                        'sample_sets': '3.0',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None,
                                        'template': 'plotly_white',
                                        'width': 800,
                                        'height': 600,
                                        'show': True,
                                        'renderer': None,
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_5_call_1_ag3_plot_samples_bar': {'x': 'country',
                                        'color': 'taxon',
                                        'sort': True,
                                        'sample_sets': '3.0',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None,
                                        'template': 'plotly_white',
                                        'width': 800,
                                        'height': 600,
                                        'show': True,
                                        'renderer': None,
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_6_call_1_ag3_plot_samples_bar': {'x': 'year',
                                        'color': 'country',
                                        'sort': True,
                                        'sample_sets': '3.0',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None,
                                        'template': 'plotly_white',
                                        'width': 800,
                                        'height': 600,
                                        'show': True,
                                        'renderer': None,
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_7_call_1_ag3_plot_samples_interactive_map': {'sample_sets': ['3.0'],
                                                    'sample_query': 'year > 2009',
                                                    'sample_query_options': None,
                                                    'sample_indices': None,
                                                    'basemap': 'mapnik',
                                                    'center': (-2, 20),
                                                    'zoom': 3,
                                                    'height': 500,
                                                    'width': '100%',
                                                    'min_samples': 1,
                                                    'count_by': 'taxon'},
 'cell_8_call_1_ag3_plot_samples_interactive_map': {'sample_sets': ['3.0'],
                                                    'sample_query': None,
                                                    'sample_query_options': None,
                                                    'sample_indices': None,
                                                    'basemap': 'mapnik',
                                                    'center': (-2, 20),
                                                    'zoom': 3,
                                                    'height': 500,
                                                    'width': '100%',
                                                    'min_samples': 1,
                                                    'count_by': 'taxon'},
 'cell_10_call_1_ag3_plot_samples_interactive_map': {'sample_sets': ['3.0'],
                                                     'sample_query': None,
                                                     'sample_query_options': None,
                                                     'sample_indices': None,
                                                     'basemap': 'mapNik',
                                                     'center': (-2, 20),
                                                     'zoom': 3,
                                                     'height': 500,
                                                     'width': '100%',
                                                     'min_samples': 1,
                                                     'count_by': 'taxon'},
 'cell_11_call_1_ag3_plot_sample_location_mapbox': {'sample_sets': ['3.0'],
                                                    'sample_query': 'year > 2012',
                                                    'sample_query_options': None,
                                                    'marker_size': 10,
                                                    'color': 'country',
                                                    'color_discrete_sequence': ['rgb(95, 70, 144)',
                                                                                'rgb(29, 105, 150)',
                                                                                'rgb(56, 166, 165)',
                                                                                'rgb(15, 133, 84)',
                                                                                'rgb(115, 175, 72)',
                                                                                'rgb(237, 173, 8)',
                                                                                'rgb(225, 124, 5)',
                                                                                'rgb(204, 80, 62)',
                                                                                'rgb(148, 52, 110)',
                                                                                'rgb(111, 64, 112)',
                                                                                'rgb(102, 102, '
                                                                                '102)'],
                                                    'category_orders': None,
                                                    'hover_name': 'location',
                                                    'zoom': 2,
                                                    'width': 800,
                                                    'height': 600,
                                                    'show': True,
                                                    'renderer': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_12_call_1_ag3_plot_sample_location_geo': {'sample_sets': ['3.0'],
                                                 'sample_query': 'year > 2012',
                                                 'sample_query_options': None,
                                                 'sample_indices': None,
                                                 'marker_size': 10,
                                                 'color': 'country',
                                                 'color_discrete_sequence': ['rgb(95, 70, 144)',
                                                                             'rgb(29, 105, 150)',
                                                                             'rgb(56, 166, 165)',
                                                                             'rgb(15, 133, 84)',
                                                                             'rgb(115, 175, 72)',
                                                                             'rgb(237, 173, 8)',
                                                                             'rgb(225, 124, 5)',
                                                                             'rgb(204, 80, 62)',
                                                                             'rgb(148, 52, 110)',
                                                                             'rgb(111, 64, 112)',
                                                                             'rgb(102, 102, 102)'],
                                                 'category_orders': None,
                                                 'hover_name': 'location',
                                                 'fitbounds': 'locations',
                                                 'scope': 'world',
                                                 'width': 800,
                                                 'height': 600,
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_15_call_1_af1_plot_samples_bar': {'x': 'country',
                                         'color': None,
                                         'sort': True,
                                         'sample_sets': '1.0',
                                         'sample_query': None,
                                         'sample_query_options': None,
                                         'sample_indices': None,
                                         'template': 'plotly_white',
                                         'width': 800,
                                         'height': 600,
                                         'show': True,
                                         'renderer': None,
                                         'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_16_call_1_af1_plot_samples_bar': {'x': 'year',
                                         'color': 'country',
                                         'sort': True,
                                         'sample_sets': '1.0',
                                         'sample_query': None,
                                         'sample_query_options': None,
                                         'sample_indices': None,
                                         'template': 'plotly_white',
                                         'width': 800,
                                         'height': 600,
                                         'show': True,
                                         'renderer': None,
                                         'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_17_call_1_af1_plot_samples_interactive_map': {'sample_sets': ['1.0'],
                                                     'sample_query': None,
                                                     'sample_query_options': None,
                                                     'sample_indices': None,
                                                     'basemap': 'mapnik',
                                                     'center': (-2, 20),
                                                     'zoom': 3,
                                                     'height': 500,
                                                     'width': '100%',
                                                     'min_samples': 1,
                                                     'count_by': 'taxon'},
 'cell_18_call_1_af1_plot_sample_location_mapbox': {'sample_sets': ['1.0'],
                                                    'sample_query': 'year > 2015',
                                                    'sample_query_options': None,
                                                    'marker_size': 10,
                                                    'color': 'country',
                                                    'color_discrete_sequence': ['rgb(95, 70, 144)',
                                                                                'rgb(29, 105, 150)',
                                                                                'rgb(56, 166, 165)',
                                                                                'rgb(15, 133, 84)',
                                                                                'rgb(115, 175, 72)',
                                                                                'rgb(237, 173, 8)',
                                                                                'rgb(225, 124, 5)',
                                                                                'rgb(204, 80, 62)',
                                                                                'rgb(148, 52, 110)',
                                                                                'rgb(111, 64, 112)',
                                                                                'rgb(102, 102, '
                                                                                '102)'],
                                                    'category_orders': None,
                                                    'hover_name': 'location',
                                                    'zoom': 2,
                                                    'width': 800,
                                                    'height': 600,
                                                    'show': True,
                                                    'renderer': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_19_call_1_af1_plot_sample_location_geo': {'sample_sets': ['1.0'],
                                                 'sample_query': 'year > 2015',
                                                 'sample_query_options': None,
                                                 'sample_indices': None,
                                                 'marker_size': 10,
                                                 'color': 'country',
                                                 'color_discrete_sequence': ['rgb(95, 70, 144)',
                                                                             'rgb(29, 105, 150)',
                                                                             'rgb(56, 166, 165)',
                                                                             'rgb(15, 133, 84)',
                                                                             'rgb(115, 175, 72)',
                                                                             'rgb(237, 173, 8)',
                                                                             'rgb(225, 124, 5)',
                                                                             'rgb(204, 80, 62)',
                                                                             'rgb(148, 52, 110)',
                                                                             'rgb(111, 64, 112)',
                                                                             'rgb(102, 102, 102)'],
                                                 'category_orders': None,
                                                 'hover_name': 'location',
                                                 'fitbounds': 'locations',
                                                 'scope': 'world',
                                                 'width': 800,
                                                 'height': 600,
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_samples'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_4_call_1_ag3_plot_samples_bar': '01_ag3_samples_bar',
 'cell_5_call_1_ag3_plot_samples_bar': '02_ag3_samples_bar_by_taxon',
 'cell_6_call_1_ag3_plot_samples_bar': '03_ag3_samples_bar_by_country',
 'cell_7_call_1_ag3_plot_samples_interactive_map': '04_ag3_samples_interactive_map',
 'cell_8_call_1_ag3_plot_samples_interactive_map': '05_ag3_samples_interactive_map',
 'cell_10_call_1_ag3_plot_samples_interactive_map': '06_ag3_samples_interactive_map',
 'cell_11_call_1_ag3_plot_sample_location_mapbox': '07_ag3_sample_location_mapbox_by_country',
 'cell_12_call_1_ag3_plot_sample_location_geo': '08_ag3_sample_location_geo_by_country',
 'cell_15_call_1_af1_plot_samples_bar': '09_af1_samples_bar',
 'cell_16_call_1_af1_plot_samples_bar': '10_af1_samples_bar_by_country',
 'cell_17_call_1_af1_plot_samples_interactive_map': '11_af1_samples_interactive_map',
 'cell_18_call_1_af1_plot_sample_location_mapbox': '12_af1_sample_location_mapbox_by_country',
 'cell_19_call_1_af1_plot_sample_location_geo': '13_af1_sample_location_geo_by_country'}


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
    import ipyleaflet
    # ## Ag3
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
    )
    nbrt.display(ag3)
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    nbrt.display(_call_api_with_parameters(ag3.plot_samples_bar, 'cell_4_call_1_ag3_plot_samples_bar', x="country", sample_sets="3.0"))
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.display(_call_api_with_parameters(ag3.plot_samples_bar, 'cell_5_call_1_ag3_plot_samples_bar', x="country", color="taxon", sample_sets="3.0"))
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_samples_bar, 'cell_6_call_1_ag3_plot_samples_bar', x="year", color="country", sample_sets="3.0"))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_samples_interactive_map, 'cell_7_call_1_ag3_plot_samples_interactive_map', sample_sets=["3.0"], sample_query="year > 2009"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    # Demo using a different basemap provider
    # - The map background will appear grey if provision of tiles fails
    tile_URL_pattern = "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
    nbrt.display(_call_api_with_parameters(ag3.plot_samples_interactive_map, 'cell_8_call_1_ag3_plot_samples_interactive_map', sample_sets=["3.0"], basemap=ipyleaflet.TileLayer(url=tile_URL_pattern)))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    # See the available basemap abbreviations
    nbrt.display(malariagen_data.anoph.map_params.basemap_abbrevs.keys())
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    # Demo using a basemap abbreviation, case-insensitive
    nbrt.display(_call_api_with_parameters(ag3.plot_samples_interactive_map, 'cell_10_call_1_ag3_plot_samples_interactive_map', sample_sets=["3.0"], basemap="mapNik"))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.plot_sample_location_mapbox, 'cell_11_call_1_ag3_plot_sample_location_mapbox', color="country", sample_sets=["3.0"], sample_query="year > 2012", zoom=2))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.plot_sample_location_geo, 'cell_12_call_1_ag3_plot_sample_location_geo', color="country", sample_sets=["3.0"], sample_query="year > 2012"))
    # ## Af1
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
        pre=True,
    )
    nbrt.display(af1)
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(af1.plot_samples_bar, 'cell_15_call_1_af1_plot_samples_bar', x="country", sample_sets="1.0"))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(af1.plot_samples_bar, 'cell_16_call_1_af1_plot_samples_bar', x="year", color="country", sample_sets="1.0"))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    # Demo using a basemap provider the same as one in its curated list
    nbrt.display(_call_api_with_parameters(af1.plot_samples_interactive_map, 'cell_17_call_1_af1_plot_samples_interactive_map', sample_sets=["1.0"], basemap=ipyleaflet.basemaps.OpenTopoMap))
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    nbrt.display(_call_api_with_parameters(af1.plot_sample_location_mapbox, 'cell_18_call_1_af1_plot_sample_location_mapbox', color="country", sample_sets=["1.0"], sample_query="year > 2015", zoom=2))
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(af1.plot_sample_location_geo, 'cell_19_call_1_af1_plot_sample_location_geo', color="country", sample_sets=["1.0"], sample_query="year > 2015"))
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    nbrt.display(help(af1.plot_samples_bar))
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(help(af1.plot_samples_interactive_map))
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(help(af1.plot_sample_location_mapbox))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(help(af1.plot_sample_location_geo))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_samples.ipynb',
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
