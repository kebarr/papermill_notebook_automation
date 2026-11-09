"""Helpers for the insight notebooks.

Each notebook repeats one Ag3 call with one argument changed. For each call,
Sweep.run records the run time and peak memory, and saves the result under
results/<sweep name>/. Sweep.plot shows the result and saves the figure.
Sweep.summarise compares every result with a reference result (by default the
largest value), so you can see where increasing the argument stops changing
the answer.

The reference is also re-run with different random draws ("replicates"). 
Agreement between replicates and the reference is the best agreement you can
expect.
"""

import csv
import inspect
import json
import re
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from memory_profiler import memory_usage
from plotly.subplots import make_subplots
from scipy.cluster.hierarchy import cophenet, dendrogram, fcluster, linkage
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist, squareform
from scipy.stats import spearmanr

HERE = Path(__file__).resolve().parent
KINDS = ("pca", "gwss", "tree", "haplotypes", "diplotypes")
VALUE_COLUMNS = ["value", "replicate", "file", "runtime_sec", "peak_memory_mib", "n_snps", "saved_at"]


def population(ag3, sample_sets, query):
    """Sample metadata for the samples a sweep draws from."""
    return ag3.sample_metadata(sample_sets=sample_sets, sample_query=query).reset_index(drop=True)


def subsample(pool, n, seed=0):
    """n sample IDs drawn at random from pool. With the same seed, a smaller
    draw is the start of a larger one, so each smaller set of samples is
    contained in every larger one and results can be compared sample by
    sample."""
    if n > len(pool):
        raise ValueError(f"Asked for {n} samples but the population has {len(pool)}.")
    order = np.random.default_rng(seed).permutation(len(pool))
    return pool["sample_id"].to_numpy()[order[:n]].tolist()


def _label(value):
    if isinstance(value, (int, np.integer)):
        return f"{value:,}"
    return str(value)


def _stem(value, replicate):
    return re.sub(r"[^\w.-]+", "_", f"{value}") + f"_rep{replicate}"


def _save_table(df, path):
    """Parquet when pyarrow (or fastparquet) is installed, CSV otherwise."""
    try:
        target = path.with_suffix(".parquet")
        df.to_parquet(target, index=False)
    except ImportError:
        target = path.with_suffix(".csv")
        df.to_csv(target, index=False)
    return target


def _load_table(path):
    return pd.read_parquet(path) if path.suffix == ".parquet" else pd.read_csv(path)


def _as_tuple(result):
    """Some library versions return a dict rather than a tuple."""
    if isinstance(result, dict):
        return tuple(result[k] for k in ("dist", "phased_samples", "n_snps"))
    return result


MIN_SHARED = 20


def _shared(ids_a, ids_b):
    """IDs shared between run and ref, in a's order; empty if
    fewer than MIN_SHARED, too few to compare."""
    index_b = {s: i for i, s in enumerate(ids_b)}
    pairs = [(i, index_b[s]) for i, s in enumerate(ids_a) if s in index_b]
    if len(pairs) < MIN_SHARED:
        return np.array([], int), np.array([], int)
    a, b = zip(*pairs)
    return np.array(a), np.array(b)


def _pairs(n, max_pairs=2_000_000, seed=0):
    """Index pairs (i < j) among n items: all of them, or a random sample of
    max_pairs when there are more. The sample estimates the same correlation
    without building arrays of every pair (200 million for 20,000 samples)."""
    if n * (n - 1) // 2 <= max_pairs:
        return np.triu_indices(n, k=1)
    i, j = np.random.default_rng(seed).integers(0, n, (2, int(max_pairs * 1.2)))
    keep = i != j
    return np.minimum(i, j)[keep][:max_pairs], np.maximum(i, j)[keep][:max_pairs]


def _condensed(values, n, i, j):
    """Entries (i, j) of a condensed distance matrix of n items."""
    i, j = np.minimum(i, j), np.maximum(i, j)
    return values[n * i - i * (i + 1) // 2 + (j - i - 1)]


def _pair_correlation(values_a, values_b):
    """Spearman correlation between the same pairs' distances in two results."""
    if len(values_a) < 3:
        return np.nan
    return float(spearmanr(values_a, values_b).statistic)


def silhouette(coords, labels, max_samples=3000):
    """Mean silhouette width: how well the labelled groups separate, from -1
    (mixed) to 1 (cleanly separated). Estimated from max_samples random
    samples when there are more."""
    labels = np.asarray(labels).astype(str)
    if len(labels) > max_samples:
        keep = np.random.default_rng(0).choice(len(labels), max_samples, replace=False)
        coords, labels = coords[keep], labels[keep]
    groups = np.unique(labels)
    if len(groups) < 2:
        return np.nan
    dist = squareform(pdist(coords))
    within = np.zeros(len(labels))
    nearest = np.full(len(labels), np.inf)
    for g in groups:
        members = labels == g
        mean = dist[:, members].sum(axis=1) / np.maximum(members.sum() - members, 1)
        within[members] = mean[members]
        nearest[~members] = np.minimum(nearest[~members], dist[~members][:, members].mean(axis=1))
    sizes = pd.Series(labels).map(pd.Series(labels).value_counts()).to_numpy()
    width = np.where(sizes > 1, (nearest - within) / np.maximum(nearest, within), 0)
    return float(np.nanmean(width))


def compare_pca(ref, run, n_pcs=4):
    """Procrustes agreement) between the samples' positions on the first
    n_pcs PCs."""
    # Columns from ref dataframe to use for comparison
    cols = [f"PC{i}" for i in range(1, n_pcs + 1)]
    a, b = _shared(ref["sample_id"].to_numpy(), run["sample_id"].to_numpy())
    if len(a) <= n_pcs:
        return np.nan
    _, _, disparity = procrustes(ref[cols].to_numpy()[a], run[cols].to_numpy()[b])
    return 1 - disparity


def gwss_stat(stat):
    """xpehh_gwss returns one column per percentile; use the last (by
    default the 100th, i.e. the window maximum)."""
    stat = np.asarray(stat, dtype=float)
    return stat[:, -1] if stat.ndim == 2 else stat


def _peaks(x, stat, quantile=0.99, merge_bp=200_000):
    """Regions (start, end) of the windows in the top 1%, merging windows
    closer than merge_bp."""
    finite = np.isfinite(stat)
    if not finite.any():
        return []
    top = np.sort(x[finite & (stat >= np.nanquantile(stat, quantile))])
    regions = []
    for pos in top:
        if regions and pos - regions[-1][1] <= merge_bp:
            regions[-1][1] = pos
        else:
            regions.append([pos, pos])
    return regions


def compare_gwss(ref_x, ref_stat, x, stat, margin_bp=100_000):
    """Spearman correlation along the contig (the run interpolated onto the
    reference windows), and the fraction of the reference's top-1% peaks the
    run also has within margin_bp."""
    ref_stat, stat = gwss_stat(ref_stat), gwss_stat(stat)
    ok = np.isfinite(stat)
    on_ref = np.interp(ref_x, x[ok], stat[ok])
    corr = float(spearmanr(ref_stat, on_ref, nan_policy="omit").statistic)
    ref_peaks, run_peaks = _peaks(ref_x, ref_stat), _peaks(x, stat)
    found = sum(
        any(s <= end + margin_bp and e >= start - margin_bp for s, e in run_peaks)
        for start, end in ref_peaks
    )
    return corr, (found / len(ref_peaks) if ref_peaks else np.nan)


def gwss_shape(x, stat):
    """Window spacing, background level and noise, and how far the highest
    window stands above the background (in units of noise)."""
    stat = gwss_stat(stat)
    finite = stat[np.isfinite(stat)]
    median = float(np.median(finite))
    noise = float(1.4826 * np.median(np.abs(finite - median))) or np.nan
    return {
        "windows": len(x),
        "median_window_spacing_kbp": float(np.median(np.diff(x))) / 1000 if len(x) > 1 else np.nan,
        "background_median": median,
        "background_noise": noise,
        "peak_height_in_noise_units": (float(finite.max()) - median) / noise,
        "highest_window_Mbp": float(x[np.nanargmax(stat)]) / 1e6,
    }


def patristic(Z):
    """Pairwise path lengths through a neighbour-joining tree (anjl's Z:
    rows of left, right, left length, right length, leaf count)."""
    n = len(Z) + 1
    out = np.zeros((n, n), dtype=np.float32)
    members = {i: (np.array([i]), np.zeros(1)) for i in range(n)}
    for row, (left, right, length_left, length_right, _) in enumerate(Z):
        leaves_l, depth_l = members.pop(int(left))
        leaves_r, depth_r = members.pop(int(right))
        depth_l, depth_r = depth_l + length_left, depth_r + length_right
        block = depth_l[:, None] + depth_r[None, :]
        out[np.ix_(leaves_l, leaves_r)] = block
        out[np.ix_(leaves_r, leaves_l)] = block.T
        members[n + row] = (np.concatenate([leaves_l, leaves_r]), np.concatenate([depth_l, depth_r]))
    return out


def compare_trees(ref, run):
    """Correlation of path lengths between the samples both trees contain."""
    a, b = _shared(ref["samples"].astype(str), run["samples"].astype(str))
    i, j = _pairs(len(a))
    ref_paths = patristic(ref["Z"])[a[i], a[j]]
    return _pair_correlation(ref_paths, patristic(run["Z"])[b[i], b[j]])


def leaf_ids(samples, kind):
    samples = np.asarray(samples).astype(str)
    if kind == "haplotypes":
        return np.char.add(np.repeat(samples, 2), np.tile(["_0", "_1"], len(samples)))
    return samples


def compare_dendrograms(ref, run, kind, linkage_method):
    """Correlation of cophenetic (dendrogram) distances between the leaves
    both runs contain."""
    a, b = _shared(leaf_ids(ref["samples"], kind), leaf_ids(run["samples"], kind))
    i, j = _pairs(len(a))
    ref_coph = cophenet(linkage(ref["dist"], method=linkage_method))
    run_coph = cophenet(linkage(run["dist"], method=linkage_method))
    n_ref, n_run = len(leaf_ids(ref["samples"], kind)), len(leaf_ids(run["samples"], kind))
    return _pair_correlation(_condensed(ref_coph, n_ref, a[i], a[j]), _condensed(run_coph, n_run, b[i], b[j]))


def largest_cluster(dist, cut):
    """Frequency of the largest group of haplotypes all within `cut` SNP
    differences of each other (complete linkage, which unlike single linkage
    doesn't chain into larger groups as more haplotypes are added), with its
    binomial standard error."""
    clusters = fcluster(linkage(dist, method="complete"), t=cut, criterion="distance")
    n = len(clusters)
    p = np.bincount(clusters).max() / n
    return p, float(np.sqrt(p * (1 - p) / n))


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------


def dendrogram_figure(dist, leaf_data, linkage_method, color=None, title=None):
    """A dendrogram with leaves coloured by a metadata column."""
    Z = linkage(dist, method=linkage_method)
    limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max(limit, 10 * len(Z) + 1000))
    try:
        dend = dendrogram(Z, no_plot=True, count_sort=True)
    finally:
        sys.setrecursionlimit(limit)
    icoord, dcoord = np.array(dend["icoord"]), np.array(dend["dcoord"])
    gap = np.full((len(icoord), 1), np.nan)
    fig = go.Figure(
        go.Scattergl(
            x=np.hstack([icoord, gap]).ravel(), y=np.hstack([dcoord, gap]).ravel(),
            mode="lines", line=dict(color="gray", width=0.7), hoverinfo="skip", showlegend=False,
        )
    )
    leaves = leaf_data.iloc[dend["leaves"]].reset_index(drop=True)
    leaves["_x"] = 5 + 10 * np.arange(len(leaves))
    leaves["_y"] = 0
    markers = px.scatter(leaves, x="_x", y="_y", color=color, hover_name="leaf_id",
                         hover_data=[c for c in ("country", "year", "taxon") if c in leaves])
    for trace in markers.data:
        trace.marker.size = 4
        fig.add_trace(trace)
    fig.update_layout(title=title, template="simple_white", height=500,
                      xaxis=dict(visible=False), yaxis_title="Distance", legend_title=color)
    return fig


class Sweep:
    """One notebook's calls: the same method, one argument (`varied`) changed.

    kind: "pca", "gwss", "tree", "haplotypes" or "diplotypes"; sets how
        results are saved, plotted and compared.
    metadata: sample metadata used to colour plots (e.g. from population()).
    color: metadata column to colour points and leaves by.
    """

    def __init__(self, name, varied, kind, metadata=None, color="taxon", results_dir=None,
                 plot_max_leaves=2000, linkage_method=None, n_pcs=4, cluster_cut=4):
        if kind not in KINDS:
            raise ValueError(f"kind must be one of {KINDS}")
        self.name, self.varied, self.kind, self.color = name, varied, kind, color
        self.metadata = metadata
        self.results_dir = Path(results_dir or HERE / "results")
        self.dir = self.results_dir / name
        self.figures = self.dir / "figures"
        self.figures.mkdir(parents=True, exist_ok=True)
        self.performance_csv = self.results_dir / f"{name}_performance.csv"
        self.manifest = self.dir / "manifest.csv"
        self.plot_max_leaves = plot_max_leaves
        self.linkage_method = linkage_method or ("single" if kind == "haplotypes" else "complete")
        self.n_pcs, self.cluster_cut = n_pcs, cluster_cut

    def run(self, method, value, replicate=0, **kwargs):
        """Call method(**kwargs), record its run time and peak memory, and
        save the result. `value` is this call's value of the varied argument;
        `replicate` numbers repeat runs of the same value with different
        random draws (0 for the main run)."""
        result = {}

        def operation():
            result["value"] = method(**kwargs)

        start = time.perf_counter()
        peak = memory_usage((operation, ()), max_usage=True)
        runtime = time.perf_counter() - start
        self._record_performance(method, kwargs, value, replicate, runtime, peak)
        path, n_snps = self._save(result["value"], value, replicate)
        self._update_manifest(value, replicate, path, runtime, peak, n_snps)
        print(f"{self.varied} = {self._tick(value)} (replicate {replicate}): {runtime:,.1f} s, "
              f"{peak:,.0f} MiB peak. Saved {path.relative_to(self.results_dir)}")
        return result["value"]

    def _record_performance(self, method, kwargs, value, replicate, runtime, peak):
        bound = inspect.signature(method).bind_partial(**kwargs)
        bound.apply_defaults()
        parameters = {k: v for k, v in bound.arguments.items() if k not in ("sample_query_options", "kwargs")}
        parameters[self.varied] = value
        parameters["replicate"] = replicate
        new = not self.performance_csv.exists()
        with self.performance_csv.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if new:
                writer.writerow(["call_key", "method", "parameters_json", "runtime_sec", "peak_memory_mib"])
            writer.writerow([
                f"{self.name}_{_stem(value, replicate)}",
                getattr(method, "__qualname__", repr(method)),
                json.dumps(parameters, sort_keys=True, default=repr),
                round(runtime, 4), round(peak, 2),
            ])

    def _save(self, result, value, replicate):
        base = self.dir / _stem(value, replicate)
        if self.kind == "pca":
            df, evr = result
            np.save(base.with_name(base.name + "_explained_variance.npy"), evr)
            return _save_table(df, base), np.nan
        if self.kind == "gwss":
            x, stat = result[0], result[1]
            np.savez(base.with_suffix(".npz"), x=x, stat=stat)
            return base.with_suffix(".npz"), np.nan
        if self.kind == "tree":
            Z, samples, n_snps = result
            np.savez(base.with_suffix(".npz"), Z=Z, samples=np.asarray(samples).astype(str), n_snps=n_snps)
            return base.with_suffix(".npz"), int(n_snps)
        dist, samples, n_snps = _as_tuple(result)
        np.savez(base.with_suffix(".npz"), dist=dist, samples=np.asarray(samples).astype(str), n_snps=n_snps)
        return base.with_suffix(".npz"), int(n_snps)

    def _update_manifest(self, value, replicate, path, runtime, peak, n_snps):
        rows = self._manifest()
        rows = rows[~((rows["value"].astype(str) == str(value)) & (rows["replicate"] == replicate))]
        row = pd.DataFrame([{
            "value": value, "replicate": replicate, "file": path.name, "runtime_sec": round(runtime, 4),
            "peak_memory_mib": round(peak, 2), "n_snps": n_snps,
            "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        }])
        rows = pd.concat([rows, row], ignore_index=True) if len(rows) else row
        rows.to_csv(self.manifest, index=False)

    def _manifest(self):
        if not self.manifest.exists():
            return pd.DataFrame(columns=VALUE_COLUMNS)
        rows = pd.read_csv(self.manifest)
        rows["value"] = rows["value"].map(lambda v: int(v) if re.fullmatch(r"-?\d+", str(v)) else v)
        return rows

    def load(self, value, replicate=0):
        """A saved result: for PCA a dict with "df" and "evr"; otherwise the
        saved arrays (e.g. "x" and "stat", "Z" and "samples", "dist" and
        "samples")."""
        rows = self._manifest()
        match = rows[(rows["value"].astype(str) == str(value)) & (rows["replicate"] == replicate)]
        if match.empty:
            raise KeyError(f"No saved result for {self.varied} = {value}, replicate {replicate}.")
        path = self.dir / match.iloc[-1]["file"]
        if self.kind == "pca":
            evr = np.load(path.with_name(path.stem + "_explained_variance.npy"))
            return {"df": _load_table(path), "evr": evr}
        with np.load(path) as data:
            return {k: data[k] for k in data.files}

    def _tick(self, value):
        """Lengths in kbp/Mbp; other values with thousands separators."""
        if self.varied.endswith("length") and isinstance(value, (int, np.integer)):
            return f"{value / 1e6:g} Mbp" if value >= 1_000_000 else f"{value / 1000:g} kbp"
        return _label(value)

    def _title(self, value, replicate):
        title = f"{self.name}: {self.varied} = {self._tick(value)}"
        return title + (f" (replicate {replicate})" if replicate else "")

    def show(self, fig, value, replicate=0):
        """Display a figure and save it as HTML (and PNG if kaleido is
        installed) in results/<sweep>/figures/."""
        fig.show()
        base = self.figures / _stem(value, replicate)
        fig.write_html(base.with_suffix(".html"), include_plotlyjs="cdn")
        try:
            fig.write_image(base.with_suffix(".png"), scale=2)
        except Exception:
            pass

    def _leaf_data(self, samples):
        ids = leaf_ids(samples, self.kind)
        data = pd.DataFrame({"leaf_id": ids, "sample_id": np.char.rpartition(ids, "_")[:, 0]
                             if self.kind == "haplotypes" else ids})
        if self.metadata is not None:
            data = data.merge(self.metadata, on="sample_id", how="left")
        return data

    def plot(self, result, value, replicate=0):
        """Show the result of one call and save the figure."""
        title = self._title(value, replicate)
        if self.kind == "pca":
            df, evr = result
            hover = [c for c in ("country", "year", "taxon") if c in df]
            fig = px.scatter(df, x="PC1", y="PC2", color=self.color if self.color in df else None,
                             hover_name="sample_id", hover_data=hover, template="simple_white",
                             title=title, height=500, width=700)
            fig.update_traces(marker_size=5)
            fig.update_xaxes(title=f"PC1 ({evr[0]:.1%})")
            fig.update_yaxes(title=f"PC2 ({evr[1]:.1%})")
        elif self.kind == "gwss":
            x, stat = result[0], gwss_stat(result[1])
            fig = px.scatter(x=np.asarray(x) / 1e6, y=stat, template="simple_white", title=title,
                             height=300, width=900, render_mode="webgl",
                             labels={"x": "Position (Mbp)", "y": self.name.split("_gwss")[0].upper()})
            fig.update_traces(marker_size=3)
        elif self.kind == "tree":
            import anjl

            Z, samples, _ = result
            if len(samples) > self.plot_max_leaves:
                print(f"Not plotting: {len(samples):,} leaves is more than plot_max_leaves.")
                return
            leaves = self._leaf_data(samples)
            fig = anjl.plot(Z, leaf_data=leaves, color=self.color if self.color in leaves else None,
                            hover_name="sample_id", width=700, height=600)
            fig.update_layout(title=title)
        else:
            dist, samples, _ = _as_tuple(result)
            leaves = self._leaf_data(samples)
            if len(leaves) > self.plot_max_leaves:
                print(f"Not plotting: {len(leaves):,} leaves is more than plot_max_leaves.")
                return
            fig = dendrogram_figure(dist, leaves, self.linkage_method,
                                    color=self.color if self.color in leaves else None, title=title)
            if self.kind == "haplotypes":
                p, se = largest_cluster(dist, self.cluster_cut)
                print(f"Largest cluster (haplotypes within {self.cluster_cut} SNPs): {p:.1%} ± {se:.1%}")
        self.show(fig, value, replicate)

    def _metrics(self, ref, run):
        if self.kind == "pca":
            out = {"agreement": compare_pca(ref["df"], run["df"], self.n_pcs)}
            pcs = run["df"][[f"PC{i}" for i in range(1, self.n_pcs + 1)]].to_numpy()
            if self.color in run["df"]:
                out[f"separation_by_{self.color}"] = silhouette(pcs, run["df"][self.color])
            return out
        if self.kind == "gwss":
            corr, found = compare_gwss(ref["x"], ref["stat"], run["x"], run["stat"])
            shape = gwss_shape(run["x"], run["stat"])
            return {"agreement": corr, "reference_peaks_found": found,
                    "peak_height_in_noise_units": shape["peak_height_in_noise_units"]}
        if self.kind == "tree":
            return {"agreement": compare_trees(ref, run)}
        out = {"agreement": compare_dendrograms(ref, run, self.kind, self.linkage_method)}
        if self.kind == "haplotypes":
            out["largest_cluster_freq"], out["largest_cluster_se"] = largest_cluster(run["dist"], self.cluster_cut)
        return out

    def summarise(self, reference=None, threshold=0.95, runtime=False):
        """Compare every saved result with the reference (default: the
        largest value), show agreement and cost side by side, and save the
        table and figure. Window-size sweeps have no reference; they show
        how the trace's resolution and noise change instead. runtime=True
        adds a run-time panel next to peak memory."""
        rows = self._manifest()
        if rows.empty:
            print("Nothing saved yet.")
            return None
        if self.kind == "gwss" and self.varied == "window_size":
            return self._summarise_windows(rows, runtime)
        if self.kind in ("haplotypes", "diplotypes") and self.varied == "region_length":
            return self._summarise_regions(rows, runtime)

        reference = rows[rows["replicate"] == 0]["value"].max() if reference is None else reference
        try:
            ref = self.load(reference, 0)
        except KeyError:
            print(f"The reference ({self.varied} = {self._tick(reference)}) hasn't been run yet; run its cell "
                  "first, or pass another value as summarise(reference=...).")
            return None
        records = []
        for _, row in rows.sort_values(["replicate", "value"]).iterrows():
            if row["replicate"] > 0 and row["value"] != reference:
                continue
            metrics = self._metrics(ref, self.load(row["value"], row["replicate"]))
            records.append({self.varied: row["value"], "replicate": row["replicate"], **metrics,
                            "runtime_sec": row["runtime_sec"], "peak_memory_mib": row["peak_memory_mib"]})
        table = pd.DataFrame(records)
        if table[table["replicate"] > 0]["agreement"].isna().any():
            print(f"Some replicates share fewer than {MIN_SHARED} samples with the reference, so can't be "
                  "compared with it. Replicates are fresh draws from the population; use a reference "
                  "that's a larger fraction of the population.")
        ceiling = table[(table["replicate"] > 0)]["agreement"].dropna()
        floor = ceiling.min() if len(ceiling) else threshold
        basis = (f"the lowest replicate agreement ({floor:.3f})" if len(ceiling)
                 else f"the threshold {threshold} (no replicates saved yet)")
        mains = table[table["replicate"] == 0]
        reached = mains[mains["agreement"] >= floor]
        print(f"Reference: {self.varied} = {self._tick(reference)}.")
        if len(reached):
            print(f"Smallest value agreeing with the reference as well as {basis}: "
                  f"{self.varied} = {self._tick(reached[self.varied].iloc[0])}.")
        else:
            print(f"No value below the reference reaches {basis}.")

        fig = self._summary_figure(table, floor if len(ceiling) else None, ceiling, runtime)
        self._save_summary(table, fig)
        return table

    @staticmethod
    def _panels(titles):
        """Subplots for summary panels: a 2x2 grid for four, otherwise one
        row. Returns the figure and each panel's (row, col)."""
        rows, cols = (2, 2) if len(titles) == 4 else (1, len(titles))
        spacing = {"vertical_spacing": 0.2} if rows > 1 else {}
        fig = make_subplots(rows=rows, cols=cols, subplot_titles=titles, horizontal_spacing=0.08, **spacing)
        fig.update_layout(height=380 * rows, width=420 * cols)
        return fig, [(i // cols + 1, i % cols + 1) for i in range(len(titles))]

    def _summary_figure(self, table, floor, ceiling, runtime=False):
        mains = table[table["replicate"] == 0]
        x = mains[self.varied]
        numeric = pd.api.types.is_numeric_dtype(x)
        columns = {"agreement": "Agreement with the reference"}
        if self.kind == "haplotypes":
            columns["largest_cluster_freq"] = f"Largest haplotype cluster (within {self.cluster_cut} SNPs)"
        if runtime:
            columns["runtime_sec"] = "Run time (s)"
        columns["peak_memory_mib"] = "Peak memory (MiB)"
        fig, cells = self._panels(list(columns.values()))
        at = dict(zip(columns, cells))
        row, col = at["agreement"]
        fig.add_trace(go.Scatter(x=x, y=mains["agreement"], mode="lines+markers", name="agreement",
                                 line=dict(color="#2a78d6")), row=row, col=col)
        if floor is not None:
            # Agreement as good as a fresh draw at the reference: the shaded band
            # spans the replicates, and each replicate is shown as an open circle.
            replicates = table[table["replicate"] > 0]
            fig.add_hrect(y0=floor, y1=ceiling.max(), fillcolor="#2a78d6", opacity=0.12, line_width=0, row=row, col=col)
            fig.add_hline(y=floor, line=dict(color="#2a78d6", dash="dot", width=1), row=row, col=col)
            fig.add_trace(go.Scatter(x=replicates[self.varied], y=replicates["agreement"], mode="markers",
                                     name="replicates", marker=dict(symbol="circle-open", size=9, color="#2a78d6")),
                          row=row, col=col)
            fig.add_annotation(text="replicates of the reference", x=0.02, xref="x domain", y=floor, yref="y",
                               yanchor="bottom", xanchor="left", showarrow=False, font=dict(size=11, color="#52514e"),
                               row=row, col=col)
        if self.kind == "haplotypes":
            row, col = at["largest_cluster_freq"]
            fig.add_trace(go.Scatter(x=x, y=mains["largest_cluster_freq"], mode="lines+markers",
                                     error_y=dict(array=1.96 * mains["largest_cluster_se"]),
                                     name="largest cluster", line=dict(color="#2a78d6")), row=row, col=col)
            fig.update_yaxes(tickformat=".0%", row=row, col=col)
        for column in ("runtime_sec", "peak_memory_mib"):
            if column in at:
                row, col = at[column]
                fig.add_trace(go.Scatter(x=x, y=mains[column], mode="lines+markers", name=columns[column],
                                         line=dict(color="#52514e")), row=row, col=col)
                fig.update_yaxes(rangemode="tozero", row=row, col=col)
        for row, col in cells:
            fig.update_xaxes(title=self.varied, type="log" if numeric else None, tickvals=list(x),
                             ticktext=[self._tick(v) for v in x], row=row, col=col)
        fig.update_layout(template="simple_white", showlegend=False,
                          title=f"{self.name}: does increasing {self.varied} change the result?")
        return fig

    def _trade_off(self, table, columns, title, note, runtime=False):
        """A summary for arguments with no best value: one panel per column."""
        if runtime:
            columns = {k: v for k, v in columns.items() if k != "peak_memory_mib"}
            columns.update({"runtime_sec": "Run time (s)", "peak_memory_mib": "Peak memory (MiB)"})
        fig, cells = self._panels(list(columns.values()))
        x = table[self.varied]
        for (row, col), column in zip(cells, columns):
            cost = column in ("runtime_sec", "peak_memory_mib")
            fig.add_trace(go.Scatter(x=x, y=table[column], mode="lines+markers",
                                     line=dict(color="#52514e" if cost else "#2a78d6")),
                          row=row, col=col)
            fig.update_xaxes(title=self.varied, type="log", tickvals=list(x), ticktext=[self._tick(v) for v in x],
                             row=row, col=col)
            if cost:
                fig.update_yaxes(rangemode="tozero", row=row, col=col)
            if column == "largest_cluster_freq":
                fig.update_yaxes(tickformat=".0%", row=row, col=col)
        fig.update_layout(template="simple_white", showlegend=False, title=title)
        print(note)
        self._save_summary(table, fig)
        return table

    def _summarise_windows(self, rows, runtime=False):
        records = []
        for _, row in rows[rows["replicate"] == 0].sort_values("value").iterrows():
            data = self.load(row["value"])
            records.append({self.varied: row["value"], **gwss_shape(data["x"], data["stat"]),
                            "runtime_sec": row["runtime_sec"], "peak_memory_mib": row["peak_memory_mib"]})
        return self._trade_off(
            pd.DataFrame(records),
            {"peak_height_in_noise_units": "Highest window above background (noise units)",
             "median_window_spacing_kbp": "Median window spacing (kbp)",
             "peak_memory_mib": "Peak memory (MiB)"},
            f"{self.name}: resolution against noise as {self.varied} changes",
            "Larger windows smooth out noise but blur peak positions; there's no single best value. "
            "Compare the traces above for where the peaks you care about are still sharp.",
            runtime,
        )

    def _summarise_regions(self, rows, runtime=False):
        """Clustering over longer regions: compared with the smallest (locus)
        region rather than a reference, because longer isn't better."""
        rows = rows[rows["replicate"] == 0].sort_values("value")
        locus = self.load(rows["value"].iloc[0])
        records = []
        for _, row in rows.iterrows():
            data = self.load(row["value"])
            # haplotype_pairwise_distances reports the region's sites, not SNPs, so it's left out.
            record = {self.varied: row["value"], **({"n_snps": row["n_snps"]} if self.kind == "diplotypes" else {}),
                      "agreement_with_smallest_region": compare_dendrograms(locus, data, self.kind, self.linkage_method)}
            if self.kind == "haplotypes":
                record["largest_cluster_freq"], record["largest_cluster_se"] = largest_cluster(data["dist"], self.cluster_cut)
            records.append({**record, "runtime_sec": row["runtime_sec"], "peak_memory_mib": row["peak_memory_mib"]})
        table = pd.DataFrame(records)
        columns = {"agreement_with_smallest_region": "Agreement with the smallest region"}
        if self.kind == "haplotypes":
            columns = {"largest_cluster_freq": f"Largest haplotype cluster (within {self.cluster_cut} SNPs)", **columns}
        columns["peak_memory_mib"] = "Peak memory (MiB)"
        return self._trade_off(
            table, columns, f"{self.name}: what clustering shows as the region grows",
            "Clustering describes a locus: as the region grows, recombination breaks haplotypes up and the "
            "clusters stop reflecting the locus. Agreement with the smallest region shows how quickly that "
            "happens; there is no reference to converge to.",
            runtime,
        )

    def _save_summary(self, table, fig):
        fig.show()
        table.to_csv(self.dir / "summary.csv", index=False)
        fig.write_html(self.figures / "summary.html", include_plotlyjs="cdn")
        try:
            fig.write_image(self.figures / "summary.png", scale=2)
        except Exception:
            pass
        print(f"Saved {self.dir.relative_to(self.results_dir)}/summary.csv and figures/summary.html")
