"""Make the insight notebooks: one per sweep, one cell per value, each cell
running the call, saving the result and showing it, then replicate cells and
a summary cell.

    python make_insight_notebooks.py        # writes the notebooks next to this script
"""

import json
from pathlib import Path

import nbformat

HERE = Path(__file__).resolve().parent
BASE_METADATA = json.loads((HERE.parent / "plot_pca.ipynb").read_text())["metadata"]

GHANA_COLU = "country == 'Ghana' and taxon == 'coluzzii'"
GHANA_GAMB = "country == 'Ghana' and taxon == 'gambiae'"
UGANDA_GAMB = "country == 'Uganda' and taxon == 'gambiae'"
NON_LAB = "country != 'Lab Cross'"
GENOME_REGION = "3L:15,000,000-41,000,000"
CYP6_REGION = "2R:28,480,000-28,500,000"

GWSS_SAMPLE_NOTE = (
    "**Population.** One population ({population}, all Ag3 releases). Selection scans assume one "
    "population: pooling populations dilutes sweeps found in only one of them, so a larger *pooled* "
    "cohort can show less. The largest useful cohort is therefore often set by how many samples one "
    "population has, not by the server.\n\n"
    "**Library default.** `{method}` uses at most `max_cohort_size=50` samples unless told otherwise; "
    "these calls set `min_cohort_size` = `max_cohort_size` = the number of samples.\n\n"
    "**Contig.** {contig} contains the *Cyp6aa/Cyp6p* cluster (~28.5 Mbp), a strong sweep in Ghanaian "
    "*An. coluzzii*, so there is a known peak to recover. Memory grows with samples × phased sites "
    "on the contig; 1,000 samples on 2R needs a large server."
)
LARGE_GWSS_NOTE = (
    "**Large values.** Values go up to the size of one population (3,282 Ghanaian *An. coluzzii* in "
    "all Ag3 releases). {two}The performance notebooks pool whole taxa to reach 10,000; that "
    "changes the question (see Population below), so it isn't repeated here. The reference is below "
    "the largest value, so replicate draws of it overlap less; a value above the reference shows "
    "whether going further still changes the scan."
)
AGREEMENT_GWSS = (
    "**Agreement.** Spearman correlation of the statistic along the contig with the reference "
    "(the run interpolated onto the reference windows). The summary table also gives the fraction "
    "of the reference's top-1% peaks the run finds (within 100 kbp), and how far the highest window "
    "stands above the background."
)
REPLICATES = (
    "**Replicates.** The reference is re-run with different random draws of samples. Their agreement "
    "with the reference is the most any value can achieve; the summary suggests the smallest value "
    "that reaches it. Replicates share samples with the reference only by chance, so if you change "
    "the reference, keep it a sizeable fraction (a third or more) of the population."
)
NESTED = (
    "**Samples.** `insight.subsample` draws samples in a fixed random order, so each smaller set of "
    "samples is contained in every larger one and results can be compared sample by sample."
)


def gwss_samples(method, stat, large=False):
    two = method in ("h1x_gwss", "xpehh_gwss")
    second = UGANDA_GAMB if large else GHANA_GAMB
    if not large:
        values, reference = [10, 20, 50, 100, 200, 500, 1000], 1000
    elif two:
        values, reference = [500, 1000, 1500, 2000], 1500
    else:
        values, reference = [500, 1000, 1500, 2000, 3000], 2000
    settings = {
        "SAMPLE_SETS": None,
        **({"POPULATION_1": GHANA_COLU, "POPULATION_2": second} if two else {"POPULATION": GHANA_COLU}),
        "CONTIG": "2R",
        "WINDOW_SIZE": 1000 if method != "xpehh_gwss" else 200,
        "REFERENCE": reference,
        "REPLICATES": [1, 2],
    }
    if two:
        setup = ("pool = insight.population(ag3, SAMPLE_SETS, POPULATION_1)\n"
                 "pool_2 = insight.population(ag3, SAMPLE_SETS, POPULATION_2)\n"
                 "print(f\"{len(pool):,} and {len(pool_2):,} samples available\")\n")
        draw = ("ids_1 = insight.subsample(pool, n, seed=<SEED>)\n"
                "ids_2 = insight.subsample(pool_2, n, seed=<SEED>)\n")
        cohort = ('    cohort1_query="sample_id in @ids_1", cohort2_query="sample_id in @ids_2",\n'
                  '    sample_query_options={"local_dict": {"ids_1": ids_1, "ids_2": ids_2}},\n')
        population = ("cohort 1 Ghanaian *An. coluzzii*, cohort 2 "
                      + ("Ugandan *An. gambiae*" if large else "Ghanaian *An. gambiae*"))
    else:
        setup = ("pool = insight.population(ag3, SAMPLE_SETS, POPULATION)\n"
                 "print(f\"{len(pool):,} samples available\")\n")
        draw = "ids = insight.subsample(pool, n, seed=<SEED>)\n"
        cohort = ('    sample_query="sample_id in @ids",\n'
                  '    sample_query_options={"local_dict": {"ids": ids}},\n')
        population = "Ghanaian *An. coluzzii*"
    call = (
        draw
        + f"result = sweep.run(\n    ag3.{method}, value=n,<REP>\n"
        "    contig=CONTIG, window_size=WINDOW_SIZE, sample_sets=SAMPLE_SETS,\n"
        + cohort
        + "    min_cohort_size=n, max_cohort_size=n,\n)\n"
    )
    notes = [GWSS_SAMPLE_NOTE.format(population=population, method=method, contig="2R"),
             AGREEMENT_GWSS, REPLICATES, NESTED]
    if large:
        notes.insert(0, LARGE_GWSS_NOTE.format(two="Ghanaian *An. gambiae* (1,379) is too small, so cohort 2 is "
                                                   "Ugandan *An. gambiae* (2,432). " if two else ""))
    return dict(
        name=f"{method}_{'large_' if large else ''}samples", method=method, varied="samples", kind="gwss", color=None,
        question=f"Does `{method}` keep improving with hundreds to thousands of samples per cohort?" if large
        else f"How many samples per cohort does `{method}` need before the {stat} scan stops changing?",
        notes=notes, settings=settings, setup=setup, var="n", values=values, call=call, replicate="seed",
    )


def gwss_window(method, stat):
    spec = gwss_samples(method, stat)
    settings = {k: v for k, v in spec["settings"].items() if k not in ("WINDOW_SIZE", "REFERENCE", "REPLICATES")}
    settings["SAMPLES"] = 200
    call = (
        "n = SAMPLES\n"
        + spec["call"].replace("value=n,", "value=window_size,").replace("window_size=WINDOW_SIZE", "window_size=window_size")
    )
    return dict(
        spec, name=f"{method}_window_size", varied="window_size", settings=settings, var="window_size",
        values=[100, 200, 500, 1000, 2000, 5000], call=call, replicate=None,
        question=f"How does the window size change what the {stat} scan shows?",
        notes=[
            "**No single best value.** The window size trades resolution against noise: small windows "
            "locate peaks precisely but are noisy, large windows are smooth but blur and merge peaks. "
            "So there's no reference here. The summary shows the highest window's height above the "
            "background (in units of background noise), the window spacing, and the cost. Compare the "
            "traces for where the peaks you care about are still sharp.",
            spec["notes"][0], NESTED,
        ],
    )


def tree_or_pca(name, method, kind, varied, question, notes, settings, values, call, replicate, color="taxon",
                setup=None, var=None, sweep_args=""):
    return dict(
        name=name, method=method, varied=varied, kind=kind, color=color, question=question, notes=notes,
        sweep_args=sweep_args,
        settings=settings, setup=setup if setup is not None else ("pool = insight.population(ag3, SAMPLE_SETS, SAMPLE_QUERY)\n"
                                           "print(f\"{len(pool):,} samples available\")\n"),
        var=var or ("n" if varied == "samples" else varied), values=values, call=call, replicate=replicate,
    )


SAMPLE_CALL = (
    "ids = insight.subsample(pool, n, seed=<SEED>)\n"
    "result = sweep.run(\n    ag3.<METHOD>, value=n,<REP>\n"
    "    <ARGS>\n"
    '    sample_query="sample_id in @ids",\n'
    '    sample_query_options={"local_dict": {"ids": ids}},\n)\n'
)


def sample_call(method, args):
    return SAMPLE_CALL.replace("<METHOD>", method).replace("<ARGS>", args)


FIXED_SAMPLES_SNPS_CALL = (
    "ids = insight.subsample(pool, SAMPLES)\n"
    "result = sweep.run(\n    ag3.njt, value=n_snps,<REP>\n"
    "    region=REGION, n_snps=n_snps, thin_offset=<THIN>, sample_sets=SAMPLE_SETS,\n"
    '    sample_query="sample_id in @ids",\n'
    '    sample_query_options={"local_dict": {"ids": ids}},\n)\n'
)
SNP_REPLICATES = (
    "**Replicates.** The reference is re-run with `thin_offset` 1 and 2: the same samples, a "
    "different, equally spaced set of SNPs. Their agreement with the reference is the most any value "
    "can achieve; the summary suggests the smallest value that reaches it."
)

SPECS = [
    tree_or_pca(
        "pca_n_snps", "pca", "pca", "n_snps",
        "How many SNPs does PCA need before the samples' positions stop changing?",
        ["**Samples.** All Ag3 3.0 samples outside the lab crosses, the same in every cell.",
         "**Agreement.** Procrustes similarity of the samples' positions on the first 4 PCs "
         "(1 = the same layout, allowing for rotation, reflection and scaling). The summary also "
         "gives how well taxa separate (mean silhouette width).",
         SNP_REPLICATES],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "REGION": GENOME_REGION, "REFERENCE": 30000,
         "REPLICATES": [1, 2]},
        [1000, 2000, 5000, 10000, 20000, 30000],
        "result = sweep.run(\n    ag3.pca, value=n_snps,<REP>\n"
        "    region=REGION, n_snps=n_snps, thin_offset=<THIN>,\n"
        "    sample_sets=SAMPLE_SETS, sample_query=SAMPLE_QUERY,\n)\n",
        "thin_offset", setup="",
    ),
    tree_or_pca(
        "pca_samples", "pca", "pca", "samples",
        "How many samples does PCA need before the structure it shows stops changing?",
        ["**Samples.** Drawn from Ag3 3.0 outside the lab crosses (2,784 samples), 10,000 SNPs from "
         f"{GENOME_REGION}.",
         "**Agreement.** Procrustes similarity, on the first 4 PCs, between each run and the "
         "reference for the samples both contain. The summary also gives how well taxa separate "
         "(mean silhouette width).",
         REPLICATES, NESTED],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "REGION": GENOME_REGION, "N_SNPS": 10000,
         "REFERENCE": 2000, "REPLICATES": [1, 2]},
        [50, 100, 200, 500, 1000, 2000],
        sample_call("pca", "region=REGION, n_snps=N_SNPS, sample_sets=SAMPLE_SETS,"),
        "seed",
    ),
    tree_or_pca(
        "njt_n_snps", "njt", "tree", "n_snps",
        "How many SNPs does a neighbour-joining tree need before it stops changing?",
        [f"**Samples.** 500 samples from Ag3 3.0 outside the lab crosses, the same in every cell; SNPs from {GENOME_REGION}.",
         "**Agreement.** Spearman correlation of the path lengths between every pair of samples "
         "through the tree, against the reference tree.",
         SNP_REPLICATES],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "REGION": GENOME_REGION, "SAMPLES": 500,
         "REFERENCE": 50000, "REPLICATES": [1, 2]},
        [1000, 2000, 5000, 10000, 20000, 50000],
        FIXED_SAMPLES_SNPS_CALL,
        "thin_offset",
    ),
    tree_or_pca(
        "njt_samples", "njt", "tree", "samples",
        "How many samples does a neighbour-joining tree need before the relationships it shows stop changing?",
        [f"**Samples.** Drawn from Ag3 3.0 outside the lab crosses; 10,000 SNPs from {GENOME_REGION}.",
         "**Agreement.** Spearman correlation of the path lengths between every pair of samples "
         "through the tree, against the reference tree, for the samples both contain.",
         "**Readability.** Trees with more than `plot_max_leaves` (2,000) samples aren't drawn. A tree "
         "with thousands of leaves is hard to read whatever the server, which is itself a limit on "
         "what a plot can show.",
         REPLICATES, NESTED],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "REGION": GENOME_REGION, "N_SNPS": 10000,
         "REFERENCE": 2000, "REPLICATES": [1, 2]},
        [50, 100, 200, 500, 1000, 2000],
        sample_call("njt", "region=REGION, n_snps=N_SNPS, sample_sets=SAMPLE_SETS,"),
        "seed",
    ),
    tree_or_pca(
        "haplotype_clustering_samples", "haplotype_pairwise_distances", "haplotypes", "samples",
        "How many samples does haplotype clustering need before the clusters, and the frequency of "
        "the swept haplotype, stop changing?",
        [f"**Region.** {CYP6_REGION}, the *Cyp6aa/Cyp6p* cluster, in Ghanaian *An. coluzzii* (all Ag3 "
         "releases), where a swept haplotype is common. Haplotype clustering is for a locus: over "
         "Mbp, recombination makes every haplotype distinct, so larger regions show less, not more.",
         "**Agreement.** Spearman correlation of the dendrogram (cophenetic) distances with the "
         "reference, for the haplotypes both contain (single linkage, as in "
         "`plot_haplotype_clustering`).",
         "**Swept haplotype frequency.** The largest group of haplotypes all within "
         "`cluster_cut` (4) SNP differences of each other, with a 95% interval. Its precision follows "
         "the binomial: about ±10% at 100 haplotypes and ±3% at 1,000 (for a frequency near 50%), so "
         "you can choose the number of samples from the precision you need.",
         REPLICATES, NESTED],
        {"SAMPLE_SETS": None, "SAMPLE_QUERY": GHANA_COLU, "REGION": CYP6_REGION, "REFERENCE": 1000,
         "REPLICATES": [1, 2]},
        [25, 50, 100, 200, 500, 1000],
        sample_call("haplotype_pairwise_distances", "region=REGION, sample_sets=SAMPLE_SETS,"),
        "seed", color="sample_set",
    ),
    tree_or_pca(
        "diplotype_clustering_samples", "diplotype_pairwise_distances", "diplotypes", "samples",
        "How many samples does diplotype clustering need before the clusters stop changing?",
        [f"**Region.** {CYP6_REGION}, the *Cyp6aa/Cyp6p* cluster, in Ghanaian *An. coluzzii* (all Ag3 releases).",
         "**Agreement.** Spearman correlation of the dendrogram (cophenetic) distances with the "
         "reference, for the samples both contain (complete linkage, as in "
         "`plot_diplotype_clustering`).",
         REPLICATES, NESTED],
        {"SAMPLE_SETS": None, "SAMPLE_QUERY": GHANA_COLU, "REGION": CYP6_REGION, "REFERENCE": 1000,
         "REPLICATES": [1, 2]},
        [25, 50, 100, 200, 500, 1000],
        sample_call("diplotype_pairwise_distances", "region=REGION, sample_sets=SAMPLE_SETS,"),
        "seed", color="sample_set",
    ),
]
for method, stat in [("h12_gwss", "H12"), ("g123_gwss", "G123"), ("h1x_gwss", "H1X"), ("xpehh_gwss", "XP-EHH")]:
    SPECS += [gwss_samples(method, stat), gwss_window(method, stat)]


# --- Large values ---------------------------------------------------------------

LARGE_REFERENCE_NOTE = (
    "**Large values.** The reference is below the largest value, so replicate draws of it overlap less "
    "with each other; the value above the reference shows whether going further still changes the result."
)
ALL_RELEASES_NOTE = (
    "**Samples.** Drawn from all Ag3 releases outside the lab crosses (24,933 samples); {snps}."
)
REGION_CALL = (
    'region = f"{CONTIG}:{START:,}-{START + length:,}"\n'
    "<DRAW>"
    "result = sweep.run(\n    ag3.<METHOD>, value=length,<REP>\n"
    "    region=region, n_snps=N_SNPS, thin_offset=<THIN>, sample_sets=SAMPLE_SETS,\n"
    "<SAMPLES>)\n"
)
CENTRED_CALL = (
    'region = f"{CONTIG}:{CENTRE - length // 2:,}-{CENTRE + length // 2:,}"\n'
    "ids = insight.subsample(pool, SAMPLES)\n"
    "result = sweep.run(\n    ag3.<METHOD>, value=length,\n"
    "    region=region, sample_sets=SAMPLE_SETS,\n"
    '    sample_query="sample_id in @ids",\n'
    '    sample_query_options={"local_dict": {"ids": ids}},\n)\n'
)
REGION_AGREEMENT = (
    "**Agreement.** Against the longest region. A short region shows the genealogy at that locus; a "
    "longer one averages over more independent loci and approaches genome-wide structure. The "
    "summary shows how much sequence you need before the picture stops changing."
)
REGION_NOTE = (
    "**Region.** From 3L:15,000,000, lengths 100 kbp to 26 Mbp (to 41 Mbp, avoiding the "
    "centromere end), with the same number of SNPs at every length."
)
CLUSTER_REGION_NOTE = (
    "**No reference.** Clustering describes a locus. Regions are centred on the *Cyp6aa/Cyp6p* "
    "cluster (2R:28,490,000) in 200 Ghanaian *An. coluzzii*; as the region grows, recombination "
    "breaks haplotypes up, so longer regions show less about the locus, not more. The summary "
    "compares each region with the smallest, and (for haplotypes) shows the swept haplotype's "
    "frequency, alongside the cost."
)

SPECS += [
    tree_or_pca(
        "pca_large_n_snps", "pca", "pca", "n_snps",
        "Does PCA keep changing with 100,000 to 1,000,000 SNPs?",
        ["**Samples.** All Ag3 3.0 samples outside the lab crosses, the same in every cell. "
         f"{GENOME_REGION} has about 3.6 million SNPs after the default filters.",
         "**Agreement.** Procrustes similarity of the samples' positions on the first 4 PCs.",
         SNP_REPLICATES],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "REGION": GENOME_REGION, "REFERENCE": 1_000_000,
         "REPLICATES": [1, 2]},
        [100_000, 200_000, 500_000, 1_000_000],
        "result = sweep.run(\n    ag3.pca, value=n_snps,<REP>\n"
        "    region=REGION, n_snps=n_snps, thin_offset=<THIN>,\n"
        "    sample_sets=SAMPLE_SETS, sample_query=SAMPLE_QUERY,\n)\n",
        "thin_offset", setup="",
    ),
    tree_or_pca(
        "pca_large_samples", "pca", "pca", "samples",
        "Does PCA keep changing with thousands of samples?",
        [ALL_RELEASES_NOTE.format(snps="5,000 SNPs from 3L:15,000,000-16,000,000"),
         "**Agreement.** Procrustes similarity, on the first 4 PCs, for the samples both runs contain. "
         "The summary also gives how well taxa separate.",
         LARGE_REFERENCE_NOTE, REPLICATES, NESTED],
        {"SAMPLE_SETS": None, "SAMPLE_QUERY": NON_LAB, "REGION": "3L:15,000,000-16,000,000", "N_SNPS": 5000,
         "REFERENCE": 10_000, "REPLICATES": [1, 2]},
        [1000, 2500, 5000, 10_000, 20_000],
        sample_call("pca", "region=REGION, n_snps=N_SNPS, sample_sets=SAMPLE_SETS,"),
        "seed",
    ),
    tree_or_pca(
        "pca_large_region", "pca", "pca", "region_length",
        "How much of the genome does PCA need before the structure it shows stops changing?",
        [REGION_NOTE + " All Ag3 3.0 samples outside the lab crosses; 5,000 SNPs.",
         REGION_AGREEMENT, SNP_REPLICATES],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "CONTIG": "3L", "START": 15_000_000, "N_SNPS": 5000,
         "REFERENCE": 26_000_000, "REPLICATES": [1, 2]},
        [100_000, 1_000_000, 5_000_000, 10_000_000, 26_000_000],
        REGION_CALL.replace("<DRAW>", "").replace("<METHOD>", "pca")
        .replace("<SAMPLES>", "    sample_query=SAMPLE_QUERY,\n"),
        "thin_offset", setup="", var="length",
    ),
    tree_or_pca(
        "njt_large_n_snps", "njt", "tree", "n_snps",
        "Does a neighbour-joining tree keep changing with 100,000 to 1,000,000 SNPs?",
        [f"**Samples.** 500 samples from Ag3 3.0 outside the lab crosses, the same in every cell; SNPs from {GENOME_REGION}.",
         "**Agreement.** Spearman correlation of the path lengths between pairs of samples through the "
         "tree, against the reference tree.",
         SNP_REPLICATES],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "REGION": GENOME_REGION, "SAMPLES": 500,
         "REFERENCE": 1_000_000, "REPLICATES": [1, 2]},
        [100_000, 200_000, 500_000, 1_000_000],
        FIXED_SAMPLES_SNPS_CALL,
        "thin_offset",
    ),
    tree_or_pca(
        "njt_large_samples", "njt", "tree", "samples",
        "Does a neighbour-joining tree keep changing with thousands of samples?",
        [ALL_RELEASES_NOTE.format(snps="5,000 SNPs from 3L:15,000,000-16,000,000"),
         "**Agreement.** Spearman correlation of the path lengths between pairs of samples through the "
         "tree, against the reference, for the samples both contain (estimated from 2 million random "
         "pairs when there are more).",
         "**Readability.** Trees above `plot_max_leaves` (2,000) aren't drawn: a tree of thousands of "
         "leaves can't be read whatever the server, which is itself a limit on what the plot shows. "
         "The 20,000-sample comparison holds two 20,000 × 20,000 path-length matrices (1.6 GB each).",
         LARGE_REFERENCE_NOTE, REPLICATES, NESTED],
        {"SAMPLE_SETS": None, "SAMPLE_QUERY": NON_LAB, "REGION": "3L:15,000,000-16,000,000", "N_SNPS": 5000,
         "REFERENCE": 10_000, "REPLICATES": [1, 2]},
        [1000, 2500, 5000, 10_000, 20_000],
        sample_call("njt", "region=REGION, n_snps=N_SNPS, sample_sets=SAMPLE_SETS,"),
        "seed",
    ),
    tree_or_pca(
        "njt_large_region", "njt", "tree", "region_length",
        "How much of the genome does a neighbour-joining tree need before it stops changing?",
        [REGION_NOTE.replace("100 kbp", "1 Mbp") + " 500 samples from Ag3 3.0 outside the lab crosses; 1,000 SNPs.",
         REGION_AGREEMENT, SNP_REPLICATES],
        {"SAMPLE_SETS": "3.0", "SAMPLE_QUERY": NON_LAB, "CONTIG": "3L", "START": 15_000_000, "SAMPLES": 500,
         "N_SNPS": 1000, "REFERENCE": 26_000_000, "REPLICATES": [1, 2]},
        [1_000_000, 5_000_000, 10_000_000, 20_000_000, 26_000_000],
        REGION_CALL.replace("<DRAW>", "ids = insight.subsample(pool, SAMPLES)\n").replace("<METHOD>", "njt")
        .replace("<SAMPLES>", '    sample_query="sample_id in @ids",\n'
                              '    sample_query_options={"local_dict": {"ids": ids}},\n'),
        "thin_offset", var="length",
    ),
]
for kind, method in [("haplotype", "haplotype_pairwise_distances"), ("diplotype", "diplotype_pairwise_distances")]:
    plural = kind + "s"
    SPECS += [
        tree_or_pca(
            f"{kind}_clustering_large_samples", method, plural, "samples",
            f"Does {kind} clustering keep changing with thousands of samples?",
            [f"**Region.** {CYP6_REGION}, the *Cyp6aa/Cyp6p* cluster, in Ghanaian *An. coluzzii* (3,282 "
             "samples in all Ag3 releases, so the largest value is 3,000). Pooling other populations to go "
             "further would change what the cluster frequencies mean.",
             "**Agreement.** Spearman correlation of the dendrogram (cophenetic) distances with the "
             "reference, for the leaves both contain."
             + (" The summary also shows the swept haplotype's frequency with a 95% interval; its "
                "precision follows the binomial (about ±1.6% at 3,000 haplotypes)." if kind == "haplotype" else ""),
             LARGE_REFERENCE_NOTE, REPLICATES, NESTED],
            {"SAMPLE_SETS": None, "SAMPLE_QUERY": GHANA_COLU, "REGION": CYP6_REGION, "REFERENCE": 2000,
             "REPLICATES": [1, 2]},
            [500, 1000, 1500, 2000, 3000],
            sample_call(method, "region=REGION, sample_sets=SAMPLE_SETS,"),
            "seed", color="sample_set", sweep_args=", plot_max_leaves=6000",
        ),
        tree_or_pca(
            f"{kind}_clustering_large_region", method, plural, "region_length",
            f"What does {kind} clustering show as the region grows from a locus to megabases?",
            [CLUSTER_REGION_NOTE],
            {"SAMPLE_SETS": None, "SAMPLE_QUERY": GHANA_COLU, "CONTIG": "2R", "CENTRE": 28_490_000,
             "SAMPLES": 200},
            [20_000, 100_000, 500_000, 1_000_000, 5_000_000],
            CENTRED_CALL.replace("<METHOD>", method),
            None, color="sample_set", var="length",
        ),
    ]
for method, stat in [("h12_gwss", "H12"), ("g123_gwss", "G123"), ("h1x_gwss", "H1X"), ("xpehh_gwss", "XP-EHH")]:
    SPECS.append(gwss_samples(method, stat, large=True))


def literal(value):
    return repr(value) if not isinstance(value, int) or value < 10_000 else f"{value:_}"


def fill(call, seed, rep, thin):
    return call.replace("<SEED>", seed).replace("<REP>", rep).replace("<THIN>", thin)


def value_cell(spec, value, replicate=None):
    var = spec["var"]
    if replicate is None:
        head = f"{var} = {literal(value)}\n"
        call = fill(spec["call"], seed="0", rep="", thin="0")
        tail = f"sweep.plot(result, value={var})\ndel result"
    else:
        head = f"{var}, replicate = REFERENCE, {replicate}\n"
        call = fill(
            spec["call"],
            seed="replicate" if spec["replicate"] == "seed" else "0",
            rep=" replicate=replicate,",
            thin="replicate" if spec["replicate"] == "thin_offset" else "0",
        )
        tail = f"sweep.plot(result, value={var}, replicate=replicate)\ndel result"
    return nbformat.v4.new_code_cell(head + call + tail)


def notebook(spec, timed=False):
    settings = "\n".join(f"{k} = {literal(v) if not isinstance(v, str) else json.dumps(v)}"
                         for k, v in spec["settings"].items())
    settings = settings.replace(" = null", " = None")
    intro = (
        f"# `{spec['method']}`: varying {spec['varied'].replace('_', ' ')}\n\n"
        f"{spec['question']}\n\n" + "\n\n".join(spec["notes"]) + "\n\n"
        "**Running.** Run the cells in order; each value cell can be run on its own after the set-up "
        "cells. Each saves its result and figure under `results/" + spec["name"] + "/` and appends "
        "its run time and peak memory to `results/" + spec["name"] + "_performance.csv`. Re-running a "
        "cell replaces its saved result. Run the summary cell at any point to compare what's saved so far."
    )
    if timed:
        intro += (
            "\n\n**Run time.** The summary also plots each value's run time. The first call in a session "
            "includes one-off loading (often a minute or more), so re-run the first value cell at the end "
            "before reading its time. This notebook shares its saved results with `" + spec["name"]
            + ".ipynb`, so if that has been run, the set-up cells and the summary cell are enough."
        )
    color = f", color={spec['color']!r}" if spec["color"] else ""
    metadata = "metadata=pool" if spec["setup"] else "metadata=None"
    cells = [
        nbformat.v4.new_markdown_cell(intro),
        nbformat.v4.new_code_cell("import malariagen_data\n\nimport insight"),
        nbformat.v4.new_code_cell("# Settings\n" + settings),
        nbformat.v4.new_code_cell('ag3 = malariagen_data.Ag3(\n    "simplecache::gs://vo_agam_release_master_us_central1",\n)\nag3'),
        nbformat.v4.new_code_cell(
            spec["setup"]
            + f"sweep = insight.Sweep({spec['name']!r}, varied={spec['varied']!r}, kind={spec['kind']!r}, "
            f"{metadata}{color}{spec.get('sweep_args', '')})"
        ),
        nbformat.v4.new_markdown_cell(
            f"## Values\n\n{spec['varied']}: " + ", ".join(f"{v:,}" for v in spec["values"])
        ),
    ]
    cells += [value_cell(spec, v) for v in spec["values"]]
    if spec["replicate"]:
        how = "different random samples" if spec["replicate"] == "seed" else "different `thin_offset`"
        cells.append(nbformat.v4.new_markdown_cell(
            f"## Replicates of the reference\n\nThe reference value again, with {how}."))
        cells += [value_cell(spec, None, r) for r in spec["settings"]["REPLICATES"]]
        summary = "table = sweep.summarise(reference=REFERENCE<RUNTIME>)\ntable"
    else:
        summary = "table = sweep.summarise(<RUNTIME>)\ntable"
    runtime = (", runtime=True" if spec["replicate"] else "runtime=True") if timed else ""
    summary = summary.replace("<RUNTIME>", runtime)
    cells += [nbformat.v4.new_markdown_cell("## Summary"), nbformat.v4.new_code_cell(summary)]
    nb = nbformat.v4.new_notebook(cells=cells, metadata=BASE_METADATA)
    nbformat.validate(nb)
    return nb


if __name__ == "__main__":
    for spec in SPECS:
        for timed in (False, True):
            path = HERE / f"{spec['name']}{'_timed' if timed else ''}.ipynb"
            nbformat.write(notebook(spec, timed), path)
            print(path.name)
