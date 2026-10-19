#!/usr/bin/env python3
"""ld_pruning: the code from notebooks/ld_pruning.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/ld_pruning.py                      # the notebook's defaults
    python scripts/ld_pruning.py --config runs.csv    # one run per CSV row
    python scripts/ld_pruning.py --list-parameters    # what a CSV can set
    python scripts/ld_pruning.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_biallelic_snps_performance.csv'
API_CALL_PARAMETERS = {'cell_6_call_1_ag3_biallelic_snp_calls_ld_pruned': {'region': '3L',
                                                     'n_snps': 100000,
                                                     'ld_window_size': 500,
                                                     'ld_window_step': 200,
                                                     'ld_threshold': 0.1,
                                                     'thin_offset': 0,
                                                     'sample_sets': 'AG1000G-BF-A',
                                                     'sample_query': None,
                                                     'sample_query_options': None,
                                                     'sample_indices': None,
                                                     'site_mask': 'default',
                                                     'min_minor_ac': 2,
                                                     'max_missing_an': 0,
                                                     'random_seed': 42,
                                                     'inline_array': True,
                                                     'chunks': 'native'},
 'cell_9_call_1_ag3_biallelic_snp_calls_ld_pruned': {'region': '3L',
                                                     'n_snps': 100000,
                                                     'ld_window_size': 500,
                                                     'ld_window_step': 200,
                                                     'ld_threshold': 0.1,
                                                     'thin_offset': 0,
                                                     'sample_sets': 'AG1000G-BF-A',
                                                     'sample_query': None,
                                                     'sample_query_options': None,
                                                     'sample_indices': None,
                                                     'site_mask': 'default',
                                                     'min_minor_ac': 2,
                                                     'max_missing_an': 0,
                                                     'random_seed': 42,
                                                     'inline_array': True,
                                                     'chunks': 'native'},
 'cell_9_call_2_ag3_biallelic_snp_calls_ld_pruned': {'region': '3L',
                                                     'n_snps': 100000,
                                                     'ld_window_size': 500,
                                                     'ld_window_step': 200,
                                                     'ld_threshold': 0.5,
                                                     'thin_offset': 0,
                                                     'sample_sets': 'AG1000G-BF-A',
                                                     'sample_query': None,
                                                     'sample_query_options': None,
                                                     'sample_indices': None,
                                                     'site_mask': 'default',
                                                     'min_minor_ac': 2,
                                                     'max_missing_an': 0,
                                                     'random_seed': 42,
                                                     'inline_array': True,
                                                     'chunks': 'native'},
 'cell_11_call_1_ag3_biallelic_snp_calls': {'region': '3L',
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
                                            'random_seed': 42,
                                            'min_minor_ac': None,
                                            'max_missing_an': None,
                                            'n_snps': 100000,
                                            'thin_offset': 0}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/ld_pruning'

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
    # # LD-pruned biallelic SNP calls
    #
    # LD pruning removes redundant SNPs that are in linkage disequilibrium, reducing correlation between variants. This is important for analyses like PCA and ADMIXTURE where independent markers are assumed.
    #
    # `biallelic_snp_calls_ld_pruned()` wraps `biallelic_snp_calls()` and applies LD pruning via `scikit-allel`'s `locate_unlinked()`. The output retains the same dataset structure and is compatible with existing downstream methods.
    # ## Setup
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    import malariagen_data
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # ## Basic usage
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    ds_pruned = _call_api_with_parameters(ag3.biallelic_snp_calls_ld_pruned, 'cell_6_call_1_ag3_biallelic_snp_calls_ld_pruned', region="3L", n_snps=100_000, sample_sets="AG1000G-BF-A")
    nbrt.display(ds_pruned)
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    # Inspect dimensions.
    print(f"variants: {ds_pruned.sizes['variants']}")
    print(f"samples:  {ds_pruned.sizes['samples']}")
    nbrt.display(print(f"alleles:  {ds_pruned.sizes['alleles']}"))
    # ## Effect of LD parameters
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    # Stricter threshold (0.1, default) removes more correlated SNPs.
    ds_strict = _call_api_with_parameters(ag3.biallelic_snp_calls_ld_pruned, 'cell_9_call_1_ag3_biallelic_snp_calls_ld_pruned', region="3L", n_snps=100_000, sample_sets="AG1000G-BF-A", ld_threshold=0.1)

    # More lenient threshold retains more SNPs.
    ds_lenient = _call_api_with_parameters(ag3.biallelic_snp_calls_ld_pruned, 'cell_9_call_2_ag3_biallelic_snp_calls_ld_pruned', region="3L", n_snps=100_000, sample_sets="AG1000G-BF-A", ld_threshold=0.5)

    print(f"strict  (threshold=0.1): {ds_strict.sizes['variants']} variants")
    nbrt.display(print(f"lenient (threshold=0.5): {ds_lenient.sizes['variants']} variants"))
    # ## Before vs after pruning
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    # Get the thinned (but not LD-pruned) SNPs for comparison.
    ds_before = _call_api_with_parameters(ag3.biallelic_snp_calls, 'cell_11_call_1_ag3_biallelic_snp_calls', region="3L", n_snps=100_000, sample_sets="AG1000G-BF-A")

    print(f"before LD pruning: {ds_before.sizes['variants']} variants")
    print(f"after  LD pruning: {ds_pruned.sizes['variants']} variants")
    nbrt.display(print(f"removed:           {ds_before.sizes['variants'] - ds_pruned.sizes['variants']} variants"))
    # ## Downstream compatibility
    #
    # The pruned dataset retains the same structure as `biallelic_snp_calls()` output, so it can be passed directly into existing workflows like PCA.
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    # Verify the pruned dataset has all variables expected by downstream methods.
    assert "call_genotype" in ds_pruned
    assert "variant_allele" in ds_pruned
    assert "variant_contig" in ds_pruned.coords
    assert "variant_position" in ds_pruned.coords
    assert "sample_id" in ds_pruned.coords

    # Shape sanity check.
    n_variants = ds_pruned.sizes["variants"]
    n_samples = ds_pruned.sizes["samples"]
    assert ds_pruned["call_genotype"].shape == (n_variants, n_samples, 2)
    assert ds_pruned["variant_allele"].shape == (n_variants, 2)

    nbrt.display(print(f"Dataset is valid: {n_variants} variants × {n_samples} samples"))


if __name__ == "__main__":
    nbrt.main(
        notebook='ld_pruning.ipynb',
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
