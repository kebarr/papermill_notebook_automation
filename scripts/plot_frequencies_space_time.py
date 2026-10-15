#!/usr/bin/env python3
"""plot_frequencies_space_time: the code from notebooks/plot_frequencies_space_time.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_frequencies_space_time.py                      # the notebook's defaults
    python scripts/plot_frequencies_space_time.py --config runs.csv    # one run per CSV row
    python scripts/plot_frequencies_space_time.py --list-parameters    # what a CSV can set
    python scripts/plot_frequencies_space_time.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_frequencies_space_time_performance.csv'
API_CALL_PARAMETERS = {'cell_5_call_1_ag3_gene_cnv_frequencies_advanced': {'region': '2R:28,450,000-28,510,000',
                                                     'area_by': 'admin1_iso',
                                                     'period_by': 'year',
                                                     'sample_sets': ['AG1000G-BF-A',
                                                                     'AG1000G-BF-B'],
                                                     'sample_query': "taxon in ['coluzzii', "
                                                                     "'gambiae']",
                                                     'sample_query_options': None,
                                                     'min_cohort_size': 10,
                                                     'drop_invariant': True,
                                                     'variant_query': None,
                                                     'max_coverage_variance': 0.2,
                                                     'nobs_mode': 'called',
                                                     'ci_method': 'wilson',
                                                     'chunks': 'native',
                                                     'inline_array': True,
                                                     'taxon_by': 'taxon',
                                                     'filter_unassigned': None},
 'cell_6_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                    'height': 500,
                                                    'width': 1000,
                                                    'title': True,
                                                    'legend_sizing': 'constant',
                                                    'show': True,
                                                    'renderer': None,
                                                    'taxa': None,
                                                    'areas': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_7_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                    'height': 500,
                                                    'width': 1000,
                                                    'title': True,
                                                    'legend_sizing': 'constant',
                                                    'show': True,
                                                    'renderer': None,
                                                    'taxa': 'gambiae',
                                                    'areas': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_8_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                    'height': 500,
                                                    'width': 1000,
                                                    'title': True,
                                                    'legend_sizing': 'constant',
                                                    'show': True,
                                                    'renderer': None,
                                                    'taxa': ('gambiae', 'arabiensis'),
                                                    'areas': None,
                                                    'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_9_call_1_ag3_gene_cnv_frequencies_advanced': {'region': '2R:28,450,000-28,510,000',
                                                     'area_by': 'admin1_iso',
                                                     'period_by': 'year',
                                                     'sample_sets': '3.0',
                                                     'sample_query': None,
                                                     'sample_query_options': None,
                                                     'min_cohort_size': 10,
                                                     'drop_invariant': True,
                                                     'variant_query': None,
                                                     'max_coverage_variance': 0.2,
                                                     'nobs_mode': 'called',
                                                     'ci_method': 'wilson',
                                                     'chunks': 'native',
                                                     'inline_array': True,
                                                     'taxon_by': 'taxon',
                                                     'filter_unassigned': None},
 'cell_10_call_1_ag3_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True},
 'cell_12_call_1_ag3_aa_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                       'area_by': 'admin1_iso',
                                                       'period_by': 'year',
                                                       'sample_sets': ['AG1000G-BF-A',
                                                                       'AG1000G-BF-B'],
                                                       'sample_query': "sex_call == 'F' and taxon "
                                                                       "== 'coluzzii'",
                                                       'sample_query_options': None,
                                                       'min_cohort_size': 10,
                                                       'variant_query': 'max_af > 0.05',
                                                       'site_mask': None,
                                                       'nobs_mode': 'called',
                                                       'ci_method': 'wilson',
                                                       'chunks': 'native',
                                                       'inline_array': True,
                                                       'taxon_by': 'taxon',
                                                       'filter_unassigned': None},
 'cell_13_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                     'height': 400,
                                                     'width': 600,
                                                     'title': True,
                                                     'legend_sizing': 'constant',
                                                     'show': True,
                                                     'renderer': None,
                                                     'taxa': None,
                                                     'areas': None,
                                                     'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_14_call_1_ag3_aa_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                       'area_by': 'admin1_iso',
                                                       'period_by': 'year',
                                                       'sample_sets': '3.0',
                                                       'sample_query': None,
                                                       'sample_query_options': None,
                                                       'min_cohort_size': 10,
                                                       'variant_query': 'max_af > 0.05',
                                                       'site_mask': None,
                                                       'nobs_mode': 'called',
                                                       'ci_method': 'wilson',
                                                       'chunks': 'native',
                                                       'inline_array': True,
                                                       'taxon_by': 'taxon',
                                                       'filter_unassigned': None},
 'cell_15_call_1_ag3_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True},
 'cell_16_call_1_af1_sample_sets': {'release': None},
 'cell_17_call_1_af1_genome_features': {'region': None, 'attributes': 'default'},
 'cell_18_call_1_af1_aa_allele_frequencies_advanced': {'transcript': 'LOC125767311_t1',
                                                       'area_by': 'admin1_iso',
                                                       'period_by': 'year',
                                                       'sample_sets': '1.0',
                                                       'sample_query': None,
                                                       'sample_query_options': None,
                                                       'min_cohort_size': 10,
                                                       'variant_query': 'max_af > 0.05',
                                                       'site_mask': None,
                                                       'nobs_mode': 'called',
                                                       'ci_method': 'wilson',
                                                       'chunks': 'native',
                                                       'inline_array': True,
                                                       'taxon_by': 'taxon',
                                                       'filter_unassigned': None},
 'cell_19_call_1_af1_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True},
 'cell_21_call_1_ag3_snp_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                        'area_by': 'admin1_iso',
                                                        'period_by': 'year',
                                                        'sample_sets': ['AG1000G-BF-A',
                                                                        'AG1000G-BF-B',
                                                                        'AG1000G-UG',
                                                                        'AG1000G-TZ'],
                                                        'sample_query': "taxon in ['gambiae', "
                                                                        "'coluzzii']",
                                                        'sample_query_options': None,
                                                        'min_cohort_size': 10,
                                                        'drop_invariant': True,
                                                        'variant_query': 'max_af > 0.05 and effect '
                                                                         '== '
                                                                         "'NON_SYNONYMOUS_CODING'",
                                                        'site_mask': None,
                                                        'nobs_mode': 'called',
                                                        'ci_method': 'wilson',
                                                        'chunks': 'native',
                                                        'inline_array': True,
                                                        'taxon_by': 'taxon',
                                                        'filter_unassigned': None},
 'cell_22_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                     'height': 900,
                                                     'width': 900,
                                                     'title': True,
                                                     'legend_sizing': 'constant',
                                                     'show': True,
                                                     'renderer': None,
                                                     'taxa': None,
                                                     'areas': None,
                                                     'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_23_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                     'height': 400,
                                                     'width': 900,
                                                     'title': True,
                                                     'legend_sizing': 'constant',
                                                     'show': True,
                                                     'renderer': None,
                                                     'taxa': None,
                                                     'areas': 'BF-09',
                                                     'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_24_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                     'height': 400,
                                                     'width': 900,
                                                     'title': True,
                                                     'legend_sizing': 'constant',
                                                     'show': True,
                                                     'renderer': None,
                                                     'taxa': None,
                                                     'areas': ('BF-09', 'TZ-25'),
                                                     'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_25_call_1_ag3_snp_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                        'area_by': 'admin1_iso',
                                                        'period_by': 'month',
                                                        'sample_sets': '3.0',
                                                        'sample_query': "country == 'Burkina Faso' "
                                                                        'and year > 2010',
                                                        'sample_query_options': None,
                                                        'min_cohort_size': 5,
                                                        'drop_invariant': True,
                                                        'variant_query': 'max_af > 0.05 and effect '
                                                                         '== '
                                                                         "'NON_SYNONYMOUS_CODING'",
                                                        'site_mask': None,
                                                        'nobs_mode': 'called',
                                                        'ci_method': 'wilson',
                                                        'chunks': 'native',
                                                        'inline_array': True,
                                                        'taxon_by': 'taxon',
                                                        'filter_unassigned': None},
 'cell_26_call_1_ag3_plot_frequencies_time_series': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                     'height': 400,
                                                     'width': 800,
                                                     'title': True,
                                                     'legend_sizing': 'constant',
                                                     'show': True,
                                                     'renderer': None,
                                                     'taxa': None,
                                                     'areas': None,
                                                     'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_27_call_1_ag3_snp_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                        'area_by': 'admin1_iso',
                                                        'period_by': 'year',
                                                        'sample_sets': '3.0',
                                                        'sample_query': None,
                                                        'sample_query_options': None,
                                                        'min_cohort_size': 10,
                                                        'drop_invariant': True,
                                                        'variant_query': 'max_af > 0.05 and effect '
                                                                         '== '
                                                                         "'NON_SYNONYMOUS_CODING'",
                                                        'site_mask': None,
                                                        'nobs_mode': 'called',
                                                        'ci_method': 'wilson',
                                                        'chunks': 'native',
                                                        'inline_array': True,
                                                        'taxon_by': 'taxon',
                                                        'filter_unassigned': None},
 'cell_28_call_1_ag3_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True},
 'cell_29_call_1_af1_snp_allele_frequencies_advanced': {'transcript': 'LOC125767311_t1',
                                                        'area_by': 'admin1_iso',
                                                        'period_by': 'year',
                                                        'sample_sets': '1.0',
                                                        'sample_query': None,
                                                        'sample_query_options': None,
                                                        'min_cohort_size': 10,
                                                        'drop_invariant': True,
                                                        'variant_query': 'max_af > 0.05 and effect '
                                                                         '== '
                                                                         "'NON_SYNONYMOUS_CODING'",
                                                        'site_mask': None,
                                                        'nobs_mode': 'called',
                                                        'ci_method': 'wilson',
                                                        'chunks': 'native',
                                                        'inline_array': True,
                                                        'taxon_by': 'taxon',
                                                        'filter_unassigned': None},
 'cell_30_call_1_af1_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True},
 'cell_32_call_1_ag3_snp_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                        'area_by': 'admin1_iso',
                                                        'period_by': 'year',
                                                        'sample_sets': ['AG1000G-BF-A',
                                                                        'AG1000G-BF-B',
                                                                        'AG1000G-UG',
                                                                        'AG1000G-TZ'],
                                                        'sample_query': 'aim_species in '
                                                                        "['gambiae', 'coluzzii']",
                                                        'sample_query_options': None,
                                                        'min_cohort_size': 10,
                                                        'drop_invariant': True,
                                                        'variant_query': 'max_af > 0.05 and effect '
                                                                         '== '
                                                                         "'NON_SYNONYMOUS_CODING'",
                                                        'site_mask': None,
                                                        'nobs_mode': 'called',
                                                        'ci_method': 'wilson',
                                                        'chunks': 'native',
                                                        'inline_array': True,
                                                        'taxon_by': 'aim_species',
                                                        'filter_unassigned': None},
 'cell_33_call_1_ag3_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True},
 'cell_36_call_1_ag3_sample_metadata': {'sample_sets': None,
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_43_call_1_ag3_add_extra_metadata': {'data': '__KEEP_CALLSITE_VALUE__', 'on': 'sample_id'},
 'cell_44_call_1_ag3_sample_metadata': {'sample_sets': None,
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_46_call_1_ag3_snp_allele_frequencies_advanced': {'transcript': 'AGAP004707-RD',
                                                        'area_by': 'admin1_iso',
                                                        'period_by': 'random_year_as_period',
                                                        'sample_sets': None,
                                                        'sample_query': None,
                                                        'sample_query_options': None,
                                                        'min_cohort_size': 10,
                                                        'drop_invariant': True,
                                                        'variant_query': None,
                                                        'site_mask': None,
                                                        'nobs_mode': 'called',
                                                        'ci_method': 'wilson',
                                                        'chunks': 'native',
                                                        'inline_array': True,
                                                        'taxon_by': 'taxon',
                                                        'filter_unassigned': None},
 'cell_47_call_1_ag3_plot_frequencies_interactive_map': {'ds': '__KEEP_CALLSITE_VALUE__',
                                                         'center': (-2, 20),
                                                         'zoom': 3,
                                                         'title': True,
                                                         'epilogue': True}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_frequencies_space_time'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_6_call_1_ag3_plot_frequencies_time_series': '01_ag3_frequencies_time_series',
 'cell_7_call_1_ag3_plot_frequencies_time_series': '02_ag3_frequencies_time_series',
 'cell_8_call_1_ag3_plot_frequencies_time_series': '03_ag3_frequencies_time_series',
 'cell_10_call_1_ag3_plot_frequencies_interactive_map': '04_ag3_frequencies_interactive_map',
 'cell_13_call_1_ag3_plot_frequencies_time_series': '05_ag3_frequencies_time_series',
 'cell_15_call_1_ag3_plot_frequencies_interactive_map': '06_ag3_frequencies_interactive_map',
 'cell_19_call_1_af1_plot_frequencies_interactive_map': '07_af1_frequencies_interactive_map',
 'cell_22_call_1_ag3_plot_frequencies_time_series': '08_ag3_frequencies_time_series',
 'cell_23_call_1_ag3_plot_frequencies_time_series': '09_ag3_frequencies_time_series',
 'cell_24_call_1_ag3_plot_frequencies_time_series': '10_ag3_frequencies_time_series',
 'cell_26_call_1_ag3_plot_frequencies_time_series': '11_ag3_frequencies_time_series',
 'cell_28_call_1_ag3_plot_frequencies_interactive_map': '12_ag3_frequencies_interactive_map',
 'cell_30_call_1_af1_plot_frequencies_interactive_map': '13_af1_frequencies_interactive_map',
 'cell_33_call_1_ag3_plot_frequencies_interactive_map': '14_ag3_frequencies_interactive_map',
 'cell_47_call_1_ag3_plot_frequencies_interactive_map': '15_ag3_frequencies_interactive_map'}


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
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
    )
    nbrt.display(af1)
    # ## Gene CNV frequencies
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    ds = _call_api_with_parameters(ag3.gene_cnv_frequencies_advanced, 'cell_5_call_1_ag3_gene_cnv_frequencies_advanced', region="2R:28,450,000-28,510,000", area_by="admin1_iso", period_by="year", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"], sample_query="taxon in ['coluzzii', 'gambiae']", min_cohort_size=10)
    nbrt.display(ds)
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_6_call_1_ag3_plot_frequencies_time_series', ds, height=500, width=1000))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_7_call_1_ag3_plot_frequencies_time_series', ds, taxa="gambiae", height=500, width=1000))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_8_call_1_ag3_plot_frequencies_time_series', ds, taxa=("gambiae", "arabiensis"), height=500, width=1000))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    ds = _call_api_with_parameters(ag3.gene_cnv_frequencies_advanced, 'cell_9_call_1_ag3_gene_cnv_frequencies_advanced', region="2R:28,450,000-28,510,000", area_by="admin1_iso", period_by="year", sample_sets="3.0", min_cohort_size=10)
    nbrt.display(ds)
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_interactive_map, 'cell_10_call_1_ag3_plot_frequencies_interactive_map', ds))
    # ## Amino acid change frequencies
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    ds = _call_api_with_parameters(ag3.aa_allele_frequencies_advanced, 'cell_12_call_1_ag3_aa_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="year", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"], sample_query="sex_call == 'F' and taxon == 'coluzzii'", min_cohort_size=10, variant_query="max_af > 0.05")
    nbrt.display(ds)
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_13_call_1_ag3_plot_frequencies_time_series', ds, height=400, width=600))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    ds = _call_api_with_parameters(ag3.aa_allele_frequencies_advanced, 'cell_14_call_1_ag3_aa_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="year", sample_sets="3.0", min_cohort_size=10, variant_query="max_af > 0.05")
    nbrt.display(ds)
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_interactive_map, 'cell_15_call_1_ag3_plot_frequencies_interactive_map', ds))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(af1.sample_sets, 'cell_16_call_1_af1_sample_sets'))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(af1.genome_features, 'cell_17_call_1_af1_genome_features'))
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    ds = _call_api_with_parameters(af1.aa_allele_frequencies_advanced, 'cell_18_call_1_af1_aa_allele_frequencies_advanced', transcript="LOC125767311_t1", area_by="admin1_iso", period_by="year", sample_sets="1.0", min_cohort_size=10, variant_query="max_af > 0.05")
    nbrt.display(ds)
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(af1.plot_frequencies_interactive_map, 'cell_19_call_1_af1_plot_frequencies_interactive_map', ds))
    # ## SNP allele frequencies
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    ds = _call_api_with_parameters(ag3.snp_allele_frequencies_advanced, 'cell_21_call_1_ag3_snp_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="year", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-UG", "AG1000G-TZ"], sample_query="taxon in ['gambiae', 'coluzzii']", min_cohort_size=10, drop_invariant=True, variant_query="max_af > 0.05 and effect == 'NON_SYNONYMOUS_CODING'", site_mask=None, nobs_mode="called", ci_method="wilson")
    nbrt.display(ds)
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_22_call_1_ag3_plot_frequencies_time_series', ds, height=900, width=900))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_23_call_1_ag3_plot_frequencies_time_series', ds, areas="BF-09", height=400, width=900))
    # --- Notebook cell 25 ---
    nbrt.start_cell("notebook_cell_25")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_24_call_1_ag3_plot_frequencies_time_series', ds, areas=("BF-09", "TZ-25"), height=400, width=900))
    # --- Notebook cell 26 ---
    nbrt.start_cell("notebook_cell_26")
    ds = _call_api_with_parameters(ag3.snp_allele_frequencies_advanced, 'cell_25_call_1_ag3_snp_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="month", sample_query="country == 'Burkina Faso' and year > 2010", variant_query="max_af > 0.05 and effect == 'NON_SYNONYMOUS_CODING'", min_cohort_size=5, sample_sets="3.0")
    nbrt.display(ds)
    # --- Notebook cell 27 ---
    nbrt.start_cell("notebook_cell_27")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_time_series, 'cell_26_call_1_ag3_plot_frequencies_time_series', ds, height=400, width=800))
    # --- Notebook cell 28 ---
    nbrt.start_cell("notebook_cell_28")
    ds = _call_api_with_parameters(ag3.snp_allele_frequencies_advanced, 'cell_27_call_1_ag3_snp_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="year", variant_query="max_af > 0.05 and effect == 'NON_SYNONYMOUS_CODING'", min_cohort_size=10, sample_sets="3.0")
    nbrt.display(ds)
    # --- Notebook cell 29 ---
    nbrt.start_cell("notebook_cell_29")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_interactive_map, 'cell_28_call_1_ag3_plot_frequencies_interactive_map', ds))
    # --- Notebook cell 30 ---
    nbrt.start_cell("notebook_cell_30")
    ds = _call_api_with_parameters(af1.snp_allele_frequencies_advanced, 'cell_29_call_1_af1_snp_allele_frequencies_advanced', transcript="LOC125767311_t1", area_by="admin1_iso", period_by="year", sample_sets="1.0", min_cohort_size=10, variant_query="max_af > 0.05 and effect == 'NON_SYNONYMOUS_CODING'")
    nbrt.display(ds)
    # --- Notebook cell 31 ---
    nbrt.start_cell("notebook_cell_31")
    nbrt.display(_call_api_with_parameters(af1.plot_frequencies_interactive_map, 'cell_30_call_1_af1_plot_frequencies_interactive_map', ds))
    # ### SNP allele frequencies using `taxon_by`
    # --- Notebook cell 33 ---
    nbrt.start_cell("notebook_cell_33")
    ds = _call_api_with_parameters(ag3.snp_allele_frequencies_advanced, 'cell_32_call_1_ag3_snp_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="year", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B", "AG1000G-UG", "AG1000G-TZ"], sample_query="aim_species in ['gambiae', 'coluzzii']", min_cohort_size=10, drop_invariant=True, variant_query="max_af > 0.05 and effect == 'NON_SYNONYMOUS_CODING'", site_mask=None, nobs_mode="called", ci_method="wilson", taxon_by="aim_species")
    nbrt.display(ds)
    # --- Notebook cell 34 ---
    nbrt.start_cell("notebook_cell_34")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_interactive_map, 'cell_33_call_1_ag3_plot_frequencies_interactive_map', ds))
    # ### SNP allele frequencies using a custom `period_by`
    # --- Notebook cell 37 ---
    nbrt.start_cell("notebook_cell_37")
    sample_metadata_df = _call_api_with_parameters(ag3.sample_metadata, 'cell_36_call_1_ag3_sample_metadata')
    # --- Notebook cell 38 ---
    nbrt.start_cell("notebook_cell_38")
    import pandas as pd
    import numpy as np
    # --- Notebook cell 39 ---
    nbrt.start_cell("notebook_cell_39")
    random_years_as_list = np.random.choice(range(1900, 2100), len(sample_metadata_df))
    nbrt.display(random_years_as_list[:3])
    # --- Notebook cell 40 ---
    nbrt.start_cell("notebook_cell_40")
    random_years_as_period_index = pd.PeriodIndex(random_years_as_list, freq="Y")
    nbrt.display(random_years_as_period_index[:3])
    # --- Notebook cell 41 ---
    nbrt.start_cell("notebook_cell_41")
    extra_metadata_df = pd.DataFrame(
        {
            "sample_id": sample_metadata_df["sample_id"],
            "random_year_as_period": random_years_as_period_index,
        }
    )
    # --- Notebook cell 42 ---
    nbrt.start_cell("notebook_cell_42")
    nbrt.display(type(extra_metadata_df["random_year_as_period"][0]))
    # --- Notebook cell 43 ---
    nbrt.start_cell("notebook_cell_43")
    nbrt.display(extra_metadata_df.head())
    # --- Notebook cell 44 ---
    nbrt.start_cell("notebook_cell_44")
    nbrt.display(_call_api_with_parameters(ag3.add_extra_metadata, 'cell_43_call_1_ag3_add_extra_metadata', extra_metadata_df))
    # --- Notebook cell 45 ---
    nbrt.start_cell("notebook_cell_45")
    extra_sample_metadata_df = _call_api_with_parameters(ag3.sample_metadata, 'cell_44_call_1_ag3_sample_metadata')
    # --- Notebook cell 46 ---
    nbrt.start_cell("notebook_cell_46")
    nbrt.display(extra_sample_metadata_df["random_year_as_period"][:3])
    # --- Notebook cell 47 ---
    nbrt.start_cell("notebook_cell_47")
    ds = _call_api_with_parameters(ag3.snp_allele_frequencies_advanced, 'cell_46_call_1_ag3_snp_allele_frequencies_advanced', transcript="AGAP004707-RD", area_by="admin1_iso", period_by="random_year_as_period")
    nbrt.display(ds)
    # --- Notebook cell 48 ---
    nbrt.start_cell("notebook_cell_48")
    nbrt.display(_call_api_with_parameters(ag3.plot_frequencies_interactive_map, 'cell_47_call_1_ag3_plot_frequencies_interactive_map', ds))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_frequencies_space_time.ipynb',
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
