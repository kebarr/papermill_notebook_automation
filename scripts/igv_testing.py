#!/usr/bin/env python3
"""igv_testing: the code from notebooks/igv_testing.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/igv_testing.py                      # the notebook's defaults
    python scripts/igv_testing.py --config runs.csv    # one run per CSV row
    python scripts/igv_testing.py --list-parameters    # what a CSV can set
    python scripts/igv_testing.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/igv_testing_performance.csv'
API_CALL_PARAMETERS = {'cell_4_call_1_af1_igv': {'region': '2RL:2,441,878-2,468,205', 'tracks': None, 'init': True},
 'cell_5_call_1_af1_view_alignments': {'region': '2RL:2,447,600-2,447,700',
                                       'sample': '__KEEP_CALLSITE_VALUE__',
                                       'visibility_window': 20000,
                                       'init': True,
                                       'snp_vcf_path': None},
 'cell_5_call_2_af1_sample_metadata': {'sample_sets': '1229-VO-GH-DADZIE-VMF00095',
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_indices': None},
 'cell_7_call_1_af1_sample_metadata': {'sample_sets': None,
                                       'sample_query': None,
                                       'sample_query_options': None,
                                       'sample_indices': None},
 'cell_7_call_2_af1_snp_calls_to_vcf': {'output_path': '__KEEP_CALLSITE_VALUE__',
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
 'cell_10_call_1_af1_view_alignments': {'region': '__KEEP_CALLSITE_VALUE__',
                                        'sample': '__KEEP_CALLSITE_VALUE__',
                                        'visibility_window': 20000,
                                        'init': True,
                                        'snp_vcf_path': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/igv_testing'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_4_call_1_af1_igv': '01_af1_igv',
 'cell_5_call_1_af1_view_alignments': '02_af1_view_alignments',
 'cell_10_call_1_af1_view_alignments': '03_af1_view_alignments'}


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
    pass  # %load_ext line_profiler: not needed in a script
    pass  # %load_ext memory_profiler: not needed in a script
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    af1 = malariagen_data.Af1()
    nbrt.display(af1)
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    nbrt.display(_call_api_with_parameters(af1.igv, 'cell_4_call_1_af1_igv', region="2RL:2,441,878-2,468,205"))
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.display(_call_api_with_parameters(af1.view_alignments, 'cell_5_call_1_af1_view_alignments', sample=_call_api_with_parameters(af1.sample_metadata, 'cell_5_call_2_af1_sample_metadata', sample_sets="1229-VO-GH-DADZIE-VMF00095").iloc[0][
            "sample_id"
        ], region="2RL:2,447,600-2,447,700"))
    # ## Local tabix-indexed VCF in IGV
    # This exports one sample to a BGZF VCF and `.tbi` under the notebook working directory, then loads it as the SNP track. Both files must be inside the Jupyter server startup directory tree. The `snp_vcf_url` below assumes the server was started from the workspace root; if it was started from `notebooks/`, use the alternate URL shown in the code cell.
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    from pathlib import Path

    #%%capture cap --no-stderr

    sample_set = "1240-VO-MZ-KOEKEMOER-VMF00101"
    sample_id = str(
        _call_api_with_parameters(af1.sample_metadata, 'cell_7_call_1_af1_sample_metadata', sample_sets=sample_set).iloc[0]["sample_id"]
    )
    region = "2RL:2,440,000-2,445,000"

    local_vcf_path = Path("local_igv_vcfs") / f"{sample_id}.vcf.gz"
    local_vcf_path.parent.mkdir(parents=True, exist_ok=True)
    regions = ["2RL:2,440,000-2,441,000", "2RL:2,440,000-2,442,000", "2RL:2,440,000-2,443,000", "2RL:2,440,000-2,444,000", 
                        "2RL:2,440,000-2,445,000", "2RL:2,440,000-2,446,000", "2RL:2,440,000-2,447,000", "2RL:2,440,000-2,448,000",
                        "2RL:2,440,000-2,449,000", "2RL:2,440,000-2,450,000"]
    def run_snp_calls():
        _call_api_with_parameters(af1.snp_calls_to_vcf, 'cell_7_call_2_af1_snp_calls_to_vcf', output_path=str(local_vcf_path), region=region, sample_sets=[sample_set], sample_query=f"sample_id == '{sample_id}'", overwrite=True)
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    #%%writefile snp_calls_to_vcf_5k_bp_time.txt
    for region in regions:
        print(f"Time for region {region}")
        nbrt.timeit(lambda: run_snp_calls())
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    #%%writefile snp_calls_to_vcf_5k_bp_mem.txt 
    for region in regions:
        print(f"Time for region {region}")
        nbrt.memit(lambda: run_snp_calls())
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    def view_alignments(region):
        _call_api_with_parameters(af1.view_alignments, 'cell_10_call_1_af1_view_alignments', sample=sample_id, region=region, snp_vcf_path=local_vcf_path)
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    for region in regions:
        nbrt.timeit(lambda: view_alignments(region))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    for region in regions:
        print(f"Memory usage for region {region}")
        nbrt.memit(lambda: view_alignments(region))


if __name__ == "__main__":
    nbrt.main(
        notebook='igv_testing.ipynb',
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
