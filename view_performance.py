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

Each CSV is also checked against its notebook (matched by file name): the
number of rows a complete run should write is worked out from the notebook's
code and compared with the rows in the CSV, so incomplete or repeated runs
stand out.

Examples:
    python view_performance.py                       # every performance CSV under .
    python view_performance.py executed_runs console/executed_runs
    python view_performance.py notebooks/plot_pca_performance.csv -o pca.html
    python view_performance.py results --notebooks notebooks_fixed_parameters_cells
"""

import argparse
import ast
import collections
import csv
import html
import json
import re
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

PARAMETERS_COLUMN = "parameters_json"
NUMERIC_COLUMNS = {"runtime_sec": "s", "peak_memory_mib": "MiB"}
SKIP_DIRS = {".ipynb_checkpoints", ".git", "__pycache__"}
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_NOTEBOOK_DIRS = [SCRIPT_DIR / "notebooks_fixed_parameters_cells", SCRIPT_DIR / "notebooks"]
API_HELPER = "_call_api_with_parameters"
# Magics that run their statement an unpredictable number of times.
VARIABLE_MAGICS = {"timeit", "memit"}

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
# Expected calls, from the notebooks
# ---------------------------------------------------------------------------


def _mask_cell(source):
    """The cell with its magics masked (same layout, so line numbers match),
    the line numbers run by %timeit/%memit, and whether the whole cell is."""
    lines = source.split("\n")
    variable_lines, whole_cell = set(), False
    for number, line in enumerate(lines, start=1):
        match = re.match(r"^(\s*)(%%|%|!)(\w*)(\s*)(.*)$", line)
        if not match:
            continue
        indent, prefix, word, gap, argument = match.groups()
        if prefix == "%" and argument:
            lines[number - 1] = indent + "_=" + " " * (len(word) - 1 + len(gap)) + argument
            if word in VARIABLE_MAGICS:
                variable_lines.add(number)
        else:
            lines[number - 1] = indent + "#" + line[len(indent) + 1:]
            if prefix == "%%" and word in VARIABLE_MAGICS:
                whole_cell = True
    return "\n".join(lines), variable_lines, whole_cell


def _call_order(key):
    match = re.match(r"cell_(\d+)_call_(\d+)_", key)
    return (int(match[1]), int(match[2])) if match else (10**9, 0)


class _ExpectedCalls:
    """How many rows each call key should write in one complete run.

    A count is None when it can't be known from the code: calls under
    %timeit/%memit, in lambdas, in while loops or if blocks, or in loops over
    something whose length isn't a literal.
    """

    def __init__(self, notebook_path):
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        self.counts = {}
        self.functions = {}
        self.literals = {}
        self.variable_statements = set()
        self.unparsed_keys = set()
        trees = []
        for cell in notebook["cells"]:
            if cell["cell_type"] != "code":
                continue
            source = "".join(cell["source"])
            masked, variable_lines, whole_cell = _mask_cell(source)
            try:
                tree = ast.parse(masked)
            except SyntaxError:
                self.unparsed_keys.update(re.findall(rf"{API_HELPER}\([^,]+,\s*'([^']+)'", source))
                continue
            trees.append(tree)
            for node in ast.walk(tree):
                if isinstance(node, ast.stmt) and (whole_cell or node.lineno in variable_lines):
                    self.variable_statements.add(id(node))
        self._collect_definitions(trees)
        for tree in trees:
            for statement in tree.body:
                self._visit(statement, 1, ())
        # Calls never reached, e.g. in a function nothing calls, write no rows.
        for tree in trees:
            for node in ast.walk(tree):
                key = self._api_key(node)
                if key is not None:
                    self.counts.setdefault(key, 0)
        for key in self.unparsed_keys:
            self.counts[key] = None

    def _collect_definitions(self, trees):
        assignments = collections.defaultdict(list)
        for tree in trees:
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    self.functions[node.name] = node
                elif (
                    isinstance(node, ast.Assign)
                    and len(node.targets) == 1
                    and isinstance(node.targets[0], ast.Name)
                ):
                    try:
                        assignments[node.targets[0].id].append(ast.literal_eval(node.value))
                    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
                        assignments[node.targets[0].id].append(object())  # not a literal
        for name, values in assignments.items():
            if all(v == values[0] for v in values):
                self.literals[name] = values[0]

    @staticmethod
    def _api_key(node):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == API_HELPER
            and len(node.args) >= 2
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)
        ):
            return node.args[1].value
        return None

    def _length(self, node):
        """How many items a loop over node yields, or None."""
        try:
            value = ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
            value = None
            if isinstance(node, ast.Name) and node.id in self.literals:
                value = self.literals[node.id]
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id == "range":
                    try:
                        return len(range(*(ast.literal_eval(a) for a in node.args)))
                    except (ValueError, TypeError, SyntaxError):
                        return None
                if node.func.id in ("enumerate", "list", "tuple", "sorted", "reversed") and node.args:
                    return self._length(node.args[0])
                if node.func.id == "zip" and node.args:
                    lengths = [self._length(a) for a in node.args]
                    return None if None in lengths else min(lengths)
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr in ("items", "keys", "values")
            ):
                return self._length(node.func.value)
        try:
            return len(value) if value is not None else None
        except TypeError:
            return None

    @staticmethod
    def _times(a, b):
        return None if a is None or b is None else a * b

    def _add(self, key, count):
        current = self.counts.get(key, 0)
        self.counts[key] = None if current is None or count is None else current + count

    def _visit_all(self, nodes, count, stack):
        for node in nodes:
            self._visit(node, count, stack)

    def _visit(self, node, count, stack):
        if isinstance(node, ast.stmt) and id(node) in self.variable_statements:
            count = None
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return  # its body runs when the function is called
        if isinstance(node, ast.Lambda):
            self._visit(node.body, None, stack)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            self._visit(node.iter, count, stack)
            self._visit_all(node.body, self._times(count, self._length(node.iter)), stack)
            self._visit_all(node.orelse, count, stack)
        elif isinstance(node, ast.While):
            self._visit(node.test, None, stack)
            self._visit_all(node.body + node.orelse, None, stack)
        elif isinstance(node, (ast.If, ast.IfExp)):
            self._visit(node.test, count, stack)
            body = node.body if isinstance(node.body, list) else [node.body]
            orelse = node.orelse if isinstance(node.orelse, list) else [node.orelse]
            self._visit_all(body + orelse, None, stack)
        elif isinstance(node, ast.Try) or type(node).__name__ == "TryStar":
            self._visit_all(node.body + node.orelse + node.finalbody, count, stack)
            for handler in node.handlers:
                self._visit_all(handler.body, None, stack)
        elif isinstance(node, (ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp)):
            inner = count
            for generator in node.generators:
                self._visit(generator.iter, inner, stack)
                inner = None if generator.ifs else self._times(inner, self._length(generator.iter))
                self._visit_all(generator.ifs, inner, stack)
            elements = [node.key, node.value] if isinstance(node, ast.DictComp) else [node.elt]
            self._visit_all(elements, inner, stack)
        elif isinstance(node, ast.Call):
            key = self._api_key(node)
            if key is not None:
                self._add(key, count)
            func = node.func
            if isinstance(func, ast.Name) and func.id in self.functions:
                if func.id not in stack:
                    self._visit_all(self.functions[func.id].body, count, stack + (func.id,))
            else:
                self._visit(func, count, stack)
            self._visit_all(list(node.args) + [k.value for k in node.keywords], count, stack)
        elif (
            isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id in self.functions
            and node.id not in stack
        ):
            # A function passed around rather than called here, e.g. to
            # memory_usage(): it may run any number of times.
            self._visit_all(self.functions[node.id].body, None, stack + (node.id,))
        else:
            self._visit_all(list(ast.iter_child_nodes(node)), count, stack)


def _find_notebooks(directories):
    """Notebook stem -> path; the first directory listed wins."""
    notebooks = {}
    for directory in directories:
        for path in sorted(directory.rglob("*.ipynb")):
            if not SKIP_DIRS.intersection(path.parts):
                notebooks.setdefault(path.stem, path)
    return notebooks


def _key_index(notebooks):
    """Call key -> stems of the notebooks that contain it."""
    index = collections.defaultdict(set)
    for stem, path in notebooks.items():
        text = path.read_text(encoding="utf-8")
        for key in re.findall(r"'(cell_\d+_call_\d+_\w+?)'", text):
            index[key].add(stem)
    return index


def _notebook_for(csv_path, notebooks):
    """The notebook a CSV came from, matched by file name, e.g.
    plot_pca_performance(1).csv -> plot_pca."""
    for name in (csv_path.stem, csv_path.stem.removeprefix("plot_")):
        matches = [
            stem for stem in notebooks
            if name == stem or re.match(rf"{re.escape(stem)}[_.( -]", name)
        ]
        if matches:
            return notebooks[max(matches, key=len)]
    return None


def _split_runs(keys, known):
    """Split the CSV's call keys into runs. Runs are appended to the same CSV,
    so each time the notebook's first call (one that runs once) reappears, a
    new run has started."""
    anchors = sorted((k for k, c in known.items() if c == 1), key=_call_order)
    if not anchors:
        return [keys]
    runs, current = [], []
    for key in keys:
        if key == anchors[0] and current:
            runs.append(current)
            current = []
        current.append(key)
    runs.append(current)
    return runs


def _judge_run(counts, known):
    """'complete', 'stopped at <key>', or 'differs' for one run."""
    if all(counts[k] == c for k, c in known.items()):
        return "complete", None
    nonzero = sorted((k for k, c in known.items() if c > 0), key=_call_order)
    missing = [k for k in nonzero if counts[k] == 0]
    if missing and not any(counts[k] > known[k] for k in known):
        first = missing[0]
        later = [k for k in nonzero if _call_order(k) >= _call_order(first)]
        if all(counts[k] == 0 for k in later):
            return "stopped", first
        return "gaps", missing
    return "differs", None


def _check(rows, notebook_path, cache, key_index):
    """Compare the rows in a CSV with the rows a complete run should write."""
    all_keys = [r["values"].get("call_key") for r in rows]
    keys = all_keys
    if notebook_path is None:
        return {
            "status": "unknown",
            "expected": "?",
            "reported": len(keys),
            "message": "No matching notebook found, so the expected calls are unknown.",
            "details": [],
        }
    if notebook_path not in cache:
        cache[notebook_path] = _ExpectedCalls(notebook_path).counts
    expected = cache[notebook_path]
    known = {k: c for k, c in expected.items() if c is not None}
    variable = sorted((k for k, c in expected.items() if c is None), key=_call_order)
    expected_total = sum(known.values())
    expected_text = str(expected_total) + (f" + {len(variable)} var." if variable else "")
    # Rows from other notebooks that write to the same CSV file.
    foreign = collections.Counter()
    for key in keys:
        owners = key_index.get(key, set()) - {notebook_path.stem}
        if key not in expected and owners:
            foreign[", ".join(sorted(owners))] += 1
    keys = [k for k in keys if k in expected or not key_index.get(k)]
    unexpected = sorted({k for k in keys if k not in expected})

    runs = _split_runs([k for k in keys if k in known], known)
    verdicts, details = [], []
    for number, run in enumerate(runs, start=1):
        counts = collections.Counter(run)
        verdict, info = _judge_run(counts, known)
        label = f"run {number}" if len(runs) > 1 else "this run"
        if verdict == "complete":
            verdicts.append("complete")
        elif verdict == "stopped":
            verdicts.append(f"stopped at or before {info} (cell {_call_order(info)[0]})")
        elif verdict == "gaps":
            verdicts.append(f"had {len(info)} call(s) missing (they may have failed)")
        else:
            verdicts.append("row counts differ")
        if verdict != "complete":
            for key in sorted(known, key=_call_order):
                if counts[key] != known[key]:
                    details.append(f"{label}: {key}: expected {known[key]}, reported {counts[key]}")
    for key in variable:
        details.append(f"{key}: runs a variable number of times; reported {keys.count(key)}")
    for key in unexpected:
        details.append(f"{key}: not in the notebook; reported {keys.count(key)}")

    complete = verdicts.count("complete")
    if unexpected:
        status = "warn"
        message = (
            f"{len(unexpected)} call key(s) in the CSV are not in {notebook_path.name}; "
            "it may be from a different version of the notebook."
        )
    elif not keys:
        status, message = "warn", f"No rows from {notebook_path.stem}."
    elif len(runs) == 1:
        status = "ok" if complete else "warn"
        if complete:
            message = "Complete: matches the notebook."
        elif verdicts[0].startswith("had"):
            message = f"This run {verdicts[0]}."
        else:
            message = verdicts[0][0].upper() + verdicts[0][1:] + "."
    else:
        status = "ok" if complete == len(runs) else "warn"
        summary = collections.Counter(verdicts)
        parts = [f"{n} {v}" for v, n in summary.items()]
        message = f"{len(runs)} runs appended to this CSV: " + "; ".join(parts) + "."
    if foreign:
        status = "warn"
        others = "; ".join(f"{name} ({n} rows)" for name, n in foreign.items())
        message = (
            f"Also has rows from other notebooks writing to the same file: {others}; "
            f"only the {notebook_path.stem} rows are checked. " + message
        )
    if variable:
        message += (
            f" {len(variable)} call(s) run a variable number of times "
            "(%timeit/%memit, lambdas, loops) and aren't counted."
        )
    return {
        "status": status,
        "expected": expected_text,
        "reported": len(all_keys),
        "runs": len(runs),
        "message": message,
        "details": details,
        "notebook": notebook_path,
    }


def _check_html(check):
    rows = len(check["details"])
    details = ""
    if check["details"]:
        items = "".join(f"<li>{html.escape(d)}</li>" for d in check["details"])
        details = f"<details><summary>{rows} call(s) to look at</summary><ul>{items}</ul></details>"
    notebook = check.get("notebook")
    source = f" &middot; notebook {html.escape(str(notebook.name))}" if notebook else ""
    return (
        f'<div class="check {check["status"]}">'
        f'<strong>Expected {html.escape(check["expected"])} call(s), CSV has '
        f'{check.get("reported", "?")}</strong>{source} &mdash; {html.escape(check["message"])}'
        f"{details}</div>"
    )


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


def _section(index, path, label, columns, rows, check):
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
        f"{_check_html(check)}"
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
    for index, path, label, (count, runtime, memory), check in summaries:
        folder = str(Path(label).parent)
        sets.setdefault(folder, []).append(
            (path.name, f'<tr><td><a href="#csv-{index}">{html.escape(path.name)}</a></td>'
                        f'<td class="num">{count}</td>'
                        f'<td class="num expected {check["status"]}" title="{html.escape(check["message"])}">'
                        f'{html.escape(check["expected"])}</td>'
                        f'<td class="num">{runtime}</td>'
                        f'<td class="num">{memory}</td></tr>')
        )
    tables = []
    for folder, rows in sets.items():
        body = "".join(row for _, row in sorted(rows))
        tables.append(
            f'<div class="set"><h3>{html.escape(folder)}/</h3>'
            "<table><thead><tr><th>CSV</th><th>Calls</th><th>Expected</th><th>Total runtime</th>"
            f"<th>Peak memory</th></tr></thead><tbody>{body}</tbody></table></div>"
        )
    return "".join(tables)


def render(paths, notebook_dirs):
    base = Path.cwd().resolve()
    notebooks = _find_notebooks(notebook_dirs)
    key_index = _key_index(notebooks)
    cache = {}
    sections, summaries = [], []
    for index, path in enumerate(paths, start=1):
        columns, rows = _load(path)
        label = _label(path, base)
        check = _check(rows, _notebook_for(path, notebooks), cache, key_index)
        summaries.append((index, path, label, _summary(rows), check))
        sections.append(_section(index, path, label, columns, rows, check))
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
  --accent: #2563c9; --ok: #1f7a3f; --warn: #a65d00;
  --ok-bg: rgba(31, 122, 63, 0.10); --warn-bg: rgba(214, 133, 0, 0.14);
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg: #15181e; --fg: #e3e6ec; --muted: #9aa2b1; --line: #2c313b;
    --head: #1d2129; --code: #1a1e25; --bar: rgba(96, 160, 255, 0.22);
    --accent: #7fb0ff; --ok: #6fcf8f; --warn: #f0b45a;
    --ok-bg: rgba(111, 207, 143, 0.12); --warn-bg: rgba(240, 180, 90, 0.14);
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
.check {{
  margin: 0 0 8px; padding: 6px 10px; border-radius: 6px; font-size: 13px;
  border-left: 3px solid var(--line);
}}
.check.ok {{ background: var(--ok-bg); border-left-color: var(--ok); }}
.check.warn {{ background: var(--warn-bg); border-left-color: var(--warn); }}
.check details {{ margin-top: 4px; }}
.check ul {{ margin: 4px 0 0; padding-left: 20px; font: 12px/1.5 ui-monospace, Menlo, Consolas, monospace; }}
td.expected.ok {{ color: var(--ok); }}
td.expected.warn {{ color: var(--warn); font-weight: 600; background: var(--warn-bg); }}
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
    parser.add_argument(
        "--notebooks",
        dest="notebook_dirs",
        action="append",
        type=Path,
        metavar="DIR",
        help=(
            "Folder of notebooks to check the CSVs against; may be repeated, and "
            "the first folder with a matching notebook wins (default: "
            + ", ".join(str(d.relative_to(SCRIPT_DIR)) for d in DEFAULT_NOTEBOOK_DIRS)
            + ")."
        ),
    )
    args = parser.parse_args()

    paths = _find_csvs(args.paths)
    if not paths:
        raise SystemExit("No CSVs with a parameters_json column found.")
    notebook_dirs = [d for d in (args.notebook_dirs or DEFAULT_NOTEBOOK_DIRS) if d.is_dir()]
    args.output.write_text(render(paths, notebook_dirs), encoding="utf-8")
    print(f"Wrote {args.output} ({len(paths)} CSV file(s)).")
    if args.open:
        webbrowser.open(args.output.resolve().as_uri())


if __name__ == "__main__":
    main()
