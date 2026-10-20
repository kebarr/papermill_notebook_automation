#!/usr/bin/env python3
"""biallelic_snps: the code from notebooks_fixed_parameters_cells/biallelic_snps.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/biallelic_snps.py                      # the notebook's defaults
    python scripts/biallelic_snps.py --config runs.csv    # one run per CSV row
    python scripts/biallelic_snps.py --list-parameters    # what a CSV can set
    python scripts/biallelic_snps.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/biallelic_snps_performance.csv'
API_CALL_PARAMETERS = {'cell_2_call_1_ag3_snp_calls': {'region': '3L',
                                 'sample_sets': 'AG1000G-BF-A',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': None,
                                 'site_class': None,
                                 'inline_array': True,
                                 'chunks': 'native',
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42},
 'cell_5_call_1_ag3_biallelic_snp_calls': {'region': '3L',
                                           'sample_sets': 'AG1000G-BF-A',
                                           'sample_query': None,
                                           'sample_query_options': None,
                                           'sample_indices': None,
                                           'site_mask': None,
                                           'site_class': None,
                                           'inline_array': True,
                                           'chunks': '300MiB',
                                           'cohort_size': None,
                                           'min_cohort_size': None,
                                           'max_cohort_size': None,
                                           'random_seed': 42,
                                           'min_minor_ac': None,
                                           'max_missing_an': None,
                                           'n_snps': None,
                                           'thin_offset': 0},
 'cell_13_call_1_ag3_biallelic_snp_calls': {'region': '3L',
                                            'sample_sets': 'AG1000G-BF-A',
                                            'sample_query': None,
                                            'sample_query_options': None,
                                            'sample_indices': None,
                                            'site_mask': None,
                                            'site_class': None,
                                            'inline_array': True,
                                            'chunks': '300MiB',
                                            'cohort_size': None,
                                            'min_cohort_size': None,
                                            'max_cohort_size': None,
                                            'random_seed': 42,
                                            'min_minor_ac': 1,
                                            'max_missing_an': 50,
                                            'n_snps': None,
                                            'thin_offset': 0},
 'cell_16_call_1_ag3_biallelic_snp_calls': {'region': '3L',
                                            'sample_sets': 'AG1000G-BF-A',
                                            'sample_query': None,
                                            'sample_query_options': None,
                                            'sample_indices': None,
                                            'site_mask': None,
                                            'site_class': None,
                                            'inline_array': True,
                                            'chunks': '300MiB',
                                            'cohort_size': None,
                                            'min_cohort_size': None,
                                            'max_cohort_size': None,
                                            'random_seed': 42,
                                            'min_minor_ac': 1,
                                            'max_missing_an': 50,
                                            'n_snps': 100000,
                                            'thin_offset': 0}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/biallelic_snps'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {}


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
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ds = _call_api_with_parameters(ag3.snp_calls, 'cell_2_call_1_ag3_snp_calls', region="3L", sample_sets="AG1000G-BF-A")
    nbrt.display(ds)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.display(ds["variant_allele"])
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(ds["variant_allele"].values)
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds_bi = _call_api_with_parameters(ag3.biallelic_snp_calls, 'cell_5_call_1_ag3_biallelic_snp_calls', region="3L", sample_sets="AG1000G-BF-A", chunks="300MiB")
    nbrt.display(ds_bi)
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(ds_bi["variant_allele"])
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(ds_bi["variant_allele"].values)
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(ds_bi["variant_allele_count"])
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    _cell_timer = nbrt.time_cell_start()  # %%time
    nbrt.display(ds_bi["variant_allele_count"].values)
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(ds_bi["call_genotype"])
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds["call_genotype"][:100_000].values;
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds_bi["call_genotype"][:100_000].values;
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds_bi2 = _call_api_with_parameters(ag3.biallelic_snp_calls, 'cell_13_call_1_ag3_biallelic_snp_calls', region="3L", sample_sets="AG1000G-BF-A", max_missing_an=50, min_minor_ac=1, chunks="300MiB")
    nbrt.display(ds_bi2)
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(ds_bi2["call_genotype"])
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds_bi2["call_genotype"][:100_000].values;
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds_bi3 = _call_api_with_parameters(ag3.biallelic_snp_calls, 'cell_16_call_1_ag3_biallelic_snp_calls', region="3L", sample_sets="AG1000G-BF-A", max_missing_an=50, min_minor_ac=1, n_snps=100_000, chunks="300MiB")
    nbrt.display(ds_bi3)
    nbrt.time_cell_report(_cell_timer)
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(ds_bi3["call_genotype"])
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    _cell_timer = nbrt.time_cell_start()  # %%time
    ds_bi3["call_genotype"][:1000].values;
    nbrt.time_cell_report(_cell_timer)


if __name__ == "__main__":
    nbrt.main(
        notebook='biallelic_snps.ipynb',
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
