import pandas as pd
import unittest
from pygskin.util import data_frame_utils


class TestDataFrameUtils(unittest.TestCase):

    def setUp(self):
        data = {
            'name': ['Aaron Rodgers', 'Aaron Jones'],
            'position': ['QB', 'RB'],
            'points': [20.0, 15.9]
        }
        self.df = pd.DataFrame.from_dict(data)

    def test_dict_from_data_frame_columns(self):
        actual = data_frame_utils.dict_from_data_frame_columns(self.df, 'name', 'points')
        expected = {'Aaron Rodgers': 20.0, 'Aaron Jones': 15.9}
        self.assertDictEqual(actual, expected)

    def test_dict_from_data_frame_columns_missing_key_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.dict_from_data_frame_columns(self.df, 'missing_key_col', 'points'))

    def test_dict_from_data_frame_columns_missing_value_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.dict_from_data_frame_columns(self.df, 'name', 'missing_value_col'))

    def test_dict_from_data_frame_columns_none_key_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.dict_from_data_frame_columns(self.df, None, 'points'))

    def test_dict_from_data_frame_columns_none_value_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.dict_from_data_frame_columns(self.df, 'name', None))

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
