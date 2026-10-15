#!/usr/bin/env python3
"""plot_haplotype_clustering: the code from notebooks/plot_haplotype_clustering.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_haplotype_clustering.py                      # the notebook's defaults
    python scripts/plot_haplotype_clustering.py --config runs.csv    # one run per CSV row
    python scripts/plot_haplotype_clustering.py --list-parameters    # what a CSV can set
    python scripts/plot_haplotype_clustering.py --output-csv my_run.csv
                                    # performance CSV -> executed_runs_scripts/my_run.csv

CSV columns are parameter names (API_KEEP_CALLSITE_VALUE, PERFORMANCE_CSV_PATH, API_CALL_PARAMETERS, FIGURE_DIR, FIGURE_FORMAT, FIGURE_NAMES).
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
# Relative to where the script is run from.
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_haplotype_clustering_performance.csv'
API_CALL_PARAMETERS = {'cell_6_call_1_ag3_plot_haplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'analysis': 'gamb_colu',
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': None,
                                                 'symbol': None,
                                                 'linkage_method': 'single',
                                                 'distance_metric': 'hamming',
                                                 'count_sort': None,
                                                 'distance_sort': None,
                                                 'title': True,
                                                 'title_font_size': 14,
                                                 'width': None,
                                                 'height': 500,
                                                 'show': True,
                                                 'renderer': None,
                                                 'render_mode': 'svg',
                                                 'leaf_y': 0,
                                                 'marker_size': 5,
                                                 'line_width': 0.5,
                                                 'line_color': 'black',
                                                 'color_discrete_sequence': None,
                                                 'color_discrete_map': None,
                                                 'category_orders': None,
                                                 'legend_sizing': 'constant',
                                                 'chunks': 'native',
                                                 'inline_array': True},
 'cell_7_call_1_ag3_plot_haplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'analysis': 'gamb_colu',
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': 'taxon',
                                                 'symbol': 'country',
                                                 'linkage_method': 'single',
                                                 'distance_metric': 'hamming',
                                                 'count_sort': None,
                                                 'distance_sort': None,
                                                 'title': True,
                                                 'title_font_size': 14,
                                                 'width': None,
                                                 'height': 500,
                                                 'show': True,
                                                 'renderer': None,
                                                 'render_mode': 'svg',
                                                 'leaf_y': 0,
                                                 'marker_size': 5,
                                                 'line_width': 0.5,
                                                 'line_color': 'black',
                                                 'color_discrete_sequence': None,
                                                 'color_discrete_map': None,
                                                 'category_orders': None,
                                                 'legend_sizing': 'constant',
                                                 'chunks': 'native',
                                                 'inline_array': True},
 'cell_8_call_1_ag3_plot_haplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'analysis': 'gamb_colu',
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': 'taxon',
                                                 'symbol': 'country',
                                                 'linkage_method': 'single',
                                                 'distance_metric': 'hamming',
                                                 'count_sort': True,
                                                 'distance_sort': False,
                                                 'title': True,
                                                 'title_font_size': 14,
                                                 'width': 1000,
                                                 'height': 500,
                                                 'show': True,
                                                 'renderer': None,
                                                 'render_mode': 'svg',
                                                 'leaf_y': 0,
                                                 'marker_size': 5,
                                                 'line_width': 0.5,
                                                 'line_color': 'black',
                                                 'color_discrete_sequence': None,
                                                 'color_discrete_map': None,
                                                 'category_orders': None,
                                                 'legend_sizing': 'constant',
                                                 'chunks': 'native',
                                                 'inline_array': True},
 'cell_9_call_1_ag3_plot_haplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'analysis': 'gamb_colu',
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': 'taxon',
                                                 'symbol': 'country',
                                                 'linkage_method': 'single',
                                                 'distance_metric': 'hamming',
                                                 'count_sort': True,
                                                 'distance_sort': False,
                                                 'title': True,
                                                 'title_font_size': 14,
                                                 'width': 1000,
                                                 'height': 500,
                                                 'show': True,
                                                 'renderer': None,
                                                 'render_mode': 'svg',
                                                 'leaf_y': 0,
                                                 'marker_size': 5,
                                                 'line_width': 0.5,
                                                 'line_color': 'black',
                                                 'color_discrete_sequence': None,
                                                 'color_discrete_map': None,
                                                 'category_orders': None,
                                                 'legend_sizing': 'constant',
                                                 'chunks': 'native',
                                                 'inline_array': True},
 'cell_10_call_1_ag3_plot_haplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                  'analysis': 'gamb_colu',
                                                  'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'country',
                                                  'symbol': 'taxon',
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': True,
                                                  'distance_sort': False,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 500,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'webgl',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_11_call_1_ag3_plot_haplotype_clustering': {'region': '2L:28,545,000-28,550,000',
                                                  'analysis': 'gamb_colu',
                                                  'sample_sets': ['AG1000G-GH',
                                                                  '1244-VO-GH-YAWSON-VMF00051'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': 500,
                                                  'random_seed': 42,
                                                  'color': 'admin1_name',
                                                  'symbol': 'taxon',
                                                  'linkage_method': 'weighted',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': True,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1200,
                                                  'height': 600,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_12_call_1_ag3_plot_haplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'analysis': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'sample_set',
                                                  'symbol': None,
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': None,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 400,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_13_call_1_ag3_plot_haplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'analysis': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'admin1_year',
                                                  'symbol': None,
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': None,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 400,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_14_call_1_ag3_plot_haplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'analysis': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'admin1_year',
                                                  'symbol': None,
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': None,
                                                  'distance_sort': None,
                                                  'title': None,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 400,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_16_call_1_ag3_plot_haplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'analysis': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': None,
                                                  'symbol': None,
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': None,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 400,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_17_call_1_ag3_plot_haplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'analysis': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': None,
                                                  'symbol': None,
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': None,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 400,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_18_call_1_ag3_plot_haplotype_clustering_advanced': {'region': '2R:28,480,000-28,490,000',
                                                           'analysis': 'gamb_colu_arab',
                                                           'snp_transcript': 'AGAP002863-RA',
                                                           'snp_colorscale': 'Greys',
                                                           'snp_filter_min_maf': 0.05,
                                                           'snp_query': 'effect in '
                                                                        "['NON_SYNONYMOUS_CODING', "
                                                                        "'START_LOST', "
                                                                        "'STOP_LOST', "
                                                                        "'STOP_GAINED']",
                                                           'sample_sets': ['3.0'],
                                                           'sample_query': "taxon == 'arabiensis'",
                                                           'sample_query_options': None,
                                                           'random_seed': 42,
                                                           'cohort_size': None,
                                                           'distance_metric': 'hamming',
                                                           'cluster_threshold': None,
                                                           'min_cluster_size': 5,
                                                           'cluster_criterion': 'distance',
                                                           'color': 'year',
                                                           'symbol': None,
                                                           'linkage_method': 'complete',
                                                           'count_sort': None,
                                                           'distance_sort': None,
                                                           'title': True,
                                                           'title_font_size': 14,
                                                           'width': None,
                                                           'dendrogram_height': 300,
                                                           'snp_row_height': 25,
                                                           'show': True,
                                                           'renderer': None,
                                                           'render_mode': 'svg',
                                                           'leaf_y': 0,
                                                           'marker_size': 5,
                                                           'line_width': 0.5,
                                                           'line_color': 'black',
                                                           'color_discrete_sequence': None,
                                                           'color_discrete_map': None,
                                                           'category_orders': None,
                                                           'legend_sizing': 'constant',
                                                           'chunks': 'native',
                                                           'inline_array': True},
 'cell_19_call_1_ag3_plot_haplotype_clustering_advanced': {'region': '2L:2,360,000-2,431,000',
                                                           'analysis': 'gamb_colu',
                                                           'snp_transcript': 'AGAP004707-RD',
                                                           'snp_colorscale': 'Greys',
                                                           'snp_filter_min_maf': 0.05,
                                                           'snp_query': 'effect in '
                                                                        "['NON_SYNONYMOUS_CODING', "
                                                                        "'START_LOST', "
                                                                        "'STOP_LOST', "
                                                                        "'STOP_GAINED']",
                                                           'sample_sets': ['AG1000G-GH'],
                                                           'sample_query': None,
                                                           'sample_query_options': None,
                                                           'random_seed': 42,
                                                           'cohort_size': None,
                                                           'distance_metric': 'dxy',
                                                           'cluster_threshold': 0.0007,
                                                           'min_cluster_size': 5,
                                                           'cluster_criterion': 'distance',
                                                           'color': 'taxon',
                                                           'symbol': None,
                                                           'linkage_method': 'complete',
                                                           'count_sort': None,
                                                           'distance_sort': None,
                                                           'title': True,
                                                           'title_font_size': 14,
                                                           'width': None,
                                                           'dendrogram_height': 300,
                                                           'snp_row_height': 25,
                                                           'show': True,
                                                           'renderer': None,
                                                           'render_mode': 'svg',
                                                           'leaf_y': 0,
                                                           'marker_size': 5,
                                                           'line_width': 0.5,
                                                           'line_color': 'black',
                                                           'color_discrete_sequence': None,
                                                           'color_discrete_map': None,
                                                           'category_orders': None,
                                                           'legend_sizing': 'constant',
                                                           'chunks': 'native',
                                                           'inline_array': True},
 'cell_22_call_1_af1_plot_haplotype_clustering': {'region': '2RL:2,410,000-2,430,000',
                                                  'analysis': 'default',
                                                  'sample_sets': ['1240-VO-CD-KOEKEMOER-VMF00099',
                                                                  '1240-VO-MZ-KOEKEMOER-VMF00101'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'sample_set',
                                                  'symbol': 'country',
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': True,
                                                  'distance_sort': False,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 500,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_23_call_1_af1_plot_haplotype_clustering': {'region': '2RL:28,545,000-28,550,000',
                                                  'analysis': 'default',
                                                  'sample_sets': ['1240-VO-CD-KOEKEMOER-VMF00099',
                                                                  '1240-VO-MZ-KOEKEMOER-VMF00101'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': 80,
                                                  'random_seed': 42,
                                                  'color': 'country',
                                                  'symbol': 'sample_set',
                                                  'linkage_method': 'weighted',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': True,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1200,
                                                  'height': 600,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True},
 'cell_24_call_1_af1_plot_haplotype_clustering': {'region': '2RL:28,480,000-28,490,000',
                                                  'analysis': 'default',
                                                  'sample_sets': ['1.0'],
                                                  'sample_query': "country == 'Ghana'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'sample_set',
                                                  'symbol': None,
                                                  'linkage_method': 'single',
                                                  'distance_metric': 'hamming',
                                                  'count_sort': None,
                                                  'distance_sort': None,
                                                  'title': True,
                                                  'title_font_size': 14,
                                                  'width': 1000,
                                                  'height': 400,
                                                  'show': True,
                                                  'renderer': None,
                                                  'render_mode': 'svg',
                                                  'leaf_y': 0,
                                                  'marker_size': 5,
                                                  'line_width': 0.5,
                                                  'line_color': 'black',
                                                  'color_discrete_sequence': None,
                                                  'color_discrete_map': None,
                                                  'category_orders': None,
                                                  'legend_sizing': 'constant',
                                                  'chunks': 'native',
                                                  'inline_array': True}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_haplotype_clustering'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_6_call_1_ag3_plot_haplotype_clustering': '01_ag3_haplotype_clustering',
 'cell_7_call_1_ag3_plot_haplotype_clustering': '02_ag3_haplotype_clustering_by_taxon',
 'cell_8_call_1_ag3_plot_haplotype_clustering': '03_ag3_haplotype_clustering_by_taxon',
 'cell_9_call_1_ag3_plot_haplotype_clustering': '04_ag3_haplotype_clustering_by_taxon',
 'cell_10_call_1_ag3_plot_haplotype_clustering': '05_ag3_haplotype_clustering_by_country',
 'cell_11_call_1_ag3_plot_haplotype_clustering': '06_ag3_haplotype_clustering_by_admin1_name',
 'cell_12_call_1_ag3_plot_haplotype_clustering': '07_ag3_haplotype_clustering_by_sample_set',
 'cell_13_call_1_ag3_plot_haplotype_clustering': '08_ag3_haplotype_clustering_by_admin1_year',
 'cell_14_call_1_ag3_plot_haplotype_clustering': '09_ag3_haplotype_clustering_by_admin1_year',
 'cell_16_call_1_ag3_plot_haplotype_clustering': '10_ag3_haplotype_clustering',
 'cell_17_call_1_ag3_plot_haplotype_clustering': '11_ag3_haplotype_clustering',
 'cell_18_call_1_ag3_plot_haplotype_clustering_advanced': '12_ag3_haplotype_clustering_advanced_by_year',
 'cell_19_call_1_ag3_plot_haplotype_clustering_advanced': '13_ag3_haplotype_clustering_advanced_by_taxon',
 'cell_22_call_1_af1_plot_haplotype_clustering': '14_af1_haplotype_clustering_by_sample_set',
 'cell_23_call_1_af1_plot_haplotype_clustering': '15_af1_haplotype_clustering_by_country',
 'cell_24_call_1_af1_plot_haplotype_clustering': '16_af1_haplotype_clustering_by_sample_set'}


def run(API_KEEP_CALLSITE_VALUE, PERFORMANCE_CSV_PATH, API_CALL_PARAMETERS):
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
    # ## Ag3
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
        pre=True,
    )
    nbrt.display(ag3)
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    # %%time
    # ag3.plot_haplotype_clustering(
    #     region="2L:2,410,000-2,430,000",
    #     sample_sets=["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7"],
    #     analysis="gamb_colu",
    #     color="taxon",
    #     symbol="country",
    #     linkage_method="single",
    #     width=1000,
    #     height=500,
    #     count_sort=True,
    #     distance_sort=False,
    #     render_mode="auto",
    #     show=False,
    # );
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    # ag3.plot_haplotype_clustering(
    #     region="2L:2,410,000-2,430,000",
    #     sample_sets=["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7"],
    #     analysis="gamb_colu",
    #     color="country",
    #     linkage_method="single",
    #     width=None,
    #     height=500,
    #     count_sort=True,
    # )
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_6_call_1_ag3_plot_haplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], analysis="gamb_colu"))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_7_call_1_ag3_plot_haplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], analysis="gamb_colu", color="taxon", symbol="country"))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_8_call_1_ag3_plot_haplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], analysis="gamb_colu", color="taxon", symbol="country", linkage_method="single", width=1000, height=500, count_sort=True, distance_sort=False))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_9_call_1_ag3_plot_haplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], analysis="gamb_colu", color="taxon", symbol="country", linkage_method="single", width=1000, height=500, count_sort=True, distance_sort=False, render_mode="svg"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_10_call_1_ag3_plot_haplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], analysis="gamb_colu", color="country", symbol="taxon", linkage_method="single", width=1000, height=500, count_sort=True, distance_sort=False, render_mode="webgl"))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_11_call_1_ag3_plot_haplotype_clustering', region="2L:28,545,000-28,550,000", sample_sets=["AG1000G-GH", "1244-VO-GH-YAWSON-VMF00051"], analysis="gamb_colu", color="admin1_name", symbol="taxon", cohort_size=500, linkage_method="weighted", count_sort=True, width=1200, height=600))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_12_call_1_ag3_plot_haplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", analysis="gamb_colu_arab", color="sample_set", cohort_size=None, width=1000, height=400))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_13_call_1_ag3_plot_haplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", analysis="gamb_colu_arab", color="admin1_year", cohort_size=None, width=1000, height=400))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_14_call_1_ag3_plot_haplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", analysis="gamb_colu_arab", color="admin1_year", cohort_size=None, width=1000, height=400, title=None))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    new_cohorts = {
        "East": "country in ['Malawi', 'Tanzania', 'Kenya', 'Uganda']",
        "West": "country in ['Mali', 'Burkina Faso', 'Cameroon']",
    }
    other_cohorts = {
        "East": "country in ['Malawi']",
        "West": "country in ['Mali', 'Burkina Faso', 'Cameroon']",
    }
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_16_call_1_ag3_plot_haplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", analysis="gamb_colu_arab", color=new_cohorts, cohort_size=None, width=1000, height=400))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering, 'cell_17_call_1_ag3_plot_haplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", analysis="gamb_colu_arab", color=other_cohorts, cohort_size=None, width=1000, height=400))
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering_advanced, 'cell_18_call_1_ag3_plot_haplotype_clustering_advanced', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", analysis="gamb_colu_arab", symbol=new_cohorts, color="year", cohort_size=None, snp_transcript="AGAP002863-RA", distance_metric='hamming', snp_filter_min_maf=0.05))
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(ag3.plot_haplotype_clustering_advanced, 'cell_19_call_1_ag3_plot_haplotype_clustering_advanced', region="2L:2,360,000-2,431,000", sample_sets=["AG1000G-GH"], analysis="gamb_colu", color="taxon", cohort_size=None, snp_transcript="AGAP004707-RD", distance_metric='dxy', cluster_criterion='distance', cluster_threshold=0.0007, min_cluster_size=5, snp_filter_min_maf=0.05, show=True))
    # ## Af1
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
        pre=True,
    )
    nbrt.display(af1)
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_clustering, 'cell_22_call_1_af1_plot_haplotype_clustering', region="2RL:2,410,000-2,430,000", sample_sets=["1240-VO-CD-KOEKEMOER-VMF00099", "1240-VO-MZ-KOEKEMOER-VMF00101"], color="sample_set", symbol="country", linkage_method="single", width=1000, height=500, count_sort=True, distance_sort=False))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_clustering, 'cell_23_call_1_af1_plot_haplotype_clustering', region="2RL:28,545,000-28,550,000", sample_sets=["1240-VO-CD-KOEKEMOER-VMF00099", "1240-VO-MZ-KOEKEMOER-VMF00101"], color="country", symbol="sample_set", cohort_size=80, linkage_method="weighted", count_sort=True, width=1200, height=600))
    # --- Notebook cell 25 ---
    nbrt.start_cell("notebook_cell_25")
    nbrt.display(_call_api_with_parameters(af1.plot_haplotype_clustering, 'cell_24_call_1_af1_plot_haplotype_clustering', region="2RL:28,480,000-28,490,000", sample_sets=["1.0"], sample_query="country == 'Ghana'", color="sample_set", cohort_size=None, width=1000, height=400))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_haplotype_clustering.ipynb',
        run=run,
        parameters={
            'API_KEEP_CALLSITE_VALUE': API_KEEP_CALLSITE_VALUE,
            'PERFORMANCE_CSV_PATH': PERFORMANCE_CSV_PATH,
            'API_CALL_PARAMETERS': API_CALL_PARAMETERS,
            'FIGURE_DIR': FIGURE_DIR,
            'FIGURE_FORMAT': FIGURE_FORMAT,
            'FIGURE_NAMES': FIGURE_NAMES,
        },
    )
