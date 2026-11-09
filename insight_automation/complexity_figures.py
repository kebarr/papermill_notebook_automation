#!/usr/bin/env python3
"""Write one standalone SVG figure per results CSV, for use in documents.

The same results as complexity_report.py, one file per figure: the method
called, run time and peak memory for each value of the varied argument, and
(optionally) the arguments that stayed fixed. File paths are left out.

A CSV that recorded calls to more than one method (e.g. njt and plot_njt)
gets one figure per method.

Examples:
    python complexity_figures.py                      # results/ -> figures/
    python complexity_figures.py results -o figures --fixed none
    python complexity_figures.py results/plot_njt_region.csv --fixed all
"""

import argparse
import collections
import html
import re
from pathlib import Path

from complexity_report import (
    HEADLINE, LABELS, SCRIPT_DIR, _dump, _fmt_mib, _fmt_seconds, _load, _nice_ticks,
    _tick_label, _value_label, _varied, _wrap,
)

# Fixed arguments worth stating in "main" mode, beyond the report's headline ones.
MAIN_FIXED = HEADLINE + [
    "metric", "distance_metric", "algorithm", "min_minor_ac", "max_missing_an", "random_seed",
]
# None is meaningful for these, so it's stated rather than dropped.
NONE_MEANS = {"sample_sets": "all releases", "sample_query": "all samples"}

FONT = "Helvetica, Arial, sans-serif"
TEXT, TEXT_2, MUTED = "#0b0b0b", "#52514e", "#75746f"
GRID, AXIS, BAR, SURFACE = "#e4e3df", "#c3c2b7", "#2a78d6", "#ffffff"
CHAR_WIDTH = 0.56  # rough average glyph width, as a fraction of the font size


def _call_name(call):
    """'ag3.plot_njt' from a call key like cell_7_call_1_ag3_plot_njt."""
    method = call["method"].rsplit(".", 1)[-1]
    rest = re.sub(r"^cell_\d+_call_\d+_", "", call["key"])
    owner = rest[: -len(method) - 1] if rest.endswith("_" + method) else ""
    return f"{owner}.{method}" if owner else method


def _text(x, y, content, size=12, fill=TEXT_2, anchor="start", weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}" '
        f'text-anchor="{anchor}" font-weight="{weight}">{html.escape(content)}</text>'
    )


def _wrap_width(text, width_px, size):
    return _wrap(text, max(10, int(width_px / (size * CHAR_WIDTH))), max_lines=None)


def _panel(x0, y0, title, unit, bars, axis_label):
    """A column chart at (x0, y0); returns (svg parts, width, height)."""
    band = 84 if len(bars) <= 6 else 64
    label_lines = max(len(_wrap(b["label"])) for b in bars)
    left, right, top, bottom = 56, 16, 44, 34 + 14 * label_lines
    width = left + right + band * max(len(bars), 1)
    plot_h = 170
    height = top + plot_h + bottom
    ticks = _nice_ticks(max(b["value"] for b in bars))
    y_max = ticks[-1] or 1
    baseline = y0 + top + plot_h
    fmt = _fmt_seconds if unit == "s" else _fmt_mib

    def y(v):
        return baseline - (v / y_max) * plot_h

    parts = [_text(x0, y0 + 14, title, size=13, fill=TEXT, weight="bold")]
    for tick in ticks:
        ty = y(tick)
        parts.append(f'<line x1="{x0 + left}" x2="{x0 + width - right}" y1="{ty:.1f}" y2="{ty:.1f}" stroke="{GRID}"/>')
        parts.append(_text(x0 + left - 8, ty + 4, _tick_label(tick, unit), size=11, fill=MUTED, anchor="end"))
    parts.append(_text(x0 + left - 8, y0 + top - 14, unit, size=11, fill=MUTED, anchor="end"))
    for i, bar in enumerate(bars):
        cx = x0 + left + band * i + band / 2
        bx0, bx1 = cx - 12, cx + 12
        yt = y(bar["value"])
        r = min(4, baseline - yt)
        parts.append(
            f'<path fill="{BAR}" d="M{bx0:.1f},{baseline:.1f} L{bx0:.1f},{yt + r:.1f} '
            f'Q{bx0:.1f},{yt:.1f} {bx0 + r:.1f},{yt:.1f} L{bx1 - r:.1f},{yt:.1f} '
            f'Q{bx1:.1f},{yt:.1f} {bx1:.1f},{yt + r:.1f} L{bx1:.1f},{baseline:.1f} Z"/>'
        )
        parts.append(_text(cx, yt - 6, fmt(bar["value"]), size=11, anchor="middle"))
        for line_number, line in enumerate(_wrap(bar["label"])):
            parts.append(_text(cx, baseline + 18 + 14 * line_number, line, size=11.5, anchor="middle"))
    parts.append(f'<line x1="{x0 + left}" x2="{x0 + width - right}" y1="{baseline}" y2="{baseline}" stroke="{AXIS}"/>')
    parts.append(_text(x0 + left + (width - left - right) / 2, y0 + height - 8, axis_label, size=11, fill=MUTED, anchor="middle"))
    return parts, width, height


def _fixed_text(calls, primary, also, mode):
    """'name = value' strings for the arguments every call shared."""
    if mode == "none":
        return []
    shared = {
        n: v for n, v in calls[0]["parameters"].items()
        if n != primary and n not in also
        and all(_dump(c["parameters"].get(n)) == _dump(v) for c in calls)
    }
    if mode == "main":
        names = [n for n in MAIN_FIXED if n in shared and (shared[n] is not None or n in NONE_MEANS)]
    else:
        names = sorted(shared)
    out = []
    for n in names:
        value = shared[n]
        if value is None and n in NONE_MEANS:
            text = f"None ({NONE_MEANS[n]})"
        elif n == "region" and _value_label(n, value) != str(value):
            text = f"{value} ({_value_label(n, value)})"
        else:
            text = value if isinstance(value, str) else repr(value)
            text = text if len(text) <= 70 else text[:69] + "…"
        out.append(f"{n} = {text}")
    return out


def figure(calls, fixed_mode):
    """The SVG for one method's calls from one CSV."""
    primary, also = _varied(calls)
    name = _call_name(calls[0])

    groups = collections.OrderedDict()
    for number, call in enumerate(calls, start=1):
        label = f"call {number}" if primary is None else _value_label(primary, call["parameters"].get(primary))
        groups.setdefault(label, []).append(call)
    latest = {label: group[-1] for label, group in groups.items()}
    axis = LABELS.get(primary, primary) if primary else "call (in order)"

    time_parts, time_w, chart_h = _panel(0, 0, "Run time", "s",
                                         [{"label": k, "value": c["time"]} for k, c in latest.items()], axis)
    gap = 32
    memory_parts, memory_w, _ = _panel(time_w + gap, 0, "Peak memory", "MiB",
                                       [{"label": k, "value": c["memory"]} for k, c in latest.items()], axis)
    charts_w = time_w + gap + memory_w
    width = max(charts_w, 600) + 48

    title = f"{name}: varying {axis}" if primary else f"{name}: nothing varied"
    lines = [(title, 15, TEXT, "bold")]
    if primary:
        lines.append((f"Values of {primary}: " + ", ".join(groups), 12, TEXT_2, "normal"))
    if also:
        lines.append(("Also changes between values: " + ", ".join(also), 12, TEXT_2, "normal"))
    header = []
    for text, size, fill, weight in lines:
        header += [(line, size, fill, weight) for line in _wrap_width(text, width - 48, size)]

    fixed = _fixed_text(calls, primary, also, fixed_mode)
    footer = []
    if fixed:
        footer.append(("Fixed for every value:", 12, TEXT, "bold"))
        footer += [(line, 11.5, TEXT_2, "normal") for line in _wrap_width("; ".join(fixed), width - 48, 11.5)]
    repeats = sum(len(g) - 1 for g in groups.values())
    if repeats:
        footer.append((f"{repeats} value(s) were run more than once; the latest run is shown.", 11, MUTED, "normal"))

    parts, y = [], 24
    for text, size, fill, weight in header:
        y += size + 6
        parts.append(_text(24, y, text, size=size, fill=fill, weight=weight))
    y += 18
    offset = 24 + (width - 48 - charts_w) / 2
    parts.append(f'<g transform="translate({offset:.1f},{y})">{"".join(time_parts + memory_parts)}</g>')
    y += chart_h + 8
    for text, size, fill, weight in footer:
        y += size + 6
        parts.append(_text(24, y, text, size=size, fill=fill, weight=weight))
    height = y + 20

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.0f} {height:.0f}" '
        f'width="{width:.0f}" height="{height:.0f}" font-family="{FONT}" role="img" '
        f'aria-label="{html.escape(title)}">'
        f'<rect width="100%" height="100%" fill="{SURFACE}"/>{"".join(parts)}</svg>\n'
    )


def main():
    parser = argparse.ArgumentParser(
        description="Write one SVG figure per results CSV (per method, if a CSV has several), "
        "showing how the varied argument affects run time and peak memory."
    )
    parser.add_argument(
        "results", nargs="*", type=Path, default=[SCRIPT_DIR / "results"],
        help="Folders of results CSVs, or CSV files (default: results/ next to this script).",
    )
    parser.add_argument(
        "-o", "--output", type=Path,
        help="Folder to write the figures to (default: figures/ next to the results folder).",
    )
    parser.add_argument(
        "--fixed", choices=["main", "all", "none"], default="main",
        help="Which fixed arguments to list under each figure: the main ones (default), "
        "every argument including defaults, or none.",
    )
    args = parser.parse_args()

    paths = []
    for item in args.results:
        paths += sorted(item.glob("*.csv")) if item.is_dir() else [item]
    if not paths:
        raise SystemExit(f"No CSVs found in {', '.join(map(str, args.results))}")
    first = args.results[0]
    output = args.output or (first if first.is_dir() else first.parent).parent / "figures"
    output.mkdir(parents=True, exist_ok=True)

    written = 0
    for path in paths:
        try:
            calls = _load(path)
        except (ValueError, KeyError, OSError) as exc:
            print(f"Skipping {path.name}: {exc}")
            continue
        by_method = collections.OrderedDict()
        for call in calls:
            by_method.setdefault(call["method"], []).append(call)
        stem = path.stem.replace("_performance", "")
        for method, method_calls in by_method.items():
            short = method.rsplit(".", 1)[-1]
            suffix = f"_{short}" if len(by_method) > 1 and not stem.startswith(short + "_") else ""
            target = output / f"{stem}{suffix}.svg"
            target.write_text(figure(method_calls, args.fixed), encoding="utf-8")
            written += 1
            print(f"{path.name} -> {target.name}")
    print(f"Wrote {written} figure(s) to {output}")


if __name__ == "__main__":
    main()
