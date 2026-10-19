# plot_cnv: the code from notebooks/plot_cnv.ipynb, to paste into a Python console.
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
exec(compile(r'''"""Shared runtime for the scripts converted from the notebooks in ../notebooks.

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

FIGURE_FORMATS = ("html", "png", "svg", "pdf")
FIGURE_PARAMETERS = ("FIGURE_DIR", "FIGURE_FORMAT", "FIGURE_NAMES")
OUTPUT_CSV_SUFFIX = "_CSV_PATH"
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
    tee = _console_tee()
    if tee is not None and tee.log is not None:
        # The command writes straight to the terminal, bypassing sys.stdout;
        # capture its output so the log gets it too.
        completed = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)
        print(completed.stdout, end="")
    else:
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


def _check_figure_format(figure_format):
    checked = str(figure_format).lower().lstrip(".")
    if checked not in FIGURE_FORMATS:
        raise ValueError(
            f"FIGURE_FORMAT must be one of {', '.join(FIGURE_FORMATS)}; "
            f"got {figure_format!r}."
        )
    return checked


class _Tee:
    """Stands in for the console's stdout, copying output to a run's log file.

    Once installed it stays as sys.stdout for the rest of the console session,
    passing output straight through between runs. Libraries can keep a
    reference to whatever sys.stdout was when they were imported:
    malariagen_data uses it as the default log stream of Ag3, Af1 etc. Swapping
    sys.stdout back after a run would leave them writing to a closed log file
    in later runs.
    """

    # Marks the tee across pastes: each console file defines its own _Tee class.
    is_nbrt_tee = True

    def __init__(self, stream):
        self.stream = stream
        self.log = None

    def open_log(self, path):
        self.close_log()
        self.log = path.open("w", encoding="utf-8")

    def close_log(self):
        if self.log is not None:
            self.log.close()
            self.log = None

    def write(self, text):
        if self.log is not None:
            self.log.write(text)
            self.log.flush()  # keep the log current if the run is abandoned
        return self.stream.write(text)

    def flush(self):
        if self.log is not None:
            self.log.flush()
        self.stream.flush()

    def __getattr__(self, name):
        # isatty(), encoding, fileno() etc. come from the console's stdout.
        return getattr(self.stream, name)


def _console_tee():
    """The tee installed as sys.stdout by an earlier console run, or None."""
    return sys.stdout if getattr(sys.stdout, "is_nbrt_tee", False) else None


def begin_console_run(figure_dir, figure_format, figure_names, output_log=None):
    """Start saving figures for notebook code pasted into a console.

    Used by the files in console/, which have no command line; relative paths
    are resolved against the console's current directory. If output_log is
    given, everything printed until end_console_run() is also written there.
    """
    global _active_saver
    if output_log is not None:
        tee = _console_tee()
        if tee is None:
            tee = sys.stdout = _Tee(sys.stdout)
        output_log = Path(output_log).resolve()
        output_log.parent.mkdir(parents=True, exist_ok=True)
        tee.open_log(output_log)
        print(f"Printed output is also written to {output_log}")
    _install_display_hooks()
    _active_saver = FigureSaver(
        Path(figure_dir).resolve(), _check_figure_format(figure_format), figure_names
    )
    print(f"Running in {Path.cwd()}; figures -> {_active_saver.figure_dir}")


def end_console_run():
    """Save any open matplotlib figures, stop saving figures and close the
    output log."""
    global _active_saver
    if _active_saver is None:
        return
    _active_saver.flush_matplotlib()
    print(f"Done; saved {len(_active_saver.saved)} figure(s) to {_active_saver.figure_dir}.")
    _active_saver = None
    tee = _console_tee()
    if tee is not None:
        tee.close_log()


# ---------------------------------------------------------------------------
''', "nbrt", "exec"), nbrt.__dict__)

# ---------------------------------------------------------------------------
# Parameters (the notebook's "parameters" cell)
# ---------------------------------------------------------------------------

# Malariagen API arguments for each call below.
# Replace a value to override it; keep the marker to use the call-site
# value or the method's default.
API_KEEP_CALLSITE_VALUE = '__KEEP_CALLSITE_VALUE__'
# Relative to where the script is run from.
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_cnv_performance.csv'
API_CALL_PARAMETERS = {'cell_6_call_1_ag3_plot_cnv_hmm_coverage_track': {'sample': 'AP0021-C',
                                                   'region': '2R:28,460,000-28,580,000',
                                                   'sample_set': None,
                                                   'y_max': 'auto',
                                                   'sizing_mode': 'stretch_width',
                                                   'width': None,
                                                   'height': 200,
                                                   'circle_kwargs': None,
                                                   'line_kwargs': None,
                                                   'show': True,
                                                   'x_range': None,
                                                   'output_backend': 'webgl'},
 'cell_7_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0091-C',
                                             'region': '2R:28,460,000-28,580,000',
                                             'sample_set': None,
                                             'y_max': 'auto',
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'track_height': 170,
                                             'genes_height': 90,
                                             'circle_kwargs': None,
                                             'line_kwargs': None,
                                             'show': True,
                                             'output_backend': 'webgl',
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_8_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0072-C',
                                             'region': '2R:28,460,000-28,580,000',
                                             'sample_set': None,
                                             'y_max': 'auto',
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'track_height': 170,
                                             'genes_height': 90,
                                             'circle_kwargs': None,
                                             'line_kwargs': None,
                                             'show': True,
                                             'output_backend': 'webgl',
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_9_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0062-C',
                                             'region': '2R:28,460,000-28,580,000',
                                             'sample_set': None,
                                             'y_max': 'auto',
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'track_height': 170,
                                             'genes_height': 90,
                                             'circle_kwargs': None,
                                             'line_kwargs': None,
                                             'show': True,
                                             'output_backend': 'webgl',
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_10_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AY0039-C',
                                              'region': '2R:28,460,000-28,580,000',
                                              'sample_set': None,
                                              'y_max': 'auto',
                                              'sizing_mode': 'stretch_width',
                                              'width': None,
                                              'track_height': 170,
                                              'genes_height': 90,
                                              'circle_kwargs': None,
                                              'line_kwargs': None,
                                              'show': True,
                                              'output_backend': 'webgl',
                                              'gene_labels': None,
                                              'gene_labelset': None},
 'cell_11_call_1_ag3_plot_cnv_hmm_coverage': {'sample': 'AG0382-CW',
                                              'region': '2R:28,460,000-28,580,000',
                                              'sample_set': None,
                                              'y_max': 'auto',
                                              'sizing_mode': 'stretch_width',
                                              'width': None,
                                              'track_height': 170,
                                              'genes_height': 90,
                                              'circle_kwargs': None,
                                              'line_kwargs': None,
                                              'show': True,
                                              'output_backend': 'webgl',
                                              'gene_labels': None,
                                              'gene_labelset': None},
 'cell_13_call_1_af1_plot_cnv_hmm_coverage_track': {'sample': 'VBS24196',
                                                    'region': '2RL:28,460,000-28,580,000',
                                                    'sample_set': None,
                                                    'y_max': 'auto',
                                                    'sizing_mode': 'stretch_width',
                                                    'width': None,
                                                    'height': 200,
                                                    'circle_kwargs': None,
                                                    'line_kwargs': None,
                                                    'show': True,
                                                    'x_range': None,
                                                    'output_backend': 'webgl'},
 'cell_16_call_1_ag3_plot_cnv_hmm_heatmap_track': {'region': '2R:28,460,000-28,580,000',
                                                   'sample_sets': 'AG1000G-FR',
                                                   'sample_query': None,
                                                   'sample_query_options': None,
                                                   'max_coverage_variance': 0.2,
                                                   'sizing_mode': 'stretch_width',
                                                   'width': None,
                                                   'row_height': 7,
                                                   'height': None,
                                                   'palette': None,
                                                   'show': True,
                                                   'output_backend': 'webgl'},
 'cell_17_call_1_ag3_plot_cnv_hmm_heatmap_track': {'region': '2R:28,460,000-28,580,000',
                                                   'sample_sets': ['AG1000G-FR', 'AG1000G-GQ'],
                                                   'sample_query': None,
                                                   'sample_query_options': None,
                                                   'max_coverage_variance': 0.2,
                                                   'sizing_mode': 'stretch_width',
                                                   'width': None,
                                                   'row_height': 7,
                                                   'height': None,
                                                   'palette': None,
                                                   'show': True,
                                                   'output_backend': 'webgl'},
 'cell_18_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-BF-A',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_19_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-BF-A',
                                             'sample_query': "taxon == 'gambiae'",
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_20_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-BF-A',
                                             'sample_query': "taxon == 'coluzzii'",
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_21_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-CI',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': 0.2,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_22_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-CI',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': None,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_23_call_1_ag3_plot_cnv_hmm_heatmap': {'region': '2R:28,460,000-28,580,000',
                                             'sample_sets': 'AG1000G-GM-B',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': None,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None},
 'cell_25_call_1_af1_plot_cnv_hmm_heatmap': {'region': '2RL:28,520,000-28,570,000',
                                             'sample_sets': '1230-VO-GA-CF-AYALA-VMF00045',
                                             'sample_query': None,
                                             'sample_query_options': None,
                                             'max_coverage_variance': None,
                                             'sizing_mode': 'stretch_width',
                                             'width': None,
                                             'row_height': 7,
                                             'track_height': None,
                                             'palette': None,
                                             'genes_height': 90,
                                             'show': True,
                                             'gene_labels': None,
                                             'gene_labelset': None}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in.
FIGURE_DIR = 'figures/plot_cnv'

# One of "html" (interactive), "png", "svg" or "pdf"; see scripts/plot_cnv.py.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it.
FIGURE_NAMES = {'cell_6_call_1_ag3_plot_cnv_hmm_coverage_track': '01_ag3_cnv_hmm_coverage_track_AP0021-C',
 'cell_7_call_1_ag3_plot_cnv_hmm_coverage': '02_ag3_cnv_hmm_coverage_AY0091-C',
 'cell_8_call_1_ag3_plot_cnv_hmm_coverage': '03_ag3_cnv_hmm_coverage_AY0072-C',
 'cell_9_call_1_ag3_plot_cnv_hmm_coverage': '04_ag3_cnv_hmm_coverage_AY0062-C',
 'cell_10_call_1_ag3_plot_cnv_hmm_coverage': '05_ag3_cnv_hmm_coverage_AY0039-C',
 'cell_11_call_1_ag3_plot_cnv_hmm_coverage': '06_ag3_cnv_hmm_coverage_AG0382-CW',
 'cell_13_call_1_af1_plot_cnv_hmm_coverage_track': '07_af1_cnv_hmm_coverage_track_VBS24196',
 'cell_16_call_1_ag3_plot_cnv_hmm_heatmap_track': '08_ag3_cnv_hmm_heatmap_track',
 'cell_17_call_1_ag3_plot_cnv_hmm_heatmap_track': '09_ag3_cnv_hmm_heatmap_track',
 'cell_18_call_1_ag3_plot_cnv_hmm_heatmap': '10_ag3_cnv_hmm_heatmap',
 'cell_19_call_1_ag3_plot_cnv_hmm_heatmap': '11_ag3_cnv_hmm_heatmap',
 'cell_20_call_1_ag3_plot_cnv_hmm_heatmap': '12_ag3_cnv_hmm_heatmap',
 'cell_21_call_1_ag3_plot_cnv_hmm_heatmap': '13_ag3_cnv_hmm_heatmap',
 'cell_22_call_1_ag3_plot_cnv_hmm_heatmap': '14_ag3_cnv_hmm_heatmap',
 'cell_23_call_1_ag3_plot_cnv_hmm_heatmap': '15_ag3_cnv_hmm_heatmap',
 'cell_25_call_1_af1_plot_cnv_hmm_heatmap': '16_af1_cnv_hmm_heatmap'}

# File that printed output is copied to, as well as being shown in the console.
OUTPUT_LOG = 'executed_runs_console/plot_cnv_stdout.txt'

nbrt.begin_console_run(FIGURE_DIR, FIGURE_FORMAT, FIGURE_NAMES, OUTPUT_LOG)

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

# Name figures after the API call that produced them.
_call_api_with_parameters = nbrt.track_api_calls(_call_api_with_parameters)

# --- Notebook cell 2 ---
nbrt.start_cell("notebook_cell_2")
import malariagen_data
import dask

# --- Notebook cell 3 ---
nbrt.start_cell("notebook_cell_3")
ag3 = malariagen_data.Ag3(
    "simplecache::gs://vo_agam_release_master_us_central1",
    simplecache=dict(cache_storage="../gcs_cache"),
)
nbrt.display(ag3)

# --- Notebook cell 4 ---
nbrt.start_cell("notebook_cell_4")
af1 = malariagen_data.Af1(
    "simplecache::gs://vo_afun_release_master_us_central1",
    simplecache=dict(cache_storage="../gcs_cache"),
)
nbrt.display(af1)

# ## CNV HMM coverage

# ### Ag3

# --- Notebook cell 7 ---
nbrt.start_cell("notebook_cell_7")
# sample with no CNV
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage_track, 'cell_6_call_1_ag3_plot_cnv_hmm_coverage_track', sample="AP0021-C", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 8 ---
nbrt.start_cell("notebook_cell_8")
# sample with a small CNV
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_7_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0091-C", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 9 ---
nbrt.start_cell("notebook_cell_9")
# sample with a big CNV
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_8_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0072-C", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 10 ---
nbrt.start_cell("notebook_cell_10")
# sample with a complex CNV
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_9_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0062-C", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 11 ---
nbrt.start_cell("notebook_cell_11")
# sample with a complex CNV
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_10_call_1_ag3_plot_cnv_hmm_coverage', sample="AY0039-C", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 12 ---
nbrt.start_cell("notebook_cell_12")
# sample with high coverage variance
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_coverage, 'cell_11_call_1_ag3_plot_cnv_hmm_coverage', sample="AG0382-CW", region="2R:28,460,000-28,580,000"))

# ### Af1

# --- Notebook cell 14 ---
nbrt.start_cell("notebook_cell_14")
# sample with a small CNV
nbrt.display(_call_api_with_parameters(af1.plot_cnv_hmm_coverage_track, 'cell_13_call_1_af1_plot_cnv_hmm_coverage_track', sample="VBS24196", region="2RL:28,460,000-28,580,000"))

# ## CNV HMM heatmap

# ### Ag3

# --- Notebook cell 17 ---
nbrt.start_cell("notebook_cell_17")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap_track, 'cell_16_call_1_ag3_plot_cnv_hmm_heatmap_track', sample_sets="AG1000G-FR", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 18 ---
nbrt.start_cell("notebook_cell_18")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap_track, 'cell_17_call_1_ag3_plot_cnv_hmm_heatmap_track', sample_sets=["AG1000G-FR", "AG1000G-GQ"], region="2R:28,460,000-28,580,000"))

# --- Notebook cell 19 ---
nbrt.start_cell("notebook_cell_19")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_18_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-BF-A", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 20 ---
nbrt.start_cell("notebook_cell_20")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_19_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-BF-A", sample_query="taxon == 'gambiae'", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 21 ---
nbrt.start_cell("notebook_cell_21")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_20_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-BF-A", sample_query="taxon == 'coluzzii'", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 22 ---
nbrt.start_cell("notebook_cell_22")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_21_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-CI", region="2R:28,460,000-28,580,000"))

# --- Notebook cell 23 ---
nbrt.start_cell("notebook_cell_23")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_22_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-CI", region="2R:28,460,000-28,580,000", max_coverage_variance=None))

# --- Notebook cell 24 ---
nbrt.start_cell("notebook_cell_24")
nbrt.display(_call_api_with_parameters(ag3.plot_cnv_hmm_heatmap, 'cell_23_call_1_ag3_plot_cnv_hmm_heatmap', sample_sets="AG1000G-GM-B", region="2R:28,460,000-28,580,000", max_coverage_variance=None))

# ### Af1

# --- Notebook cell 26 ---
nbrt.start_cell("notebook_cell_26")
nbrt.display(_call_api_with_parameters(af1.plot_cnv_hmm_heatmap, 'cell_25_call_1_af1_plot_cnv_hmm_heatmap', sample_sets="1230-VO-GA-CF-AYALA-VMF00045", region="2RL:28,520,000-28,570,000", max_coverage_variance=None))

nbrt.end_console_run()
