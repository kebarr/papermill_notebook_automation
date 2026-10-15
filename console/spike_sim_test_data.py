# spike_sim_test_data: the code from notebooks/spike_sim_test_data.ipynb, to paste into a Python console.
#
# Paste the whole file. It runs once with the notebook's default parameters,
# saving figures to FIGURE_DIR instead of displaying them; other cell outputs
# are printed. Relative paths, in the settings below and in the notebook code
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


def begin_console_run(figure_dir, figure_format, figure_names):
    """Start saving figures for notebook code pasted into a console.

    Used by the files in console/, which have no command line; relative paths
    are resolved against the console's current directory.
    """
    global _active_saver
    _install_display_hooks()
    _active_saver = FigureSaver(
        Path(figure_dir).resolve(), _check_figure_format(figure_format), figure_names
    )
    print(f"Running in {Path.cwd()}; figures -> {_active_saver.figure_dir}")


def end_console_run():
    """Save any open matplotlib figures and stop saving figures."""
    global _active_saver
    if _active_saver is None:
        return
    _active_saver.flush_matplotlib()
    print(f"Done; saved {len(_active_saver.saved)} figure(s) to {_active_saver.figure_dir}.")
    _active_saver = None


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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_biallelic_snps_performance.csv'
API_CALL_PARAMETERS = {'cell_7_call_1_ag3_snp_calls': {'region': '3L',
                                 'sample_sets': 'AG1000G-BF-A',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': None,
                                 'site_class': None,
                                 'inline_array': True,
                                 'chunks': 'native',
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42},
 'cell_8_call_1_ag3_haplotypes': {'region': '3L',
                                  'analysis': 'gamb_colu_arab',
                                  'sample_sets': 'AG1000G-BF-A',
                                  'sample_query': None,
                                  'sample_query_options': None,
                                  'inline_array': True,
                                  'chunks': 'native',
                                  'cohort_size': None,
                                  'min_cohort_size': None,
                                  'max_cohort_size': None,
                                  'random_seed': 42},
 'cell_10_call_1_ag3_haplotypes': {'region': '3L',
                                   'analysis': 'gamb_colu',
                                   'sample_sets': 'AG1000G-BF-A',
                                   'sample_query': None,
                                   'sample_query_options': None,
                                   'inline_array': True,
                                   'chunks': 'native',
                                   'cohort_size': None,
                                   'min_cohort_size': None,
                                   'max_cohort_size': None,
                                   'random_seed': 42},
 'cell_11_call_1_ag3_haplotypes': {'region': '3L',
                                   'analysis': 'arab',
                                   'sample_sets': 'AG1000G-UG',
                                   'sample_query': None,
                                   'sample_query_options': None,
                                   'inline_array': True,
                                   'chunks': 'native',
                                   'cohort_size': None,
                                   'min_cohort_size': None,
                                   'max_cohort_size': None,
                                   'random_seed': 42},
 'cell_22_call_1_ag3_haplotypes': {'region': '3L',
                                   'analysis': 'gamb_colu_arab',
                                   'sample_sets': 'AG1000G-BF-A',
                                   'sample_query': None,
                                   'sample_query_options': None,
                                   'inline_array': True,
                                   'chunks': 'native',
                                   'cohort_size': None,
                                   'min_cohort_size': None,
                                   'max_cohort_size': None,
                                   'random_seed': 42},
 'cell_23_call_1_ag3_haplotypes': {'region': '3L',
                                   'analysis': 'gamb_colu',
                                   'sample_sets': 'AG1000G-BF-A',
                                   'sample_query': None,
                                   'sample_query_options': None,
                                   'inline_array': True,
                                   'chunks': 'native',
                                   'cohort_size': None,
                                   'min_cohort_size': None,
                                   'max_cohort_size': None,
                                   'random_seed': 42},
 'cell_24_call_1_ag3_haplotypes': {'region': '3L',
                                   'analysis': 'arab',
                                   'sample_sets': 'AG1000G-UG',
                                   'sample_query': None,
                                   'sample_query_options': None,
                                   'inline_array': True,
                                   'chunks': 'native',
                                   'cohort_size': None,
                                   'min_cohort_size': None,
                                   'max_cohort_size': None,
                                   'random_seed': 42},
 'cell_28_call_1_ag3_open_site_annotations': {},
 'cell_45_call_1_ag3_snp_calls': {'region': '3L',
                                  'sample_sets': 'AG1000G-BF-A',
                                  'sample_query': None,
                                  'sample_query_options': None,
                                  'sample_indices': None,
                                  'site_mask': None,
                                  'site_class': None,
                                  'inline_array': True,
                                  'chunks': 'native',
                                  'cohort_size': None,
                                  'min_cohort_size': None,
                                  'max_cohort_size': None,
                                  'random_seed': 42},
 'cell_101_call_1_ag3_genome_sequence': {'region': '3L', 'inline_array': True, 'chunks': 'native'},
 'cell_105_call_1_af1_site_filters': {'region': '3RL:10,000,000-11,000,000',
                                      'mask': 'funestus',
                                      'field': 'filter_pass',
                                      'inline_array': True,
                                      'chunks': 'native'},
 'cell_107_call_1_af1_genome_sequence': {'region': '3RL', 'inline_array': True, 'chunks': 'native'},
 'cell_116_call_1_af1_sample_sets': {'release': None},
 'cell_117_call_1_af1_snp_calls': {'region': '3RL:10_000_000-10_500_000',
                                   'sample_sets': '1230-VO-GA-CF-AYALA-VMF00045',
                                   'sample_query': None,
                                   'sample_query_options': None,
                                   'sample_indices': None,
                                   'site_mask': None,
                                   'site_class': None,
                                   'inline_array': True,
                                   'chunks': 'native',
                                   'cohort_size': None,
                                   'min_cohort_size': None,
                                   'max_cohort_size': None,
                                   'random_seed': 42}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in.
FIGURE_DIR = 'figures/spike_sim_test_data'

# One of "html" (interactive), "png", "svg" or "pdf"; see scripts/spike_sim_test_data.py.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it.
FIGURE_NAMES = {'notebook_cell_32': '01_histogram_codon_degeneracy',
 'notebook_cell_34': '02_histogram_codon_nonsyn',
 'notebook_cell_36': '03_histogram_codon_position',
 'notebook_cell_38': '04_histogram_seq_cls',
 'notebook_cell_40': '05_histogram_seq_flen',
 'notebook_cell_41': '06_histogram_seq_relpos_start',
 'notebook_cell_42': '07_histogram_seq_relpos_stop',
 'notebook_cell_43': '08_histogram_x',
 'notebook_cell_69': '09_cell_69_figure',
 'notebook_cell_72': '10_bar_p_gq',
 'notebook_cell_75': '11_cell_75_figure',
 'notebook_cell_77': '12_bar_p_mq',
 'notebook_cell_82': '13_cell_82_figure',
 'notebook_cell_83': '14_cell_83_figure',
 'notebook_cell_84': '15_cell_84_figure',
 'notebook_cell_87': '16_bar_p_ad0',
 'notebook_cell_88': '17_bar_p_ad1',
 'notebook_cell_89': '18_bar_p_ad2',
 'notebook_cell_90': '19_bar_p_ad3',
 'notebook_cell_93': '20_cell_93_figure',
 'notebook_cell_112': '21_bar_p_ad0'}

nbrt.begin_console_run(FIGURE_DIR, FIGURE_FORMAT, FIGURE_NAMES)

# --- Notebook cell 1 ---
nbrt.start_cell("notebook_cell_1")
import inspect
from memory_profiler import memory_usage


def _call_api_with_parameters(method, call_key, *args, **kwargs):
    signature = inspect.signature(method)
    bound = signature.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    for name, value in API_CALL_PARAMETERS[call_key].items():
        if not (isinstance(value, str) and value == API_KEEP_CALLSITE_VALUE):
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
    return method(*positional, **keyword)

# Name figures after the API call that produced them.
_call_api_with_parameters = nbrt.track_api_calls(_call_api_with_parameters)

# # Explore real data to help with simulating test data

# --- Notebook cell 3 ---
nbrt.start_cell("notebook_cell_3")
import malariagen_data
import allel
import numpy as np
import plotly.express as px
import plotly.io as pio

# --- Notebook cell 4 ---
nbrt.start_cell("notebook_cell_4")
pio.templates.default = "plotly_dark"

# --- Notebook cell 5 ---
nbrt.start_cell("notebook_cell_5")
ag3 = malariagen_data.Ag3(
    "simplecache::gs://vo_agam_release_master_us_central1",
    simplecache=dict(cache_storage="../gcs_cache"),
)
nbrt.display(ag3)

# --- Notebook cell 6 ---
nbrt.start_cell("notebook_cell_6")
af1 = malariagen_data.Af1(
    "simplecache::gs://vo_afun_release_master_us_central1",
    simplecache=dict(cache_storage="../gcs_cache"),
)
nbrt.display(af1)

# ## Haplotypes

# --- Notebook cell 8 ---
nbrt.start_cell("notebook_cell_8")
ds_snps = _call_api_with_parameters(ag3.snp_calls, 'cell_7_call_1_ag3_snp_calls', region="3L", sample_sets="AG1000G-BF-A")
nbrt.display(ds_snps)

# --- Notebook cell 9 ---
nbrt.start_cell("notebook_cell_9")
ds_haps = _call_api_with_parameters(ag3.haplotypes, 'cell_8_call_1_ag3_haplotypes', region="3L", sample_sets="AG1000G-BF-A", analysis="gamb_colu_arab")
nbrt.display(ds_haps)

# --- Notebook cell 10 ---
nbrt.start_cell("notebook_cell_10")
nbrt.display(ds_haps.sizes["variants"] / ds_snps.sizes["variants"])

# --- Notebook cell 11 ---
nbrt.start_cell("notebook_cell_11")
ds_haps = _call_api_with_parameters(ag3.haplotypes, 'cell_10_call_1_ag3_haplotypes', region="3L", sample_sets="AG1000G-BF-A", analysis="gamb_colu")
nbrt.display(ds_haps.sizes["variants"] / ds_snps.sizes["variants"])

# --- Notebook cell 12 ---
nbrt.start_cell("notebook_cell_12")
ds_haps = _call_api_with_parameters(ag3.haplotypes, 'cell_11_call_1_ag3_haplotypes', region="3L", sample_sets="AG1000G-UG", analysis="arab")
nbrt.display(ds_haps.sizes["variants"] / ds_snps.sizes["variants"])

# --- Notebook cell 13 ---
nbrt.start_cell("notebook_cell_13")
snp_alleles = ds_snps["variant_allele"].values
nbrt.display(snp_alleles)

# --- Notebook cell 14 ---
nbrt.start_cell("notebook_cell_14")
snp_pos = ds_snps["variant_position"].values
nbrt.display(snp_pos)

# --- Notebook cell 15 ---
nbrt.start_cell("notebook_cell_15")
loc_hap_sites = np.random.choice([False, True], size=snp_pos.shape[0], p=[0.75, 0.25])
nbrt.display(loc_hap_sites)

# --- Notebook cell 16 ---
nbrt.start_cell("notebook_cell_16")
n_hap_sites = np.sum(loc_hap_sites)
nbrt.display(n_hap_sites)

# --- Notebook cell 17 ---
nbrt.start_cell("notebook_cell_17")
sim_hap_ref = snp_alleles[loc_hap_sites, 0]
nbrt.display(sim_hap_ref)

# --- Notebook cell 18 ---
nbrt.start_cell("notebook_cell_18")
nbrt.display(np.arange(1, 4))

# --- Notebook cell 19 ---
nbrt.start_cell("notebook_cell_19")
sim_alt_choice = np.random.choice(np.arange(1, 4), size=n_hap_sites)
nbrt.display(sim_alt_choice)

# --- Notebook cell 20 ---
nbrt.start_cell("notebook_cell_20")
sim_hap_alt = np.take_along_axis(
    snp_alleles[loc_hap_sites], indices=sim_alt_choice[:, None], axis=1
)[:, 0]
nbrt.display(sim_hap_alt)

# --- Notebook cell 21 ---
nbrt.start_cell("notebook_cell_21")
nbrt.display(sim_hap_alt.shape)

# --- Notebook cell 22 ---
nbrt.start_cell("notebook_cell_22")
nbrt.display(ds_haps)

# --- Notebook cell 23 ---
nbrt.start_cell("notebook_cell_23")
ds_haps = _call_api_with_parameters(ag3.haplotypes, 'cell_22_call_1_ag3_haplotypes', region="3L", sample_sets="AG1000G-BF-A", analysis="gamb_colu_arab")
gt = ds_haps["call_genotype"][:1_000_000].values
p_hap_01 = np.bincount(gt.flatten())
p_hap_01 = p_hap_01 / p_hap_01.sum()
nbrt.display(p_hap_01)

# --- Notebook cell 24 ---
nbrt.start_cell("notebook_cell_24")
ds_haps = _call_api_with_parameters(ag3.haplotypes, 'cell_23_call_1_ag3_haplotypes', region="3L", sample_sets="AG1000G-BF-A", analysis="gamb_colu")
gt = ds_haps["call_genotype"][:1_000_000].values
p_hap_01 = np.bincount(gt.flatten())
p_hap_01 = p_hap_01 / p_hap_01.sum()
nbrt.display(p_hap_01)

# --- Notebook cell 25 ---
nbrt.start_cell("notebook_cell_25")
ds_haps = _call_api_with_parameters(ag3.haplotypes, 'cell_24_call_1_ag3_haplotypes', region="3L", sample_sets="AG1000G-UG", analysis="arab")
gt = ds_haps["call_genotype"][:1_000_000].values
p_hap_01 = np.bincount(gt.flatten())
p_hap_01 = p_hap_01 / p_hap_01.sum()
nbrt.display(p_hap_01)

# --- Notebook cell 26 ---
nbrt.start_cell("notebook_cell_26")
hap_gt_sim = np.random.choice(
    [0, 1], size=(100_000, 100), replace=True, p=p_hap_01
).astype("i1")
nbrt.display(hap_gt_sim)

# --- Notebook cell 27 ---
nbrt.start_cell("notebook_cell_27")
nbrt.display(np.bincount(hap_gt_sim.flatten()))

# ## Site annotations

# --- Notebook cell 29 ---
nbrt.start_cell("notebook_cell_29")
ann = _call_api_with_parameters(ag3.open_site_annotations, 'cell_28_call_1_ag3_open_site_annotations')
nbrt.display(ann)

# --- Notebook cell 30 ---
nbrt.start_cell("notebook_cell_30")
nbrt.display(list(ann))

# --- Notebook cell 31 ---
nbrt.start_cell("notebook_cell_31")
nbrt.display(print(ann.tree()))

# --- Notebook cell 32 ---
nbrt.start_cell("notebook_cell_32")
codon_degeneracy = ann["codon_degeneracy"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(codon_degeneracy))

# --- Notebook cell 33 ---
nbrt.start_cell("notebook_cell_33")
nbrt.display(np.bincount(codon_degeneracy + 1) / codon_degeneracy.size)

# --- Notebook cell 34 ---
nbrt.start_cell("notebook_cell_34")
codon_nonsyn = ann["codon_nonsyn"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(codon_nonsyn))

# --- Notebook cell 35 ---
nbrt.start_cell("notebook_cell_35")
nbrt.display(np.bincount(codon_nonsyn) / codon_nonsyn.size)

# --- Notebook cell 36 ---
nbrt.start_cell("notebook_cell_36")
codon_position = ann["codon_position"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(codon_position))

# --- Notebook cell 37 ---
nbrt.start_cell("notebook_cell_37")
nbrt.display(np.bincount(codon_position + 1) / codon_position.size)

# --- Notebook cell 38 ---
nbrt.start_cell("notebook_cell_38")
seq_cls = ann["seq_cls"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(seq_cls))

# --- Notebook cell 39 ---
nbrt.start_cell("notebook_cell_39")
nbrt.display(np.bincount(seq_cls) / seq_cls.size)

# --- Notebook cell 40 ---
nbrt.start_cell("notebook_cell_40")
seq_flen = ann["seq_flen"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(seq_flen, nbins=20))

# --- Notebook cell 41 ---
nbrt.start_cell("notebook_cell_41")
seq_relpos_start = ann["seq_relpos_start"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(seq_relpos_start, nbins=20))

# --- Notebook cell 42 ---
nbrt.start_cell("notebook_cell_42")
seq_relpos_stop = ann["seq_relpos_stop"]["3L"][10_000_000:11_000_000]
nbrt.display(px.histogram(seq_relpos_stop, nbins=20))

# --- Notebook cell 43 ---
nbrt.start_cell("notebook_cell_43")
x = np.random.beta(a=0.4, b=4, size=100_000) * 40_000
nbrt.display(px.histogram(x, nbins=20))

# --- Notebook cell 44 ---
nbrt.start_cell("notebook_cell_44")
nbrt.display(list(ann))

# ## SNP calls

# --- Notebook cell 46 ---
nbrt.start_cell("notebook_cell_46")
ds = _call_api_with_parameters(ag3.snp_calls, 'cell_45_call_1_ag3_snp_calls', region="3L", sample_sets="AG1000G-BF-A")
nbrt.display(ds)

# --- Notebook cell 47 ---
nbrt.start_cell("notebook_cell_47")
ds2 = ds.isel(variants=slice(10_500_000, 10_600_000))
nbrt.display(ds2)

# --- Notebook cell 48 ---
nbrt.start_cell("notebook_cell_48")
gt = ds2["call_genotype"].values
nbrt.display(gt)

# --- Notebook cell 49 ---
nbrt.start_cell("notebook_cell_49")
gt2 = allel.GenotypeArray(gt)
nbrt.display(gt2)

# --- Notebook cell 50 ---
nbrt.start_cell("notebook_cell_50")
nbrt.display(np.bincount(gt.flatten() + 1) / gt.size)

# --- Notebook cell 51 ---
nbrt.start_cell("notebook_cell_51")
missing_fraction = gt2.count_missing() / (gt2.n_variants * gt2.n_samples)
nbrt.display(missing_fraction)

# --- Notebook cell 52 ---
nbrt.start_cell("notebook_cell_52")
allele_counts = np.bincount(gt.flatten() + 1)[1:]
nbrt.display(allele_counts)

# --- Notebook cell 53 ---
nbrt.start_cell("notebook_cell_53")
allele_fractions = allele_counts / np.sum(allele_counts)
nbrt.display(allele_fractions)

# --- Notebook cell 54 ---
nbrt.start_cell("notebook_cell_54")
gt_sim = np.random.choice(4, size=gt.shape, replace=True, p=allele_fractions)
nbrt.display(gt_sim)

# --- Notebook cell 55 ---
nbrt.start_cell("notebook_cell_55")
n_calls = gt_sim.shape[0] * gt_sim.shape[1]
nbrt.display(n_calls)

# --- Notebook cell 56 ---
nbrt.start_cell("notebook_cell_56")
gt_sim_flat = gt_sim.reshape(-1, 2)
nbrt.display(gt_sim_flat)

# --- Notebook cell 57 ---
nbrt.start_cell("notebook_cell_57")
loc_missing = np.random.choice(
    n_calls,
    size=int(missing_fraction * n_calls),
    replace=False,
)
nbrt.display(loc_missing)

# --- Notebook cell 58 ---
nbrt.start_cell("notebook_cell_58")
gt_sim_flat[loc_missing] = -1

# --- Notebook cell 59 ---
nbrt.start_cell("notebook_cell_59")
nbrt.display(gt_sim)

# --- Notebook cell 60 ---
nbrt.start_cell("notebook_cell_60")
nbrt.display(np.bincount(gt_sim.flatten() + 1) / gt_sim.size)

# --- Notebook cell 61 ---
nbrt.start_cell("notebook_cell_61")
nbrt.display(np.bincount(gt.flatten() + 1) / gt.size)

# --- Notebook cell 62 ---
nbrt.start_cell("notebook_cell_62")
nbrt.display(allel.GenotypeArray(gt).count_missing())

# --- Notebook cell 63 ---
nbrt.start_cell("notebook_cell_63")
nbrt.display(allel.GenotypeArray(gt_sim).count_missing())

# --- Notebook cell 64 ---
nbrt.start_cell("notebook_cell_64")
nbrt.display(allel.GenotypeArray(gt).count_hom_ref())

# --- Notebook cell 65 ---
nbrt.start_cell("notebook_cell_65")
nbrt.display(allel.GenotypeArray(gt_sim).count_hom_ref())

# --- Notebook cell 66 ---
nbrt.start_cell("notebook_cell_66")
nbrt.display(allel.GenotypeArray(gt).count_hom_alt())

# --- Notebook cell 67 ---
nbrt.start_cell("notebook_cell_67")
nbrt.display(allel.GenotypeArray(gt_sim).count_hom_alt())

# --- Notebook cell 68 ---
nbrt.start_cell("notebook_cell_68")
gq = ds2["call_GQ"].values

# --- Notebook cell 69 ---
nbrt.start_cell("notebook_cell_69")
nbrt.display(px.histogram(gq.flatten()[:100_000]))

# --- Notebook cell 70 ---
nbrt.start_cell("notebook_cell_70")
gqf = gq.flatten()
n_gq = np.bincount(gqf[gqf >= 0])
nbrt.display(n_gq)

# --- Notebook cell 71 ---
nbrt.start_cell("notebook_cell_71")
p_gq = np.bincount(gqf[gqf >= 0]) / gqf.size
nbrt.display(p_gq)

# --- Notebook cell 72 ---
nbrt.start_cell("notebook_cell_72")
nbrt.display(px.bar(p_gq))

# --- Notebook cell 73 ---
nbrt.start_cell("notebook_cell_73")
mq = ds2["call_MQ"].values
nbrt.display(mq)

# --- Notebook cell 74 ---
nbrt.start_cell("notebook_cell_74")
mqf = mq.flatten()

# --- Notebook cell 75 ---
nbrt.start_cell("notebook_cell_75")
nbrt.display(px.histogram(mqf[:100_000]))

# --- Notebook cell 76 ---
nbrt.start_cell("notebook_cell_76")
p_mq = np.bincount(mqf[mqf >= 0]) / mqf.size
nbrt.display(p_mq)

# --- Notebook cell 77 ---
nbrt.start_cell("notebook_cell_77")
nbrt.display(px.bar(p_mq))

# --- Notebook cell 78 ---
nbrt.start_cell("notebook_cell_78")
ad = ds2["call_AD"].values
nbrt.display(ad)

# --- Notebook cell 79 ---
nbrt.start_cell("notebook_cell_79")
ad0 = ad[:, :, 0].flatten()
nbrt.display(ad0)

# --- Notebook cell 80 ---
nbrt.start_cell("notebook_cell_80")
ad1 = ad[:, :, 1].flatten()
nbrt.display(ad1)

# --- Notebook cell 81 ---
nbrt.start_cell("notebook_cell_81")
ad2 = ad[:, :, 2].flatten()
ad3 = ad[:, :, 3].flatten()

# --- Notebook cell 82 ---
nbrt.start_cell("notebook_cell_82")
nbrt.display(px.histogram(ad0[:10_000]))

# --- Notebook cell 83 ---
nbrt.start_cell("notebook_cell_83")
nbrt.display(px.histogram(ad1[:10_000]))

# --- Notebook cell 84 ---
nbrt.start_cell("notebook_cell_84")
nbrt.display(px.histogram(ad2[:10_000]))

# --- Notebook cell 87 ---
nbrt.start_cell("notebook_cell_87")
p_ad0 = np.bincount(ad0[ad0 >= 0]) / ad0.size
nbrt.display(px.bar(p_ad0))

# --- Notebook cell 88 ---
nbrt.start_cell("notebook_cell_88")
p_ad1 = np.bincount(ad1[ad1 >= 2]) / ad1.size
nbrt.display(px.bar(p_ad1))

# --- Notebook cell 89 ---
nbrt.start_cell("notebook_cell_89")
p_ad2 = np.bincount(ad2[ad2 >= 2]) / ad1.size
nbrt.display(px.bar(p_ad2))

# --- Notebook cell 90 ---
nbrt.start_cell("notebook_cell_90")
p_ad3 = np.bincount(ad3[ad3 >= 2]) / ad1.size
nbrt.display(px.bar(p_ad3))

# --- Notebook cell 91 ---
nbrt.start_cell("notebook_cell_91")
pos = ds2["variant_position"].values

# --- Notebook cell 92 ---
nbrt.start_cell("notebook_cell_92")
nbrt.display(pos)

# --- Notebook cell 93 ---
nbrt.start_cell("notebook_cell_93")
nbrt.display(px.line(pos[:100_000]))

# --- Notebook cell 94 ---
nbrt.start_cell("notebook_cell_94")
alleles = ds2["variant_allele"].values[:10]
nbrt.display(alleles)

# --- Notebook cell 95 ---
nbrt.start_cell("notebook_cell_95")
ref = alleles[:, 0]

# --- Notebook cell 96 ---
nbrt.start_cell("notebook_cell_96")
alt_sim = np.empty(shape=(alleles.shape[0], alleles.shape[1] - 1), dtype="S1")
alt_sim[ref == b"A"] = np.array([b"C", b"T", b"G"])
alt_sim[ref == b"C"] = np.array([b"A", b"T", b"G"])
alt_sim[ref == b"T"] = np.array([b"A", b"C", b"G"])
alt_sim[ref == b"G"] = np.array([b"A", b"C", b"T"])
nbrt.display(alt_sim)

# --- Notebook cell 97 ---
nbrt.start_cell("notebook_cell_97")
nbrt.display(ds2)

# --- Notebook cell 98 ---
nbrt.start_cell("notebook_cell_98")
pass_gc = ds2["variant_filter_pass_gamb_colu"].values
p_pass_gc = np.sum(pass_gc) / pass_gc.size
nbrt.display(p_pass_gc)

# --- Notebook cell 99 ---
nbrt.start_cell("notebook_cell_99")
pass_a = ds2["variant_filter_pass_arab"].values
p_pass_a = np.sum(pass_a) / pass_a.size
nbrt.display(p_pass_a)

# --- Notebook cell 100 ---
nbrt.start_cell("notebook_cell_100")
pass_gca = ds2["variant_filter_pass_gamb_colu_arab"].values
p_pass_gca = np.sum(pass_gca) / pass_gca.size
nbrt.display(p_pass_gca)

# ## Sequence composition

# --- Notebook cell 102 ---
nbrt.start_cell("notebook_cell_102")
ag_seq = _call_api_with_parameters(ag3.genome_sequence, 'cell_101_call_1_ag3_genome_sequence', "3L").compute()
nbrt.display(ag_seq)

# --- Notebook cell 103 ---
nbrt.start_cell("notebook_cell_103")
from collections import Counter

# --- Notebook cell 104 ---
nbrt.start_cell("notebook_cell_104")
ag_seq_count = Counter(ag_seq)
nbrt.display(ag_seq_count)

# --- Notebook cell 106 ---
nbrt.start_cell("notebook_cell_106")
filter_pass = _call_api_with_parameters(af1.site_filters, 'cell_105_call_1_af1_site_filters', region="3RL:10,000,000-11,000,000", mask="funestus")
nbrt.display(filter_pass)

# --- Notebook cell 107 ---
nbrt.start_cell("notebook_cell_107")
nbrt.display(np.sum(filter_pass).compute() / filter_pass.size)

# --- Notebook cell 108 ---
nbrt.start_cell("notebook_cell_108")
af_seq = _call_api_with_parameters(af1.genome_sequence, 'cell_107_call_1_af1_genome_sequence', "3RL")[:60_000_000].compute()
nbrt.display(af_seq)

# --- Notebook cell 109 ---
nbrt.start_cell("notebook_cell_109")
bases = np.array([b"a", b"c", b"g", b"t", b"n", b"A", b"C", b"G", b"T", b"N"])
nbrt.display(bases)

# --- Notebook cell 110 ---
nbrt.start_cell("notebook_cell_110")
af_seq_count = Counter(af_seq)
nbrt.display(af_seq_count)

# --- Notebook cell 111 ---
nbrt.start_cell("notebook_cell_111")
p_bases_af = {b: af_seq_count[b] / af_seq.size for b in bases}
nbrt.display(p_bases_af)

# --- Notebook cell 112 ---
nbrt.start_cell("notebook_cell_112")
p_ad0 = np.bincount(ad0[ad0 >= 0]) / ad0.size
nbrt.display(px.bar(p_ad0))

# --- Notebook cell 113 ---
nbrt.start_cell("notebook_cell_113")
p_bases_ag = {b: ag_seq_count[b] / ag_seq.size for b in bases}
nbrt.display(p_bases_ag)

# --- Notebook cell 114 ---
nbrt.start_cell("notebook_cell_114")
p_bases_ag = np.array([ag_seq_count[b] for b in bases]) / ag_seq.size
nbrt.display(p_bases_ag)

# --- Notebook cell 115 ---
nbrt.start_cell("notebook_cell_115")
nbrt.display(p_bases_ag.sum())

# --- Notebook cell 116 ---
nbrt.start_cell("notebook_cell_116")
seq_sim = np.random.choice(bases, size=ag_seq.size, replace=True, p=p_bases_ag)
nbrt.display(seq_sim)

# --- Notebook cell 117 ---
nbrt.start_cell("notebook_cell_117")
nbrt.display(_call_api_with_parameters(af1.sample_sets, 'cell_116_call_1_af1_sample_sets'))

# --- Notebook cell 118 ---
nbrt.start_cell("notebook_cell_118")
ds = _call_api_with_parameters(af1.snp_calls, 'cell_117_call_1_af1_snp_calls', region="3RL:10_000_000-10_500_000", sample_sets="1230-VO-GA-CF-AYALA-VMF00045")
nbrt.display(ds)

# --- Notebook cell 119 ---
nbrt.start_cell("notebook_cell_119")
gt = ds["call_genotype"].values
nbrt.display(gt)

# --- Notebook cell 120 ---
nbrt.start_cell("notebook_cell_120")
allele_counts = np.bincount(gt.flatten() + 1)[1:]
nbrt.display(allele_counts)

# --- Notebook cell 121 ---
nbrt.start_cell("notebook_cell_121")
nbrt.display(allele_counts / np.sum(allele_counts))

# --- Notebook cell 122 ---
nbrt.start_cell("notebook_cell_122")
nbrt.display(np.sum(gt < 0) / gt.size)

nbrt.end_console_run()
