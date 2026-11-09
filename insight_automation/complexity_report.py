#!/usr/bin/env python3
"""Write an HTML page showing how one varied argument affects run time and memory.

Each results CSV comes from one of the notebooks in this folder: the same API
call repeated with one argument changed (samples, window size, region length,
mask, ...). The CSV records the arguments each call actually used, so the
varied argument is worked out from the CSV itself.

For each CSV the page shows one figure, with run time and peak memory side by
side for each value, the settings that stayed fixed, and a table of the
numbers. If a CSV has several runs appended, the latest call for each value is
plotted and the tooltip lists the earlier ones.

Examples:
    python complexity_report.py                       # results/ next to this script
    python complexity_report.py path/to/results -o report.html --open
"""

import argparse
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

csv.field_size_limit(sys.maxsize)

SCRIPT_DIR = Path(__file__).resolve().parent

# Checked in this order: the first that varies is plotted, others are listed
# as changing alongside it.
PREFERRED = ["samples", "cohort_size", "window_size", "region", "n_snps", "analysis", "site_mask"]
# Fixed settings shown up front; the rest go in a collapsible list.
HEADLINE = [
    "contig", "region", "sample_sets", "sample_query", "cohort1_query", "cohort2_query",
    "samples", "cohort_size", "window_size", "n_snps", "analysis", "site_mask",
]
LABELS = {
    "samples": "samples per cohort",
    "region": "region length",
}


# ---------------------------------------------------------------------------
# Reading a results CSV
# ---------------------------------------------------------------------------


def _region_length(region):
    match = re.fullmatch(r"[^:]+:([\d,]+)-([\d,]+)", str(region))
    if not match:
        return None
    return int(match[2].replace(",", "")) - int(match[1].replace(",", ""))


def _fmt_bp(n):
    for size, unit in ((1_000_000, "Mbp"), (1_000, "kbp")):
        if n >= size:
            return f"{n / size:g} {unit}"
    return f"{n:,} bp"


def _load(path):
    calls = []
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                parameters = json.loads(row.get("parameters_json") or "{}")
            except json.JSONDecodeError:
                parameters = {}
            # min = max cohort size is how the notebooks fix the number of samples.
            low, high = parameters.get("min_cohort_size"), parameters.get("max_cohort_size")
            if low is not None and low == high:
                parameters["samples"] = parameters.pop("min_cohort_size")
                parameters.pop("max_cohort_size")
            calls.append(
                {
                    "key": row.get("call_key", ""),
                    "method": row.get("method", ""),
                    "parameters": parameters,
                    "time": float(row["runtime_sec"]),
                    "memory": float(row["peak_memory_mib"]),
                }
            )
    return calls


def _dump(value):
    return json.dumps(value, sort_keys=True)


def _varied(calls):
    """(the varied argument or None, other arguments that also changed)."""
    names = list(dict.fromkeys(n for c in calls for n in c["parameters"]))
    changing = [
        n for n in names
        if len({_dump(c["parameters"].get(n)) for c in calls}) > 1
    ]
    if not changing:
        return None, []
    primary = next((n for n in PREFERRED if n in changing), changing[0])
    return primary, [n for n in changing if n != primary]


def _value_label(name, value):
    if name == "region":
        length = _region_length(value)
        if length is not None:
            return _fmt_bp(length)
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{value:,}"
    return str(value)


def _short(value, limit=90):
    text = value if isinstance(value, str) else json.dumps(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


# ---------------------------------------------------------------------------
# Charts (inline SVG; hover tooltips added by the page script)
# ---------------------------------------------------------------------------


def _fmt_seconds(value):
    if value < 1:
        return f"{value:.2f} s"
    if value < 100:
        return f"{value:.1f} s"
    return f"{value:,.0f} s"


def _fmt_mib(value):
    return f"{value:,.0f} MiB"


def _nice_ticks(maximum, count=4):
    if not maximum or maximum <= 0:
        return [0, 1]
    raw = maximum / count
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
    top = step * math.ceil(maximum / step)
    return [round(i * step, 10) for i in range(int(round(top / step)) + 1)]


def _tick_label(value, unit):
    if unit == "MiB" and value >= 1000:
        return f"{value / 1000:g}K"
    return f"{value:g}"


def _wrap(text, width=14, max_lines=3):
    words, lines, current = text.split(" "), [], ""
    for word in words:
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = f"{current} {word}".strip()
    lines.append(current)
    return lines[:max_lines]


def _column_chart(title, unit, bars, axis_label):
    """bars: list of dicts with label, value and tip (list of (value, label))."""
    band = 84 if len(bars) <= 6 else 64
    left, right, top, bottom = 52, 16, 28, 64
    width = left + right + band * max(len(bars), 1)
    height = 250
    plot_h = height - top - bottom
    ticks = _nice_ticks(max(b["value"] for b in bars))
    y_max = ticks[-1] or 1
    baseline = top + plot_h
    fmt = _fmt_seconds if unit == "s" else _fmt_mib

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
    parts.append(f'<text class="tick" x="{left - 8}" y="{top - 12}" text-anchor="end">{unit}</text>')
    for i, bar in enumerate(bars):
        cx = left + band * i + band / 2
        x0, x1 = cx - 12, cx + 12
        yt = y(bar["value"])
        r = min(4, baseline - yt)
        parts.append(
            f'<path class="bar" d="M{x0:.1f},{baseline:.1f} L{x0:.1f},{yt + r:.1f} '
            f'Q{x0:.1f},{yt:.1f} {x0 + r:.1f},{yt:.1f} L{x1 - r:.1f},{yt:.1f} '
            f'Q{x1:.1f},{yt:.1f} {x1:.1f},{yt + r:.1f} L{x1:.1f},{baseline:.1f} Z"/>'
        )
        parts.append(
            f'<text class="cap" x="{cx:.1f}" y="{yt - 6:.1f}" text-anchor="middle">{html.escape(fmt(bar["value"]))}</text>'
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
    return f'<div class="panel"><h3>{html.escape(title)}</h3>{"".join(parts)}</div>'


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------


def _section(index, path):
    calls = _load(path)
    if not calls:
        raise ValueError("no calls recorded")
    primary, also = _varied(calls)
    method = calls[0]["method"]
    name = path.stem.replace("_performance", "")

    # One bar per value (latest call wins); with nothing varied, one per call.
    groups = collections.OrderedDict()
    for number, call in enumerate(calls, start=1):
        if primary is None:
            label = f"call {number}"
        else:
            label = _value_label(primary, call["parameters"].get(primary))
        groups.setdefault(label, []).append(call)

    bars_time, bars_memory, rows = [], [], []
    for label, group in groups.items():
        latest = group[-1]
        extra = [(_short(latest["parameters"].get(n)), n) for n in also]
        earlier = [
            (f"{_fmt_seconds(c['time'])}, {_fmt_mib(c['memory'])}", "earlier run")
            for c in group[:-1]
        ]
        bars_time.append(
            {"label": label, "value": latest["time"],
             "tip": [(_fmt_seconds(latest["time"]), label), *extra, *earlier]}
        )
        bars_memory.append(
            {"label": label, "value": latest["memory"],
             "tip": [(_fmt_mib(latest["memory"]), label), *extra, *earlier]}
        )
        rows.append(
            f"<tr><td>{html.escape(label)}</td>"
            + "".join(f"<td>{html.escape(_short(latest['parameters'].get(n), 60))}</td>" for n in also)
            + f'<td class="num">{_fmt_seconds(latest["time"])}</td>'
            f'<td class="num">{_fmt_mib(latest["memory"])}</td>'
            f'<td class="num">{len(group)}</td></tr>'
        )

    axis = LABELS.get(primary, primary) if primary else "call (in order)"
    charts = (
        _column_chart("Run time", "s", bars_time, axis)
        + _column_chart("Peak memory", "MiB", bars_memory, axis)
    )

    fixed = {
        n: v for n, v in calls[0]["parameters"].items()
        if n != primary and n not in also and v is not None
        and all(_dump(c["parameters"].get(n)) == _dump(v) for c in calls)
    }
    headline = [n for n in HEADLINE if n in fixed]
    rest = [n for n in fixed if n not in headline]

    def setting(n):
        value = _value_label(n, fixed[n]) if n == "region" else _short(fixed[n])
        if n == "region":
            value = f"{fixed[n]} ({value})"
        return f"<li><code>{html.escape(n)}</code> = {html.escape(str(value))}</li>"

    if primary is None:
        varied = (
            '<p class="warn">⚠ Every call used the same arguments, so nothing varied. If the '
            "notebook changes an argument between cells, check that the parameters cell sets it "
            "to <code>API_KEEP_CALLSITE_VALUE</code>; any other value there replaces the "
            "value in the call.</p>"
        )
    else:
        varied = f"<p>Varied <code>{html.escape(primary)}</code>"
        if primary in LABELS:
            varied += f" ({html.escape(LABELS[primary])})"
        varied += f": {html.escape(', '.join(groups))}.</p>"
        if also:
            varied += (
                '<p class="note">Also changes between values: '
                + ", ".join(f"<code>{html.escape(n)}</code>" for n in also)
                + " (see the table).</p>"
            )
    repeats = sum(len(g) - 1 for g in groups.values())
    if repeats:
        varied += (
            f'<p class="note">{repeats} value(s) were run more than once; the latest run is '
            "plotted, and the tooltip lists earlier ones.</p>"
        )

    head = (
        "<th>" + html.escape(LABELS.get(primary, primary) if primary else "call") + "</th>"
        + "".join(f"<th>{html.escape(n)}</th>" for n in also)
        + "<th>Run time</th><th>Peak memory</th><th>Runs</th>"
    )
    section = f"""
<section id="csv-{index}">
  <h2>{html.escape(name)}</h2>
  <p class="meta"><code>{html.escape(method)}</code> · {html.escape(str(path))}</p>
  {varied}
  <figure class="chart-card"><div class="charts">{charts}</div></figure>
  <div class="settings">
    <div><h3>Fixed for every value</h3><ul>{"".join(setting(n) for n in headline) or "<li>none</li>"}</ul></div>
  </div>
  {"<details><summary>Other fixed arguments (" + str(len(rest)) + ")</summary><ul>" + "".join(setting(n) for n in rest) + "</ul></details>" if rest else ""}
  <details><summary>Table view</summary>
    <div class="scroll"><table><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>
  </details>
</section>"""
    summary = {
        "index": index,
        "name": name,
        "method": method,
        "varied": LABELS.get(primary, primary) if primary else "nothing",
        "values": len(groups),
    }
    return summary, section


def render(paths):
    summaries, sections = [], []
    for index, path in enumerate(paths, start=1):
        try:
            summary, section = _section(index, path)
        except (ValueError, KeyError, OSError) as exc:
            print(f"Skipping {path.name}: {exc}")
            continue
        summaries.append(summary)
        sections.append(section)
    contents = "".join(
        f'<tr><td><a href="#csv-{s["index"]}">{html.escape(s["name"])}</a></td>'
        f'<td><code>{html.escape(s["method"])}</code></td><td>{html.escape(s["varied"])}</td>'
        f'<td class="num">{s["values"]}</td></tr>'
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
<title>Complexity results</title>
<style>
:root {{
  color-scheme: light;
  --surface: #fcfcfb; --raised: #f3f2ef; --text: #0b0b0b; --text-2: #52514e; --muted: #75746f;
  --grid: #e4e3df; --axis: #c3c2b7; --series-1: #2a78d6; --accent: #2a78d6; --warn: #8a5a00;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    color-scheme: dark;
    --surface: #1a1a19; --raised: #232321; --text: #f0efec; --text-2: #c3c2b7; --muted: #9a998f;
    --grid: #2e2e2c; --axis: #4a4a46; --series-1: #3987e5; --accent: #6da7ec; --warn: #e0b45c;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --surface: #1a1a19; --raised: #232321; --text: #f0efec; --text-2: #c3c2b7; --muted: #9a998f;
  --grid: #2e2e2c; --axis: #4a4a46; --series-1: #3987e5; --accent: #6da7ec; --warn: #e0b45c;
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
code {{ font: 12.5px ui-monospace, Menlo, Consolas, monospace; }}
p {{ margin: 6px 0; }}
.meta, .note, .lede {{ color: var(--text-2); font-size: 13px; }}
.meta {{ overflow-wrap: anywhere; }}
.scroll {{ max-width: 100%; overflow-x: auto; }}
.lede {{ max-width: 900px; }}
.warn {{ color: var(--warn); }}
.settings {{ margin: 10px 0; font-size: 13px; }}
.settings ul, details ul {{ margin: 0; padding-left: 18px; font-size: 13px; }}
.chart-card {{ margin: 12px 0; padding: 12px; background: var(--raised); border-radius: 8px; max-width: 100%; overflow-x: auto; }}
.charts {{ display: flex; flex-wrap: wrap; gap: 24px; }}
svg.chart {{ display: block; max-width: 100%; height: auto; }}
svg .grid {{ stroke: var(--grid); stroke-width: 1; }}
svg .axis {{ stroke: var(--axis); stroke-width: 1; }}
svg .tick, svg .xaxis {{ fill: var(--muted); font-size: 11px; font-variant-numeric: tabular-nums; }}
svg .xlabel {{ fill: var(--text-2); font-size: 11.5px; }}
svg .cap {{ fill: var(--text-2); font-size: 11px; font-variant-numeric: tabular-nums; }}
svg .bar {{ fill: var(--series-1); }}
svg .hit {{ fill: transparent; outline: none; }}
svg .hit:hover, svg .hit:focus-visible {{ fill: color-mix(in srgb, var(--text) 5%, transparent); }}
table {{ border-collapse: collapse; margin: 8px 0; }}
th, td {{ border: 1px solid var(--grid); padding: 4px 8px; text-align: left; vertical-align: top; }}
th {{ background: var(--raised); font-weight: 600; font-size: 13px; }}
td.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }}
details {{ margin: 8px 0; }}
summary {{ cursor: pointer; color: var(--text-2); }}
#tooltip {{
  position: fixed; pointer-events: none; display: none; z-index: 10; min-width: 160px; max-width: 420px;
  background: var(--surface); color: var(--text); border: 1px solid var(--axis); border-radius: 6px;
  padding: 6px 10px; font-size: 12.5px; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.15);
}}
#tooltip .value {{ font-weight: 600; }}
#tooltip .label {{ color: var(--text-2); }}
</style>
</head>
<body>
<header>
  <h1>Complexity results</h1>
  <p class="meta">{count} results CSV(s) · generated {generated}</p>
  <p class="lede">Each figure shows one notebook: the same call repeated with one argument changed.
  Run time is the call's wall-clock time. Peak memory is the highest memory the whole Python
  process used during the call, so it includes what earlier cells had already loaded; compare
  values within a notebook rather than across notebooks. Calls faster than about half a second are
  repeated by memory_profiler, so their times are inflated.</p>
</header>
<div class="scroll"><table>
  <thead><tr><th>Results</th><th>Method</th><th>Varied</th><th>Values</th></tr></thead>
  <tbody>{contents}</tbody>
</table></div>
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
        description="Make an HTML page with one figure per results CSV, showing how the varied "
        "argument affects run time and peak memory."
    )
    parser.add_argument(
        "results", nargs="?", type=Path, default=SCRIPT_DIR / "results",
        help="Folder of results CSVs, or CSV files (default: results/ next to this script).",
    )
    parser.add_argument("more", nargs="*", type=Path, help=argparse.SUPPRESS)
    parser.add_argument(
        "-o", "--output", type=Path,
        help="HTML file to write (default: complexity_report.html next to the results).",
    )
    parser.add_argument("--open", action="store_true", help="Open the page in a browser.")
    args = parser.parse_args()

    inputs = [args.results, *args.more]
    paths = []
    for item in inputs:
        paths += sorted(item.glob("*.csv")) if item.is_dir() else [item]
    if not paths:
        raise SystemExit(f"No CSVs found in {', '.join(map(str, inputs))}")
    output = args.output or (
        (args.results if args.results.is_dir() else args.results.parent).parent / "complexity_report.html"
    )
    page, count = render(paths)
    output.write_text(page, encoding="utf-8")
    print(f"Wrote {output} ({count} figure(s)).")
    if args.open:
        webbrowser.open(output.resolve().as_uri())


if __name__ == "__main__":
    main()
