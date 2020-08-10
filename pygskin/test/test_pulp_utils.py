import unittest

from pygskin import pulp_utils


class TestPulpUtils(unittest.TestCase):

    def test_index_from_variable_name(self):
        self.assertEqual(1, pulp_utils.index_from_lp_variable_name('QB_1'))
        self.assertEqual(37, pulp_utils.index_from_lp_variable_name('WR|37', delimiter='|'))
        self.assertEqual(21, pulp_utils.index_from_lp_variable_name('DST*21', delimiter='*'))

    def test_index_from_variable_name_none_name(self):
        self.assertRaises(ValueError, lambda: pulp_utils.index_from_lp_variable_name(None))

    def test_index_from_variable_name_empty_name(self):
        self.assertRaises(ValueError, lambda: pulp_utils.index_from_lp_variable_name(''))

    def test_index_from_variable_name_none_delimiter(self):
        self.assertRaises(ValueError, lambda: pulp_utils.index_from_lp_variable_name('QB_1', delimiter=None))

    def test_index_from_variable_name_missing_delimiter(self):
        self.assertRaises(ValueError, lambda: pulp_utils.index_from_lp_variable_name('QB_1', delimiter='|'))
