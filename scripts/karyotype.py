#!/usr/bin/env python3
"""karyotype: the code from notebooks_fixed_parameters_cells/karyotype.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/karyotype.py                      # the notebook's defaults
    python scripts/karyotype.py --config runs.csv    # one run per CSV row
    python scripts/karyotype.py --list-parameters    # what a CSV can set
    python scripts/karyotype.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/karyotype_performance.csv'
API_CALL_PARAMETERS = {'cell_6_call_1_ag3_karyotype': {'inversion': '2La',
                                 'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                 'sample_query': None,
                                 'sample_query_options': None},
 'cell_7_call_1_ag3_pca': {'region': '__KEEP_CALLSITE_VALUE__',
                           'n_snps': 50000,
                           'n_components': 20,
                           'thin_offset': 0,
                           'sample_sets': '__KEEP_CALLSITE_VALUE__',
                           'sample_query': None,
                           'sample_query_options': None,
                           'sample_indices': None,
                           'cohorts': None,
                           'cohort_size': None,
                           'min_cohort_size': None,
                           'max_cohort_size': None,
                           'site_mask': 'default',
                           'site_class': None,
                           'min_minor_ac': 2,
                           'max_missing_an': 0,
                           'imputation_method': 'most_common',
                           'exclude_samples': None,
                           'fit_exclude_samples': None,
                           'random_seed': 42,
                           'inline_array': True,
                           'chunks': 'native'},
 'cell_8_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                       'x': 'PC1',
                                       'y': 'PC2',
                                       'color': 'taxon',
                                       'symbol': None,
                                       'opacity': 0.9,
                                       'jitter_frac': 0.02,
                                       'random_seed': 42,
                                       'width': 600,
                                       'height': 500,
                                       'marker_size': 10,
                                       'color_discrete_sequence': None,
                                       'color_discrete_map': None,
                                       'category_orders': None,
                                       'legend_sizing': 'constant',
                                       'show': True,
                                       'renderer': None,
                                       'render_mode': 'svg',
                                       'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_9_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                       'x': 'PC1',
                                       'y': 'PC2',
                                       'color': 'karyotype_2La',
                                       'symbol': 'taxon',
                                       'opacity': 0.9,
                                       'jitter_frac': 0.02,
                                       'random_seed': 42,
                                       'width': 600,
                                       'height': 500,
                                       'marker_size': 10,
                                       'color_discrete_sequence': None,
                                       'color_discrete_map': None,
                                       'category_orders': None,
                                       'legend_sizing': 'constant',
                                       'show': True,
                                       'renderer': None,
                                       'render_mode': 'svg',
                                       'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_10_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'karyotype_2La_mean',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 700,
                                        'height': 500,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_13_call_1_ag3_karyotype': {'inversion': '2Rb',
                                  'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                  'sample_query': None,
                                  'sample_query_options': None},
 'cell_14_call_1_ag3_pca': {'region': '__KEEP_CALLSITE_VALUE__',
                            'n_snps': 50000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '__KEEP_CALLSITE_VALUE__',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_15_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'karyotype_2Rb',
                                        'symbol': 'taxon',
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 600,
                                        'height': 500,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_18_call_1_ag3_karyotype': {'inversion': '2Rc_gam',
                                  'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                  'sample_query': "taxon == 'gambiae'",
                                  'sample_query_options': None},
 'cell_20_call_1_ag3_pca': {'region': '__KEEP_CALLSITE_VALUE__',
                            'n_snps': 50000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '__KEEP_CALLSITE_VALUE__',
                            'sample_query': "taxon == 'gambiae'",
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_21_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'karyotype_2Rc_gam',
                                        'symbol': 'taxon',
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 600,
                                        'height': 500,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_22_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'country',
                                        'symbol': 'taxon',
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 600,
                                        'height': 500,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_24_call_1_ag3_karyotype': {'inversion': '2Rc_col',
                                  'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                  'sample_query': "taxon == 'coluzzii'",
                                  'sample_query_options': None},
 'cell_26_call_1_ag3_pca': {'region': '__KEEP_CALLSITE_VALUE__',
                            'n_snps': 50000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '__KEEP_CALLSITE_VALUE__',
                            'sample_query': "taxon == 'coluzzii'",
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_27_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'karyotype_2Rc_col',
                                        'symbol': 'country',
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 600,
                                        'height': 500,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/karyotype'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_8_call_1_ag3_plot_pca_coords': '01_ag3_pca_coords_by_taxon',
 'cell_9_call_1_ag3_plot_pca_coords': '02_ag3_pca_coords_by_karyotype_2La',
 'cell_10_call_1_ag3_plot_pca_coords': '03_ag3_pca_coords_by_karyotype_2La_mean',
 'notebook_cell_12': '04_hist_karyotype_2La_mean',
 'cell_15_call_1_ag3_plot_pca_coords': '05_ag3_pca_coords_by_karyotype_2Rb',
 'notebook_cell_17': '06_hist_karyotype_2Rb_mean',
 'notebook_cell_20': '07_hist_karyotype_2Rc_gam_mean',
 'cell_21_call_1_ag3_plot_pca_coords': '08_ag3_pca_coords_by_karyotype_2Rc_gam',
 'cell_22_call_1_ag3_plot_pca_coords': '09_ag3_pca_coords_by_country',
 'notebook_cell_26': '10_hist_karyotype_2Rc_col_mean',
 'cell_27_call_1_ag3_plot_pca_coords': '11_ag3_pca_coords_by_karyotype_2Rc_col'}


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
    sample_sets = ["AG1000G-BF-A", "AG1000G-GH"]
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    # Not sure if these inversion coordinates are exactly right, but should do as an approximation.
    region_2la = "2L:20,528,089-42,165,182"
    region_2rb = "2R:19,444,433-26,313,071"
    region_2rj = "2R:4,050,701-14,952,998"
    region_2rc = "2R:27,025,144-31,450,000"
    region_2ru = "2R:33,575,891-34,873,652"
    region_2rd = "2R:33,575,891-41,360,919"
    region_2rk = "2R:25,146,360-30,717,395"
    # ## 2La
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    kt_df_2la = _call_api_with_parameters(ag3.karyotype, 'cell_6_call_1_ag3_karyotype', inversion="2La", sample_sets=sample_sets)
    nbrt.display(kt_df_2la.head())
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    pca_df_2la, pca_evr_2la = _call_api_with_parameters(ag3.pca, 'cell_7_call_1_ag3_pca', region=region_2la, sample_sets=sample_sets, n_snps=50_000)
    pca_df_2la = pca_df_2la.merge(kt_df_2la, on="sample_id")
    nbrt.display(pca_df_2la.head())
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_8_call_1_ag3_plot_pca_coords', pca_df_2la, color="taxon", width=600, height=500))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_9_call_1_ag3_plot_pca_coords', pca_df_2la, color="karyotype_2La", symbol="taxon", width=600, height=500))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_10_call_1_ag3_plot_pca_coords', pca_df_2la, color="karyotype_2La_mean", width=700, height=500))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(kt_df_2la["karyotype_2La_mean"].hist(backend="plotly"))
    # ## 2Rb
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    kt_df_2rb = _call_api_with_parameters(ag3.karyotype, 'cell_13_call_1_ag3_karyotype', inversion="2Rb", sample_sets=sample_sets)
    nbrt.display(kt_df_2rb.head())
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    pca_df_2rb, pca_evr_2rb = _call_api_with_parameters(ag3.pca, 'cell_14_call_1_ag3_pca', region=region_2rb, sample_sets=sample_sets, n_snps=50_000)
    pca_df_2rb = pca_df_2rb.merge(kt_df_2rb, on="sample_id")
    nbrt.display(pca_df_2rb.head())
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_15_call_1_ag3_plot_pca_coords', pca_df_2rb, color="karyotype_2Rb", symbol="taxon", width=600, height=500))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(pca_df_2rb["karyotype_2Rb_mean"].hist(backend="plotly"))
    # ## 2Rc_gam
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    kt_df_2rc_gam = _call_api_with_parameters(ag3.karyotype, 'cell_18_call_1_ag3_karyotype', inversion="2Rc_gam", sample_sets=sample_sets, sample_query="taxon == 'gambiae'")
    nbrt.display(kt_df_2rc_gam.head())
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    fig = kt_df_2rc_gam["karyotype_2Rc_gam_mean"].hist(backend="plotly")
    fig.update_xaxes(range=[0, 2])
    nbrt.display(fig)
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    pca_df_2rc_gam, _ = _call_api_with_parameters(ag3.pca, 'cell_20_call_1_ag3_pca', region=region_2rc, sample_sets=sample_sets, sample_query="taxon == 'gambiae'", n_snps=50_000)
    pca_df_2rc_gam = pca_df_2rc_gam.merge(kt_df_2rc_gam, on="sample_id")
    nbrt.display(pca_df_2rc_gam.head())
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_21_call_1_ag3_plot_pca_coords', pca_df_2rc_gam, color="karyotype_2Rc_gam", symbol="taxon", width=600, height=500))
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_22_call_1_ag3_plot_pca_coords', pca_df_2rc_gam, color="country", symbol="taxon", width=600, height=500))
    # ## 2Rc_col
    # --- Notebook cell 25 ---
    nbrt.start_cell("notebook_cell_25")
    kt_df_2rc_col = _call_api_with_parameters(ag3.karyotype, 'cell_24_call_1_ag3_karyotype', inversion="2Rc_col", sample_sets=sample_sets, sample_query="taxon == 'coluzzii'")
    nbrt.display(kt_df_2rc_col.head())
    # --- Notebook cell 26 ---
    nbrt.start_cell("notebook_cell_26")
    fig = kt_df_2rc_col["karyotype_2Rc_col_mean"].hist(backend="plotly")
    fig.update_xaxes(range=[0, 2])
    nbrt.display(fig)
    # --- Notebook cell 27 ---
    nbrt.start_cell("notebook_cell_27")
    pca_df_2rc_col, _ = _call_api_with_parameters(ag3.pca, 'cell_26_call_1_ag3_pca', region=region_2rc, sample_sets=sample_sets, sample_query="taxon == 'coluzzii'", n_snps=50_000)
    pca_df_2rc_col = pca_df_2rc_col.merge(kt_df_2rc_col, on="sample_id")
    nbrt.display(pca_df_2rc_col.head())
    # --- Notebook cell 28 ---
    nbrt.start_cell("notebook_cell_28")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_27_call_1_ag3_plot_pca_coords', pca_df_2rc_col, color="karyotype_2Rc_col", symbol="country", width=600, height=500))


if __name__ == "__main__":
    nbrt.main(
        notebook='karyotype.ipynb',
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
