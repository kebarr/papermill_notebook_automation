#!/usr/bin/env python3
"""Add Papermill parameters to the malariagen-data example notebooks.

For each notebook, every call to a malariagen-data API client (for example
ag3.pca(...), where ag3 = malariagen_data.Ag3(...)) is rewritten as

    _call_api_with_parameters(ag3.pca, 'cell_8_call_1_ag3_pca', ...)

and a "parameters" cell is added whose API_CALL_PARAMETERS gives every
argument of every call, so a CSV can change any of them. A helper cell applies
those values and records each call's runtime and peak memory in
PERFORMANCE_CSV_PATH.

The value recorded for each argument:
- a literal at the call site (e.g. n_snps=50_000): that value;
- anything else at the call site (a variable, an expression, an f-string):
  the API_KEEP_CALLSITE_VALUE marker, so the notebook's own value is used;
- not passed: the method's default, or the marker when the default can't be
  written as a literal, or when the call unpacks *args/**kwargs that might
  supply it.

Call keys are cell_<N>_call_<M>_<client>_<method>, where N is the position of
the cell in the original notebook counting from 1 (markdown cells included)
and M numbers the API calls within the cell in source order.

Examples:
    python parameterise_notebooks.py
    python parameterise_notebooks.py plot_pca karyotype
    python parameterise_notebooks.py --source ~/malariagen-data-python/notebooks \\
        --output notebooks_fixed_parameters_cells
"""

import argparse
import ast
import inspect
import json
import pprint
import re
import uuid
from pathlib import Path

# Notes from Claude:
# How it decides each argument's value:

#Literal at the call site (e.g. n_snps=50_000): that value, editable from a CSV.
#Anything else at the call site (a variable, [demo_sample_set], dict(...), an f-string): __KEEP_CALLSITE_VALUE__, so the notebook's own value is used. This is the fix.
#Not passed: the method's default from its real signature, or KEEP if the default can't be written as a literal, or if the call uses */** unpacking that might supply it.
#Checks on the output:

#No overrides: none of the 84 call-site values the old cells overrode are overridden now; I rescanned, including positional arguments. For example, karyotype's sample_sets is now KEEP, so its PCA uses the two intended sample sets.
#Same call keys: the keys match your existing notebooks/ exactly, so runners_and_csvs configs, FIGURE_NAMES and earlier performance CSVs still line up.
#Valid notebooks: all 37 pass nbformat validation. Nested calls (IGV) and multi-line calls are rewritten correctly, magics are kept, and tuple defaults like percentiles stay tuples.
#Current helper: every notebook gets the full helper (performance CSV plus the tuple conversion). Before, spike_sim_test_data was missing it.
#Clean outputs and a bare CSV name: old outputs are cleared, and PERFORMANCE_CSV_PATH is <notebook>_performance.csv. Your sed line or the runner's --output-csv sets its location.

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_SOURCE = SCRIPT_DIR.parent / "malariagen-data-python" / "notebooks"
DEFAULT_OUTPUT = SCRIPT_DIR / "notebooks_fixed_parameters_cells"
KEEP = "__KEEP_CALLSITE_VALUE__"
API_HELPER = "_call_api_with_parameters"

PARAMETERS_CELL = """\
# Malariagen API arguments for each call below.
# Replace a value to override it; keep the marker to use the call-site
# value or the method's default.
API_KEEP_CALLSITE_VALUE = {keep!r}
PERFORMANCE_CSV_PATH = {performance_csv!r}
API_CALL_PARAMETERS = {parameters}"""

HELPER_CELL = '''\
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
'''


# ---------------------------------------------------------------------------
# Parsing cells that contain IPython magics
# ---------------------------------------------------------------------------


def _mask_magics(source, comment_line_magics=False):
    """Replace magics with Python of exactly the same length, so ast positions
    still match the original text. `%timeit expr` becomes `_=      expr`, so
    API calls inside line magics are still found; cell magics and shell
    commands become comments."""
    lines = source.split("\n")
    for i, line in enumerate(lines):
        match = re.match(r"^(\s*)(%%|%|!)(\S*)(\s*)(.*)$", line)
        if not match:
            continue
        indent, prefix, word, gap, argument = match.groups()
        if prefix == "%" and argument and not comment_line_magics:
            lines[i] = indent + "_=" + " " * (len(word) - 1 + len(gap)) + argument
        else:
            lines[i] = indent + "#" + line[len(indent) + 1:]
    return "\n".join(lines)


def _parse_cell(source):
    for comment_line_magics in (False, True):
        try:
            return ast.parse(_mask_magics(source, comment_line_magics))
        except SyntaxError:
            continue
    return None


class _Positions:
    """Converts ast (line, byte column) positions to offsets in the text."""

    def __init__(self, source):
        self.lines = source.split("\n")
        self.starts = [0]
        for line in self.lines:
            self.starts.append(self.starts[-1] + len(line) + 1)

    def offset(self, lineno, col):
        line = self.lines[lineno - 1]
        chars = len(line.encode("utf-8")[:col].decode("utf-8", errors="ignore"))
        return self.starts[lineno - 1] + chars

    def span(self, node):
        return (
            self.offset(node.lineno, node.col_offset),
            self.offset(node.end_lineno, node.end_col_offset),
        )


# ---------------------------------------------------------------------------
# Finding API clients and calls
# ---------------------------------------------------------------------------


def _client_classes():
    import malariagen_data

    return {
        name: cls
        for name, cls in inspect.getmembers(malariagen_data, inspect.isclass)
        if callable(getattr(cls, "sample_metadata", None))
    }


def _find_clients(trees, classes):
    """Variables assigned a malariagen-data client, mapped to its class."""
    clients = {}
    for tree in trees:
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Assign) and isinstance(node.value, ast.Call)):
                continue
            func = node.value.func
            if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
                class_name = func.attr if func.value.id == "malariagen_data" else None
            elif isinstance(func, ast.Name):
                class_name = func.id
            else:
                class_name = None
            if class_name not in classes:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    clients[target.id] = classes[class_name]
    return clients


def _inside_fstring(node, parents):
    while node in parents:
        node = parents[node]
        if isinstance(node, ast.JoinedStr):
            return True
    return False


def _api_calls(tree, clients, warnings, where):
    """API calls in a cell, in source order, as (node, client, method)."""
    parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
    calls = []
    for node in ast.walk(tree):
        if not (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in clients
        ):
            continue
        client, method = node.func.value.id, node.func.attr
        if not callable(getattr(clients[client], method, None)):
            warnings.append(f"{where}: {client}.{method} is not an API method; left as is")
            continue
        if _inside_fstring(node, parents):
            warnings.append(f"{where}: {client}.{method}(...) inside an f-string; left as is")
            continue
        calls.append((node, client, method))
    return sorted(calls, key=lambda c: (c[0].lineno, c[0].col_offset))


# ---------------------------------------------------------------------------
# Parameter values
# ---------------------------------------------------------------------------


def _literal(node):
    """(True, value) if node is a literal, else (False, None)."""
    try:
        return True, ast.literal_eval(node)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False, None


def _writable_default(value):
    """Whether a default can be written in the parameters cell as a literal."""
    try:
        return ast.literal_eval(repr(value)) == value
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False


def _call_parameters(method, call, counts):
    """Every argument of the method, with the value to record for it."""
    parameters = list(inspect.signature(method).parameters.values())
    if parameters and parameters[0].name in ("self", "cls"):
        parameters = parameters[1:]

    unpacked = any(isinstance(a, ast.Starred) for a in call.args) or any(
        k.arg is None for k in call.keywords
    )
    passed = {}
    positional = [p for p in parameters if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    for parameter, arg in zip(positional, call.args):
        if isinstance(arg, ast.Starred):
            break
        passed[parameter.name] = arg
    for keyword in call.keywords:
        if keyword.arg is not None:
            passed[keyword.arg] = keyword.value

    values = {}
    for parameter in parameters:
        if parameter.kind in (parameter.VAR_POSITIONAL, parameter.VAR_KEYWORD):
            values[parameter.name] = KEEP
        elif parameter.name in passed:
            is_literal, value = _literal(passed[parameter.name])
            values[parameter.name] = value if is_literal else KEEP
            counts["keep_callsite" if not is_literal else "literal"] += 1
        elif unpacked:
            values[parameter.name] = KEEP
        elif parameter.default is parameter.empty or not _writable_default(parameter.default):
            values[parameter.name] = KEEP
        else:
            values[parameter.name] = parameter.default
    return values


# ---------------------------------------------------------------------------
# Rewriting cells
# ---------------------------------------------------------------------------


def _rewrite_cell(source, tree, calls, cell_number, clients, api_parameters, counts):
    positions = _Positions(source)
    spans = {id(node): positions.span(node) for node, _, _ in calls}
    keys = {}
    for number, (node, client, method) in enumerate(calls, start=1):
        key = f"cell_{cell_number}_call_{number}_{client}_{method}"
        keys[id(node)] = key
        api_parameters[key] = _call_parameters(getattr(clients[client], method), node, counts)

    def render(start, end):
        """Source text from start to end with the API calls in it rewritten."""
        pieces, position = [], start
        for node, _, _ in calls:
            call_start, call_end = spans[id(node)]
            if call_start < position or call_end > end or call_start < start:
                continue  # outside this range, or nested in a call already done
            pieces.append(source[position:call_start])
            pieces.append(render_call(node))
            position = call_end
        pieces.append(source[position:end])
        return "".join(pieces)

    def render_call(node):
        arguments = sorted(
            list(node.args) + list(node.keywords), key=lambda a: (a.lineno, a.col_offset)
        )
        parts = [render(*positions.span(node.func)), repr(keys[id(node)])]
        parts += [render(*positions.span(argument)) for argument in arguments]
        return f"{API_HELPER}({', '.join(parts)})"

    return render(0, len(source))


def _new_cell(source, tags=None, with_id=False):
    lines = source.split("\n")
    cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {"tags": tags} if tags else {},
        "outputs": [],
        "source": [line + "\n" for line in lines[:-1]] + [lines[-1]],
    }
    if with_id:
        cell["id"] = str(uuid.uuid4())
    return cell


def parameterise(source_path, output_path, classes):
    notebook = json.loads(source_path.read_text(encoding="utf-8"))
    cells = notebook["cells"]
    with_ids = notebook.get("nbformat", 4) >= 4 and notebook.get("nbformat_minor", 0) >= 5

    sources = ["".join(c["source"]) for c in cells]
    trees = [
        _parse_cell(s) if c["cell_type"] == "code" else None
        for c, s in zip(cells, sources)
    ]
    clients = _find_clients([t for t in trees if t is not None], classes)

    warnings, api_parameters = [], {}
    counts = {"calls": 0, "literal": 0, "keep_callsite": 0}
    for index, (cell, source, tree) in enumerate(zip(cells, sources, trees)):
        if cell["cell_type"] != "code":
            continue
        cell["outputs"] = []
        cell["execution_count"] = None
        where = f"{source_path.name} cell {index}"
        if tree is None:
            if any(f"{client}." in source for client in clients):
                warnings.append(f"{where}: could not parse; API calls left as is")
            continue
        calls = _api_calls(tree, clients, warnings, where)
        if not calls:
            continue
        counts["calls"] += len(calls)
        new_source = _rewrite_cell(source, tree, calls, index + 1, clients, api_parameters, counts)
        lines = new_source.split("\n")
        cell["source"] = [line + "\n" for line in lines[:-1]] + [lines[-1]]

    parameters_source = PARAMETERS_CELL.format(
        keep=KEEP,
        performance_csv=f"{source_path.stem}_performance.csv",
        parameters=pprint.pformat(api_parameters, sort_dicts=False),
    )
    notebook["cells"] = [
        _new_cell(parameters_source, tags=["parameters"], with_id=with_ids),
        _new_cell(HELPER_CELL.rstrip("\n"), with_id=with_ids),
    ] + cells

    # Check every rewritten cell is still valid Python (apart from magics).
    for cell in notebook["cells"]:
        text = "".join(cell["source"])
        if cell["cell_type"] == "code" and f"{API_HELPER}(" in text and _parse_cell(text) is None:
            raise ValueError(f"{source_path.name}: rewritten cell does not parse:\n{text}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(notebook, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return clients, counts, warnings


def main():
    parser = argparse.ArgumentParser(
        description="Add Papermill parameters cells to the malariagen-data notebooks."
    )
    parser.add_argument(
        "notebooks",
        nargs="*",
        help="Notebook names (default: every notebook under --source).",
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    paths = sorted(
        p for p in source.rglob("*.ipynb") if ".ipynb_checkpoints" not in p.parts
    )
    if args.notebooks:
        wanted = {n.removesuffix(".ipynb") for n in args.notebooks}
        paths = [p for p in paths if p.stem in wanted]
        missing = wanted - {p.stem for p in paths}
        if missing:
            raise SystemExit(f"Not found under {source}: {', '.join(sorted(missing))}")

    classes = _client_classes()
    for path in paths:
        relative = path.relative_to(source)
        clients, counts, warnings = parameterise(path, args.output / relative, classes)
        print(
            f"{relative}: {counts['calls']} API calls "
            f"({', '.join(sorted(clients)) or 'no clients'}); "
            f"{counts['keep_callsite']} call-site expressions kept"
        )
        for warning in warnings:
            print(f"  warning: {warning}")
    print(f"Wrote {len(paths)} notebook(s) to {args.output}")


if __name__ == "__main__":
    main()
