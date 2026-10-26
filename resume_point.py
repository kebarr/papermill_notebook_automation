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

    fieldnames, config_rows, api_parameters = _read_config(args.config)
    _, results = vp._load(args.results)

    notebook = args.notebook
    if notebook is None:
        notebooks = vp._find_notebooks([d for d in vp.DEFAULT_NOTEBOOK_DIRS if d.is_dir()])
        notebook = vp._notebook_for(args.config, notebooks) or vp._notebook_for(args.results, notebooks)
    if notebook is None:
        raise SystemExit("Could not tell which notebook these are from; pass --notebook.")
    expected = vp._ExpectedCalls(notebook).counts
    known = {k: c for k, c in expected.items() if c is not None}

    keyed = []
    for row in results:
        key = row["values"].get("call_key")
        if key in known:
            used = row["parameters"] if isinstance(row["parameters"], dict) else {}
            keyed.append((key, used))

    # Split into runs, as the viewer does, keeping each call's arguments.
    runs, current = [], []
    anchors = sorted((k for k, c in known.items() if c == 1), key=vp._call_order)
    for key, used in keyed:
        if anchors and key == anchors[0] and current:
            runs.append(current)
            current = []
        current.append((key, used))
    if current:
        runs.append(current)
    judged = []
    for run in runs:
        verdict, info = vp._judge_run(collections.Counter(k for k, _ in run), known)
        judged.append((run, verdict, info))

    matches = _match_runs([(run, verdict == "complete") for run, verdict, _ in judged], api_parameters)

    status = {}
    for (run, verdict, info), row, number in zip(judged, matches, range(1, len(judged) + 1)):
        if row is None:
            print(f"Run {number}: matches no config row (different config or notebook?)")
            continue
        if verdict == "complete":
            text = "complete"
        elif verdict == "stopped":
            text = f"stopped at or before {info} (notebook cell {vp._call_order(info)[0]})"
        elif verdict == "gaps":
            text = f"{len(info)} call(s) missing"
        else:
            text = "row counts differ from the notebook"
        # A later complete run of the same row supersedes an earlier failure.
        if status.get(row, ("",))[0] != "complete":
            status[row] = (text, number)

    print(f"Notebook: {notebook}")
    print(f"Config:   {args.config} ({len(config_rows)} row(s))")
    print(f"Results:  {args.results} ({len(results)} row(s), {len(runs)} run(s))\n")
    for index in range(len(config_rows)):
        text, run = status.get(index, ("not started", None))
        source = f" (run {run})" if run else ""
        print(f"  config row {index + 1} (CSV line {index + 2}): {text}{source}")

    todo = [i for i in range(len(config_rows)) if status.get(i, ("",))[0] != "complete"]
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
