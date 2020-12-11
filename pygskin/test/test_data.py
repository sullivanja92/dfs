import unittest

from pygskin import data


class TestData(unittest.TestCase):

    def setUp(self) -> None:
        self.df = data.load_2020_data()

    def test_load_2020_data_default_weeks(self):
        self.assertListEqual(list(range(1, 5)), list(self.df['week'].unique()))

    def test_load_2020_data_custom_weeks(self):
        self.assertListEqual([2, 3], list(data.load_2020_data([2, 3])['week'].unique()))

    def test_load_2020_data_none_weeks(self):
        self.assertRaises(ValueError, lambda: data.load_2020_data(None))

    def test_load_2020_data_negative_weeks(self):
        self.assertRaises(ValueError, lambda: data.load_2020_data([-1]))

    def test_load_2020_data_zero_weeks(self):
        self.assertRaises(ValueError, lambda: data.load_2020_data([0]))

    def test_load_2020_data_invalid_weeks(self):
        self.assertRaises(ValueError, lambda: data.load_2020_data([4, 5]))

    def test_load_2020_data_empty_weeks(self):
        self.assertRaises(ValueError, lambda: data.load_2020_data([]))
