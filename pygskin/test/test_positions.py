import unittest

from pygskin.positions import Position, normalize_position


class TestPositions(unittest.TestCase):

    def test_normalize_position(self):
        self.assertEqual(Position.QB, normalize_position('QB'))
        self.assertEqual(Position.RB, normalize_position('RB'))
        self.assertEqual(Position.WR, normalize_position('WR'))
        self.assertEqual(Position.TE, normalize_position('TE'))
        self.assertEqual(Position.DST, normalize_position('DST'))

    def test_normalize_position_with_periods(self):
        self.assertEqual(Position.QB, normalize_position('Q.B.'))
        self.assertEqual(Position.RB, normalize_position('R.B.'))
        self.assertEqual(Position.WR, normalize_position('W.R.'))
        self.assertEqual(Position.TE, normalize_position('T.E.'))
        self.assertEqual(Position.DST, normalize_position('D'))

    def test_normalize_position_full(self):
        self.assertEqual(Position.QB, normalize_position('Quarterback'))
        self.assertEqual(Position.RB, normalize_position('Running back'))
        self.assertEqual(Position.WR, normalize_position('Wide receiver'))
        self.assertEqual(Position.TE, normalize_position('Tight end'))
        self.assertEqual(Position.DST, normalize_position('Defense'))

    def test_normalize_position_none(self):
        self.assertIsNone(normalize_position(None))

    def test_normalize_position_blank(self):
        self.assertIsNone(normalize_position(''))

    def test_normalize_position_slash(self):
        self.assertEqual(Position.DST, normalize_position('D/ST'))

    def test_normalize_position_with_underscores(self):
        self.assertEqual(Position.QB, normalize_position('quarter_back'))
        self.assertEqual(Position.RB, normalize_position('running_back'))
        self.assertEqual(Position.WR, normalize_position('wide_receiver'))
        self.assertEqual(Position.TE, normalize_position('tight_end'))
        self.assertEqual(Position.DST, normalize_position('defense_special_teams'))
