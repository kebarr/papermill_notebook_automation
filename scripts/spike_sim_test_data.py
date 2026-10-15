#!/usr/bin/env python3
"""spike_sim_test_data: the code from notebooks/spike_sim_test_data.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/spike_sim_test_data.py                      # the notebook's defaults
    python scripts/spike_sim_test_data.py --config runs.csv    # one run per CSV row
    python scripts/spike_sim_test_data.py --list-parameters    # what a CSV can set

CSV columns are parameter names (API_KEEP_CALLSITE_VALUE, API_CALL_PARAMETERS, FIGURE_DIR, FIGURE_FORMAT, FIGURE_NAMES).
Values are JSON; empty cells keep the default. API_CALL_PARAMETERS and
FIGURE_NAMES only need the entries you want to change.

Generated from the notebook by notebook_to_script.py.
"""

import notebook_runtime as nbrt

# ---------------------------------------------------------------------------
# Parameters (the notebook's "parameters" cell)
# ---------------------------------------------------------------------------

# Malariagen API arguments for each call below.
# Replace a value to override it; keep the marker to use the call-site
# value or the method's default.
API_KEEP_CALLSITE_VALUE = '__KEEP_CALLSITE_VALUE__'
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

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/spike_sim_test_data'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
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


def run(API_KEEP_CALLSITE_VALUE, API_CALL_PARAMETERS):
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


if __name__ == "__main__":
    nbrt.main(
        notebook='spike_sim_test_data.ipynb',
        run=run,
        parameters={
            'API_KEEP_CALLSITE_VALUE': API_KEEP_CALLSITE_VALUE,
            'API_CALL_PARAMETERS': API_CALL_PARAMETERS,
            'FIGURE_DIR': FIGURE_DIR,
            'FIGURE_FORMAT': FIGURE_FORMAT,
            'FIGURE_NAMES': FIGURE_NAMES,
        },
    )
