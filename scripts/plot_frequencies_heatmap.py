#!/usr/bin/env python3
"""plot_frequencies_heatmap: the code from notebooks_fixed_parameters_cells/plot_frequencies_heatmap.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_frequencies_heatmap.py                      # the notebook's defaults
    python scripts/plot_frequencies_heatmap.py --config runs.csv    # one run per CSV row
    python scripts/plot_frequencies_heatmap.py --list-parameters    # what a CSV can set
    python scripts/plot_frequencies_heatmap.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_frequencies_heatmap_performance.csv'
API_CALL_PARAMETERS = {'cell_4_call_1_ag3_snp_allele_frequencies': {'transcript': 'AGAP004707-RD',
                                              'region': None,
                                              'cohorts': 'admin1_year',
                                              'sample_query': 'taxon == '
                                                              "'coluzzii'",
                                              'sample_query_options': None,
                                              'min_cohort_size': 10,
                                              'site_mask': None,
                                              'sample_sets': ('AG1000G-BF-A',
                                                              'AG1000G-BF-B',
                                                              'AG1000G-BF-C'),
                                              'drop_invariant': True,
                                              'effects': True,
                                              'include_counts': False,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_6_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_7_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_8_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_9_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
                                                'title': 'SNP frequencies: '
                                                         'Vgsc',
                                                'show': True,
                                                'renderer': None,
                                                'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_10_call_1_af1_sample_sets': {'release': None},
 'cell_11_call_1_af1_genome_features': {'region': None,
                                        'attributes': 'default'},
 'cell_12_call_1_af1_snp_allele_frequencies': {'transcript': 'LOC125767311_t1',
                                               'region': None,
                                               'cohorts': 'admin1_year',
                                               'sample_query': None,
                                               'sample_query_options': None,
                                               'min_cohort_size': 10,
                                               'site_mask': None,
                                               'sample_sets': ('1231-VO-MULTI-WONDJI-VMF00043',
                                                               '1240-VO-CD-KOEKEMOER-VMF00099'),
                                               'drop_invariant': True,
                                               'effects': True,
                                               'include_counts': False,
                                               'chunks': 'native',
                                               'inline_array': True},
 'cell_14_call_1_af1_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_16_call_1_ag3_aa_allele_frequencies': {'transcript': 'AGAP004707-RD',
                                              'cohorts': 'admin1_year',
                                              'sample_query': 'taxon == '
                                                              "'coluzzii'",
                                              'sample_query_options': None,
                                              'min_cohort_size': 10,
                                              'site_mask': None,
                                              'sample_sets': ('AG1000G-BF-A',
                                                              'AG1000G-BF-B',
                                                              'AG1000G-BF-C'),
                                              'drop_invariant': True,
                                              'include_counts': False,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_19_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_20_call_1_ag3_aa_allele_frequencies': {'transcript': 'AGAP004707-RD',
                                              'cohorts': 'admin1_year',
                                              'sample_query': 'taxon == '
                                                              "'coluzzii'",
                                              'sample_query_options': None,
                                              'min_cohort_size': 10,
                                              'site_mask': None,
                                              'sample_sets': '3.0',
                                              'drop_invariant': True,
                                              'include_counts': False,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_21_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_22_call_1_ag3_aa_allele_frequencies': {'transcript': 'AGAP004707-RD',
                                              'cohorts': 'admin1_year',
                                              'sample_query': None,
                                              'sample_query_options': None,
                                              'min_cohort_size': 10,
                                              'site_mask': None,
                                              'sample_sets': '3.0',
                                              'drop_invariant': True,
                                              'include_counts': False,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_22_call_2_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_23_call_1_af1_aa_allele_frequencies': {'transcript': 'LOC125767311_t1',
                                              'cohorts': 'admin1_year',
                                              'sample_query': None,
                                              'sample_query_options': None,
                                              'min_cohort_size': 10,
                                              'site_mask': None,
                                              'sample_sets': ('1231-VO-MULTI-WONDJI-VMF00043',
                                                              '1240-VO-CD-KOEKEMOER-VMF00099'),
                                              'drop_invariant': True,
                                              'include_counts': False,
                                              'chunks': 'native',
                                              'inline_array': True},
 'cell_24_call_1_af1_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_27_call_1_ag3_gene_cnv_frequencies': {'region': '__KEEP_CALLSITE_VALUE__',
                                             'cohorts': 'admin1_year',
                                             'sample_query': 'taxon == '
                                                             "'coluzzii'",
                                             'sample_query_options': None,
                                             'min_cohort_size': 10,
                                             'max_coverage_variance': 0.2,
                                             'sample_sets': ('AG1000G-BF-A',
                                                             'AG1000G-BF-B',
                                                             'AG1000G-BF-C'),
                                             'drop_invariant': True,
                                             'include_counts': False,
                                             'chunks': 'native',
                                             'inline_array': True},
 'cell_29_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_30_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
 'cell_31_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
                                                 'color_continuous_scale': 'Blues',
                                                 'title': 'Cyp6p/aa gene CNV '
                                                          'frequencies',
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_32_call_1_ag3_gene_cnv_frequencies': {'region': '__KEEP_CALLSITE_VALUE__',
                                             'cohorts': 'admin1_year',
                                             'sample_query': 'taxon == '
                                                             "'coluzzii'",
                                             'sample_query_options': None,
                                             'min_cohort_size': 10,
                                             'max_coverage_variance': 0.2,
                                             'sample_sets': ('AG1000G-BF-A',
                                                             'AG1000G-BF-B',
                                                             'AG1000G-BF-C'),
                                             'drop_invariant': True,
                                             'include_counts': False,
                                             'chunks': 'native',
                                             'inline_array': True},
 'cell_33_call_1_ag3_plot_frequencies_heatmap': {'df': '__KEEP_CALLSITE_VALUE__',
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
                                                 'color_continuous_scale': 'Blues',
                                                 'title': 'Cyp gene CNV '
                                                          'frequencies',
                                                 'show': True,
                                                 'renderer': None,
                                                 'kwargs': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_frequencies_heatmap'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_6_call_1_ag3_plot_frequencies_heatmap': '01_ag3_frequencies_heatmap',
 'cell_7_call_1_ag3_plot_frequencies_heatmap': '02_ag3_frequencies_heatmap',
 'cell_8_call_1_ag3_plot_frequencies_heatmap': '03_ag3_frequencies_heatmap',
 'cell_9_call_1_ag3_plot_frequencies_heatmap': '04_ag3_frequencies_heatmap',
 'cell_14_call_1_af1_plot_frequencies_heatmap': '05_af1_frequencies_heatmap',
 'cell_19_call_1_ag3_plot_frequencies_heatmap': '06_ag3_frequencies_heatmap',
 'cell_21_call_1_ag3_plot_frequencies_heatmap': '07_ag3_frequencies_heatmap',
 'cell_22_call_2_ag3_plot_frequencies_heatmap': '08_ag3_frequencies_heatmap',
 'cell_24_call_1_af1_plot_frequencies_heatmap': '09_af1_frequencies_heatmap',
 'cell_29_call_1_ag3_plot_frequencies_heatmap': '10_ag3_frequencies_heatmap',
 'cell_30_call_1_ag3_plot_frequencies_heatmap': '11_ag3_frequencies_heatmap',
 'cell_31_call_1_ag3_plot_frequencies_heatmap': '12_ag3_frequencies_heatmap',
 'cell_33_call_1_ag3_plot_frequencies_heatmap': '13_ag3_frequencies_heatmap'}


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

    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230516",
    )
    nbrt.display(ag3)
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    import malariagen_data

    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        cohorts_analysis="20230823",
    )
    nbrt.display(af1)
    # ## SNP allele frequencies
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    allele_freqs_df = _call_api_with_parameters(ag3.snp_allele_frequencies, 'cell_4_call_1_ag3_snp_allele_frequencies', transcript="AGAP004707-RD", cohorts="admin1_year", sample_sets=("AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-BF-C"), sample_query="taxon == 'coluzzii'")
    nbrt.display(allele_freqs_df)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    snps_df = allele_freqs_df.query("effect == 'NON_SYNONYMOUS_CODING' and max_af > 0.05")
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_6_call_1_ag3_plot_frequencies_heatmap', df=snps_df))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_7_call_1_ag3_plot_frequencies_heatmap', df=snps_df.iloc[:2]))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_8_call_1_ag3_plot_frequencies_heatmap', df=snps_df.iloc[:1]))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_9_call_1_ag3_plot_frequencies_heatmap', df=snps_df, title="SNP frequencies: Vgsc"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(af1.sample_sets, 'cell_10_call_1_af1_sample_sets'))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(af1.genome_features, 'cell_11_call_1_af1_genome_features'))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    allele_freqs_df = _call_api_with_parameters(af1.snp_allele_frequencies, 'cell_12_call_1_af1_snp_allele_frequencies', transcript="LOC125767311_t1", cohorts="admin1_year", sample_sets=("1231-VO-MULTI-WONDJI-VMF00043", "1240-VO-CD-KOEKEMOER-VMF00099"))
    nbrt.display(allele_freqs_df)
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    snps_df = allele_freqs_df.query("effect == 'NON_SYNONYMOUS_CODING' and max_af > 0.05")
    nbrt.display(snps_df)
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(af1.plot_frequencies_heatmap, 'cell_14_call_1_af1_plot_frequencies_heatmap', df=snps_df))
    # ## Amino acid frequencies
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    aa_freqs_df = _call_api_with_parameters(ag3.aa_allele_frequencies, 'cell_16_call_1_ag3_aa_allele_frequencies', transcript="AGAP004707-RD", cohorts="admin1_year", sample_sets=("AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-BF-C"), sample_query="taxon == 'coluzzii'")
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    aa_df = aa_freqs_df.query("max_af > 0.05")
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    nbrt.display(aa_df)
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_19_call_1_ag3_plot_frequencies_heatmap', df=aa_df))
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    aa_freqs_df = _call_api_with_parameters(ag3.aa_allele_frequencies, 'cell_20_call_1_ag3_aa_allele_frequencies', transcript="AGAP004707-RD", cohorts="admin1_year", sample_sets="3.0", sample_query="taxon == 'coluzzii'").query("max_af > 0.05")
    nbrt.display(aa_freqs_df)
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_21_call_1_ag3_plot_frequencies_heatmap', df=aa_freqs_df))
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    aa_freqs_df = _call_api_with_parameters(ag3.aa_allele_frequencies, 'cell_22_call_1_ag3_aa_allele_frequencies', transcript="AGAP004707-RD", cohorts="admin1_year", sample_sets="3.0").query("max_af > 0.05")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_22_call_2_ag3_plot_frequencies_heatmap', df=aa_freqs_df))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    aa_freqs_df = _call_api_with_parameters(af1.aa_allele_frequencies, 'cell_23_call_1_af1_aa_allele_frequencies', transcript="LOC125767311_t1", cohorts="admin1_year", sample_sets=("1231-VO-MULTI-WONDJI-VMF00043", "1240-VO-CD-KOEKEMOER-VMF00099")).query("max_af > 0.05")
    nbrt.display(aa_freqs_df)
    # --- Notebook cell 25 ---
    nbrt.start_cell("notebook_cell_25")
    nbrt.display(_call_api_with_parameters(af1.plot_frequencies_heatmap, 'cell_24_call_1_af1_plot_frequencies_heatmap', df=aa_freqs_df))
    # ## Gene CNV frequencies
    # --- Notebook cell 27 ---
    nbrt.start_cell("notebook_cell_27")
    cyp6aap_region = "2R:28,450,000-28,510,000"
    # --- Notebook cell 28 ---
    nbrt.start_cell("notebook_cell_28")
    cyp6aap_cnv_freqs_df = _call_api_with_parameters(ag3.gene_cnv_frequencies, 'cell_27_call_1_ag3_gene_cnv_frequencies', region=cyp6aap_region, cohorts="admin1_year", sample_sets=("AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-BF-C"), sample_query="taxon == 'coluzzii'")
    # --- Notebook cell 29 ---
    nbrt.start_cell("notebook_cell_29")
    nbrt.display(cyp6aap_cnv_freqs_df)
    # --- Notebook cell 30 ---
    nbrt.start_cell("notebook_cell_30")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_29_call_1_ag3_plot_frequencies_heatmap', df=cyp6aap_cnv_freqs_df))
    # --- Notebook cell 31 ---
    nbrt.start_cell("notebook_cell_31")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_30_call_1_ag3_plot_frequencies_heatmap', df=cyp6aap_cnv_freqs_df[["label", "frq_BF-09_colu_2014"]]))
    # --- Notebook cell 32 ---
    nbrt.start_cell("notebook_cell_32")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_31_call_1_ag3_plot_frequencies_heatmap', df=cyp6aap_cnv_freqs_df, color_continuous_scale="Blues", title="Cyp6p/aa gene CNV frequencies"))
    # --- Notebook cell 33 ---
    nbrt.start_cell("notebook_cell_33")
    interesting_cyp_genes = [
        "AGAP002862",  # Cyp6aa1
        "AGAP013128",  # Cyp6aa2
        "AGAP002865",  # Cyp6p3
        "AGAP000818",  # Cyp9k1
        "AGAP008212",  # Cyp6m2
        "AGAP008218",  # Cyp6z2
    ]

    cyp_cnv_freqs_df = _call_api_with_parameters(ag3.gene_cnv_frequencies, 'cell_32_call_1_ag3_gene_cnv_frequencies', region=interesting_cyp_genes, cohorts="admin1_year", sample_sets=("AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-BF-C"), sample_query="taxon == 'coluzzii'")
    # --- Notebook cell 34 ---
    nbrt.start_cell("notebook_cell_34")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_heatmap, 'cell_33_call_1_ag3_plot_frequencies_heatmap', df=cyp_cnv_freqs_df, color_continuous_scale="Blues", title="Cyp gene CNV frequencies"))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_frequencies_heatmap.ipynb',
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
