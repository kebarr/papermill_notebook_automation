#!/usr/bin/env python3
"""Write an HTML page for reading the performance CSVs the notebooks write.

Each CSV row is one API call: call_key, method, parameters_json, runtime_sec
and peak_memory_mib. The page shows one table per CSV with the parameters
pretty-printed in a wide column, so the timings stay readable. Nothing in the
CSVs is changed.

In the page you can:
- filter rows by any text (call key, method or a parameter value);
- sort by any column (click its heading);
- show only the parameters that vary between calls to the same method.

Examples:
    python view_performance.py                       # every performance CSV under .
    python view_performance.py executed_runs console/executed_runs
    python view_performance.py notebooks/plot_pca_performance.csv -o pca.html
"""

import argparse
import csv
import html
import json
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

PARAMETERS_COLUMN = "parameters_json"
NUMERIC_COLUMNS = {"runtime_sec": "s", "peak_memory_mib": "MiB"}
SKIP_DIRS = {".ipynb_checkpoints", ".git", "__pycache__"}

# Large enough for every row's parameters, which can be long.
csv.field_size_limit(sys.maxsize)


# ---------------------------------------------------------------------------
# Reading the CSVs
# ---------------------------------------------------------------------------


def _is_performance_csv(path):
    try:
        with path.open(newline="", encoding="utf-8") as f:
            header = next(csv.reader(f), [])
    except (OSError, UnicodeDecodeError):
        return False
    return PARAMETERS_COLUMN in header


def _find_csvs(paths):
    found = []
    for path in paths:
        if path.is_dir():
            candidates = sorted(
                p for p in path.rglob("*.csv")
                if not SKIP_DIRS.intersection(p.parts)
            )
        elif path.is_file():
            candidates = [path]
        else:
            raise SystemExit(f"Not found: {path}")
        found.extend(p for p in candidates if _is_performance_csv(p))
    # Keep the order given, dropping duplicates from overlapping paths.
    return list(dict.fromkeys(p.resolve() for p in found))


def _load(path):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = [c for c in reader.fieldnames or [] if c != PARAMETERS_COLUMN]
        rows = []
        for row in reader:
            raw = row.get(PARAMETERS_COLUMN) or ""
            try:
                parameters = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                parameters = None  # shown as the raw text
            rows.append({"values": row, "raw": raw, "parameters": parameters})
    return columns, rows


def _varying_names(rows):
    """For each method, the parameter names whose values differ between its
    calls. Methods called once get None: there is nothing to compare."""
    by_method = {}
    for row in rows:
        if isinstance(row["parameters"], dict):
            by_method.setdefault(row["values"].get("method"), []).append(row["parameters"])
    varying = {}
    for method, calls in by_method.items():
        if len(calls) < 2:
            varying[method] = None
            continue
        names = set().union(*calls)
        varying[method] = {
            name
            for name in names
            if len({json.dumps(c.get(name, "<missing>"), sort_keys=True, default=str)
                    for c in calls}) > 1
        }
    return varying


def _number(text):
    try:
        return float(text)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------


def _pretty(value):
    return json.dumps(value, indent=2, ensure_ascii=False, default=str)


def _compact(value):
    return json.dumps(value, ensure_ascii=False, default=str, separators=(", ", ": "))


def _parameters_cell(row, varying):
    """The parameters as wrapping name/value pairs, plus pretty-printed JSON
    for the "Show as JSON" view."""
    parameters = row["parameters"]
    if not isinstance(parameters, dict):
        text = html.escape(row["raw"])
        return f'<td class="params"><pre class="raw">{text}</pre></td>'

    names = varying.get(row["values"].get("method"))
    if names is None:
        note = "only call to this method: all parameters shown"
        subset = parameters
    else:
        subset = {k: v for k, v in parameters.items() if k in names}
        note = (
            f"{len(parameters) - len(subset)} parameter(s) hidden: the same in "
            "every call to this method"
        )
    pairs = []
    for name, value in parameters.items():
        classes = ["kv"]
        if names is not None and name not in names:
            classes.append("same")
        if value is None:
            classes.append("null")
        pairs.append(
            f'<span class="{" ".join(classes)}"><span class="k">{html.escape(name)}</span> '
            f'<span class="v">{html.escape(_compact(value))}</span></span>'
        )
    return (
        '<td class="params">'
        f'<div class="grid">{"".join(pairs)}</div>'
        f'<pre class="full">{html.escape(_pretty(parameters))}</pre>'
        f'<pre class="varying">{html.escape(_pretty(subset))}</pre>'
        f'<div class="note">{html.escape(note)}</div>'
        "</td>"
    )


def _numeric_cell(text, maximum, unit):
    value = _number(text)
    if value is None:
        return f'<td class="num" data-sort="">{html.escape(text or "")}</td>'
    share = 100 * value / maximum if maximum else 0
    return (
        f'<td class="num" data-sort="{value}" style="--w:{share:.1f}%">'
        f"{html.escape(text)} <span class=\"unit\">{unit}</span></td>"
    )


def _section(index, path, label, columns, rows):
    varying = _varying_names(rows)
    maxima = {
        column: max((_number(r["values"].get(column)) or 0 for r in rows), default=0)
        for column in NUMERIC_COLUMNS
    }
    headings = ["#"] + columns + ["parameters"]
    head = "".join(
        f'<th data-type="{"num" if c in NUMERIC_COLUMNS or c == "#" else "text"}">'
        f"{html.escape(c)}</th>"
        for c in headings
    )
    body = []
    for number, row in enumerate(rows, start=1):
        cells = [f'<td class="num" data-sort="{number}">{number}</td>']
        for column in columns:
            text = row["values"].get(column) or ""
            if column in NUMERIC_COLUMNS:
                cells.append(_numeric_cell(text, maxima[column], NUMERIC_COLUMNS[column]))
            else:
                cells.append(f'<td class="text">{html.escape(text)}</td>')
        cells.append(_parameters_cell(row, varying))
        search = " ".join(
            [row["values"].get(c) or "" for c in columns] + [row["raw"]]
        ).lower()
        body.append(f'<tr data-search="{html.escape(search)}">{"".join(cells)}</tr>')
    return (
        f'<section id="csv-{index}">'
        f"<h2>{html.escape(label)}</h2>"
        f'<p class="path">{html.escape(str(path))}</p>'
        f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"
        "</section>"
    )


def _summary(rows):
    runtimes = [_number(r["values"].get("runtime_sec")) for r in rows]
    memories = [_number(r["values"].get("peak_memory_mib")) for r in rows]
    runtimes = [v for v in runtimes if v is not None]
    memories = [v for v in memories if v is not None]
    return (
        len(rows),
        f"{sum(runtimes):.1f} s" if runtimes else "",
        f"{max(memories):.0f} MiB" if memories else "",
    )


def _label(path, base):
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _summary_tables(summaries):
    """One summary table per folder (set of runs), laid side by side."""
    sets = {}
    for index, path, label, (count, runtime, memory) in summaries:
        folder = str(Path(label).parent)
        sets.setdefault(folder, []).append(
            (path.name, f'<tr><td><a href="#csv-{index}">{html.escape(path.name)}</a></td>'
                        f'<td class="num">{count}</td><td class="num">{runtime}</td>'
                        f'<td class="num">{memory}</td></tr>')
        )
    tables = []
    for folder, rows in sets.items():
        body = "".join(row for _, row in sorted(rows))
        tables.append(
            f'<div class="set"><h3>{html.escape(folder)}/</h3>'
            "<table><thead><tr><th>CSV</th><th>Calls</th><th>Total runtime</th>"
            f"<th>Peak memory</th></tr></thead><tbody>{body}</tbody></table></div>"
        )
    return "".join(tables)


def render(paths):
    base = Path.cwd().resolve()
    sections, summaries = [], []
    for index, path in enumerate(paths, start=1):
        columns, rows = _load(path)
        label = _label(path, base)
        summaries.append((index, path, label, _summary(rows)))
        sections.append(_section(index, path, label, columns, rows))
    generated = datetime.now().strftime("%Y-%m-%d %H:%M")
    return PAGE.format(
        generated=generated,
        files=len(paths),
        summaries=_summary_tables(summaries),
        sections="".join(sections),
    )


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Performance results</title>
<style>
:root {{
  --bg: #ffffff; --fg: #1d2330; --muted: #5d6576; --line: #dde1e8;
  --head: #f3f5f8; --code: #f7f8fa; --bar: rgba(52, 120, 220, 0.16);
  --accent: #2563c9;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #15181e; --fg: #e3e6ec; --muted: #9aa2b1; --line: #2c313b;
    --head: #1d2129; --code: #1a1e25; --bar: rgba(96, 160, 255, 0.22);
    --accent: #7fb0ff;
  }}
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; padding: 0 16px 48px; background: var(--bg); color: var(--fg);
  font: 14px/1.45 system-ui, -apple-system, "Segoe UI", sans-serif;
}}
header {{
  padding: 12px 0; border-bottom: 1px solid var(--line);
  display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: center;
}}
h1 {{ font-size: 18px; margin: 0; }}
h2 {{ font-size: 16px; margin: 32px 0 2px; }}
.meta, .path, .note, .unit {{ color: var(--muted); }}
.meta {{ font-size: 13px; }}
.path {{ font-size: 12px; margin: 0 0 8px; word-break: break-all; }}
input[type=search] {{
  font: inherit; padding: 5px 8px; min-width: 260px; color: var(--fg);
  background: var(--code); border: 1px solid var(--line); border-radius: 6px;
}}
label {{ cursor: pointer; user-select: none; }}
a {{ color: var(--accent); }}
table {{ border-collapse: collapse; width: 100%; }}
th, td {{ border: 1px solid var(--line); padding: 4px 8px; vertical-align: top; text-align: left; }}
th {{ background: var(--head); position: sticky; top: 0; z-index: 1; cursor: pointer; white-space: nowrap; }}
th[data-dir=asc]::after {{ content: " \\25B2"; }}
th[data-dir=desc]::after {{ content: " \\25BC"; }}
td.num {{
  text-align: right; white-space: nowrap; font-variant-numeric: tabular-nums;
  background: linear-gradient(to right, var(--bar) var(--w, 0%), transparent 0);
}}
td.text {{ white-space: nowrap; font-family: ui-monospace, Menlo, Consolas, monospace; font-size: 12.5px; }}
td.params {{ width: 100%; background: var(--code); }}
pre {{
  margin: 0; font: 12.5px/1.4 ui-monospace, Menlo, Consolas, monospace;
  white-space: pre-wrap; word-break: break-word;
}}
.grid {{
  display: flex; flex-wrap: wrap; gap: 2px 16px;
  font: 12.5px/1.5 ui-monospace, Menlo, Consolas, monospace;
}}
.kv .k {{ color: var(--muted); }}
.kv.null .v {{ color: var(--muted); }}
.note {{ font-size: 12px; margin-top: 2px; display: none; }}
pre.full, pre.varying {{ display: none; }}
body.only-varying .note {{ display: block; }}
body.only-varying .kv.same {{ display: none; }}
body.as-json .grid {{ display: none; }}
body.as-json:not(.only-varying) pre.full {{ display: block; }}
body.as-json.only-varying pre.varying {{ display: block; }}
tr.hidden {{ display: none; }}
.sets {{
  display: flex; gap: 24px; align-items: flex-start;
  overflow-x: auto; padding: 4px 0 12px; margin-top: 16px;
}}
.set {{ flex: none; }}
.set h3 {{ font-size: 14px; margin: 0 0 6px; }}
.set table {{ width: auto; }}
.set td, .set th {{ white-space: nowrap; }}
.set th {{ position: static; cursor: default; }}
</style>
</head>
<body>
<header>
  <h1>Performance results</h1>
  <span class="meta">{files} CSV file(s) &middot; generated {generated}</span>
  <input type="search" id="filter" placeholder="Filter rows (call key, method, parameter value)">
  <label><input type="checkbox" id="varying"> Varying parameters only</label>
  <label><input type="checkbox" id="json"> Show as JSON</label>
</header>
<div class="sets">{summaries}</div>
{sections}
<script>
document.getElementById("varying").addEventListener("change", function (e) {{
  document.body.classList.toggle("only-varying", e.target.checked);
}});
document.getElementById("json").addEventListener("change", function (e) {{
  document.body.classList.toggle("as-json", e.target.checked);
}});
document.getElementById("filter").addEventListener("input", function (e) {{
  var words = e.target.value.toLowerCase().split(/\\s+/).filter(Boolean);
  document.querySelectorAll("section tbody tr").forEach(function (row) {{
    var text = row.dataset.search;
    row.classList.toggle("hidden", !words.every(function (w) {{ return text.indexOf(w) !== -1; }}));
  }});
}});
document.querySelectorAll("section th").forEach(function (th) {{
  th.addEventListener("click", function () {{
    var table = th.closest("table"), body = table.tBodies[0];
    var index = Array.prototype.indexOf.call(th.parentNode.children, th);
    var dir = th.dataset.dir === "asc" ? "desc" : "asc";
    th.parentNode.querySelectorAll("th").forEach(function (h) {{ delete h.dataset.dir; }});
    th.dataset.dir = dir;
    var numeric = th.dataset.type === "num";
    var rows = Array.prototype.slice.call(body.rows);
    rows.sort(function (a, b) {{
      var x = a.cells[index], y = b.cells[index];
      var p = numeric ? parseFloat(x.dataset.sort) : x.textContent;
      var q = numeric ? parseFloat(y.dataset.sort) : y.textContent;
      if (numeric) {{ p = isNaN(p) ? -Infinity : p; q = isNaN(q) ? -Infinity : q; }}
      var order = numeric ? p - q : p.localeCompare(q);
      return dir === "asc" ? order : -order;
    }});
    rows.forEach(function (r) {{ body.appendChild(r); }});
  }});
}});
</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Write an HTML page for reading performance CSVs.",
        epilog="Folders are searched recursively for CSVs with a parameters_json column.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="CSV files or folders (default: the current folder).",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("performance_report.html"),
        help="HTML file to write (default: performance_report.html).",
    )
    parser.add_argument(
        "--open", action="store_true", help="Open the page in a browser afterwards."
    )
    args = parser.parse_args()

    paths = _find_csvs(args.paths)
    if not paths:
        raise SystemExit("No CSVs with a parameters_json column found.")
    args.output.write_text(render(paths), encoding="utf-8")
    print(f"Wrote {args.output} ({len(paths)} CSV file(s)).")
    if args.open:
        webbrowser.open(args.output.resolve().as_uri())


if __name__ == "__main__":
    main()
