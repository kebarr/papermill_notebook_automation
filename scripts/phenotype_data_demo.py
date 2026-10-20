#!/usr/bin/env python3
"""phenotype_data_demo: the code from notebooks_fixed_parameters_cells/phenotype_data_demo.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/phenotype_data_demo.py                      # the notebook's defaults
    python scripts/phenotype_data_demo.py --config runs.csv    # one run per CSV row
    python scripts/phenotype_data_demo.py --list-parameters    # what a CSV can set
    python scripts/phenotype_data_demo.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/phenotype_data_demo_performance.csv'
API_CALL_PARAMETERS = {'cell_5_call_1_ag3_phenotype_sample_sets': {},
 'cell_8_call_1_ag3_phenotype_data': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                      'sample_query': 'insecticide == '
                                                      "'Deltamethrin'",
                                      'sample_query_options': None,
                                      'cohort_size': None,
                                      'min_cohort_size': None,
                                      'max_cohort_size': None},
 'cell_10_call_1_ag3_phenotype_data': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                       'sample_query': 'insecticide == '
                                                       "'Deltamethrin' and "
                                                       'dose >= 1.0',
                                       'sample_query_options': None,
                                       'cohort_size': None,
                                       'min_cohort_size': None,
                                       'max_cohort_size': None},
 'cell_12_call_1_ag3_phenotype_data': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                       'sample_query': 'insecticide == '
                                                       "'Deltamethrin'",
                                       'sample_query_options': None,
                                       'cohort_size': None,
                                       'min_cohort_size': 10,
                                       'max_cohort_size': None},
 'cell_13_call_1_ag3_phenotype_binary': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'insecticide': None,
                                         'dose': None,
                                         'phenotype': None,
                                         'sample_query': 'insecticide == '
                                                         "'Deltamethrin'",
                                         'sample_query_options': None,
                                         'cohort_size': None,
                                         'min_cohort_size': None,
                                         'max_cohort_size': None},
 'cell_13_call_2_ag3_phenotype_binary': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'insecticide': None,
                                         'dose': None,
                                         'phenotype': None,
                                         'sample_query': 'insecticide == '
                                                         "'Deltamethrin' and "
                                                         "phenotype == 'alive'",
                                         'sample_query_options': None,
                                         'cohort_size': None,
                                         'min_cohort_size': None,
                                         'max_cohort_size': None},
 'cell_13_call_3_ag3_phenotype_binary': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'insecticide': None,
                                         'dose': None,
                                         'phenotype': None,
                                         'sample_query': 'dose == 0.5',
                                         'sample_query_options': None,
                                         'cohort_size': None,
                                         'min_cohort_size': None,
                                         'max_cohort_size': None},
 'cell_15_call_1_ag3_phenotype_binary': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'insecticide': None,
                                         'dose': None,
                                         'phenotype': None,
                                         'sample_query': 'insecticide == '
                                                         "'Deltamethrin'",
                                         'sample_query_options': None,
                                         'cohort_size': None,
                                         'min_cohort_size': None,
                                         'max_cohort_size': None},
 'cell_15_call_2_ag3_phenotype_binary': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'insecticide': None,
                                         'dose': None,
                                         'phenotype': None,
                                         'sample_query': 'insecticide == '
                                                         "'Deltamethrin' and "
                                                         "phenotype == 'alive'",
                                         'sample_query_options': None,
                                         'cohort_size': None,
                                         'min_cohort_size': None,
                                         'max_cohort_size': None},
 'cell_15_call_3_ag3_phenotype_binary': {'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'insecticide': None,
                                         'dose': None,
                                         'phenotype': None,
                                         'sample_query': 'dose == 0.5',
                                         'sample_query_options': None,
                                         'cohort_size': None,
                                         'min_cohort_size': None,
                                         'max_cohort_size': None},
 'cell_17_call_1_ag3_phenotypes_with_snps': {'region': '__KEEP_CALLSITE_VALUE__',
                                             'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                             'sample_query': 'insecticide == '
                                                             "'Deltamethrin' "
                                                             'and phenotype == '
                                                             "'alive'",
                                             'sample_query_options': None,
                                             'cohort_size': None,
                                             'min_cohort_size': None,
                                             'max_cohort_size': None},
 'cell_19_call_1_ag3_phenotypes_with_haplotypes': {'region': '__KEEP_CALLSITE_VALUE__',
                                                   'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                                   'sample_query': 'insecticide '
                                                                   '== '
                                                                   "'Deltamethrin' "
                                                                   'and '
                                                                   'phenotype '
                                                                   "== 'dead'",
                                                   'sample_query_options': None,
                                                   'cohort_size': None,
                                                   'min_cohort_size': None,
                                                   'max_cohort_size': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/phenotype_data_demo'

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
    # # Demonstrating New Phenotype Data Access and Filtering
    #
    # This notebook showcases the updated functionalities for accessing and filtering insecticide resistance phenotype data, and merging it with genetic data (SNPs and Haplotypes), as per the recent refactoring.
    # ## 1. Setup and Imports
    #
    # First, we'll import the necessary libraries and instantiate the `Ag3` API client.
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    import pandas as pd
    import xarray as xr
    import warnings
    from malariagen_data import Ag3

    # Suppress warnings for cleaner output in the notebook
    warnings.simplefilter("ignore", UserWarning)

    # Instantiate the Ag3 API client
    # Use pre=True for development versions, or specify a release like release="v3.2"
    ag3 = Ag3(pre=True)

    print("MalariaGEN Ag3 API client initialized.")
    nbrt.display(print(ag3))
    # ## 2. Listing Available Phenotype Sample Sets
    # Let's see which sample sets have phenotype data available.
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    phenotype_sample_sets = _call_api_with_parameters(ag3.phenotype_sample_sets, 'cell_5_call_1_ag3_phenotype_sample_sets')
    print(f"Available phenotype sample sets: {phenotype_sample_sets}")

    # We'll pick one sample set for demonstration, preferably one known to have data
    # For this example, we'll use '1237-VO-BJ-DJOGBENOU-VMF00050'
    demo_sample_set = "1237-VO-BJ-DJOGBENOU-VMF00050"
    if demo_sample_set not in phenotype_sample_sets:
        print(
            f"Warning: '{demo_sample_set}' not found. Using the first available: {phenotype_sample_sets}"
        )
        demo_sample_set = phenotype_sample_sets

    nbrt.display(print(f"\nUsing sample set for demonstration: {demo_sample_set}"))
    # ## 3. Loading Phenotype Data with sample_query
    # The phenotype_data() method now exclusively returns a Pandas DataFrame containing phenotype and sample metadata. Filtering by attributes like insecticide, location, dose, etc., is done using the sample_query parameter, which accepts a Pandas-style query string.
    # ### Example 1: Filter by a specific insecticide
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    print(
        f"\n--- Loading phenotype data for '{demo_sample_set}' filtered by Deltamethrin ---"
    )
    df_deltamethrin = _call_api_with_parameters(ag3.phenotype_data, 'cell_8_call_1_ag3_phenotype_data', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin'")

    print(f"Shape of DataFrame: {df_deltamethrin.shape}")
    print("\nFirst 5 rows of the filtered DataFrame:")
    df_deltamethrin.head()
    print(
        f"\nUnique insecticides in filtered data: {df_deltamethrin['insecticide'].unique()}"
    )
    print("\nDataFrame Info:")
    nbrt.display(df_deltamethrin.info())
    # ### Example 2: Filter by multiple conditions (insecticide and dose)
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    print(f"\n--- Loading phenotype data filtered by Deltamethrin and dose >= 1.0 ---")
    df_filtered_multi = _call_api_with_parameters(ag3.phenotype_data, 'cell_10_call_1_ag3_phenotype_data', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin' and dose >= 1.0")

    print(f"Shape of DataFrame: {df_filtered_multi.shape}")
    print("\nFirst 5 rows of the multi-filtered DataFrame:")
    df_filtered_multi.head()

    print(f"\nUnique insecticides: {df_filtered_multi['insecticide'].unique()}")
    print(f"Unique doses: {df_filtered_multi['dose'].unique()}")
    print("\nDataFrame Info:")
    nbrt.display(df_filtered_multi.info())
    # ### Example 3: Applying cohort size filtering
    # Cohort filtering parameters (cohort_size, min_cohort_size, max_cohort_size) can be combined with sample_query.
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    print(f"\n--- Loading phenotype data with min_cohort_size=10 ---")
    df_cohort_filtered = _call_api_with_parameters(ag3.phenotype_data, 'cell_12_call_1_ag3_phenotype_data', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin'", min_cohort_size=10)

    print(f"Shape of DataFrame: {df_cohort_filtered.shape}")
    print("\nFirst 5 rows of the cohort-filtered DataFrame:")
    df_cohort_filtered.head()
    print("\nDataFrame Info:")
    nbrt.display(df_cohort_filtered.info())
    # Verify cohort sizes (optional, for internal testing)
    # if not df_cohort_filtered.empty:
    #     cohort_keys = ["insecticide", "dose", "location", "country", "sample_set"]
    #     available_keys = [col for col in cohort_keys if col in df_cohort_filtered.columns]
    #     if available_keys:
    #         cohort_sizes = df_cohort_filtered.groupby(available_keys).size()
    #         print("\nCohort sizes after filtering:")
    #         print(cohort_sizes)
    #         print(f"All cohorts meet min_cohort_size (>=10): {all(cohort_sizes >= 10)}")
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    print(f"\n--- Getting binary phenotype outcomes for '{demo_sample_set}' ---")

    # Example 1: Binary outcomes for all Deltamethrin samples
    binary_deltamethrin = _call_api_with_parameters(ag3.phenotype_binary, 'cell_13_call_1_ag3_phenotype_binary', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin'")

    print(f"Shape of binary series: {binary_deltamethrin.shape}")
    print("First 5 entries:")
    print(binary_deltamethrin.head())
    print(f"Unique values in series: {binary_deltamethrin.unique()}")


    # Example 2: Binary outcomes for samples that were 'alive' with Deltamethrin
    binary_alive_deltamethrin = _call_api_with_parameters(ag3.phenotype_binary, 'cell_13_call_2_ag3_phenotype_binary', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin' and phenotype == 'alive'")

    print(
        f"\nShape of binary series (alive Deltamethrin): {binary_alive_deltamethrin.shape}"
    )
    print("First 5 entries:")
    print(binary_alive_deltamethrin.head())
    print(f"Unique values in series: {binary_alive_deltamethrin.unique()}")

    # Example 3: Binary outcomes for samples with dose 0.5
    binary_dose_0_5 = _call_api_with_parameters(ag3.phenotype_binary, 'cell_13_call_3_ag3_phenotype_binary', sample_sets=[demo_sample_set], sample_query="dose == 0.5")

    print(f"\nShape of binary series (dose 0.5): {binary_dose_0_5.shape}")
    print("First 5 entries:")
    print(binary_dose_0_5.head())
    nbrt.display(print(f"Unique values in series: {binary_dose_0_5.unique()}"))
    # ## 4. Getting Binary Phenotype Outcomes with phenotype_binary
    #
    # The `phenotype_binary()` method provides a convenient way to get phenotype outcomes as a binary Pandas Series (1 for alive/resistant, 0 for dead/susceptible, NaN for unmapped). It also uses the `sample_query` for filtering.
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    print(f"\n--- Getting binary phenotype outcomes for '{demo_sample_set}' ---")

    # Example 1: Binary outcomes for all Deltamethrin samples
    binary_deltamethrin = _call_api_with_parameters(ag3.phenotype_binary, 'cell_15_call_1_ag3_phenotype_binary', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin'")

    print(f"Shape of binary series: {binary_deltamethrin.shape}")
    print("First 5 entries:")
    print(binary_deltamethrin.head())
    print(f"Unique values in series: {binary_deltamethrin.unique()}")


    # Example 2: Binary outcomes for samples that were 'alive' with Deltamethrin
    binary_alive_deltamethrin = _call_api_with_parameters(ag3.phenotype_binary, 'cell_15_call_2_ag3_phenotype_binary', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin' and phenotype == 'alive'")

    print(
        f"\nShape of binary series (alive Deltamethrin): {binary_alive_deltamethrin.shape}"
    )
    print("First 5 entries:")
    print(binary_alive_deltamethrin.head())
    print(f"Unique values in series: {binary_alive_deltamethrin.unique()}")

    # Example 3: Binary outcomes for samples with dose 0.5
    binary_dose_0_5 = _call_api_with_parameters(ag3.phenotype_binary, 'cell_15_call_3_ag3_phenotype_binary', sample_sets=[demo_sample_set], sample_query="dose == 0.5")

    print(f"\nShape of binary series (dose 0.5): {binary_dose_0_5.shape}")
    print("First 5 entries:")
    print(binary_dose_0_5.head())
    nbrt.display(print(f"Unique values in series: {binary_dose_0_5.unique()}"))
    # ## 5. Loading Phenotype Data Merged with SNP Calls
    # The phenotypes_with_snps() method returns an xarray.Dataset that combines phenotype data with SNP calls for a specified genomic region. The sample_query parameter is still used to filter the phenotype data before merging.
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    print(f"\n--- Loading phenotype data merged with SNP calls ---")

    # Choose a small region for faster loading
    demo_region_snps = "2L:2420000-2430000"

    ds_snps = _call_api_with_parameters(ag3.phenotypes_with_snps, 'cell_17_call_1_ag3_phenotypes_with_snps', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin' and phenotype == 'alive'", region=demo_region_snps)

    print(f"Dataset dimensions: {ds_snps.dims}")
    print("\nDataset structure (rich display):")
    ds_snps

    print("\nFirst 5 samples and their phenotype_binary values:")
    print(ds_snps["phenotype_binary"].head(5).values)
    print("\nFirst 5 samples and their insecticide values:")
    print(ds_snps["insecticide"].head(5).values)
    print("\nFirst 5 variant positions:")
    print(ds_snps["variant_position"].head(5).values)
    print("\nDataset Info:")
    nbrt.display(ds_snps.info())
    # ## 6. Loading Phenotype Data Merged with Haplotypes
    # Similarly, the phenotypes_with_haplotypes() method returns an xarray.Dataset combining phenotype data with haplotype calls for a given region.
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    print(f"\n--- Loading phenotype data merged with Haplotypes ---")

    # Choose a small region for faster loading
    demo_region_haps = "2L:2420000-2430000"

    ds_haps = _call_api_with_parameters(ag3.phenotypes_with_haplotypes, 'cell_19_call_1_ag3_phenotypes_with_haplotypes', sample_sets=[demo_sample_set], sample_query="insecticide == 'Deltamethrin' and phenotype == 'dead'", region=demo_region_haps)

    print(f"Dataset dimensions: {ds_haps.dims}")
    print("\nDataset structure (rich display):")
    ds_haps

    print("\nFirst 5 samples and their phenotype_binary values:")
    print(ds_haps["phenotype_binary"].head(5).values)
    print("\nFirst 5 samples and their insecticide values:")
    print(ds_haps["insecticide"].head(5).values)
    print("\nFirst 5 variant positions:")
    print(ds_haps["variant_position"].head(5).values)
    print("\nDataset Info:")
    nbrt.display(ds_haps.info())
    # ## Conclusion
    # This notebook demonstrates the streamlined approach to accessing and combining phenotype and genetic data. The use of sample_query provides flexible filtering, and the dedicated functions for SNPs and Haplotypes (and potentially CNVs in the future) ensure clarity and separation of concerns.


if __name__ == "__main__":
    nbrt.main(
        notebook='phenotype_data_demo.ipynb',
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
