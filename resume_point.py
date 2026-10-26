#!/usr/bin/env python3
"""Work out which rows of a config CSV a results CSV covers, and where to resume.

The results CSV (PERFORMANCE_CSV_PATH / --output-csv) has one row per API call
but no record of which config row produced it. This matches them up: the
results are split into runs (each time the notebook's first call reappears),
and each run is matched to the config row whose API_CALL_PARAMETERS agree with
the arguments the run's calls actually used. Each config row is then reported
as complete, stopped part way, or not started.

With --remaining, the config rows still to do are written to a new CSV, which
can be passed to the same runner or script as --config.

Examples:
    python resume_point.py --config runners_and_csvs_new/plot_pca_n_snps.csv \\
        --results executed_runs_sweeps/plot_pca_n_snps.csv
    python resume_point.py --config runners_and_csvs_new/plot_pca_n_snps.csv \\
        --results executed_runs_sweeps/plot_pca_n_snps.csv \\
        --remaining runners_and_csvs_new/plot_pca_n_snps_remaining.csv
"""

import argparse
import collections
import csv
import json
import sys
from pathlib import Path

import view_performance as vp

KEEP = "__KEEP_CALLSITE_VALUE__"
MISSING = object()

csv.field_size_limit(sys.maxsize)


def _normalise(value):
    """Compare values as the results CSV stores them (JSON; tuples as lists)."""
    return json.loads(json.dumps(value, sort_keys=True, default=str))


def _read_config(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        rows = list(reader)
    api_parameters = []
    for row in rows:
        text = (row.get("API_CALL_PARAMETERS") or "").strip()
        api_parameters.append(json.loads(text) if text else {})
    return fieldnames, rows, api_parameters


def _consistent(run_rows, call_parameters):
    """Whether every call in the run used this config row's values."""
    for key, used in run_rows:
        configured = call_parameters.get(key)
        if not configured:
            continue
        for name, value in configured.items():
            if isinstance(value, str) and value == KEEP:
                continue
            actual = used.get(name, MISSING)
            if actual is not MISSING and _normalise(value) != _normalise(actual):
                return False
    return True


def _match_runs(runs, api_parameters):
    """Config row index for each run, assuming rows are run in order and a
    fresh invocation of the runner starts again from the first row."""
    matches, next_row = [], 0
    for run, complete in runs:
        candidates = [
            index for index, parameters in enumerate(api_parameters)
            if _consistent(run, parameters)
        ]
        if not candidates:
            matches.append(None)
            continue
        row = next_row if next_row in candidates else min(candidates)
        matches.append(row)
        next_row = row + 1 if complete else row
    return matches


def find_notebook(config_path, results_path, api_parameters):
    """The notebook a sweep came from: the one whose call keys match the
    config's, falling back to matching file names."""
    notebooks = vp._find_notebooks([d for d in vp.DEFAULT_NOTEBOOK_DIRS if d.is_dir()])
    config_keys = set().union(*(set(p) for p in api_parameters)) if api_parameters else set()
    if config_keys:
        index = vp._key_index(notebooks)
        owners = [index.get(key, set()) for key in config_keys]
        common = set.intersection(*owners) if owners else set()
        if common:
            return notebooks[sorted(common)[0]]
    return vp._notebook_for(config_path, notebooks) or vp._notebook_for(results_path, notebooks)


def match_results(config_path, results_path, notebook=None):
    """Split a results CSV into runs and match each run to a config row.

    Returns the notebook, config rows and API_CALL_PARAMETERS per row, the
    expected call counts, and the runs: each a dict with "rows" (the results
    rows, as loaded by view_performance), "verdict" and "info" (as from
    view_performance._judge_run) and "config_row" (an index, or None).
    """
    fieldnames, config_rows, api_parameters = _read_config(config_path)
    _, results = vp._load(results_path)
    if notebook is None:
        notebook = find_notebook(config_path, results_path, api_parameters)
    if notebook is None:
        raise ValueError(
            f"Could not tell which notebook {config_path} is for; pass the notebook."
        )
    expected = vp._ExpectedCalls(notebook).counts
    known = {k: c for k, c in expected.items() if c is not None}

    anchors = sorted((k for k, c in known.items() if c == 1), key=vp._call_order)
    runs, current = [], []
    for row in results:
        key = row["values"].get("call_key")
        if key not in known:
            continue
        if anchors and key == anchors[0] and current:
            runs.append(current)
            current = []
        current.append(row)
    if current:
        runs.append(current)

    judged = []
    for rows in runs:
        verdict, info = vp._judge_run(
            collections.Counter(r["values"].get("call_key") for r in rows), known
        )
        used = [
            (r["values"].get("call_key"), r["parameters"] if isinstance(r["parameters"], dict) else {})
            for r in rows
        ]
        judged.append({"rows": rows, "used": used, "verdict": verdict, "info": info})
    matches = _match_runs(
        [(run["used"], run["verdict"] == "complete") for run in judged], api_parameters
    )
    for run, row in zip(judged, matches):
        run["config_row"] = row
    return {
        "notebook": notebook,
        "fieldnames": fieldnames,
        "config_rows": config_rows,
        "api_parameters": api_parameters,
        "expected": expected,
        "results": results,
        "runs": judged,
    }


def describe(run):
    verdict, info = run["verdict"], run["info"]
    if verdict == "complete":
        return "complete"
    if verdict == "stopped":
        return f"stopped at or before {info} (notebook cell {vp._call_order(info)[0]})"
    if verdict == "gaps":
        return f"{len(info)} call(s) missing"
    return "row counts differ from the notebook"


def row_status(runs, n_rows):
    """Per config row: (description, run number, run), preferring a complete
    run over an earlier failure."""
    status = {}
    for number, run in enumerate(runs, start=1):
        row = run["config_row"]
        if row is None:
            continue
        if status.get(row, ("",))[0] != "complete":
            status[row] = (describe(run), number, run)
    return [status.get(i, ("not started", None, None)) for i in range(n_rows)]


def main():
    parser = argparse.ArgumentParser(
        description="Report which config rows a results CSV covers, and where to resume."
    )
    parser.add_argument("--config", type=Path, required=True, help="The CSV passed as --config.")
    parser.add_argument("--results", type=Path, required=True, help="The results CSV the runs wrote.")
    parser.add_argument(
        "--notebook",
        type=Path,
        help="The notebook (default: matched by file name in "
        + ", ".join(str(d.relative_to(vp.SCRIPT_DIR)) for d in vp.DEFAULT_NOTEBOOK_DIRS)
        + ").",
    )
    parser.add_argument(
        "--remaining",
        type=Path,
        help="Write the config rows still to do to this CSV, to use as --config.",
    )
    args = parser.parse_args()

    try:
        analysis = match_results(args.config, args.results, args.notebook)
    except ValueError as exc:
        raise SystemExit(str(exc))
    notebook = analysis["notebook"]
    config_rows = analysis["config_rows"]
    fieldnames = analysis["fieldnames"]
    results = analysis["results"]
    runs = analysis["runs"]
    for number, run in enumerate(runs, start=1):
        if run["config_row"] is None:
            print(f"Run {number}: matches no config row (different config or notebook?)")
    statuses = row_status(runs, len(config_rows))

    print(f"Notebook: {notebook}")
    print(f"Config:   {args.config} ({len(config_rows)} row(s))")
    print(f"Results:  {args.results} ({len(results)} row(s), {len(runs)} run(s))\n")
    for index, (text, run, _) in enumerate(statuses):
        source = f" (run {run})" if run else ""
        print(f"  config row {index + 1} (CSV line {index + 2}): {text}{source}")

    todo = [i for i, (text, _, _) in enumerate(statuses) if text != "complete"]
    if not todo:
        print("\nAll config rows are complete.")
        return
    first = todo[0]
    print(
        f"\nResume from config row {first + 1} (CSV line {first + 2}); "
        f"{len(todo)} row(s) still to do: {', '.join(str(i + 1) for i in todo)}."
    )
    if args.remaining:
        with args.remaining.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator="\n")
            writer.writeheader()
            for index in todo:
                writer.writerow(config_rows[index])
        print(f"Wrote the remaining rows to {args.remaining}")


if __name__ == "__main__":
    main()
