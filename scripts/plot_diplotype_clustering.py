#!/usr/bin/env python3
"""plot_diplotype_clustering: the code from notebooks/plot_diplotype_clustering.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_diplotype_clustering.py                      # the notebook's defaults
    python scripts/plot_diplotype_clustering.py --config runs.csv    # one run per CSV row
    python scripts/plot_diplotype_clustering.py --list-parameters    # what a CSV can set
    python scripts/plot_diplotype_clustering.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_diplotype_clustering_performance.csv'
API_CALL_PARAMETERS = {'cell_4_call_1_ag3_plot_diplotype_clustering_advanced': {'region': '2R:28,480,000-28,500,000',
                                                          'heterozygosity': True,
                                                          'heterozygosity_colorscale': 'Greys',
                                                          'snp_transcript': 'AGAP002862-RA',
                                                          'snp_colorscale': 'Greys',
                                                          'snp_filter_min_maf': 0.05,
                                                          'snp_query': 'effect in '
                                                                       "['NON_SYNONYMOUS_CODING', "
                                                                       "'START_LOST', 'STOP_LOST', "
                                                                       "'STOP_GAINED']",
                                                          'cnv_region': '2R:28,480,000-28,500,000',
                                                          'cnv_colorscale': None,
                                                          'cnv_max_coverage_variance': 0.2,
                                                          'site_mask': 'gamb_colu',
                                                          'sample_sets': 'AG1000G-GH',
                                                          'sample_query': None,
                                                          'sample_query_options': None,
                                                          'random_seed': 42,
                                                          'cohort_size': None,
                                                          'color': 'taxon',
                                                          'symbol': 'country',
                                                          'linkage_method': 'complete',
                                                          'distance_metric': 'cityblock',
                                                          'count_sort': True,
                                                          'distance_sort': False,
                                                          'title': True,
                                                          'title_font_size': 14,
                                                          'width': None,
                                                          'dendrogram_height': 300,
                                                          'heterozygosity_height': 25,
                                                          'snp_row_height': 25,
                                                          'cnv_row_height': 25,
                                                          'show': False,
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
 'cell_5_call_1_ag3_plot_diplotype_clustering_advanced': {'region': '2R:28,480,000-28,490,000',
                                                          'heterozygosity': True,
                                                          'heterozygosity_colorscale': 'Greys',
                                                          'snp_transcript': ['AGAP002862-RA',
                                                                             'AGAP002864-RA'],
                                                          'snp_colorscale': 'Greys',
                                                          'snp_filter_min_maf': 0.1,
                                                          'snp_query': 'effect == '
                                                                       "'NON_SYNONYMOUS_CODING'",
                                                          'cnv_region': None,
                                                          'cnv_colorscale': None,
                                                          'cnv_max_coverage_variance': 0.2,
                                                          'site_mask': 'gamb_colu',
                                                          'sample_sets': 'AG1000G-GH',
                                                          'sample_query': None,
                                                          'sample_query_options': None,
                                                          'random_seed': 42,
                                                          'cohort_size': None,
                                                          'color': 'taxon',
                                                          'symbol': 'country',
                                                          'linkage_method': 'complete',
                                                          'distance_metric': 'cityblock',
                                                          'count_sort': True,
                                                          'distance_sort': False,
                                                          'title': True,
                                                          'title_font_size': 14,
                                                          'width': None,
                                                          'dendrogram_height': 300,
                                                          'heterozygosity_height': 25,
                                                          'snp_row_height': 25,
                                                          'cnv_row_height': 25,
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
 'cell_6_call_1_ag3_plot_diplotype_clustering_advanced': {'region': '2R:28,480,000-28,500,000',
                                                          'heterozygosity': True,
                                                          'heterozygosity_colorscale': 'Greys',
                                                          'snp_transcript': None,
                                                          'snp_colorscale': 'Greys',
                                                          'snp_filter_min_maf': 0.05,
                                                          'snp_query': 'effect in '
                                                                       "['NON_SYNONYMOUS_CODING', "
                                                                       "'START_LOST', 'STOP_LOST', "
                                                                       "'STOP_GAINED']",
                                                          'cnv_region': '2R:28,480,000-28,500,000',
                                                          'cnv_colorscale': None,
                                                          'cnv_max_coverage_variance': 0.2,
                                                          'site_mask': 'gamb_colu',
                                                          'sample_sets': ['AG1000G-GH',
                                                                          'AG1000G-BF-A'],
                                                          'sample_query': None,
                                                          'sample_query_options': None,
                                                          'random_seed': 42,
                                                          'cohort_size': None,
                                                          'color': 'taxon',
                                                          'symbol': 'country',
                                                          'linkage_method': 'complete',
                                                          'distance_metric': 'cityblock',
                                                          'count_sort': True,
                                                          'distance_sort': False,
                                                          'title': True,
                                                          'title_font_size': 14,
                                                          'width': None,
                                                          'dendrogram_height': 300,
                                                          'heterozygosity_height': 25,
                                                          'snp_row_height': 25,
                                                          'cnv_row_height': 25,
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
 'cell_7_call_1_ag3_plot_diplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'site_mask': 'gamb_colu',
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': 'taxon',
                                                 'symbol': 'country',
                                                 'linkage_method': 'complete',
                                                 'distance_metric': 'cityblock',
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
 'cell_8_call_1_ag3_plot_diplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'site_mask': None,
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': 'taxon',
                                                 'symbol': 'country',
                                                 'linkage_method': 'complete',
                                                 'distance_metric': 'cityblock',
                                                 'count_sort': True,
                                                 'distance_sort': False,
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
 'cell_9_call_1_ag3_plot_diplotype_clustering': {'region': '2L:2,410,000-2,430,000',
                                                 'site_mask': 'gamb_colu',
                                                 'sample_sets': ['AG1000G-GH', 'AG1000G-BF-B'],
                                                 'sample_query': None,
                                                 'sample_query_options': None,
                                                 'cohort_size': None,
                                                 'random_seed': 42,
                                                 'color': 'country',
                                                 'symbol': 'taxon',
                                                 'linkage_method': 'single',
                                                 'distance_metric': 'cityblock',
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
 'cell_10_call_1_ag3_plot_diplotype_clustering': {'region': '2L:28,545,000-28,550,000',
                                                  'site_mask': 'gamb_colu',
                                                  'sample_sets': ['AG1000G-GH',
                                                                  '1244-VO-GH-YAWSON-VMF00051'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': 500,
                                                  'random_seed': 42,
                                                  'color': 'admin1_name',
                                                  'symbol': 'taxon',
                                                  'linkage_method': 'weighted',
                                                  'distance_metric': 'euclidean',
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
 'cell_11_call_1_ag3_plot_diplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'site_mask': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'sample_set',
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'cityblock',
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
 'cell_12_call_1_ag3_plot_diplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'site_mask': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'admin1_year',
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'cityblock',
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
 'cell_13_call_1_ag3_plot_diplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'site_mask': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'admin1_year',
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'cityblock',
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
 'cell_15_call_1_ag3_plot_diplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'site_mask': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': None,
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'euclidean',
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
 'cell_16_call_1_ag3_plot_diplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'site_mask': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': None,
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'cityblock',
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
 'cell_17_call_1_ag3_plot_diplotype_clustering': {'region': '2R:28,480,000-28,490,000',
                                                  'site_mask': 'gamb_colu_arab',
                                                  'sample_sets': ['3.0'],
                                                  'sample_query': "taxon == 'arabiensis'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'year',
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'cityblock',
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
 'cell_20_call_1_af1_plot_diplotype_clustering': {'region': '2RL:2,410,000-2,430,000',
                                                  'site_mask': 'default',
                                                  'sample_sets': ['1240-VO-CD-KOEKEMOER-VMF00099',
                                                                  '1240-VO-MZ-KOEKEMOER-VMF00101'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'sample_set',
                                                  'symbol': 'country',
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'euclidean',
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
 'cell_21_call_1_af1_plot_diplotype_clustering': {'region': '2RL:28,545,000-28,550,000',
                                                  'site_mask': 'default',
                                                  'sample_sets': ['1240-VO-CD-KOEKEMOER-VMF00099',
                                                                  '1240-VO-MZ-KOEKEMOER-VMF00101'],
                                                  'sample_query': None,
                                                  'sample_query_options': None,
                                                  'cohort_size': 80,
                                                  'random_seed': 42,
                                                  'color': 'country',
                                                  'symbol': 'sample_set',
                                                  'linkage_method': 'weighted',
                                                  'distance_metric': 'cityblock',
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
 'cell_22_call_1_af1_plot_diplotype_clustering': {'region': '2RL:28,480,000-28,490,000',
                                                  'site_mask': 'default',
                                                  'sample_sets': ['1.0'],
                                                  'sample_query': "country == 'Ghana'",
                                                  'sample_query_options': None,
                                                  'cohort_size': None,
                                                  'random_seed': 42,
                                                  'color': 'sample_set',
                                                  'symbol': None,
                                                  'linkage_method': 'complete',
                                                  'distance_metric': 'cityblock',
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
 'cell_23_call_1_af1_plot_diplotype_clustering_advanced': {'region': 'X:8,438,477-8,460,887',
                                                           'heterozygosity': True,
                                                           'heterozygosity_colorscale': 'Greys',
                                                           'snp_transcript': ['LOC125764232_t1'],
                                                           'snp_colorscale': 'Greys',
                                                           'snp_filter_min_maf': 0.05,
                                                           'snp_query': 'effect in '
                                                                        "['NON_SYNONYMOUS_CODING', "
                                                                        "'START_LOST', "
                                                                        "'STOP_LOST', "
                                                                        "'STOP_GAINED']",
                                                           'cnv_region': 'X:8,418,477-8,480,887',
                                                           'cnv_colorscale': None,
                                                           'cnv_max_coverage_variance': 0.2,
                                                           'site_mask': None,
                                                           'sample_sets': ['1232-VO-KE-OCHOMO-VMF00044',
                                                                           '1231-VO-MULTI-WONDJI-VMF00043',
                                                                           '1236-VO-TZ-OKUMU-VMF00090'],
                                                           'sample_query': "country in ['Kenya', "
                                                                           "'Uganda', 'Tanzania'] "
                                                                           'and taxon == '
                                                                           "'funestus'",
                                                           'sample_query_options': None,
                                                           'random_seed': 42,
                                                           'cohort_size': None,
                                                           'color': None,
                                                           'symbol': None,
                                                           'linkage_method': 'complete',
                                                           'distance_metric': 'cityblock',
                                                           'count_sort': None,
                                                           'distance_sort': None,
                                                           'title': True,
                                                           'title_font_size': 14,
                                                           'width': None,
                                                           'dendrogram_height': 300,
                                                           'heterozygosity_height': 25,
                                                           'snp_row_height': 25,
                                                           'cnv_row_height': 25,
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
FIGURE_DIR = 'figures/plot_diplotype_clustering'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'notebook_cell_5': '01_cell_5_figure',
 'cell_5_call_1_ag3_plot_diplotype_clustering_advanced': '02_ag3_diplotype_clustering_advanced_by_taxon',
 'cell_6_call_1_ag3_plot_diplotype_clustering_advanced': '03_ag3_diplotype_clustering_advanced_by_taxon',
 'cell_7_call_1_ag3_plot_diplotype_clustering': '04_ag3_diplotype_clustering_by_taxon',
 'cell_8_call_1_ag3_plot_diplotype_clustering': '05_ag3_diplotype_clustering_by_taxon',
 'cell_9_call_1_ag3_plot_diplotype_clustering': '06_ag3_diplotype_clustering_by_country',
 'cell_10_call_1_ag3_plot_diplotype_clustering': '07_ag3_diplotype_clustering_by_admin1_name',
 'cell_11_call_1_ag3_plot_diplotype_clustering': '08_ag3_diplotype_clustering_by_sample_set',
 'cell_12_call_1_ag3_plot_diplotype_clustering': '09_ag3_diplotype_clustering_by_admin1_year',
 'cell_13_call_1_ag3_plot_diplotype_clustering': '10_ag3_diplotype_clustering_by_admin1_year',
 'cell_15_call_1_ag3_plot_diplotype_clustering': '11_ag3_diplotype_clustering',
 'cell_16_call_1_ag3_plot_diplotype_clustering': '12_ag3_diplotype_clustering',
 'cell_17_call_1_ag3_plot_diplotype_clustering': '13_ag3_diplotype_clustering_by_year',
 'cell_20_call_1_af1_plot_diplotype_clustering': '14_af1_diplotype_clustering_by_sample_set',
 'cell_21_call_1_af1_plot_diplotype_clustering': '15_af1_diplotype_clustering_by_country',
 'cell_22_call_1_af1_plot_diplotype_clustering': '16_af1_diplotype_clustering_by_sample_set',
 'cell_23_call_1_af1_plot_diplotype_clustering_advanced': '17_af1_diplotype_clustering_advanced'}


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
    )
    nbrt.display(ag3)
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    fig = _call_api_with_parameters(ag3.plot_diplotype_clustering_advanced, 'cell_4_call_1_ag3_plot_diplotype_clustering_advanced', region="2R:28,480,000-28,500,000", cnv_region="2R:28,480,000-28,500,000", snp_transcript="AGAP002862-RA", snp_filter_min_maf=0.05, sample_sets="AG1000G-GH", site_mask="gamb_colu", color="taxon", symbol="country", linkage_method="complete", count_sort=True, distance_sort=False, show=False)
    nbrt.display(fig)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering_advanced, 'cell_5_call_1_ag3_plot_diplotype_clustering_advanced', region="2R:28,480,000-28,490,000", snp_transcript=["AGAP002862-RA", "AGAP002864-RA"], snp_query="effect == 'NON_SYNONYMOUS_CODING'", snp_filter_min_maf=0.1, sample_sets="AG1000G-GH", site_mask="gamb_colu", color="taxon", symbol="country", linkage_method="complete", count_sort=True, distance_sort=False))
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering_advanced, 'cell_6_call_1_ag3_plot_diplotype_clustering_advanced', region="2R:28,480,000-28,500,000", cnv_region="2R:28,480,000-28,500,000", snp_transcript=None, sample_sets=["AG1000G-GH", "AG1000G-BF-A"], snp_filter_min_maf=0.05, site_mask="gamb_colu", color="taxon", symbol="country", linkage_method="complete", count_sort=True, distance_sort=False))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_7_call_1_ag3_plot_diplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], site_mask="gamb_colu", color="taxon", symbol="country", linkage_method="complete", width=1000, height=500, count_sort=True, distance_sort=False))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_8_call_1_ag3_plot_diplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], site_mask=None, color="taxon", symbol="country", linkage_method="complete", count_sort=True, distance_sort=False, render_mode="svg"))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_9_call_1_ag3_plot_diplotype_clustering', region="2L:2,410,000-2,430,000", sample_sets=["AG1000G-GH", "AG1000G-BF-B"], site_mask="gamb_colu", color="country", symbol="taxon", linkage_method="single", width=1000, height=500, count_sort=True, distance_sort=False, render_mode="webgl"))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_10_call_1_ag3_plot_diplotype_clustering', region="2L:28,545,000-28,550,000", sample_sets=["AG1000G-GH", "1244-VO-GH-YAWSON-VMF00051"], site_mask="gamb_colu", color="admin1_name", symbol="taxon", cohort_size=500, linkage_method="weighted", distance_metric="euclidean", count_sort=True, width=1200, height=600))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_11_call_1_ag3_plot_diplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", site_mask="gamb_colu_arab", color="sample_set", cohort_size=None, width=1000, height=400))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_12_call_1_ag3_plot_diplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", site_mask="gamb_colu_arab", color="admin1_year", cohort_size=None, width=1000, height=400))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_13_call_1_ag3_plot_diplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", site_mask="gamb_colu_arab", color="admin1_year", cohort_size=None, width=1000, height=400, title=None))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    new_cohorts = {
        "East": "country in ['Malawi', 'Tanzania', 'Kenya', 'Uganda']",
        "West": "country in ['Mali', 'Burkina Faso', 'Cameroon']",
    }
    other_cohorts = {
        "East": "country in ['Malawi']",
        "West": "country in ['Mali', 'Burkina Faso', 'Cameroon']",
    }
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_15_call_1_ag3_plot_diplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", distance_metric="euclidean", site_mask="gamb_colu_arab", color=new_cohorts, cohort_size=None, width=1000, height=400))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_16_call_1_ag3_plot_diplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", site_mask="gamb_colu_arab", color=other_cohorts, cohort_size=None, width=1000, height=400))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(ag3.plot_diplotype_clustering, 'cell_17_call_1_ag3_plot_diplotype_clustering', region="2R:28,480,000-28,490,000", sample_sets=["3.0"], sample_query="taxon == 'arabiensis'", site_mask="gamb_colu_arab", symbol=new_cohorts, color="year", cohort_size=None, width=1000, height=400))
    # ## Af1
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        debug=False,
        pre=True,
    )
    nbrt.display(af1)
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    nbrt.display(_call_api_with_parameters(af1.plot_diplotype_clustering, 'cell_20_call_1_af1_plot_diplotype_clustering', region="2RL:2,410,000-2,430,000", sample_sets=["1240-VO-CD-KOEKEMOER-VMF00099", "1240-VO-MZ-KOEKEMOER-VMF00101"], color="sample_set", symbol="country", linkage_method="complete", distance_metric="euclidean", width=1000, height=500, count_sort=True, distance_sort=False))
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(_call_api_with_parameters(af1.plot_diplotype_clustering, 'cell_21_call_1_af1_plot_diplotype_clustering', region="2RL:28,545,000-28,550,000", sample_sets=["1240-VO-CD-KOEKEMOER-VMF00099", "1240-VO-MZ-KOEKEMOER-VMF00101"], color="country", symbol="sample_set", cohort_size=80, linkage_method="weighted", count_sort=True, width=1200, height=600))
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    nbrt.display(_call_api_with_parameters(af1.plot_diplotype_clustering, 'cell_22_call_1_af1_plot_diplotype_clustering', region="2RL:28,480,000-28,490,000", sample_sets=["1.0"], sample_query="country == 'Ghana'", color="sample_set", cohort_size=None, width=1000, height=400))
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(af1.plot_diplotype_clustering_advanced, 'cell_23_call_1_af1_plot_diplotype_clustering_advanced', region="X:8,438,477-8,460,887", snp_transcript=["LOC125764232_t1"], cnv_region="X:8,418,477-8,480,887", sample_sets=[
            "1232-VO-KE-OCHOMO-VMF00044",
            "1231-VO-MULTI-WONDJI-VMF00043",
            "1236-VO-TZ-OKUMU-VMF00090",
        ], sample_query="country in ['Kenya', 'Uganda', 'Tanzania'] and taxon == 'funestus'"))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_diplotype_clustering.ipynb',
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
