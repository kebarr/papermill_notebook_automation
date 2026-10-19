#!/usr/bin/env python3
"""igv: the code from notebooks/igv.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/igv.py                      # the notebook's defaults
    python scripts/igv.py --config runs.csv    # one run per CSV row
    python scripts/igv.py --list-parameters    # what a CSV can set
    python scripts/igv.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/igv_performance.csv'
API_CALL_PARAMETERS = {'cell_3_call_1_ag3_igv': {'region': '2L:2,422,600-2,422,700', 'tracks': None, 'init': True},
 'cell_4_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                       'sample': 'AR0002-C',
                                       'visibility_window': 20000,
                                       'init': True,
                                       'snp_vcf_path': None},
 'cell_5_call_1_ag3_sample_metadata': {'sample_sets': '3.1',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_indices': None},
 'cell_6_call_1_ag3_sample_sets': {'release': '3.1'},
 'cell_7_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                       'sample': '__KEEP_CALLSITE_VALUE__',
                                       'visibility_window': 20000,
                                       'init': True,
                                       'snp_vcf_path': None},
 'cell_7_call_2_ag3_sample_metadata': {'sample_sets': '3.1',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_indices': None},
 'cell_8_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                       'sample': '__KEEP_CALLSITE_VALUE__',
                                       'visibility_window': 20000,
                                       'init': True,
                                       'snp_vcf_path': None},
 'cell_8_call_2_ag3_sample_metadata': {'sample_sets': '3.2',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_indices': None},
 'cell_9_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                       'sample': '__KEEP_CALLSITE_VALUE__',
                                       'visibility_window': 20000,
                                       'init': True,
                                       'snp_vcf_path': None},
 'cell_9_call_2_ag3_sample_metadata': {'sample_sets': '3.3',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_indices': None},
 'cell_10_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None},
 'cell_10_call_2_ag3_sample_metadata': {'sample_sets': '3.4',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_11_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None},
 'cell_11_call_2_ag3_sample_metadata': {'sample_sets': '3.5',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_12_call_1_ag3_view_alignments': {'region': '2L:2,422,600-2,422,700',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None},
 'cell_12_call_2_ag3_sample_metadata': {'sample_sets': '3.6',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_14_call_1_af1_igv': {'region': '2RL:2,441,878-2,468,205', 'tracks': None, 'init': True},
 'cell_15_call_1_af1_sample_sets': {'release': None},
 'cell_16_call_1_af1_view_alignments': {'region': '2RL:2,447,600-2,447,700',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None},
 'cell_16_call_2_af1_sample_metadata': {'sample_sets': '1229-VO-GH-DADZIE-VMF00095',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_17_call_1_af1_view_alignments': {'region': '2RL:2,447,600-2,447,700',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None},
 'cell_17_call_2_af1_sample_metadata': {'sample_sets': '1240-VO-MZ-KOEKEMOER-VMF00101',
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_19_call_1_af1_sample_metadata': {'sample_sets': None,
                                        'sample_query': None,
                                        'sample_query_options': None,
                                        'sample_indices': None},
 'cell_19_call_2_af1_snp_calls_to_vcf': {'output_path': '__KEEP_CALLSITE_VALUE__',
                                         'region': '__KEEP_CALLSITE_VALUE__',
                                         'sample_sets': '__KEEP_CALLSITE_VALUE__',
                                         'sample_query': '__KEEP_CALLSITE_VALUE__',
                                         'sample_query_options': None,
                                         'site_mask': None,
                                         'max_region_size': 1000000,
                                         'inline_array': True,
                                         'chunks': 'native',
                                         'overwrite': True,
                                         'fields': ('GT',)},
 'cell_19_call_3_af1_view_alignments': {'region': '__KEEP_CALLSITE_VALUE__',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None},
 'cell_20_call_1_af1_view_alignments': {'region': '__KEEP_CALLSITE_VALUE__',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/igv'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_3_call_1_ag3_igv': '01_ag3_igv',
 'cell_4_call_1_ag3_view_alignments': '02_ag3_view_alignments_AR0002-C',
 'cell_7_call_1_ag3_view_alignments': '03_ag3_view_alignments',
 'cell_8_call_1_ag3_view_alignments': '04_ag3_view_alignments',
 'cell_9_call_1_ag3_view_alignments': '05_ag3_view_alignments',
 'cell_10_call_1_ag3_view_alignments': '06_ag3_view_alignments',
 'cell_11_call_1_ag3_view_alignments': '07_ag3_view_alignments',
 'cell_12_call_1_ag3_view_alignments': '08_ag3_view_alignments',
 'cell_14_call_1_af1_igv': '09_af1_igv',
 'cell_16_call_1_af1_view_alignments': '10_af1_view_alignments',
 'cell_17_call_1_af1_view_alignments': '11_af1_view_alignments',
 'cell_19_call_3_af1_view_alignments': '12_af1_view_alignments',
 'cell_20_call_1_af1_view_alignments': '13_af1_view_alignments'}


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
    ag3 = malariagen_data.Ag3()
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.display(_call_api_with_parameters(ag3.igv, 'cell_3_call_1_ag3_igv', region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_4_call_1_ag3_view_alignments', sample="AR0002-C", region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.display(_call_api_with_parameters(ag3.sample_metadata, 'cell_5_call_1_ag3_sample_metadata', sample_sets="3.1").head())
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.sample_sets, 'cell_6_call_1_ag3_sample_sets', release="3.1"))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_7_call_1_ag3_view_alignments', sample=_call_api_with_parameters(ag3.sample_metadata, 'cell_7_call_2_ag3_sample_metadata', sample_sets="3.1").iloc[0]["sample_id"], region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_8_call_1_ag3_view_alignments', sample=_call_api_with_parameters(ag3.sample_metadata, 'cell_8_call_2_ag3_sample_metadata', sample_sets="3.2").iloc[0]["sample_id"], region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_9_call_1_ag3_view_alignments', sample=_call_api_with_parameters(ag3.sample_metadata, 'cell_9_call_2_ag3_sample_metadata', sample_sets="3.3").iloc[0]["sample_id"], region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_10_call_1_ag3_view_alignments', sample=_call_api_with_parameters(ag3.sample_metadata, 'cell_10_call_2_ag3_sample_metadata', sample_sets="3.4").iloc[0]["sample_id"], region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_11_call_1_ag3_view_alignments', sample=_call_api_with_parameters(ag3.sample_metadata, 'cell_11_call_2_ag3_sample_metadata', sample_sets="3.5").iloc[0]["sample_id"], region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.view_alignments, 'cell_12_call_1_ag3_view_alignments', sample=_call_api_with_parameters(ag3.sample_metadata, 'cell_12_call_2_ag3_sample_metadata', sample_sets="3.6").iloc[0]["sample_id"], region="2L:2,422,600-2,422,700"))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    af1 = malariagen_data.Af1(pre=True)
    nbrt.display(af1)
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(af1.igv, 'cell_14_call_1_af1_igv', region="2RL:2,441,878-2,468,205"))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(af1.sample_sets, 'cell_15_call_1_af1_sample_sets'))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(af1.view_alignments, 'cell_16_call_1_af1_view_alignments', sample=_call_api_with_parameters(af1.sample_metadata, 'cell_16_call_2_af1_sample_metadata', sample_sets="1229-VO-GH-DADZIE-VMF00095").iloc[0][
            "sample_id"
        ], region="2RL:2,447,600-2,447,700"))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(af1.view_alignments, 'cell_17_call_1_af1_view_alignments', sample=_call_api_with_parameters(af1.sample_metadata, 'cell_17_call_2_af1_sample_metadata', sample_sets="1240-VO-MZ-KOEKEMOER-VMF00101").iloc[0][
            "sample_id"
        ], region="2RL:2,447,600-2,447,700"))
    # ## Local VCF in IGV
    # This exports one sample over a region to a BGZF-compressed VCF under the notebook working directory, then loads it as the SNP track. No index is created, so IGV loads the whole file; keep the region small- 5000 base pairs, as shown in this demo, works on a modern (2026 Mac) but if you are experiencing crashes, reduce the number of base pairs in the region the VCF is created for. The file is passed to `view_alignments()` by its local path and embedded in the notebook, so it works in any notebook environment (Jupyter, VS Code, Colab). If no variants are present, the SNPs track will be empty, as homozygous calls are escluded for resource reasons.
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    from pathlib import Path


    sample_set = "1240-VO-MZ-KOEKEMOER-VMF00101"
    sample_id = str(
        _call_api_with_parameters(af1.sample_metadata, 'cell_19_call_1_af1_sample_metadata', sample_sets=sample_set).iloc[0]["sample_id"]
    )
    region = "2RL:2,440,000-2,445,000"

    local_vcf_path = Path("local_igv_vcfs") / f"{sample_id}.vcf.gz"
    local_vcf_path.parent.mkdir(parents=True, exist_ok=True)

    _call_api_with_parameters(af1.snp_calls_to_vcf, 'cell_19_call_2_af1_snp_calls_to_vcf', output_path=str(local_vcf_path), region=region, sample_sets=[sample_set], sample_query=f"sample_id == '{sample_id}'", overwrite=True)

    nbrt.display(_call_api_with_parameters(af1.view_alignments, 'cell_19_call_3_af1_view_alignments', sample=sample_id, region=region, snp_vcf_path=local_vcf_path))
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    nbrt.display(_call_api_with_parameters(af1.view_alignments, 'cell_20_call_1_af1_view_alignments', sample=sample_id, region=region))


if __name__ == "__main__":
    nbrt.main(
        notebook='igv.ipynb',
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
