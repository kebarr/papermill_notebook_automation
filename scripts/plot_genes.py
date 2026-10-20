#!/usr/bin/env python3
"""plot_genes: the code from notebooks_fixed_parameters_cells/plot_genes.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_genes.py                      # the notebook's defaults
    python scripts/plot_genes.py --config runs.csv    # one run per CSV row
    python scripts/plot_genes.py --list-parameters    # what a CSV can set
    python scripts/plot_genes.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_genes_performance.csv'
API_CALL_PARAMETERS = {'cell_3_call_1_ag3_plot_genes': {'region': '2R',
                                  'sizing_mode': 'stretch_width',
                                  'width': None,
                                  'height': 120,
                                  'show': True,
                                  'toolbar_location': 'above',
                                  'x_range': None,
                                  'title': None,
                                  'output_backend': 'webgl',
                                  'gene_labels': None,
                                  'gene_labelset': None},
 'cell_4_call_1_ag3_plot_genes': {'region': '2R:28,000,000-29,000,000',
                                  'sizing_mode': 'stretch_width',
                                  'width': None,
                                  'height': 120,
                                  'show': True,
                                  'toolbar_location': 'above',
                                  'x_range': None,
                                  'title': None,
                                  'output_backend': 'webgl',
                                  'gene_labels': None,
                                  'gene_labelset': None},
 'cell_5_call_1_ag3_plot_genes': {'region': '2R',
                                  'sizing_mode': 'stretch_width',
                                  'width': None,
                                  'height': 120,
                                  'show': False,
                                  'toolbar_location': 'above',
                                  'x_range': None,
                                  'title': None,
                                  'output_backend': 'webgl',
                                  'gene_labels': None,
                                  'gene_labelset': None},
 'cell_5_call_2_ag3_plot_genes': {'region': '2L',
                                  'sizing_mode': 'stretch_width',
                                  'width': None,
                                  'height': 120,
                                  'show': False,
                                  'toolbar_location': 'above',
                                  'x_range': None,
                                  'title': None,
                                  'output_backend': 'webgl',
                                  'gene_labels': None,
                                  'gene_labelset': None},
 'cell_6_call_1_ag3_genome_feature_children': {'parent': 'AGAP004707-RD',
                                               'attributes': 'default'},
 'cell_7_call_1_ag3_plot_transcript': {'transcript': 'AGAP004707-RD',
                                       'sizing_mode': 'stretch_width',
                                       'width': None,
                                       'height': 100,
                                       'show': True,
                                       'x_range': None,
                                       'toolbar_location': 'above',
                                       'title': True},
 'cell_8_call_1_ag3_genome_feature_children': {'parent': 'AGAP004050-RA',
                                               'attributes': 'default'},
 'cell_9_call_1_ag3_plot_transcript': {'transcript': 'AGAP004050-RA',
                                       'sizing_mode': 'stretch_width',
                                       'width': None,
                                       'height': 100,
                                       'show': True,
                                       'x_range': None,
                                       'toolbar_location': 'above',
                                       'title': True},
 'cell_10_call_1_ag3_plot_transcript': {'transcript': '__KEEP_CALLSITE_VALUE__',
                                        'sizing_mode': 'stretch_width',
                                        'width': None,
                                        'height': 100,
                                        'show': False,
                                        'x_range': None,
                                        'toolbar_location': 'above',
                                        'title': True},
 'cell_10_call_2_ag3_plot_transcript': {'transcript': '__KEEP_CALLSITE_VALUE__',
                                        'sizing_mode': 'stretch_width',
                                        'width': None,
                                        'height': 100,
                                        'show': False,
                                        'x_range': '__KEEP_CALLSITE_VALUE__',
                                        'toolbar_location': None,
                                        'title': True},
 'cell_12_call_1_af1_plot_genes': {'region': '3RL',
                                   'sizing_mode': 'stretch_width',
                                   'width': None,
                                   'height': 120,
                                   'show': True,
                                   'toolbar_location': 'above',
                                   'x_range': None,
                                   'title': None,
                                   'output_backend': 'webgl',
                                   'gene_labels': None,
                                   'gene_labelset': None},
 'cell_13_call_1_af1_plot_genes': {'region': '2RL:28,000,000-29,000,000',
                                   'sizing_mode': 'stretch_width',
                                   'width': None,
                                   'height': 120,
                                   'show': True,
                                   'toolbar_location': 'above',
                                   'x_range': None,
                                   'title': None,
                                   'output_backend': 'webgl',
                                   'gene_labels': None,
                                   'gene_labelset': None},
 'cell_14_call_1_af1_plot_transcript': {'transcript': 'LOC125767311_t1',
                                        'sizing_mode': 'stretch_width',
                                        'width': None,
                                        'height': 100,
                                        'show': True,
                                        'x_range': None,
                                        'toolbar_location': 'above',
                                        'title': True},
 'cell_15_call_1_af1_plot_transcript': {'transcript': 'LOC125767311_t2',
                                        'sizing_mode': 'stretch_width',
                                        'width': None,
                                        'height': 100,
                                        'show': True,
                                        'x_range': None,
                                        'toolbar_location': 'above',
                                        'title': True},
 'cell_16_call_1_ag3_plot_genes': {'region': '2R',
                                   'sizing_mode': 'stretch_width',
                                   'width': None,
                                   'height': 120,
                                   'show': True,
                                   'toolbar_location': 'above',
                                   'x_range': None,
                                   'title': None,
                                   'output_backend': 'webgl',
                                   'gene_labels': {'AGAP001096': 'far left + '
                                                                 'gene',
                                                   'AGAP001099': 'far left - '
                                                                 'gene',
                                                   'AGAP002942': 'central + '
                                                                 'gene',
                                                   'AGAP002949': 'central - '
                                                                 'gene',
                                                   'AGAP004676': 'far right + '
                                                                 'gene',
                                                   'AGAP004674': 'far right - '
                                                                 'gene'},
                                   'gene_labelset': None},
 'cell_17_call_1_ag3_plot_genes': {'region': '2R',
                                   'sizing_mode': 'stretch_width',
                                   'width': None,
                                   'height': 200,
                                   'show': True,
                                   'toolbar_location': 'above',
                                   'x_range': None,
                                   'title': None,
                                   'output_backend': 'webgl',
                                   'gene_labels': None,
                                   'gene_labelset': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_genes'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_3_call_1_ag3_plot_genes': '01_ag3_genes',
 'cell_4_call_1_ag3_plot_genes': '02_ag3_genes',
 'notebook_cell_6': '03_cell_6_figure',
 'cell_7_call_1_ag3_plot_transcript': '04_ag3_transcript_AGAP004707-RD',
 'cell_9_call_1_ag3_plot_transcript': '05_ag3_transcript_AGAP004050-RA',
 'notebook_cell_11': '06_cell_11_figure',
 'cell_12_call_1_af1_plot_genes': '07_af1_genes',
 'cell_13_call_1_af1_plot_genes': '08_af1_genes',
 'cell_14_call_1_af1_plot_transcript': '09_af1_transcript_LOC125767311_t1',
 'cell_15_call_1_af1_plot_transcript': '10_af1_transcript_LOC125767311_t2',
 'cell_16_call_1_ag3_plot_genes': '11_ag3_genes',
 'cell_17_call_1_ag3_plot_genes': '12_ag3_genes'}


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
    import bokeh.layouts as bklay
    import bokeh.plotting as bkplt
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.display(_call_api_with_parameters(ag3.plot_genes, 'cell_3_call_1_ag3_plot_genes', "2R"))
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    nbrt.display(_call_api_with_parameters(ag3.plot_genes, 'cell_4_call_1_ag3_plot_genes', "2R:28,000,000-29,000,000"))
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    fig = bklay.column(
        [
            _call_api_with_parameters(ag3.plot_genes, 'cell_5_call_1_ag3_plot_genes', "2R", show=False),
            _call_api_with_parameters(ag3.plot_genes, 'cell_5_call_2_ag3_plot_genes', "2L", show=False),
        ],
        sizing_mode="stretch_width",
    )
    nbrt.display(bkplt.show(fig))
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.genome_feature_children, 'cell_6_call_1_ag3_genome_feature_children', parent="AGAP004707-RD"))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_transcript, 'cell_7_call_1_ag3_plot_transcript', "AGAP004707-RD"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.genome_feature_children, 'cell_8_call_1_ag3_genome_feature_children', parent="AGAP004050-RA"))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_transcript, 'cell_9_call_1_ag3_plot_transcript', "AGAP004050-RA"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    fig1 = _call_api_with_parameters(ag3.plot_transcript, 'cell_10_call_1_ag3_plot_transcript', f"AGAP004707-RA", show=False)
    figs = [fig1] + [
        _call_api_with_parameters(ag3.plot_transcript, 'cell_10_call_2_ag3_plot_transcript', f"AGAP004707-R{x}", x_range=fig1.x_range, show=False, toolbar_location=None)
        for x in "BCD"
    ]

    fig = bklay.column(figs, sizing_mode="stretch_width")
    nbrt.display(bkplt.show(fig))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
    )
    nbrt.display(af1)
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(af1.plot_genes, 'cell_12_call_1_af1_plot_genes', "3RL"))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(af1.plot_genes, 'cell_13_call_1_af1_plot_genes', "2RL:28,000,000-29,000,000"))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(af1.plot_transcript, 'cell_14_call_1_af1_plot_transcript', "LOC125767311_t1"))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(af1.plot_transcript, 'cell_15_call_1_af1_plot_transcript', "LOC125767311_t2"))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(ag3.plot_genes, 'cell_16_call_1_ag3_plot_genes', region="2R", gene_labels={
            "AGAP001096": "far left + gene",
            "AGAP001099": "far left - gene",
            "AGAP002942": "central + gene",
            "AGAP002949": "central - gene",
            "AGAP004676": "far right + gene",
            "AGAP004674": "far right - gene",
        }))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    import bokeh
    import pandas as pd

    data = pd.DataFrame.from_dict(
        [
            {"pos": 10_000_000, "y": 2, "label": "Custom Label A"},
            {"pos": 30_000_000, "y": 0.9, "label": "Custom Label B"},
            {"pos": 50_000_000, "y": -0.1, "label": "Custom Label C"},
        ]
    )
    data_as_cds = bokeh.models.ColumnDataSource(data)
    gene_labelset = bokeh.models.LabelSet(
        source=data_as_cds,
        x="pos",
        y="y",
        text="label",
        text_align="center",
        text_baseline="middle",
        text_font_size="9pt",
        text_color="blue",
    )

    nbrt.display(_call_api_with_parameters(ag3.plot_genes, 'cell_17_call_1_ag3_plot_genes', region="2R", gene_labelset=gene_labelset, height=200))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_genes.ipynb',
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
