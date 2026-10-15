"""Shared runtime for the scripts converted from the notebooks in ../notebooks.

Each converted script holds the notebook's code; this module replaces the parts
of Jupyter that code relies on:

- figures that the notebook would display are saved to files instead, named
  from the script's FIGURE_NAMES parameter;
- the value of each cell's last expression is printed, as Jupyter would show it;
- the IPython magics used by the notebooks (%%time, %timeit, %memit, !cmd);
- a command line that runs the script once with its default parameters, or once
  per row of a CSV whose columns override them.
"""

import argparse
import contextlib
import csv
import json
import os
import statistics
import subprocess
import sys
import time
import timeit as _timeit
import traceback
import warnings
from copy import deepcopy
from pathlib import Path

# Render matplotlib figures off screen; they are saved, never shown.
os.environ.setdefault("MPLBACKEND", "Agg")

SCRIPTS_DIR = Path(__file__).resolve().parent
DEFAULT_WORKDIR = SCRIPTS_DIR.parent / "notebooks"
FIGURE_FORMATS = ("html", "png", "svg", "pdf")
FIGURE_PARAMETERS = ("FIGURE_DIR", "FIGURE_FORMAT", "FIGURE_NAMES")
# Parameters whose override must only name call keys the notebook already has.
STRICT_KEY_PARAMETERS = ("API_CALL_PARAMETERS",)
IGV_JS_URL = "https://cdn.jsdelivr.net/npm/igv@{version}/dist/igv.min.js"
IGV_FALLBACK_VERSION = "3.1.4"
OMIT = object()

_active_saver = None
_display_hooks_installed = False


# ---------------------------------------------------------------------------
# Figure saving
# ---------------------------------------------------------------------------


class IgvBrowser:
    """Stands in for igv_notebook.Browser, which only works inside Jupyter.

    Instead of rendering in a notebook, the browser configuration is written to
    a standalone HTML page that loads igv.js.
    """

    def __init__(self, config):
        self.config = config
        self.path = None
        if _active_saver is not None:
            _active_saver.save(self)

    def _rewrite(self):
        if self.path is not None:
            _write_igv_html(self, self.path)

    def load_track(self, config):
        self.config.setdefault("tracks", []).append(config)
        self._rewrite()

    def load_roi(self, config):
        rois = config if isinstance(config, list) else [config]
        self.config.setdefault("roi", []).extend(rois)
        self._rewrite()

    def clear_rois(self):
        self.config.pop("roi", None)
        self._rewrite()

    def search(self, locus):
        self.config["locus"] = locus
        self._rewrite()

    def load_session(self, *args, **kwargs):
        warnings.warn("IGV load_session() is not supported outside Jupyter; ignored.")

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def to_svg(self):
        warnings.warn("IGV to_svg() is not supported outside Jupyter; ignored.")


def _igv_version():
    try:
        import igv_notebook

        return igv_notebook.igv_version()
    except Exception:
        return IGV_FALLBACK_VERSION


def _write_igv_html(browser, path):
    config = json.dumps(browser.config, indent=2, default=str)
    path.write_text(
        "<!doctype html>\n"
        '<html>\n<head>\n<meta charset="utf-8">\n'
        f"<title>{path.stem}</title>\n"
        f'<script src="{IGV_JS_URL.format(version=_igv_version())}"></script>\n'
        "</head>\n<body>\n"
        '<div id="igv"></div>\n'
        "<script>\n"
        f"igv.createBrowser(document.getElementById('igv'), {config});\n"
        "</script>\n</body>\n</html>\n",
        encoding="utf-8",
    )


def _figure_kind(obj):
    """Return the plotting library obj is a figure of, or None."""
    if isinstance(obj, IgvBrowser):
        return "igv"
    if "plotly" in sys.modules:
        from plotly.basedatatypes import BaseFigure

        if isinstance(obj, BaseFigure):
            return "plotly"
    if "bokeh" in sys.modules:
        from bokeh.models import LayoutDOM

        if isinstance(obj, LayoutDOM):
            return "bokeh"
    if "matplotlib" in sys.modules:
        from matplotlib.axes import Axes
        from matplotlib.figure import Figure

        if isinstance(obj, (Figure, Axes)):
            return "matplotlib"
    return None


class FigureSaver:
    """Saves the figures of one run under names taken from FIGURE_NAMES."""

    def __init__(self, figure_dir, figure_format, figure_names):
        self.figure_dir = Path(figure_dir)
        self.figure_format = figure_format
        self.figure_names = figure_names
        self.cell_key = None
        self.saved = []
        self._call_keys = []
        self._origins = {}
        self._saved_ids = set()
        self._used_names = set()
        self._keep_alive = []
        self._suppressed = 0

    @property
    def current_key(self):
        return self._call_keys[-1] if self._call_keys else self.cell_key

    @contextlib.contextmanager
    def call_context(self, call_key):
        self._call_keys.append(call_key)
        try:
            yield
        finally:
            self._call_keys.pop()

    def tag(self, obj, call_key):
        """Remember that obj was returned by call_key, for naming it later."""
        if _figure_kind(obj) is not None:
            self._origins.setdefault(id(obj), call_key)
            self._keep_alive.append(obj)

    def _file_name(self, key):
        base = self.figure_names.get(key)
        if base is None:
            base = key or "figure"
            print(f"Note: no FIGURE_NAMES entry for {key!r}; using {base!r}.")
        name, n = base, 1
        while name in self._used_names:
            n += 1
            name = f"{base}_{n}"
        self._used_names.add(name)
        return name

    def save(self, obj):
        kind = _figure_kind(obj)
        if kind is None or self._suppressed or id(obj) in self._saved_ids:
            return None
        if kind == "matplotlib" and not hasattr(obj, "savefig"):
            obj = obj.figure  # an Axes, e.g. from DataFrame.plot()
        self._saved_ids.add(id(obj))
        self._keep_alive.append(obj)

        key = self._origins.get(id(obj), self.current_key)
        name = self._file_name(key)
        self.figure_dir.mkdir(parents=True, exist_ok=True)
        path = _SAVERS[kind](obj, self.figure_dir, name, self.figure_format)
        self.saved.append(path)
        print(f"Saved figure: {path}")
        return path

    def flush_matplotlib(self):
        """Save open matplotlib figures, as Jupyter shows them at a cell's end."""
        if "matplotlib.pyplot" not in sys.modules:
            return
        import matplotlib.pyplot as plt

        for number in plt.get_fignums():
            figure = plt.figure(number)
            self.save(figure)
            plt.close(figure)


def _save_plotly(fig, directory, name, figure_format):
    path = directory / f"{name}.{figure_format}"
    if figure_format == "html":
        fig.write_html(path, include_plotlyjs="cdn")
    else:
        fig.write_image(path)  # needs the kaleido package
    return path


def _save_bokeh(fig, directory, name, figure_format):
    import bokeh.io
    from bokeh.resources import CDN

    if figure_format in ("png", "svg"):
        path = directory / f"{name}.{figure_format}"
        export = bokeh.io.export_png if figure_format == "png" else bokeh.io.export_svg
        try:
            export(fig, filename=str(path))
            return path
        except Exception as exc:  # needs selenium and a browser driver
            warnings.warn(
                f"Could not export bokeh figure {name!r} as {figure_format} "
                f"({exc}); saving it as html instead."
            )
    elif figure_format != "html":
        warnings.warn(
            f"Bokeh figures cannot be saved as {figure_format}; "
            f"saving {name!r} as html instead."
        )
    path = directory / f"{name}.html"
    bokeh.io.save(fig, filename=str(path), resources=CDN, title=name)
    return path


def _save_matplotlib(fig, directory, name, figure_format):
    import matplotlib.pyplot as plt

    # Matplotlib has no html output; png is the closest static equivalent.
    suffix = "png" if figure_format == "html" else figure_format
    path = directory / f"{name}.{suffix}"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def _save_igv(browser, directory, name, figure_format):
    if figure_format != "html":
        warnings.warn(f"IGV views can only be saved as html; saving {name!r} as html.")
    path = directory / f"{name}.html"
    browser.path = path
    _write_igv_html(browser, path)
    return path


_SAVERS = {
    "plotly": _save_plotly,
    "bokeh": _save_bokeh,
    "matplotlib": _save_matplotlib,
    "igv": _save_igv,
}


def _install_display_hooks():
    """Route every way the notebooks show a figure to the active FigureSaver."""
    global _display_hooks_installed
    if _display_hooks_installed:
        return
    _display_hooks_installed = True

    def saving(original):
        def show(obj=None, *args, **kwargs):
            if _active_saver is None:
                return original(obj, *args, **kwargs)
            _active_saver.save(obj)

        return show

    try:
        import plotly.basedatatypes
        import plotly.io

        plotly.basedatatypes.BaseFigure.show = saving(plotly.basedatatypes.BaseFigure.show)
        plotly.io.show = saving(plotly.io.show)
    except ImportError:
        pass

    try:
        import bokeh.io
        import bokeh.io.showing
        import bokeh.plotting

        show = saving(bokeh.io.showing.show)
        bokeh.io.show = bokeh.io.showing.show = bokeh.plotting.show = show
        # malariagen_data turns on notebook output by default; there is no
        # notebook here, and figures are saved rather than shown.
        bokeh.io.output_notebook = lambda *args, **kwargs: None
    except ImportError:
        pass

    try:
        import matplotlib.pyplot as plt

        original_show = plt.show

        def plt_show(*args, **kwargs):
            if _active_saver is None:
                return original_show(*args, **kwargs)
            _active_saver.flush_matplotlib()

        plt.show = plt_show
    except ImportError:
        pass

    try:
        import igv_notebook

        igv_notebook.init = lambda *args, **kwargs: None
        igv_notebook.Browser = IgvBrowser
    except ImportError:
        pass


# ---------------------------------------------------------------------------
# Functions called from the converted notebook code
# ---------------------------------------------------------------------------


def start_cell(cell_key):
    """Mark the start of a notebook cell; figures it shows default to its key."""
    if _active_saver is not None:
        _active_saver.flush_matplotlib()
        _active_saver.cell_key = cell_key


def track_api_calls(call_api_with_parameters):
    """Wrap the notebook's _call_api_with_parameters helper so that figures
    shown or returned by an API call are named after that call's key."""

    def wrapper(method, call_key, *args, **kwargs):
        if _active_saver is None:
            return call_api_with_parameters(method, call_key, *args, **kwargs)
        with _active_saver.call_context(call_key):
            result = call_api_with_parameters(method, call_key, *args, **kwargs)
        _active_saver.tag(result, call_key)
        return result

    return wrapper


def display(obj):
    """Show the value of a cell's last expression: save it if it is a figure,
    otherwise print it."""
    if obj is None:
        return
    if _figure_kind(obj) is not None:
        if _active_saver is not None:
            _active_saver.save(obj)
        return
    print(repr(obj))


def shell(command):
    """Run a `!command` shell line."""
    sys.stdout.flush()  # keep output in order with the command's
    completed = subprocess.run(command, shell=True)
    if completed.returncode:
        print(f"Command exited with status {completed.returncode}: {command}")


@contextlib.contextmanager
def _figures_suppressed():
    if _active_saver is not None:
        _active_saver._suppressed += 1
    try:
        yield
    finally:
        if _active_saver is not None:
            _active_saver._suppressed -= 1


def _format_seconds(seconds):
    for unit, scale in (("s", 1), ("ms", 1e-3), ("µs", 1e-6)):
        if seconds >= scale:
            return f"{seconds / scale:.3g} {unit}"
    return f"{seconds / 1e-9:.3g} ns"


def timeit(statement, repeat=7):
    """Equivalent of `%timeit statement`. Figures are not saved while timing."""
    with _figures_suppressed():
        timer = _timeit.Timer(statement)
        number, _ = timer.autorange()
        per_loop = [t / number for t in timer.repeat(repeat=repeat, number=number)]
    mean = statistics.mean(per_loop)
    std = statistics.stdev(per_loop) if len(per_loop) > 1 else 0.0
    print(
        f"{_format_seconds(mean)} ± {_format_seconds(std)} per loop "
        f"(mean ± std. dev. of {repeat} runs, {number} loops each)"
    )


def memit(statement):
    """Equivalent of `%memit statement`. Figures are not saved while measuring."""
    from memory_profiler import memory_usage

    baseline = memory_usage(-1, interval=0.1, timeout=0.5)[0]
    with _figures_suppressed():
        peak = memory_usage((statement, (), {}), interval=0.1, max_usage=True)
    if isinstance(peak, (list, tuple)):
        peak = max(peak)
    print(f"peak memory: {peak:.2f} MiB, increment: {peak - baseline:.2f} MiB")


def time_cell_start():
    """Start timing a `%%time` cell."""
    return time.perf_counter(), time.process_time()


def time_cell_report(start):
    """Report the time taken by a `%%time` cell."""
    wall_start, cpu_start = start
    print(
        f"CPU time: {_format_seconds(time.process_time() - cpu_start)}, "
        f"Wall time: {_format_seconds(time.perf_counter() - wall_start)}"
    )


# ---------------------------------------------------------------------------
# Command line and CSV configuration
# ---------------------------------------------------------------------------


def _parse_csv_value(value):
    value = value.strip()
    if not value:
        return OMIT
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _read_config(config_path, parameter_names):
    """Return one dict of parameter overrides per CSV row."""
    with config_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        if not columns:
            raise ValueError(f"{config_path} is missing a CSV header.")
        if len(columns) != len(set(columns)):
            raise ValueError(f"{config_path} contains duplicate column names.")
        unknown = set(columns) - set(parameter_names)
        if unknown:
            raise ValueError(
                f"Unknown parameters in {config_path}: {', '.join(sorted(unknown))}. "
                f"Valid parameters: {', '.join(parameter_names)}"
            )
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row:
                raise ValueError(
                    f"Line {line_number} of {config_path} has more values than "
                    "there are CSV columns."
                )
            overrides = {}
            for name, value in row.items():
                parsed = OMIT if value is None else _parse_csv_value(value)
                if parsed is not OMIT:
                    overrides[name] = parsed
            rows.append(overrides)
    if not rows:
        raise ValueError(f"No configurations found in {config_path}.")
    return rows


def _merge_parameters(defaults, overrides):
    """Apply overrides to defaults.

    Dictionary parameters (API_CALL_PARAMETERS, FIGURE_NAMES) are merged rather
    than replaced, so a CSV only needs to give the entries it changes; for
    API_CALL_PARAMETERS each call's arguments are merged too.
    """
    merged = deepcopy(defaults)
    for name, value in overrides.items():
        default = merged[name]
        if not isinstance(default, dict):
            merged[name] = value
            continue
        if not isinstance(value, dict):
            raise ValueError(
                f"{name} must be a JSON object, e.g. {{\"key\": \"value\"}}; "
                f"got {value!r}. In a CSV, double any quotes inside a quoted cell."
            )
        if name in STRICT_KEY_PARAMETERS:
            unknown = set(value) - set(default)
            if unknown:
                raise ValueError(
                    f"{name} has no entries for {', '.join(sorted(unknown))}. "
                    "Use --list-parameters to see the valid keys."
                )
        for key, item in value.items():
            if isinstance(default.get(key), dict) and isinstance(item, dict):
                default[key] = {**default[key], **item}
            else:
                default[key] = item
    return merged


def _print_parameters(parameters):
    for name, value in parameters.items():
        print(f"{name} = {json.dumps(value, indent=2, default=repr)}\n")


def main(*, notebook, run, parameters):
    """Run a converted notebook from the command line."""
    parser = argparse.ArgumentParser(
        description=(
            f"Run the code from {notebook}, saving figures instead of showing "
            "them. With --config, run once per CSV row; each column is a "
            "parameter name and each value is JSON (or a plain string). Empty "
            "cells keep the default."
        )
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="CSV of parameter overrides, one run per row.",
    )
    parser.add_argument(
        "--workdir",
        type=Path,
        default=DEFAULT_WORKDIR,
        help=(
            "Directory to run in, so relative paths in the notebook code "
            f"resolve as they did in Jupyter (default: {DEFAULT_WORKDIR})."
        ),
    )
    parser.add_argument(
        "--list-parameters",
        action="store_true",
        help="Print the parameters a CSV can set, with their defaults, and exit.",
    )
    args = parser.parse_args()

    if args.list_parameters:
        _print_parameters(parameters)
        return

    if args.config is None:
        runs = [{}]
    else:
        runs = _read_config(args.config.resolve(), list(parameters))

    invocation_dir = Path.cwd()
    workdir = args.workdir.resolve()
    failures = []
    for index, overrides in enumerate(runs, start=1):
        label = f"run {index}/{len(runs)}"
        try:
            settings = _merge_parameters(parameters, overrides)
            figure_format = str(settings["FIGURE_FORMAT"]).lower().lstrip(".")
            if figure_format not in FIGURE_FORMATS:
                raise ValueError(
                    f"FIGURE_FORMAT must be one of {', '.join(FIGURE_FORMATS)}; "
                    f"got {settings['FIGURE_FORMAT']!r}."
                )
            figure_dir = invocation_dir / settings["FIGURE_DIR"]
            if len(runs) > 1:
                figure_dir = figure_dir / f"run_{index:03d}"
            notebook_parameters = {
                name: value
                for name, value in settings.items()
                if name not in FIGURE_PARAMETERS
            }
            print(f"[{label}] {notebook}; figures -> {figure_dir}")
            if overrides:
                print(f"[{label}] overrides: {', '.join(overrides)}")
            saver = FigureSaver(figure_dir, figure_format, settings["FIGURE_NAMES"])
            _run_once(run, notebook_parameters, saver, workdir)
            print(f"[{label}] done; saved {len(saver.saved)} figure(s).")
        except Exception:
            traceback.print_exc()
            print(f"[{label}] FAILED")
            failures.append(index)

    if failures:
        print(f"{len(failures)} of {len(runs)} run(s) failed: {failures}")
        sys.exit(1)


def _run_once(run, notebook_parameters, saver, workdir):
    global _active_saver

    _install_display_hooks()
    original_dir = Path.cwd()
    os.chdir(workdir)
    # Jupyter puts the notebook's directory on the import path.
    sys.path.insert(0, str(workdir))
    _active_saver = saver
    try:
        run(**notebook_parameters)
        saver.flush_matplotlib()
    finally:
        _active_saver = None
        sys.path.remove(str(workdir))
        os.chdir(original_dir)
