#!/usr/bin/env python3
"""plot_pca: the code from notebooks/plot_pca.ipynb as a runnable script.

Figures the notebook displays are saved to FIGURE_DIR instead, named from
FIGURE_NAMES. Other cell outputs are printed.

Usage (from the repository root):
    python scripts/plot_pca.py                      # the notebook's defaults
    python scripts/plot_pca.py --config runs.csv    # one run per CSV row
    python scripts/plot_pca.py --list-parameters    # what a CSV can set

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
PERFORMANCE_CSV_PATH = 'plot_pca_performance.csv'
API_CALL_PARAMETERS = {'cell_8_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                           'n_snps': 10000,
                           'n_components': 20,
                           'thin_offset': 0,
                           'sample_sets': 'AG1000G-FR',
                           'sample_query': None,
                           'sample_query_options': None,
                           'sample_indices': None,
                           'cohorts': None,
                           'cohort_size': None,
                           'min_cohort_size': None,
                           'max_cohort_size': None,
                           'site_mask': 'default',
                           'site_class': None,
                           'min_minor_ac': 2,
                           'max_missing_an': 0,
                           'imputation_method': 'most_common',
                           'exclude_samples': None,
                           'fit_exclude_samples': None,
                           'random_seed': 42,
                           'inline_array': True,
                           'chunks': 'native'},
 'cell_10_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': None,
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_11_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'location',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_12_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': 'AG1000G-FR',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_13_call_1_ag3_plot_pca_variance': {'evr': '__KEEP_CALLSITE_VALUE__',
                                          'width': 900,
                                          'height': 400,
                                          'show': True,
                                          'renderer': None,
                                          'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_14_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'location',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_16_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': 'AG1000G-BF-A',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': 50,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_17_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'taxon',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_18_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'admin1_year',
                                        'symbol': 'taxon',
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_20_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '3.0',
                            'sample_query': "country != 'Lab Cross'",
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_21_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '3.0',
                            'sample_query': "country != 'Lab Cross'",
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_22_call_1_ag3_plot_pca_variance': {'evr': '__KEEP_CALLSITE_VALUE__',
                                          'width': 900,
                                          'height': 400,
                                          'show': True,
                                          'renderer': None,
                                          'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_23_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'taxon',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 5,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_24_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC3',
                                        'y': 'PC4',
                                        'color': 'country',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 5,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_25_call_1_ag3_plot_pca_coords_3d': {'data': '__KEEP_CALLSITE_VALUE__',
                                           'x': 'PC1',
                                           'y': 'PC2',
                                           'z': 'PC3',
                                           'color': 'taxon',
                                           'symbol': None,
                                           'jitter_frac': 0.02,
                                           'random_seed': 42,
                                           'width': 900,
                                           'height': 600,
                                           'marker_size': 2,
                                           'color_discrete_sequence': None,
                                           'color_discrete_map': None,
                                           'category_orders': None,
                                           'legend_sizing': 'constant',
                                           'show': True,
                                           'renderer': None,
                                           'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_26_call_1_ag3_plot_pca_coords_3d': {'data': '__KEEP_CALLSITE_VALUE__',
                                           'x': 'PC1',
                                           'y': 'PC2',
                                           'z': 'PC3',
                                           'color': 'taxon',
                                           'symbol': None,
                                           'jitter_frac': 0.02,
                                           'random_seed': 42,
                                           'width': 900,
                                           'height': 600,
                                           'marker_size': 2,
                                           'color_discrete_sequence': None,
                                           'color_discrete_map': None,
                                           'category_orders': None,
                                           'legend_sizing': 'constant',
                                           'show': True,
                                           'renderer': None,
                                           'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_28_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': None,
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 5,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_29_call_1_ag3_plot_pca_coords_3d': {'data': '__KEEP_CALLSITE_VALUE__',
                                           'x': 'PC1',
                                           'y': 'PC2',
                                           'z': 'PC3',
                                           'color': None,
                                           'symbol': None,
                                           'jitter_frac': 0.02,
                                           'random_seed': 42,
                                           'width': 900,
                                           'height': 600,
                                           'marker_size': 2,
                                           'color_discrete_sequence': None,
                                           'color_discrete_map': None,
                                           'category_orders': None,
                                           'legend_sizing': 'constant',
                                           'show': True,
                                           'renderer': None,
                                           'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_31_call_1_af1_pca': {'region': '3RL:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '1.0',
                            'sample_query': "country != 'Ghana'",
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': None,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_32_call_1_af1_plot_pca_variance': {'evr': '__KEEP_CALLSITE_VALUE__',
                                          'width': 900,
                                          'height': 400,
                                          'show': True,
                                          'renderer': None,
                                          'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_33_call_1_af1_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'country',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_34_call_1_af1_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC3',
                                        'y': 'PC4',
                                        'color': 'country',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_36_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': 'AG1000G-BF-A',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': 50,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_38_call_1_ag3_plot_pca_variance': {'evr': '__KEEP_CALLSITE_VALUE__',
                                          'width': 900,
                                          'height': 400,
                                          'show': True,
                                          'renderer': None,
                                          'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_39_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'taxon',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_40_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': 'AG1000G-BF-A',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': 50,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_43_call_1_ag3_plot_pca_variance': {'evr': '__KEEP_CALLSITE_VALUE__',
                                          'width': 900,
                                          'height': 400,
                                          'show': True,
                                          'renderer': None,
                                          'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_44_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'taxon',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_46_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': 'AG1000G-BF-A',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': None,
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': 50,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_49_call_1_ag3_plot_pca_variance': {'evr': '__KEEP_CALLSITE_VALUE__',
                                          'width': 900,
                                          'height': 400,
                                          'show': True,
                                          'renderer': None,
                                          'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_50_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'taxon',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_51_call_1_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'pca_fit',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'},
 'cell_53_call_1_ag3_pca': {'region': '3L:15,000,000-16,000,000',
                            'n_snps': 10000,
                            'n_components': 20,
                            'thin_offset': 0,
                            'sample_sets': '3.0',
                            'sample_query': None,
                            'sample_query_options': None,
                            'sample_indices': None,
                            'cohorts': 'country',
                            'cohort_size': None,
                            'min_cohort_size': None,
                            'max_cohort_size': 20,
                            'site_mask': 'default',
                            'site_class': None,
                            'min_minor_ac': 2,
                            'max_missing_an': 0,
                            'imputation_method': 'most_common',
                            'exclude_samples': None,
                            'fit_exclude_samples': None,
                            'random_seed': 42,
                            'inline_array': True,
                            'chunks': 'native'},
 'cell_53_call_2_ag3_plot_pca_coords': {'data': '__KEEP_CALLSITE_VALUE__',
                                        'x': 'PC1',
                                        'y': 'PC2',
                                        'color': 'country',
                                        'symbol': None,
                                        'opacity': 0.9,
                                        'jitter_frac': 0.02,
                                        'random_seed': 42,
                                        'width': 900,
                                        'height': 600,
                                        'marker_size': 10,
                                        'color_discrete_sequence': None,
                                        'color_discrete_map': None,
                                        'category_orders': None,
                                        'legend_sizing': 'constant',
                                        'show': True,
                                        'renderer': None,
                                        'render_mode': 'svg',
                                        'kwargs': '__KEEP_CALLSITE_VALUE__'}}

# ---------------------------------------------------------------------------
# Figure parameters
# ---------------------------------------------------------------------------

# Directory figures are saved in, relative to where the script is run from.
# With several CSV rows, each run saves to its own run_NNN subdirectory.
FIGURE_DIR = 'figures/plot_pca'

# One of "html" (interactive), "png", "svg" or "pdf". Static formats need
# kaleido for plotly figures and selenium for bokeh figures; bokeh figures fall
# back to html without it. Matplotlib figures are saved as png for "html", and
# IGV views are always html.
FIGURE_FORMAT = "html"

# File name (without extension) for each figure, keyed by the API call key or
# notebook cell that displays it. A call that shows several figures gets
# numbered suffixes. Figures from keys not listed here are named after the key.
FIGURE_NAMES = {'cell_10_call_1_ag3_plot_pca_coords': '01_ag3_pca_coords',
 'cell_11_call_1_ag3_plot_pca_coords': '02_ag3_pca_coords_by_location',
 'cell_13_call_1_ag3_plot_pca_variance': '03_ag3_pca_variance',
 'cell_14_call_1_ag3_plot_pca_coords': '04_ag3_pca_coords_by_location',
 'cell_17_call_1_ag3_plot_pca_coords': '05_ag3_pca_coords_by_taxon',
 'cell_18_call_1_ag3_plot_pca_coords': '06_ag3_pca_coords_by_admin1_year',
 'cell_22_call_1_ag3_plot_pca_variance': '07_ag3_pca_variance',
 'cell_23_call_1_ag3_plot_pca_coords': '08_ag3_pca_coords_by_taxon',
 'cell_24_call_1_ag3_plot_pca_coords': '09_ag3_pca_coords_by_country',
 'cell_25_call_1_ag3_plot_pca_coords_3d': '10_ag3_pca_coords_3d_by_taxon',
 'cell_26_call_1_ag3_plot_pca_coords_3d': '11_ag3_pca_coords_3d_by_taxon',
 'cell_28_call_1_ag3_plot_pca_coords': '12_ag3_pca_coords',
 'cell_29_call_1_ag3_plot_pca_coords_3d': '13_ag3_pca_coords_3d',
 'cell_32_call_1_af1_plot_pca_variance': '14_af1_pca_variance',
 'cell_33_call_1_af1_plot_pca_coords': '15_af1_pca_coords_by_country',
 'cell_34_call_1_af1_plot_pca_coords': '16_af1_pca_coords_by_country',
 'cell_38_call_1_ag3_plot_pca_variance': '17_ag3_pca_variance',
 'cell_39_call_1_ag3_plot_pca_coords': '18_ag3_pca_coords_by_taxon',
 'cell_43_call_1_ag3_plot_pca_variance': '19_ag3_pca_variance',
 'cell_44_call_1_ag3_plot_pca_coords': '20_ag3_pca_coords_by_taxon',
 'cell_49_call_1_ag3_plot_pca_variance': '21_ag3_pca_variance',
 'cell_50_call_1_ag3_plot_pca_coords': '22_ag3_pca_coords_by_taxon',
 'cell_51_call_1_ag3_plot_pca_coords': '23_ag3_pca_coords_by_pca_fit',
 'cell_53_call_2_ag3_plot_pca_coords': '24_ag3_pca_coords_by_country'}


def run(API_KEEP_CALLSITE_VALUE, PERFORMANCE_CSV_PATH, API_CALL_PARAMETERS):
    # --- Notebook cell 1 ---
    nbrt.start_cell("notebook_cell_1")
    import csv
    import inspect
    import json
    from pathlib import Path
    from memory_profiler import memory_usage
    import time


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
    # # PCA plotting
    # ### Setup
    # --- Notebook cell 4 ---
    nbrt.start_cell("notebook_cell_4")
    import malariagen_data
    # --- Notebook cell 5 ---
    nbrt.start_cell("notebook_cell_5")
    ag3 = malariagen_data.Ag3(
        "simplecache::gs://vo_agam_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
    )
    nbrt.display(ag3)
    # --- Notebook cell 6 ---
    nbrt.start_cell("notebook_cell_6")
    af1 = malariagen_data.Af1(
        "simplecache::gs://vo_afun_release_master_us_central1",
        simplecache=dict(cache_storage="../gcs_cache"),
        results_cache="results_cache",
    )
    nbrt.display(af1)
    # --- Notebook cell 7 ---
    nbrt.start_cell("notebook_cell_7")
    nbrt.shell('rm -rf results_cache')
    # ## Mayotte
    # --- Notebook cell 10 ---
    nbrt.start_cell("notebook_cell_10")
    df_pca, evr = _call_api_with_parameters(ag3.pca, 'cell_8_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-FR", n_snps=10_000)
    nbrt.display(df_pca)
    # --- Notebook cell 11 ---
    nbrt.start_cell("notebook_cell_11")
    nbrt.display(evr)
    # --- Notebook cell 12 ---
    nbrt.start_cell("notebook_cell_12")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_10_call_1_ag3_plot_pca_coords', df_pca))
    # --- Notebook cell 13 ---
    nbrt.start_cell("notebook_cell_13")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_11_call_1_ag3_plot_pca_coords', df_pca, color="location"))
    # --- Notebook cell 14 ---
    nbrt.start_cell("notebook_cell_14")
    df_pca, evr = _call_api_with_parameters(ag3.pca, 'cell_12_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-FR", n_snps=10_000)
    # --- Notebook cell 15 ---
    nbrt.start_cell("notebook_cell_15")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_variance, 'cell_13_call_1_ag3_plot_pca_variance', evr))
    # --- Notebook cell 16 ---
    nbrt.start_cell("notebook_cell_16")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_14_call_1_ag3_plot_pca_coords', df_pca, color="location"))
    # ## Burkina Faso
    # --- Notebook cell 18 ---
    nbrt.start_cell("notebook_cell_18")
    df_pca, evr = _call_api_with_parameters(ag3.pca, 'cell_16_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, max_cohort_size=50)
    # --- Notebook cell 19 ---
    nbrt.start_cell("notebook_cell_19")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_17_call_1_ag3_plot_pca_coords', df_pca, color="taxon", category_orders=dict(taxon=["coluzzii", "gambiae"])))
    # --- Notebook cell 20 ---
    nbrt.start_cell("notebook_cell_20")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_18_call_1_ag3_plot_pca_coords', df_pca, color="admin1_year", symbol="taxon"))
    # ## Ag3.0
    # --- Notebook cell 22 ---
    nbrt.start_cell("notebook_cell_22")
    df_pca, evr = _call_api_with_parameters(ag3.pca, 'cell_20_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="3.0", sample_query="country != 'Lab Cross'", n_snps=10_000)
    # --- Notebook cell 23 ---
    nbrt.start_cell("notebook_cell_23")
    df_pca, evr = _call_api_with_parameters(ag3.pca, 'cell_21_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="3.0", sample_query="country != 'Lab Cross'", n_snps=10_000)
    # --- Notebook cell 24 ---
    nbrt.start_cell("notebook_cell_24")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_variance, 'cell_22_call_1_ag3_plot_pca_variance', evr))
    # --- Notebook cell 25 ---
    nbrt.start_cell("notebook_cell_25")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_23_call_1_ag3_plot_pca_coords', df_pca, color="taxon", marker_size=5))
    # --- Notebook cell 26 ---
    nbrt.start_cell("notebook_cell_26")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_24_call_1_ag3_plot_pca_coords', df_pca, x="PC3", y="PC4", color="country", marker_size=5))
    # --- Notebook cell 27 ---
    nbrt.start_cell("notebook_cell_27")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords_3d, 'cell_25_call_1_ag3_plot_pca_coords_3d', df_pca, color="taxon", marker_size=2))
    # --- Notebook cell 28 ---
    nbrt.start_cell("notebook_cell_28")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords_3d, 'cell_26_call_1_ag3_plot_pca_coords_3d', df_pca, color="taxon", category_orders=dict(
            taxon=["coluzzii", "gambiae", "arabiensis", "gcx1", "gcx2", "gcx3"]
        ), marker_size=2))
    # --- Notebook cell 29 ---
    nbrt.start_cell("notebook_cell_29")
    new_cohorts = {
        "East": "country in ['Malawi', 'Tanzania', 'Kenya', 'Uganda']",
        "West": "country in ['Mali', 'Burkina Faso', 'Cameroon']",
    }
    # --- Notebook cell 30 ---
    nbrt.start_cell("notebook_cell_30")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_28_call_1_ag3_plot_pca_coords', df_pca, color=new_cohorts, marker_size=5))
    # --- Notebook cell 31 ---
    nbrt.start_cell("notebook_cell_31")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords_3d, 'cell_29_call_1_ag3_plot_pca_coords_3d', df_pca, color=new_cohorts, marker_size=2))
    # ## Af1.0
    # --- Notebook cell 33 ---
    nbrt.start_cell("notebook_cell_33")
    df_pca, evr = _call_api_with_parameters(af1.pca, 'cell_31_call_1_af1_pca', region="3RL:15,000,000-16,000,000", sample_sets="1.0", sample_query="country != 'Ghana'", n_snps=10_000)
    # --- Notebook cell 34 ---
    nbrt.start_cell("notebook_cell_34")
    nbrt.display(_call_api_with_parameters(af1.plot_pca_variance, 'cell_32_call_1_af1_plot_pca_variance', evr))
    # --- Notebook cell 35 ---
    nbrt.start_cell("notebook_cell_35")
    nbrt.display(_call_api_with_parameters(af1.plot_pca_coords, 'cell_33_call_1_af1_plot_pca_coords', df_pca, color="country"))
    # --- Notebook cell 36 ---
    nbrt.start_cell("notebook_cell_36")
    nbrt.display(_call_api_with_parameters(af1.plot_pca_coords, 'cell_34_call_1_af1_plot_pca_coords', df_pca, x="PC3", y="PC4", color="country"))
    # ## Excluding samples
    # --- Notebook cell 38 ---
    nbrt.start_cell("notebook_cell_38")
    df_pca, evr = _call_api_with_parameters(ag3.pca, 'cell_36_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, max_cohort_size=50)
    # --- Notebook cell 39 ---
    nbrt.start_cell("notebook_cell_39")
    nbrt.display(df_pca.head())
    # --- Notebook cell 40 ---
    nbrt.start_cell("notebook_cell_40")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_variance, 'cell_38_call_1_ag3_plot_pca_variance', evr))
    # --- Notebook cell 41 ---
    nbrt.start_cell("notebook_cell_41")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_39_call_1_ag3_plot_pca_coords', df_pca, color="taxon"))
    # --- Notebook cell 42 ---
    nbrt.start_cell("notebook_cell_42")
    exclude_samples = ["AB0096-C", "AB0241-C", "AB0275-C", "AB0197-C"]

    df_pca_ex, evr_ex = _call_api_with_parameters(ag3.pca, 'cell_40_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, max_cohort_size=50, exclude_samples=exclude_samples)
    # --- Notebook cell 43 ---
    nbrt.start_cell("notebook_cell_43")
    nbrt.display(df_pca_ex.head())
    # --- Notebook cell 44 ---
    nbrt.start_cell("notebook_cell_44")
    nbrt.display(df_pca_ex.query(f"sample_id in {exclude_samples}"))
    # --- Notebook cell 45 ---
    nbrt.start_cell("notebook_cell_45")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_variance, 'cell_43_call_1_ag3_plot_pca_variance', evr_ex))
    # --- Notebook cell 46 ---
    nbrt.start_cell("notebook_cell_46")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_44_call_1_ag3_plot_pca_coords', df_pca_ex, color="taxon"))
    # ## Excluding samples during fit
    # --- Notebook cell 48 ---
    nbrt.start_cell("notebook_cell_48")
    fit_exclude_samples = ["AB0096-C", "AB0241-C", "AB0275-C", "AB0197-C"]

    df_pca_fex, evr_fex = _call_api_with_parameters(ag3.pca, 'cell_46_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="AG1000G-BF-A", n_snps=10_000, max_cohort_size=50, fit_exclude_samples=fit_exclude_samples)
    # --- Notebook cell 49 ---
    nbrt.start_cell("notebook_cell_49")
    nbrt.display(df_pca_fex.head())
    # --- Notebook cell 50 ---
    nbrt.start_cell("notebook_cell_50")
    nbrt.display(df_pca_fex.query(f"sample_id in {fit_exclude_samples}"))
    # --- Notebook cell 51 ---
    nbrt.start_cell("notebook_cell_51")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_variance, 'cell_49_call_1_ag3_plot_pca_variance', evr_fex))
    # --- Notebook cell 52 ---
    nbrt.start_cell("notebook_cell_52")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_50_call_1_ag3_plot_pca_coords', df_pca_fex, color="taxon"))
    # --- Notebook cell 53 ---
    nbrt.start_cell("notebook_cell_53")
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_51_call_1_ag3_plot_pca_coords', df_pca_fex, color="pca_fit"))
    # ## PCA with cohort downsampling
    # --- Notebook cell 55 ---
    nbrt.start_cell("notebook_cell_55")
    df_pca_cohorts, evr_cohorts = _call_api_with_parameters(ag3.pca, 'cell_53_call_1_ag3_pca', region="3L:15,000,000-16,000,000", sample_sets="3.0", n_snps=10_000, cohorts="country", max_cohort_size=20)
    nbrt.display(_call_api_with_parameters(ag3.plot_pca_coords, 'cell_53_call_2_ag3_plot_pca_coords', df_pca_cohorts, color="country"))


if __name__ == "__main__":
    nbrt.main(
        notebook='plot_pca.ipynb',
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
