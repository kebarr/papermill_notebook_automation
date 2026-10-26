#!/usr/bin/env python3
"""Write an HTML page showing how swept parameters affect run time and memory.

A sweep is a config CSV made by `papermill_csv_config.py create ... --sweep`
(one row per value) plus the results CSV its runs wrote (--output-csv /
PERFORMANCE_CSV_PATH). For each sweep the page shows:
- which parameter varied (worked out from the config) and the settings fixed
  alongside it;
- run time and peak memory for each value, as two column charts, counting
  only the calls the sweep changed;
- a table with those numbers and the whole-run totals, and each row's status
  (complete, stopped part way, not run);
- a per-call breakdown, to see which calls grow with the parameter.

Runs are matched to config rows as in resume_point.py, so results CSVs with
several runs appended, failed runs and reruns are handled.

Examples:
    python sweep_report.py --configs runners_and_csvs_new --results executed_runs_sweeps
    python sweep_report.py --sweep runners_and_csvs_new/plot_pca_n_snps.csv \\
        executed_runs_sweeps/plot_pca_n_snps.csv -o pca_sweep.html --open
"""

import argparse
import ast
import collections
import csv
import html
import json
import math
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

import resume_point as rp
import view_performance as vp

KEEP = "__KEEP_CALLSITE_VALUE__"
MISSING = "<missing>"

csv.field_size_limit(sys.maxsize)


# ---------------------------------------------------------------------------
# Working out what each sweep varied
# ---------------------------------------------------------------------------


def _short(value):
    """A compact label for a parameter value."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        if len(value) > 4:
            return f"{len(value)} values ({_short(value[0])}…{_short(value[-1])})"
        return "[" + ", ".join(_short(v) for v in value) + "]"
    if isinstance(value, int):
        return f"{value:,}"
    if isinstance(value, str):
        match = re.fullmatch(r"(\w+):([\d,]+)-([\d,]+)", value)
        if match:
            start, end = (int(x.replace(",", "")) for x in match.groups()[1:])
            return f"{match[1]}:{start / 1e6:g}–{end / 1e6:g} Mbp"
        return value
    return str(value)


def _factors(api_parameters):
    """The parameters whose values differ between config rows, grouped so a
    parameter swept across several calls with the same values is one factor."""
    keys = sorted(set().union(*(set(p) for p in api_parameters)), key=vp._call_order)
    groups = collections.OrderedDict()
    for key in keys:
        names = list(dict.fromkeys(n for p in api_parameters for n in p.get(key, {})))
        for name in names:
            values = tuple(
                json.dumps(p.get(key, {}).get(name, MISSING), sort_keys=True)
                for p in api_parameters
            )
            if len(set(values)) > 1:
                groups.setdefault((name, values), []).append(key)
    names = collections.Counter(name for name, _ in groups)
    factors = []
    for (name, values), call_keys in groups.items():
        label = name if names[name] == 1 else f"{name} ({_method(call_keys[0])})"
        factors.append(
            {"name": name, "label": label, "keys": call_keys, "values": [json.loads(v) for v in values]}
        )
    return factors


def _method(key):
    return key.split("_call_", 1)[-1].split("_", 1)[-1]


def _notebook_defaults(notebook):
    cells = json.loads(Path(notebook).read_text(encoding="utf-8"))["cells"]
    for cell in cells:
        if "parameters" in cell.get("metadata", {}).get("tags", []):
            source = "".join(cell["source"])
            if "API_CALL_PARAMETERS = " in source:
                return ast.literal_eval(source.split("API_CALL_PARAMETERS = ", 1)[1].strip())
    return {}


def _fixed_settings(api_parameters, defaults):
    """Settings the same in every config row but different from the notebook,
    e.g. a --set used alongside the sweep."""
    if not api_parameters:
        return []
    fixed = collections.OrderedDict()
    first = api_parameters[0]
    for key in sorted(first, key=vp._call_order):
        for name, value in first[key].items():
            if any(p.get(key, {}).get(name, MISSING) != value for p in api_parameters[1:]):
                continue
            default = defaults.get(key, {}).get(name, MISSING)
            if rp._normalise(default) == rp._normalise(value):
                continue
            fixed.setdefault((name, json.dumps(value, sort_keys=True)), []).append(key)
    return [
        (name, json.loads(value), keys) for (name, value), keys in fixed.items()
    ]


# ---------------------------------------------------------------------------
# Numbers per config row
# ---------------------------------------------------------------------------


def _metrics(run, swept_keys):
    per_call = collections.OrderedDict()
    totals = {"runtime": 0.0, "peak": None, "swept_runtime": 0.0, "swept_peak": None, "calls": 0}
    for row in run["rows"]:
        key = row["values"].get("call_key")
        runtime = vp._number(row["values"].get("runtime_sec")) or 0.0
        memory = vp._number(row["values"].get("peak_memory_mib"))
        totals["calls"] += 1
        totals["runtime"] += runtime
        if memory is not None:
            totals["peak"] = memory if totals["peak"] is None else max(totals["peak"], memory)
        if key in swept_keys:
            totals["swept_runtime"] += runtime
            if memory is not None:
                totals["swept_peak"] = (
                    memory if totals["swept_peak"] is None else max(totals["swept_peak"], memory)
                )
            call = per_call.setdefault(key, {"runtime": 0.0, "peak": None})
            call["runtime"] += runtime
            if memory is not None:
                call["peak"] = memory if call["peak"] is None else max(call["peak"], memory)
    totals["per_call"] = per_call
    return totals


def _fmt_seconds(value):
    if value is None:
        return "–"
    if value < 1:
        return f"{value:.2f} s"
    if value < 100:
        return f"{value:.1f} s"
    return f"{value:,.0f} s"


def _fmt_mib(value):
    return "–" if value is None else f"{value:,.0f} MiB"


# ---------------------------------------------------------------------------
# Charts (inline SVG; hover tooltips added by the page script)
# ---------------------------------------------------------------------------


def _nice_ticks(maximum, count=4):
    if not maximum or maximum <= 0:
        return [0, 1]
    raw = maximum / count
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
    top = step * math.ceil(maximum / step)
    return [round(i * step, 10) for i in range(int(round(top / step)) + 1)]


def _tick_label(value, unit):
    if unit == "s":
        return f"{value:g}"
    return f"{value / 1000:g}K" if value >= 1000 else f"{value:g}"


def _wrap(text, width=14):
    words, lines, current = text.split(" "), [], ""
    for word in words:
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    lines.append(current)
    return lines[:3]


def _column_chart(title, unit, bars, axis_label):
    """bars: list of dicts with label, value (or None), status, tip (list of
    (label, value) pairs)."""
    n = max(len(bars), 1)
    band = 96
    left, right, top, bottom = 52, 16, 28, 64
    width = left + right + band * n
    height = 250
    plot_h = height - top - bottom
    values = [b["value"] for b in bars if b["value"] is not None]
    ticks = _nice_ticks(max(values) if values else 0)
    y_max = ticks[-1] or 1
    baseline = top + plot_h

    def y(v):
        return baseline - (v / y_max) * plot_h

    parts = [
        f'<svg class="chart" viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'role="img" aria-label="{html.escape(title)}">'
    ]
    for tick in ticks:
        ty = y(tick)
        parts.append(f'<line class="grid" x1="{left}" x2="{width - right}" y1="{ty:.1f}" y2="{ty:.1f}"/>')
        parts.append(
            f'<text class="tick" x="{left - 8}" y="{ty + 4:.1f}" text-anchor="end">{_tick_label(tick, unit)}</text>'
        )
    parts.append(
        f'<text class="tick" x="{left - 8}" y="{top - 12}" text-anchor="end">{html.escape(unit)}</text>'
    )
    label_values = len(bars) <= 8
    for i, bar in enumerate(bars):
        cx = left + band * i + band / 2
        bar_w = 24
        x0, x1 = cx - bar_w / 2, cx + bar_w / 2
        value, status = bar["value"], bar["status"]
        if value is not None:
            yt = y(value)
            r = min(4, baseline - yt)
            cls = "bar" if status == "complete" else "bar incomplete"
            parts.append(
                f'<path class="{cls}" d="M{x0:.1f},{baseline:.1f} L{x0:.1f},{yt + r:.1f} '
                f'Q{x0:.1f},{yt:.1f} {x0 + r:.1f},{yt:.1f} L{x1 - r:.1f},{yt:.1f} '
                f'Q{x1:.1f},{yt:.1f} {x1:.1f},{yt + r:.1f} L{x1:.1f},{baseline:.1f} Z"/>'
            )
            if label_values:
                text = _fmt_seconds(value) if unit == "s" else _fmt_mib(value)
                parts.append(
                    f'<text class="cap" x="{cx:.1f}" y="{yt - 6:.1f}" text-anchor="middle">{html.escape(text)}</text>'
                )
            if status != "complete":
                parts.append(
                    f'<text class="flag" x="{cx:.1f}" y="{yt - (20 if label_values else 6):.1f}" '
                    f'text-anchor="middle">⚠ stopped</text>'
                )
        else:
            parts.append(
                f'<text class="flag" x="{cx:.1f}" y="{baseline - 6:.1f}" text-anchor="middle">not run</text>'
            )
        for line_number, line in enumerate(_wrap(bar["label"])):
            parts.append(
                f'<text class="xlabel" x="{cx:.1f}" y="{baseline + 18 + 14 * line_number:.1f}" '
                f'text-anchor="middle">{html.escape(line)}</text>'
            )
        tip = html.escape(json.dumps(bar["tip"]))
        parts.append(
            f'<rect class="hit" x="{cx - band / 2:.1f}" y="{top}" width="{band}" height="{plot_h}" '
            f'tabindex="0" data-tip="{tip}" aria-label="{html.escape(bar["label"])}"/>'
        )
    parts.append(f'<line class="axis" x1="{left}" x2="{width - right}" y1="{baseline}" y2="{baseline}"/>')
    parts.append(
        f'<text class="xaxis" x="{left + (width - left - right) / 2:.1f}" y="{height - 6}" '
        f'text-anchor="middle">{html.escape(axis_label)}</text>'
    )
    parts.append("</svg>")
    return (
        f'<figure class="chart-card"><figcaption>{html.escape(title)}</figcaption>'
        f'{"".join(parts)}</figure>'
    )


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------


def _heat_table(caption, keys, columns, cell, fmt):
    values = [cell(k, c) for k in keys for c in columns]
    values = [v for v in values if v is not None]
    top = max(values) if values else 0
    head = "".join(f"<th>{html.escape(c['label'])}</th>" for c in columns)
    body = []
    for key in keys:
        cells = []
        for column in columns:
            value = cell(key, column)
            if value is None:
                cells.append('<td class="num">–</td>')
                continue
            share = value / top if top else 0
            cells.append(
                f'<td class="num heat" style="--heat:{8 + 72 * share:.0f}%">{html.escape(fmt(value))}</td>'
            )
        body.append(f'<tr><td class="key">{html.escape(key)}</td>{"".join(cells)}</tr>')
    return (
        f'<table class="heat-table"><caption>{html.escape(caption)}</caption>'
        f"<thead><tr><th>Call</th>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"
    )


def _sweep_section(index, config_path, results_path, base):
    analysis = rp.match_results(config_path, results_path)
    api_parameters = analysis["api_parameters"]
    notebook = analysis["notebook"]
    factors = _factors(api_parameters)
    swept_keys = set().union(*(set(f["keys"]) for f in factors)) if factors else set()
    statuses = rp.row_status(analysis["runs"], len(api_parameters))
    fixed = _fixed_settings(api_parameters, _notebook_defaults(notebook))
    unmatched = sum(1 for run in analysis["runs"] if run["config_row"] is None)

    def value_label(factor, value):
        # For cohort sizes, null means no limit: every sample is used.
        if value is None and "cohort_size" in factor["name"]:
            return "all (null)"
        return _short(value)

    if len(factors) == 1:
        factor_title = factors[0]["label"]
        row_labels = [value_label(factors[0], v) for v in factors[0]["values"]]
    elif factors:
        factor_title = " × ".join(f["label"] for f in factors)
        row_labels = [
            " · ".join(f"{f['label']}={value_label(f, f['values'][i])}" for f in factors)
            for i in range(len(api_parameters))
        ]
    else:
        factor_title = "(no varied parameter found)"
        row_labels = [f"row {i + 1}" for i in range(len(api_parameters))]

    rows = []
    for i, (text, run_number, run) in enumerate(statuses):
        metrics = _metrics(run, swept_keys) if run else None
        status = "complete" if text == "complete" else ("not run" if run is None else "incomplete")
        rows.append({"label": row_labels[i], "text": text, "status": status, "metrics": metrics, "run": run_number})

    def bars(field, unit_fmt):
        out = []
        for row in rows:
            m = row["metrics"]
            value = m[field] if m else None
            tip = [[unit_fmt(value) if value is not None else "not run", factor_title + " = " + row["label"]]]
            tip.append([row["text"], "status"])
            if m:
                tip.append([str(m["calls"]), "calls recorded"])
            out.append({"label": row["label"], "value": value, "status": row["status"], "tip": tip})
        return out

    n_calls = len(swept_keys)
    scope = f"the {n_calls} call{'s' if n_calls != 1 else ''} the sweep changed"
    charts = (
        _column_chart(f"Run time of {scope}", "s", bars("swept_runtime", _fmt_seconds), factor_title)
        + _column_chart(f"Peak memory during {scope}", "MiB", bars("swept_peak", _fmt_mib), factor_title)
    )

    table_rows = []
    for i, row in enumerate(rows):
        m = row["metrics"] or {}
        flag = "" if row["status"] == "complete" else "⚠ "
        table_rows.append(
            "<tr>"
            f'<td class="num">{i + 1}</td><td>{html.escape(row["label"])}</td>'
            f'<td>{flag}{html.escape(row["text"])}</td>'
            f'<td class="num">{_fmt_seconds(m.get("swept_runtime")) if m else "–"}</td>'
            f'<td class="num">{_fmt_mib(m.get("swept_peak")) if m else "–"}</td>'
            f'<td class="num">{_fmt_seconds(m.get("runtime")) if m else "–"}</td>'
            f'<td class="num">{_fmt_mib(m.get("peak")) if m else "–"}</td>'
            f'<td class="num">{m.get("calls", "–") if m else "–"}</td>'
            "</tr>"
        )
    table = (
        '<table class="data"><thead><tr><th>Config row</th>'
        f"<th>{html.escape(factor_title)}</th><th>Status</th>"
        "<th>Swept calls: time</th><th>Swept calls: peak memory</th>"
        "<th>Whole run: time</th><th>Whole run: peak memory</th><th>Calls recorded</th>"
        f"</tr></thead><tbody>{''.join(table_rows)}</tbody></table>"
    )

    columns = [r for r in rows if r["metrics"]]
    keys = sorted(swept_keys, key=vp._call_order)
    breakdown = ""
    if columns and keys:
        breakdown = (
            "<details><summary>Per-call breakdown</summary>"
            + _heat_table(
                "Run time per call", keys, columns,
                lambda k, c: c["metrics"]["per_call"].get(k, {}).get("runtime"), _fmt_seconds,
            )
            + _heat_table(
                "Peak memory per call", keys, columns,
                lambda k, c: c["metrics"]["per_call"].get(k, {}).get("peak"), _fmt_mib,
            )
            + "</details>"
        )

    varied = "".join(
        f"<li><strong>{html.escape(f['label'])}</strong> on {len(f['keys'])} call(s): "
        f"{html.escape(', '.join(f['keys'][:4]))}{' …' if len(f['keys']) > 4 else ''}</li>"
        for f in factors
    )
    fixed_html = "".join(
        f"<li>{html.escape(name)} = {html.escape(_short(value))} on {len(keys_)} call(s)</li>"
        for name, value, keys_ in fixed
    ) or "<li>none (notebook defaults)</li>"
    notes = []
    if unmatched:
        notes.append(f"{unmatched} run(s) in the results matched no config row and are left out.")
    note_html = "".join(f'<p class="note">⚠ {html.escape(n)}</p>' for n in notes)
    complete = sum(1 for r in rows if r["status"] == "complete")

    summary = {
        "index": index,
        "notebook": Path(notebook).stem,
        "factor": factor_title,
        "values": len(rows),
        "complete": complete,
        "name": config_path.stem,
    }
    section = (
        f'<section id="sweep-{index}">'
        f"<h2>{html.escape(Path(notebook).stem)} — {html.escape(factor_title)}</h2>"
        f'<p class="meta">Config {html.escape(vp._label(config_path.resolve(), base))} · '
        f"results {html.escape(vp._label(results_path.resolve(), base))} · "
        f"{complete} of {len(rows)} value(s) complete</p>"
        f"{note_html}"
        f'<div class="settings"><div><h3>Varied</h3><ul>{varied}</ul></div>'
        f"<div><h3>Fixed for every value</h3><ul>{fixed_html}</ul></div></div>"
        f'<div class="charts">{charts}</div>'
        f"{table}{breakdown}</section>"
    )
    return summary, section


def _discover(configs_dir, results_dir):
    """Pair each multi-row config with the results CSV named after it."""
    results = [p for p in results_dir.rglob("*.csv") if not vp.SKIP_DIRS.intersection(p.parts)]
    pairs = []
    for config in sorted(configs_dir.glob("*.csv")):
        try:
            _, rows, _ = rp._read_config(config)
        except (json.JSONDecodeError, KeyError, UnicodeDecodeError):
            continue
        if len(rows) < 2:
            continue
        matches = sorted(
            (p for p in results if p.stem == config.stem or p.stem.startswith(config.stem + "_")),
            key=lambda p: (p.stem != config.stem, str(p)),
        )
        if matches:
            pairs.append((config, matches[0]))
        else:
            print(f"Note: no results found for sweep {config.name}")
    return pairs


def render(pairs):
    base = Path.cwd().resolve()
    summaries, sections = [], []
    for index, (config, results) in enumerate(pairs, start=1):
        try:
            summary, section = _sweep_section(index, config, results, base)
        except (ValueError, OSError) as exc:
            print(f"Skipping {config.name}: {exc}")
            continue
        summaries.append(summary)
        sections.append(section)
    contents = "".join(
        f'<tr><td><a href="#sweep-{s["index"]}">{html.escape(s["name"])}</a></td>'
        f'<td>{html.escape(s["notebook"])}</td><td>{html.escape(s["factor"])}</td>'
        f'<td class="num">{s["complete"]} / {s["values"]}</td></tr>'
        for s in summaries
    )
    return PAGE.format(
        generated=datetime.now().strftime("%Y-%m-%d %H:%M"),
        count=len(summaries),
        contents=contents,
        sections="".join(sections),
    ), len(summaries)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sweep results</title>
<style>
:root {{
  color-scheme: light;
  --surface: #fcfcfb; --raised: #f3f2ef; --text: #0b0b0b; --text-2: #52514e; --muted: #75746f;
  --grid: #e4e3df; --axis: #c3c2b7; --series-1: #2a78d6; --mark-muted: #b5b4ad; --accent: #2a78d6;
}}
@media (prefers-color-scheme: dark) {{
  :root:where(:not([data-theme="light"])) {{
    color-scheme: dark;
    --surface: #1a1a19; --raised: #232321; --text: #f0efec; --text-2: #c3c2b7; --muted: #9a998f;
    --grid: #2e2e2c; --axis: #4a4a46; --series-1: #3987e5; --mark-muted: #5c5b56; --accent: #6da7ec;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --surface: #1a1a19; --raised: #232321; --text: #f0efec; --text-2: #c3c2b7; --muted: #9a998f;
  --grid: #2e2e2c; --axis: #4a4a46; --series-1: #3987e5; --mark-muted: #5c5b56; --accent: #6da7ec;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0 auto; max-width: 1400px; padding: 0 16px 48px; background: var(--surface); color: var(--text);
  font: 14px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif;
}}
header {{ padding: 16px 0 8px; border-bottom: 1px solid var(--grid); }}
h1 {{ font-size: 20px; margin: 0 0 4px; }}
h2 {{ font-size: 17px; margin: 40px 0 2px; }}
h3 {{ font-size: 13px; margin: 0 0 4px; color: var(--text-2); font-weight: 600; }}
a {{ color: var(--accent); }}
.meta, .note, .lede {{ color: var(--text-2); font-size: 13px; }}
.lede {{ max-width: 900px; }}
.note {{ margin: 4px 0; }}
.settings {{ display: flex; flex-wrap: wrap; gap: 8px 40px; margin: 10px 0; font-size: 13px; }}
.settings ul {{ margin: 0; padding-left: 18px; }}
.charts {{ display: flex; flex-wrap: wrap; gap: 16px; margin: 12px 0; }}
.chart-card {{ margin: 0; padding: 12px 12px 4px; background: var(--raised); border-radius: 8px; max-width: 100%; overflow-x: auto; }}
.chart-card figcaption {{ font-weight: 600; font-size: 13px; margin-bottom: 4px; }}
svg.chart {{ display: block; }}
svg .grid {{ stroke: var(--grid); stroke-width: 1; }}
svg .axis {{ stroke: var(--axis); stroke-width: 1; }}
svg .tick, svg .xaxis {{ fill: var(--muted); font-size: 11px; font-variant-numeric: tabular-nums; }}
svg .xlabel {{ fill: var(--text-2); font-size: 11.5px; }}
svg .cap {{ fill: var(--text-2); font-size: 11px; font-variant-numeric: tabular-nums; }}
svg .flag {{ fill: var(--muted); font-size: 11px; }}
svg .bar {{ fill: var(--series-1); }}
svg .bar.incomplete {{ fill: var(--mark-muted); }}
svg .hit {{ fill: transparent; cursor: default; outline: none; }}
svg .hit:hover, svg .hit:focus-visible {{ fill: color-mix(in srgb, var(--text) 5%, transparent); }}
table {{ border-collapse: collapse; margin: 8px 0; }}
th, td {{ border: 1px solid var(--grid); padding: 4px 8px; text-align: left; vertical-align: top; }}
th {{ background: var(--raised); font-weight: 600; font-size: 13px; }}
td.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
td.key {{ font: 12.5px ui-monospace, Menlo, Consolas, monospace; white-space: nowrap; }}
td.heat {{ background: color-mix(in srgb, var(--series-1) var(--heat), transparent); }}
caption {{ text-align: left; font-weight: 600; font-size: 13px; padding: 8px 0 4px; }}
details {{ margin: 8px 0; }}
summary {{ cursor: pointer; color: var(--text-2); }}
#tooltip {{
  position: fixed; pointer-events: none; display: none; z-index: 10; min-width: 160px;
  background: var(--surface); color: var(--text); border: 1px solid var(--axis); border-radius: 6px;
  padding: 6px 10px; font-size: 12.5px; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
}}
#tooltip .value {{ font-weight: 600; }}
#tooltip .label {{ color: var(--text-2); }}
</style>
</head>
<body>
<header>
  <h1>Sweep results</h1>
  <p class="meta">{count} sweep(s) · generated {generated}</p>
  <p class="lede">Each chart counts only the calls the sweep changed, so the effect of the parameter
  isn't diluted by the rest of the notebook; whole-run totals are in each table. Times are the sum
  of the recorded call times; peak memory is the highest per-call peak, and includes the memory the
  process was already using. Calls faster than about half a second are timed over two or three
  repeats by memory_profiler, so their times are inflated. Grey bars marked "stopped" come from runs
  that didn't finish.</p>
</header>
<table>
  <thead><tr><th>Sweep</th><th>Notebook</th><th>Varied</th><th>Values complete</th></tr></thead>
  <tbody>{contents}</tbody>
</table>
{sections}
<div id="tooltip" role="status"></div>
<script>
(function () {{
  var tooltip = document.getElementById("tooltip");
  function show(target, x, y) {{
    var rows = JSON.parse(target.getAttribute("data-tip") || "[]");
    tooltip.textContent = "";
    rows.forEach(function (row, i) {{
      var line = document.createElement("div");
      var value = document.createElement("span");
      value.className = i === 0 ? "value" : "";
      value.textContent = row[0];
      var label = document.createElement("span");
      label.className = "label";
      label.textContent = "  " + row[1];
      line.appendChild(value);
      line.appendChild(label);
      tooltip.appendChild(line);
    }});
    tooltip.style.display = "block";
    var box = tooltip.getBoundingClientRect();
    tooltip.style.left = Math.min(x + 14, window.innerWidth - box.width - 8) + "px";
    tooltip.style.top = Math.max(8, y - box.height - 10) + "px";
  }}
  document.querySelectorAll("svg .hit").forEach(function (hit) {{
    hit.addEventListener("pointermove", function (e) {{ show(hit, e.clientX, e.clientY); }});
    hit.addEventListener("pointerleave", function () {{ tooltip.style.display = "none"; }});
    hit.addEventListener("focus", function () {{
      var r = hit.getBoundingClientRect(); show(hit, r.left + r.width / 2, r.top + 20);
    }});
    hit.addEventListener("blur", function () {{ tooltip.style.display = "none"; }});
  }});
}})();
</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Write an HTML page showing how swept parameters affect run time and memory."
    )
    parser.add_argument(
        "--sweep",
        nargs=2,
        action="append",
        default=[],
        type=Path,
        metavar=("CONFIG", "RESULTS"),
        help="A sweep's config CSV and the results CSV its runs wrote; may be repeated.",
    )
    parser.add_argument("--configs", type=Path, help="Folder of sweep config CSVs (multi-row).")
    parser.add_argument(
        "--results",
        type=Path,
        help="Folder searched for each config's results CSV, named <config name>.csv "
        "or <config name>_*.csv.",
    )
    parser.add_argument("-o", "--output", type=Path, default=Path("sweep_report.html"))
    parser.add_argument("--open", action="store_true", help="Open the page in a browser afterwards.")
    args = parser.parse_args()

    pairs = [tuple(pair) for pair in args.sweep]
    if args.configs or args.results:
        if not (args.configs and args.results):
            parser.error("--configs and --results go together.")
        pairs += _discover(args.configs, args.results)
    if not pairs:
        parser.error("Give --sweep CONFIG RESULTS, or --configs DIR --results DIR.")

    page, count = render(pairs)
    args.output.write_text(page, encoding="utf-8")
    print(f"Wrote {args.output} ({count} sweep(s)).")
    if args.open:
        webbrowser.open(args.output.resolve().as_uri())


if __name__ == "__main__":
    main()
