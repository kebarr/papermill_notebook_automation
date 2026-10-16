#!/usr/bin/env python3
"""Convert the parameterised notebooks into runnable Python scripts.

Each notebook becomes scripts/<notebook>.py. The script keeps the notebook's
"parameters" cell as its default parameters, adds FIGURE_DIR, FIGURE_FORMAT and
FIGURE_NAMES parameters, and saves figures instead of displaying them. The
scripts share scripts/notebook_runtime.py.

Each notebook also becomes console/<notebook>.py: a self-contained version,
with notebook_runtime.py embedded, to paste into a Python console. It runs once
with the default parameters.

Examples:
    python notebook_to_script.py              # convert every notebook
    python notebook_to_script.py plot_pca     # convert one notebook
"""

import argparse
import ast
import io
import json
import pprint
import re
import tokenize
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_NOTEBOOKS_DIR = SCRIPT_DIR / "notebooks"
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "scripts"
DEFAULT_CONSOLE_DIR = SCRIPT_DIR / "console"
RUNTIME_PATH = DEFAULT_OUTPUT_DIR / "notebook_runtime.py"
# notebook_runtime.py is embedded in console files up to this section.
RUNTIME_CLI_MARKER = "# Command line and CSV configuration"
# Parameters ending in OUTPUT_CSV_SUFFIX (e.g. PERFORMANCE_CSV_PATH) default to
# a file of the same name in OUTPUT_CSV_DIR, relative to where the script is run.
OUTPUT_CSV_SUFFIX = "_CSV_PATH"
OUTPUT_CSV_DIR = "executed_runs_scripts"
# Console files copy their printed output to <CONSOLE_OUTPUT_DIR>/<notebook>_stdout.txt.
CONSOLE_OUTPUT_DIR = "executed_runs_console"
API_HELPER = "_call_api_with_parameters"
KEEP_CALLSITE_VALUE = "__KEEP_CALLSITE_VALUE__"
INDENT = "    "

# API methods that display a figure even though their names don't start
# with "plot_".
FIGURE_METHODS = {"igv", "view_alignments"}
# Calls made in notebook code (outside the API helper) that create or show a
# figure, e.g. px.histogram(...), bkplt.show(fig), series.hist(backend="plotly").
FIGURE_MODULES = {"px", "go", "plt"}
FIGURE_FUNCTIONS = {"show", "hist", "plot", "savefig"}
# API arguments used, in order of preference, to tell apart default figure
# names for calls to the same method.
QUALIFIER_PARAMETERS = (
    ("color", "by_{}"),
    ("transcript", "{}"),
    ("contig", "{}"),
    ("sample", "{}"),
)


# ---------------------------------------------------------------------------
# Reading notebooks
# ---------------------------------------------------------------------------


def _is_parameters_cell(cell):
    return "parameters" in cell.get("metadata", {}).get("tags", [])


def _parameters_cell(notebook_path, notebook):
    cells = [
        cell
        for cell in notebook["cells"]
        if cell["cell_type"] == "code" and _is_parameters_cell(cell)
    ]
    if len(cells) != 1:
        raise ValueError(
            f"{notebook_path} must have exactly one parameters-tagged cell; "
            f"found {len(cells)}."
        )
    source = "".join(cells[0]["source"]).strip()
    lines = source.splitlines()
    parameters = {}
    # Walk backwards so replacing one assignment leaves earlier line numbers valid.
    for node in reversed(ast.parse(source).body):
        if not (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(node.targets[0], ast.Name)
        ):
            raise ValueError(
                f"The parameters cell of {notebook_path} may only contain "
                "simple assignments."
            )
        name = node.targets[0].id
        value = ast.literal_eval(node.value)
        if name.endswith(OUTPUT_CSV_SUFFIX) and isinstance(value, str):
            value = f"{OUTPUT_CSV_DIR}/{Path(value).name}"
            lines[node.lineno - 1 : node.end_lineno] = [
                "# Relative to where the script is run from.",
                f"{name} = {value!r}",
            ]
        parameters[name] = value
    return "\n".join(lines), dict(reversed(parameters.items()))


# ---------------------------------------------------------------------------
# IPython magics
# ---------------------------------------------------------------------------


def _translate_magics(source, where):
    """Replace IPython magics with calls to notebook_runtime.

    Returns the translated source and whether the cell used %%time.
    """
    lines = source.splitlines()
    timed = False
    if lines and lines[0].startswith("%%"):
        magic = lines[0].split()[0]
        if magic != "%%time":
            raise ValueError(f"{where}: unsupported cell magic {magic}.")
        timed = True
        lines = lines[1:]

    translated = []
    for line in lines:
        match = re.match(r"^(\s*)([!%])(.*)$", line)
        if not match:
            translated.append(line)
            continue
        indent, prefix, rest = match.groups()
        if prefix == "!":
            translated.append(f"{indent}nbrt.shell({rest.strip()!r})")
            continue
        magic, _, argument = rest.partition(" ")
        argument = argument.strip()
        if magic in ("timeit", "memit"):
            translated.append(f"{indent}nbrt.{magic}(lambda: {argument})")
        elif magic == "load_ext":
            translated.append(f"{indent}pass  # %load_ext {argument}: not needed in a script")
        else:
            raise ValueError(f"{where}: unsupported magic %{magic}.")
    return "\n".join(translated), timed


# ---------------------------------------------------------------------------
# Rewriting cell code
# ---------------------------------------------------------------------------


def _display_last_expression(source):
    """Wrap the cell's last expression in nbrt.display(), as Jupyter shows the
    value of a cell's last expression (unless it ends with a semicolon)."""
    module = ast.parse(source)
    if not module.body or not isinstance(module.body[-1], ast.Expr):
        return source
    node = module.body[-1]
    call = node.value
    if (
        isinstance(call, ast.Call)
        and isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id == "nbrt"
    ):
        return source  # a translated magic
    lines = source.splitlines()
    end_line = lines[node.end_lineno - 1]
    if end_line[node.end_col_offset:].lstrip().startswith(";"):
        return source
    lines[node.end_lineno - 1] = (
        end_line[: node.end_col_offset] + ")" + end_line[node.end_col_offset:]
    )
    start_line = lines[node.lineno - 1]
    lines[node.lineno - 1] = (
        start_line[: node.col_offset] + "nbrt.display(" + start_line[node.col_offset:]
    )
    return "\n".join(lines)


def _indent(source, prefix=INDENT):
    """Indent code, leaving the inside of multi-line strings untouched."""
    inside_strings = set()
    tokens = tokenize.generate_tokens(io.StringIO(source + "\n").readline)
    for token in tokens:
        if token.type == tokenize.STRING or token.type == getattr(
            tokenize, "FSTRING_MIDDLE", None
        ):
            inside_strings.update(range(token.start[0] + 1, token.end[0] + 1))
    return "\n".join(
        line if number in inside_strings or not line.strip() else prefix + line
        for number, line in enumerate(source.splitlines(), start=1)
    )


def _comment(text):
    return "\n".join(
        f"# {line}".rstrip() for line in text.strip().splitlines()
    )


# ---------------------------------------------------------------------------
# Default figure names
# ---------------------------------------------------------------------------


def _api_calls(tree):
    """Yield (call_key, client, method, call node) for each API helper call."""
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == API_HELPER
            and len(node.args) >= 2
            and isinstance(node.args[0], ast.Attribute)
            and isinstance(node.args[1], ast.Constant)
        ):
            target = node.args[0]
            client = target.value.id if isinstance(target.value, ast.Name) else "api"
            yield node.args[1].value, client, target.attr, node


def _shows_figure(method, call, call_parameters):
    """Whether an API call displays a figure with the notebook's defaults."""
    if not (method.startswith("plot_") or method in FIGURE_METHODS):
        return False
    show = call_parameters.get("show", KEEP_CALLSITE_VALUE)
    if isinstance(show, bool):
        return show
    for keyword in call.keywords:
        if keyword.arg == "show" and isinstance(keyword.value, ast.Constant):
            return bool(keyword.value.value)
    return True


def _call_qualifier(call, call_parameters):
    """A short description of what an API call plots, e.g. "by_country" or
    "AGAP004707-RD", to tell apart figures from the same method."""
    callsite = {
        keyword.arg: keyword.value.value
        for keyword in call.keywords
        if isinstance(keyword.value, ast.Constant)
    }
    for name, template in QUALIFIER_PARAMETERS:
        value = call_parameters.get(name, KEEP_CALLSITE_VALUE)
        if value == KEEP_CALLSITE_VALUE:
            value = callsite.get(name)
        if isinstance(value, str) and value:
            return template.format(re.sub(r"[^A-Za-z0-9_-]+", "_", value).strip("_"))
    return None


def _cell_figure_label(cell_key, tree):
    """A label for a figure the cell makes outside the API helper, or None."""
    api_nodes = {id(node) for *_, node in _api_calls(tree)}
    last = tree.body[-1] if tree.body else None
    makes_figure = (
        isinstance(last, ast.Expr)
        and isinstance(last.value, ast.Name)
        and last.value.id.startswith("fig")
    )
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or id(node) in api_nodes:
            continue
        func = node.func
        if isinstance(func, ast.Attribute) and (
            func.attr in FIGURE_FUNCTIONS
            or (isinstance(func.value, ast.Name) and func.value.id in FIGURE_MODULES)
        ):
            makes_figure = True
            break
    if not makes_figure:
        return None

    # Name the figure after what it plots where that is easy to tell, e.g.
    # px.histogram(seq_flen) -> histogram_seq_flen.
    if isinstance(last, ast.Expr) and isinstance(last.value, ast.Call):
        func = last.value.func
        args = last.value.args
        if (
            isinstance(func, ast.Attribute)
            and isinstance(func.value, ast.Name)
            and func.value.id in FIGURE_MODULES
            and args
            and isinstance(args[0], ast.Name)
        ):
            return f"{func.attr}_{args[0].id}"
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "hist"
            and isinstance(node.func.value, ast.Subscript)
            and isinstance(node.func.value.slice, ast.Constant)
        ):
            return f"hist_{node.func.value.slice.value}"
    return cell_key.removeprefix("notebook_") + "_figure"


def _figure_names(code_cells, api_parameters):
    """Default FIGURE_NAMES: one entry per figure the notebook displays, in
    order, keyed by API call key or notebook cell key."""
    entries = []
    for cell_key, tree in code_cells:
        for call_key, client, method, call in _api_calls(tree):
            if call_key in api_parameters and _shows_figure(
                method, call, api_parameters[call_key]
            ):
                label = f"{client}_{method.removeprefix('plot_')}"
                qualifier = _call_qualifier(call, api_parameters[call_key])
                entries.append((call_key, f"{label}_{qualifier}" if qualifier else label))
        label = _cell_figure_label(cell_key, tree)
        if label is not None:
            entries.append((cell_key, label))

    width = max(2, len(str(len(entries))))
    return {
        key: f"{number:0{width}d}_{label}"
        for number, (key, label) in enumerate(entries, start=1)
    }


# ---------------------------------------------------------------------------
# Console files
# ---------------------------------------------------------------------------


def _console_runtime():
    """notebook_runtime.py without its command line, for embedding in a
    console file as a raw string."""
    source = RUNTIME_PATH.read_text(encoding="utf-8")
    source = source[: source.index(RUNTIME_CLI_MARKER)].rstrip()
    if "\'\'\'" in source or source.endswith("\\"):
        raise ValueError(f"{RUNTIME_PATH} cannot be embedded in a raw string.")
    return source + "\n"


def _lines_inside_strings(source):
    """Line numbers (1-based) that continue a multi-line string."""
    lines = set()
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.STRING or token.type == getattr(
            tokenize, "FSTRING_MIDDLE", None
        ):
            lines.update(range(token.start[0] + 1, token.end[0] + 1))
    return lines


def _console_safe(source):
    """Lay out code so it can be pasted into the standard Python console.

    The console ends an indented block at the first blank line, and needs a
    blank line before a new statement can follow a block. So drop blank lines
    inside statements (but not inside strings) and add one after each compound
    statement.
    """
    in_strings = _lines_inside_strings(source)
    in_statements = set()
    block_ends = set()
    for node in ast.parse(source).body:
        start = min(
            [node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])]
        )
        in_statements.update(range(start, node.end_lineno + 1))
        if isinstance(getattr(node, "body", None), list):
            block_ends.add(node.end_lineno)
    output = []
    for number, line in enumerate(source.splitlines(), start=1):
        if not line.strip() and number in in_statements and number not in in_strings:
            continue
        output.append(line.rstrip() if number not in in_strings else line)
        if number in block_ends:
            output.append("")
    return "\n".join(output) + "\n"


# ---------------------------------------------------------------------------
# Rendering the script
# ---------------------------------------------------------------------------


def convert(notebook_path, output_dir, console_dir):
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    parameters_source, parameters = _parameters_cell(notebook_path, notebook)
    api_parameters = parameters.get("API_CALL_PARAMETERS", {})
    relative_notebook = (
        notebook_path.relative_to(SCRIPT_DIR)
        if notebook_path.is_relative_to(SCRIPT_DIR)
        else notebook_path
    )

    body = []
    code_cells = []
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell["source"]).strip()
        if not source or _is_parameters_cell(cell):
            continue
        if cell["cell_type"] == "markdown":
            body.append(_comment(source))
            continue
        if cell["cell_type"] != "code":
            continue

        cell_key = f"notebook_cell_{index}"
        where = f"{relative_notebook} cell {index}"
        code, timed = _translate_magics(source, where)
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            raise ValueError(f"{where}: cannot convert ({exc}).") from exc
        code_cells.append((cell_key, tree))
        code = _display_last_expression(code)

        lines = [f"# --- Notebook cell {index} ---", f'nbrt.start_cell("{cell_key}")']
        if timed:
            lines.append("_cell_timer = nbrt.time_cell_start()  # %%time")
        lines.append(code)
        if timed:
            lines.append("nbrt.time_cell_report(_cell_timer)")
        if re.search(rf"^def {API_HELPER}\(", code, re.MULTILINE):
            lines.append(
                "# Name figures after the API call that produced them.\n"
                f"{API_HELPER} = nbrt.track_api_calls({API_HELPER})"
            )
        body.append("\n".join(lines))

    figure_names = _figure_names(code_cells, api_parameters)
    stem = notebook_path.stem
    parameter_names = list(parameters)
    all_parameters = parameter_names + ["FIGURE_DIR", "FIGURE_FORMAT", "FIGURE_NAMES"]

    script = f'''#!/usr/bin/env python3
"""{stem}: the code from {relative_notebook} as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/{stem}.py                      # the notebook's defaults
    python scripts/{stem}.py --config runs.csv    # one run per CSV row
    python scripts/{stem}.py --list-parameters    # what a CSV can set
    python scripts/{stem}.py --output-csv my_run.csv
                                    # performance CSV -> {OUTPUT_CSV_DIR}/my_run.csv

CSV columns are parameter names ({", ".join(all_parameters)}).
Values are JSON; empty cells keep the default. API_CALL_PARAMETERS and
FIGURE_NAMES only need the entries you want to change.

Generated from the notebook by notebook_to_script.py.
"""

import notebook_runtime as nbrt

# ---------------------------------------------------------------------------
# Parameters (the notebook's "parameters" cell)
# ---------------------------------------------------------------------------

{parameters_source}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = {f"figures/{stem}"!r}

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {pprint.pformat(figure_names, sort_dicts=False, width=79)}


def run({", ".join(parameter_names)}):
{chr(10).join(_indent(chunk) for chunk in body) if body else INDENT + "pass"}


if __name__ == "__main__":
    nbrt.main(
        notebook={relative_notebook.name!r},
        run=run,
        parameters={{
{chr(10).join(f"            {name!r}: {name}," for name in all_parameters)}
        }},
    )
'''
    compile(script, str(output_dir / f"{stem}.py"), "exec")
    output_path = output_dir / f"{stem}.py"
    output_path.write_text(script, encoding="utf-8")

    console = f"""# {stem}: the code from {relative_notebook}, to paste into a Python console.
#
# Paste the whole file. It runs once with the notebook's default parameters,
# saving figures to FIGURE_DIR instead of displaying them; other cell outputs
# are printed, and copied to OUTPUT_LOG. Relative paths, in the settings below and in the notebook code
# (e.g. ../gcs_cache), resolve against the console's current directory: start
# the console in the notebooks folder to match Jupyter.
#
# The layout works in the standard Python console as well as IPython: there are
# no blank lines inside indented blocks, and each block ends with a blank line.
# If a statement fails, the console carries on with the next one, so check the
# output for the first traceback.
#
# Generated from the notebook by notebook_to_script.py.

# Support code shared by all the console files: saves figures, emulates
# IPython magics. It is the same as scripts/notebook_runtime.py.
import types
nbrt = types.ModuleType("nbrt")
exec(compile(r'''{_console_runtime()}''', "nbrt", "exec"), nbrt.__dict__)

# ---------------------------------------------------------------------------
# Parameters (the notebook's "parameters" cell)
# ---------------------------------------------------------------------------

{parameters_source}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in.
FIGURE_DIR = {f"figures/{stem}"!r}

# One of "html" (interactive), "png", "svg" or "pdf"; see scripts/{stem}.py.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it.
FIGURE_NAMES = {pprint.pformat(figure_names, sort_dicts=False, width=79)}

# File that printed output is copied to, as well as being shown in the console.
OUTPUT_LOG = {f"{CONSOLE_OUTPUT_DIR}/{stem}_stdout.txt"!r}

nbrt.begin_console_run(FIGURE_DIR, FIGURE_FORMAT, FIGURE_NAMES, OUTPUT_LOG)

{(chr(10) * 2).join(body)}

nbrt.end_console_run()
"""
    console = _console_safe(console)
    compile(console, str(console_dir / f"{stem}.py"), "exec")
    console_path = console_dir / f"{stem}.py"
    console_path.write_text(console, encoding="utf-8")
    return output_path, console_path, figure_names


def main():
    parser = argparse.ArgumentParser(
        description="Convert parameterised notebooks into runnable scripts."
    )
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="Notebook names (default: every notebook in --notebooks-dir).",
    )
    parser.add_argument("--notebooks-dir", type=Path, default=DEFAULT_NOTEBOOKS_DIR)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--console-dir",
        type=Path,
        default=DEFAULT_CONSOLE_DIR,
        help="Directory for the copy-and-paste console versions.",
    )
    args = parser.parse_args()

    notebooks_dir = args.notebooks_dir.resolve()
    if args.notebooks:
        paths = [
            notebooks_dir / (name if name.endswith(".ipynb") else f"{name}.ipynb")
            for name in args.notebooks
        ]
    else:
        paths = sorted(notebooks_dir.glob("*.ipynb"))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.console_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        output_path, console_path, figure_names = convert(
            path, args.output_dir.resolve(), args.console_dir.resolve()
        )
        print(f"{path.name} -> {output_path}, {console_path} "
              f"({len(figure_names)} figures)")


if __name__ == "__main__":
    main()
