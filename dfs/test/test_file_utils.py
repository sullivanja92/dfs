import unittest

from dfs import file_utils


class TestFileUtils(unittest.TestCase):

    def test_get_extension(self):
        self.assertEqual('csv', file_utils.get_extension('./myFile.csv'))
        self.assertEqual('xlsx', file_utils.get_extension('./myFile.xlsx'))
        self.assertEqual('', file_utils.get_extension('./myFile'))

    def test_get_extension_none(self):
        with self.assertRaises(ValueError):
            file_utils.get_extension(file_path=None)

    def test_get_extension_empty(self):
        with self.assertRaises(ValueError):
            file_utils.get_extension(file_path='')
