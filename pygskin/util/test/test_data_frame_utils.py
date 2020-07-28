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

    def test_data_frame_to_dict(self):
        actual = data_frame_utils.data_frame_to_dict(self.df, 'name', 'points')
        expected = {'Aaron Rodgers': 20.0, 'Aaron Jones': 15.9}
        self.assertDictEqual(actual, expected)

    def test_data_frame_to_dict_missing_key_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.data_frame_to_dict(self.df, 'missing_key_col', 'points'))

    def test_data_frame_to_dict_missing_value_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.data_frame_to_dict(self.df, 'name', 'missing_value_col'))

    def test_data_frame_to_dict_none_key_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.data_frame_to_dict(self.df, None, 'points'))

    def test_data_frame_to_dict_none_value_col(self):
        self.assertRaises(ValueError, lambda: data_frame_utils.data_frame_to_dict(self.df, 'name', None))

    def test_col_contains_all_values_true(self):
        self.assertTrue(data_frame_utils.col_contains_all_values(self.df, 'position', ['QB', 'RB']))

    def test_col_contains_all_values_false(self):
        self.assertTrue(data_frame_utils.col_contains_all_values(self.df, 'position', ['QB', 'RB', 'WR']))
