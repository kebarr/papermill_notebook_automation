#!/usr/bin/env python3
"""plot_njt: the code from notebooks_fixed_parameters_cells/plot_njt.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_njt.py                      # the notebook's defaults
    python scripts/plot_njt.py --config runs.csv    # one run per CSV row
    python scripts/plot_njt.py --list-parameters    # what a CSV can set
    python scripts/plot_njt.py --output-csv my_run.csv
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
PERFORMANCE_CSV_PATH = 'executed_runs_scripts/plot_njt_performance.csv'
API_CALL_PARAMETERS = {'cell_4_call_1_ag3_njt': {'region': '3L:15,000,000-16,000,000',
                           'n_snps': 10000,
                           'algorithm': 'dynamic',
                           'metric': 'cityblock',
                           'thin_offset': 0,
                           'sample_sets': 'AG1000G-BF-A',
                           'sample_query': None,
                           'sample_query_options': None,
                           'sample_indices': None,
                           'site_mask': 'default',
                           'site_class': None,
                           'min_minor_ac': 2,
                           'max_missing_an': 0,
                           'cohort_size': None,
                           'min_cohort_size': None,
                           'max_cohort_size': None,
                           'random_seed': 42,
                           'inline_array': True,
                           'chunks': 'native'},
 'cell_5_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                'n_snps': 10000,
                                'color': None,
                                'symbol': None,
                                'algorithm': 'dynamic',
                                'metric': 'cityblock',
                                'distance_sort': None,
                                'count_sort': None,
                                'center_x': 0,
                                'center_y': 0,
                                'arc_start': 0,
                                'arc_stop': 6.283185307179586,
                                'width': 800,
                                'height': 600,
                                'show': True,
                                'renderer': None,
                                'render_mode': 'svg',
                                'title': True,
                                'title_font_size': 14,
                                'line_width': 0.5,
                                'marker_size': 5,
                                'color_discrete_sequence': None,
                                'color_discrete_map': None,
                                'category_orders': None,
                                'edge_legend': False,
                                'leaf_legend': False,
                                'legend_sizing': 'constant',
                                'thin_offset': 0,
                                'sample_sets': 'AG1000G-BF-A',
                                'sample_query': None,
                                'sample_query_options': None,
                                'sample_indices': None,
                                'site_mask': 'default',
                                'site_class': None,
                                'min_minor_ac': 2,
                                'max_missing_an': 0,
                                'cohort_size': None,
                                'min_cohort_size': None,
                                'max_cohort_size': None,
                                'random_seed': 42,
                                'inline_array': True,
                                'chunks': 'native'},
 'cell_6_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                'n_snps': 10000,
                                'color': 'taxon',
                                'symbol': None,
                                'algorithm': 'dynamic',
                                'metric': 'cityblock',
                                'distance_sort': None,
                                'count_sort': None,
                                'center_x': 0,
                                'center_y': 0,
                                'arc_start': 0,
                                'arc_stop': 6.283185307179586,
                                'width': 700,
                                'height': 600,
                                'show': True,
                                'renderer': None,
                                'render_mode': 'svg',
                                'title': True,
                                'title_font_size': 14,
                                'line_width': 0.5,
                                'marker_size': 5,
                                'color_discrete_sequence': None,
                                'color_discrete_map': None,
                                'category_orders': None,
                                'edge_legend': False,
                                'leaf_legend': True,
                                'legend_sizing': 'constant',
                                'thin_offset': 0,
                                'sample_sets': 'AG1000G-BF-A',
                                'sample_query': None,
                                'sample_query_options': None,
                                'sample_indices': None,
                                'site_mask': 'default',
                                'site_class': None,
                                'min_minor_ac': 2,
                                'max_missing_an': 0,
                                'cohort_size': None,
                                'min_cohort_size': None,
                                'max_cohort_size': None,
                                'random_seed': 42,
                                'inline_array': True,
                                'chunks': 'native'},
 'cell_7_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                'n_snps': 10000,
                                'color': 'taxon',
                                'symbol': None,
                                'algorithm': 'dynamic',
                                'metric': 'cityblock',
                                'distance_sort': None,
                                'count_sort': None,
                                'center_x': 0,
                                'center_y': 0,
                                'arc_start': 0,
                                'arc_stop': 6.283185307179586,
                                'width': 700,
                                'height': 600,
                                'show': True,
                                'renderer': None,
                                'render_mode': 'svg',
                                'title': True,
                                'title_font_size': 14,
                                'line_width': 0.5,
                                'marker_size': 5,
                                'color_discrete_sequence': None,
                                'color_discrete_map': None,
                                'category_orders': '__KEEP_CALLSITE_VALUE__',
                                'edge_legend': False,
                                'leaf_legend': True,
                                'legend_sizing': 'constant',
                                'thin_offset': 0,
                                'sample_sets': 'AG1000G-BF-A',
                                'sample_query': None,
                                'sample_query_options': None,
                                'sample_indices': None,
                                'site_mask': 'default',
                                'site_class': None,
                                'min_minor_ac': 2,
                                'max_missing_an': 0,
                                'cohort_size': None,
                                'min_cohort_size': None,
                                'max_cohort_size': None,
                                'random_seed': 42,
                                'inline_array': True,
                                'chunks': 'native'},
 'cell_8_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                'n_snps': 10000,
                                'color': 'taxon',
                                'symbol': None,
                                'algorithm': 'dynamic',
                                'metric': 'cityblock',
                                'distance_sort': None,
                                'count_sort': None,
                                'center_x': 0,
                                'center_y': 0,
                                'arc_start': 0,
                                'arc_stop': 6.283185307179586,
                                'width': 700,
                                'height': 600,
                                'show': True,
                                'renderer': None,
                                'render_mode': 'svg',
                                'title': True,
                                'title_font_size': 14,
                                'line_width': 0.5,
                                'marker_size': 5,
                                'color_discrete_sequence': None,
                                'color_discrete_map': None,
                                'category_orders': None,
                                'edge_legend': True,
                                'leaf_legend': True,
                                'legend_sizing': 'constant',
                                'thin_offset': 0,
                                'sample_sets': 'AG1000G-BF-A',
                                'sample_query': None,
                                'sample_query_options': None,
                                'sample_indices': None,
                                'site_mask': 'default',
                                'site_class': None,
                                'min_minor_ac': 2,
                                'max_missing_an': 0,
                                'cohort_size': None,
                                'min_cohort_size': None,
                                'max_cohort_size': None,
                                'random_seed': 42,
                                'inline_array': True,
                                'chunks': 'native'},
 'cell_9_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                'n_snps': 10000,
                                'color': 'taxon',
                                'symbol': None,
                                'algorithm': 'dynamic',
                                'metric': 'cityblock',
                                'distance_sort': None,
                                'count_sort': None,
                                'center_x': 0,
                                'center_y': 0,
                                'arc_start': 0,
                                'arc_stop': 6.283185307179586,
                                'width': 700,
                                'height': 600,
                                'show': True,
                                'renderer': None,
                                'render_mode': 'svg',
                                'title': True,
                                'title_font_size': 14,
                                'line_width': 0.5,
                                'marker_size': 5,
                                'color_discrete_sequence': None,
                                'color_discrete_map': None,
                                'category_orders': None,
                                'edge_legend': True,
                                'leaf_legend': False,
                                'legend_sizing': 'constant',
                                'thin_offset': 0,
                                'sample_sets': 'AG1000G-BF-A',
                                'sample_query': None,
                                'sample_query_options': None,
                                'sample_indices': None,
                                'site_mask': 'default',
                                'site_class': None,
                                'min_minor_ac': 2,
                                'max_missing_an': 0,
                                'cohort_size': None,
                                'min_cohort_size': None,
                                'max_cohort_size': None,
                                'random_seed': 42,
                                'inline_array': True,
                                'chunks': 'native'},
 'cell_10_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'taxon',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': True,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': 'AG1000G-BF-A',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_11_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'location',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': 'AG1000G-BF-A',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_12_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'location',
                                 'symbol': 'taxon',
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 10,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': 'AG1000G-BF-A',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_13_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'location',
                                 'symbol': 'taxon',
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': None,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': False,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': 'AG1000G-BF-A',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_14_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'admin1_year',
                                 'symbol': 'taxon',
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': ['AG1000G-BF-A',
                                                 'AG1000G-BF-B'],
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_15_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'taxon',
                                 'symbol': 'admin2_month',
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': ['AG1000G-BF-A',
                                                 'AG1000G-BF-B'],
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_16_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'country',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': ['AG1000G-BF-A', 'AG1000G-UG'],
                                 'sample_query': "taxon == 'gambiae'",
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_17_call_1_ag3_plot_njt': {'region': '3L:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'country',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'euclidean',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': ['AG1000G-BF-A', 'AG1000G-UG'],
                                 'sample_query': "taxon == 'gambiae'",
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_18_call_1_ag3_plot_njt': {'region': '3L:15,000,000-15,100,000',
                                 'n_snps': 1000,
                                 'color': 'taxon',
                                 'symbol': None,
                                 'algorithm': 'canonical',
                                 'metric': 'euclidean',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': '3.0',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_20_call_1_af1_plot_njt': {'region': '3RL:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'country',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'cityblock',
                                 'distance_sort': None,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': '1.0',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_21_call_1_af1_plot_njt': {'region': '3RL:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': 'country',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'euclidean',
                                 'distance_sort': True,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': '1.0',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'},
 'cell_23_call_1_af1_plot_njt': {'region': '3RL:15,000,000-16,000,000',
                                 'n_snps': 10000,
                                 'color': '__KEEP_CALLSITE_VALUE__',
                                 'symbol': None,
                                 'algorithm': 'dynamic',
                                 'metric': 'euclidean',
                                 'distance_sort': True,
                                 'count_sort': None,
                                 'center_x': 0,
                                 'center_y': 0,
                                 'arc_start': 0,
                                 'arc_stop': 6.283185307179586,
                                 'width': 800,
                                 'height': 600,
                                 'show': True,
                                 'renderer': None,
                                 'render_mode': 'svg',
                                 'title': True,
                                 'title_font_size': 14,
                                 'line_width': 0.5,
                                 'marker_size': 5,
                                 'color_discrete_sequence': None,
                                 'color_discrete_map': None,
                                 'category_orders': None,
                                 'edge_legend': False,
                                 'leaf_legend': True,
                                 'legend_sizing': 'constant',
                                 'thin_offset': 0,
                                 'sample_sets': '1.0',
                                 'sample_query': None,
                                 'sample_query_options': None,
                                 'sample_indices': None,
                                 'site_mask': 'default',
                                 'site_class': None,
                                 'min_minor_ac': 2,
                                 'max_missing_an': 0,
                                 'cohort_size': None,
                                 'min_cohort_size': None,
                                 'max_cohort_size': None,
                                 'random_seed': 42,
                                 'inline_array': True,
                                 'chunks': 'native'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_njt'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_5_call_1_ag3_plot_njt': '01_ag3_njt',
 'cell_6_call_1_ag3_plot_njt': '02_ag3_njt_by_taxon',
 'cell_7_call_1_ag3_plot_njt': '03_ag3_njt_by_taxon',
 'cell_8_call_1_ag3_plot_njt': '04_ag3_njt_by_taxon',
 'cell_9_call_1_ag3_plot_njt': '05_ag3_njt_by_taxon',
 'cell_10_call_1_ag3_plot_njt': '06_ag3_njt_by_taxon',
 'cell_11_call_1_ag3_plot_njt': '07_ag3_njt_by_location',
 'cell_12_call_1_ag3_plot_njt': '08_ag3_njt_by_location',
 'cell_13_call_1_ag3_plot_njt': '09_ag3_njt_by_location',
 'cell_14_call_1_ag3_plot_njt': '10_ag3_njt_by_admin1_year',
 'cell_15_call_1_ag3_plot_njt': '11_ag3_njt_by_taxon',
 'cell_16_call_1_ag3_plot_njt': '12_ag3_njt_by_country',
 'cell_17_call_1_ag3_plot_njt': '13_ag3_njt_by_country',
 'cell_18_call_1_ag3_plot_njt': '14_ag3_njt_by_taxon',
 'cell_20_call_1_af1_plot_njt': '15_af1_njt_by_country',
 'cell_21_call_1_af1_plot_njt': '16_af1_njt_by_country',
 'cell_23_call_1_af1_plot_njt': '17_af1_njt'}


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
    # --- Notebook cell 3 ---
    nbrt.start_cell("notebook_cell_3")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    nbrt.shell('rm -rf results_cache')
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    Z, samples, n_snps = _call_api_with_parameters(ag3.njt, 'cell_4_call_1_ag3_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000)
    nbrt.display(Z.shape)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_5_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, leaf_legend=False))
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_6_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="taxon", width=700))
    # --- Notebook cell 8 ---
    nbrt.start_cell("notebook_cell_8")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_7_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="taxon", width=700, legend_sizing="constant", category_orders=dict(taxon=["coluzzii", "gambiae"])))
    # --- Notebook cell 9 ---
    nbrt.start_cell("notebook_cell_9")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_8_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="taxon", width=700, edge_legend=True))
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_9_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="taxon", width=700, leaf_legend=False, edge_legend=True))
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_10_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="taxon", distance_sort=True))
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_11_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="location"))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_12_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="location", symbol="taxon", edge_legend=False, marker_size=10))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_13_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, color="location", symbol="taxon", leaf_legend=False, title=None))
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_14_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"], n_snps=10_000, color="admin1_year", symbol="taxon"))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_15_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets=["AG1000G-BF-A", "AG1000G-BF-B"], n_snps=10_000, color="taxon", symbol="admin2_month"))
    # --- Notebook cell 17 ---
    nbrt.start_cell("notebook_cell_17")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_16_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets=["AG1000G-BF-A", "AG1000G-UG"], sample_query="taxon == 'gambiae'", n_snps=10_000, color="country"))
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_17_call_1_ag3_plot_njt', region="3L:15,000,000-16,000,000", sample_sets=["AG1000G-BF-A", "AG1000G-UG"], sample_query="taxon == 'gambiae'", n_snps=10_000, color="country", metric="euclidean"))
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    nbrt.display(_call_api_with_parameters(ag3.plot_njt, 'cell_18_call_1_ag3_plot_njt', region="3L:15,000,000-15,100,000", sample_sets="3.0", n_snps=1_000, color="taxon", metric="euclidean", algorithm="canonical"))
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
    )
    nbrt.display(af1)
    # --- Notebook cell 21 ---
    nbrt.start_cell("notebook_cell_21")
    nbrt.display(_call_api_with_parameters(af1.plot_njt, 'cell_20_call_1_af1_plot_njt', n_snps=10_000, region="3RL:15,000,000-16,000,000", sample_sets="1.0", color="country"))
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    nbrt.display(_call_api_with_parameters(af1.plot_njt, 'cell_21_call_1_af1_plot_njt', n_snps=10_000, region="3RL:15,000,000-16,000,000", sample_sets="1.0", color="country", metric="euclidean", distance_sort=True))
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    new_cohorts = {
        "East": "country in ['Malawi', 'Tanzania', 'Kenya', 'Uganda']",
        "West": "country in ['Mali', 'Burkina Faso', 'Cameroon']",
    }
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(af1.plot_njt, 'cell_23_call_1_af1_plot_njt', n_snps=10_000, region="3RL:15,000,000-16,000,000", sample_sets="1.0", color=new_cohorts, metric="euclidean", distance_sort=True))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_njt.ipynb',
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
