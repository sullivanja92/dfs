import unittest

import pandas as pd

from dfs import data_frame_utils


class TestDataFrameUtils(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame.from_dict(data={
            'name': ['Aaron Rodgers', 'Aaron Jones'],
            'position': ['QB', 'RB'],
            'points': [20.0, 15.9]
        })

    def test_contains_all_columns_true(self):
        self.assertTrue(data_frame_utils.contains_all_columns(self.df, ['name', 'position', 'points']))

    def test_contains_all_columns_false(self):
        self.assertFalse(data_frame_utils.contains_all_columns(self.df, ['name', 'position', 'points', 'week']))

    def test_contains_all_columns_none_df(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.contains_all_columns(None, []))

    def test_contains_all_columns_none_cols(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.contains_all_columns(self.df, None))

    def test_col_contains_all_values_true(self):
        self.assertTrue(data_frame_utils.col_contains_all_values(self.df, 'position', ['QB', 'RB']))

    def test_col_contains_all_values_false(self):
        self.assertFalse(data_frame_utils.col_contains_all_values(self.df, 'position', ['QB', 'RB', 'WR']))

    def test_map_index_to_col(self):
        self.assertDictEqual({0: 20.0, 1: 15.9}, data_frame_utils.map_index_to_col(self.df, 'points'))

    def test_map_index_to_col_none_data_frame(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.map_index_to_col(None, 'points'))

    def test_map_index_to_col_none_column(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.map_index_to_col(self.df, None))

    def test_map_index_to_col_missing_column(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.map_index_to_col(self.df, 'missing'))

    def test_merge_dicts(self):
        self.assertDictEqual({'a': 1, 'b': 2}, data_frame_utils.merge_dicts({'a': 1}, {'b': 2}))

    def test_merge_dicts_overlap(self):
        self.assertDictEqual({'a': 1, 'b': 2, 'c': 3}, data_frame_utils.merge_dicts({'a': 1, 'b': 2}, {'b': 2, 'c': 3}))

    def test_merge_dicts_without_args(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.merge_dicts())

    def test_merge_dicts_none_args(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.merge_dicts(None, None))

    def test_merge_dicts_none_arg(self):
        self.assertDictEqual({'a': 1, 'b': 2}, data_frame_utils.merge_dicts({'a': 1}, None, {'b': 2}))

    def test_map_cols_and_filter_by_values(self):
        actual = data_frame_utils.map_cols_and_filter_by_values(self.df, {'name': 'n'})
        self.assertListEqual(list(actual.columns), ['n'])
        self.assertEqual(len(actual), 2)
        self.assertEqual(len(actual[actual['n'] == 'Aaron Rodgers']), 1)
        self.assertEqual(len(actual[actual['n'] == 'Aaron Jones']), 1)

    def test_map_cols_and_filter_by_values_none_df(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.map_cols_and_filter_by_values(None, {}))

    def test_map_cols_and_filter_by_values_none_mappings(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.map_cols_and_filter_by_values(self.df, None))
