import unittest
from datetime import datetime

from dfs.schedule import ScheduleType


class TestSchedule(unittest.TestCase):

    def test_schedule_type_matches_datetime_none_datetime(self):
        self.assertFalse(ScheduleType.ALL.matches(None))

    def test_schedule_type_matches_datetime_all(self):
        for i in range(1, 30):
            self.assertTrue(ScheduleType.ALL.matches(datetime(2020, 9, i)))

    def test_schedule_type_matches_datetime_sunday_all(self):
        self.assertTrue(ScheduleType.SUNDAY_ALL.matches(datetime(2020, 9, 13)))
        self.assertFalse(ScheduleType.SUNDAY_ALL.matches(datetime(2020, 9, 14)))

    def test_schedule_type_matches_datetime_sunday_early(self):
        self.assertTrue(ScheduleType.SUNDAY_EARLY.matches(datetime(2020, 9, 13, 13, 0, 0)))
        self.assertFalse(ScheduleType.SUNDAY_EARLY.matches(datetime(2020, 9, 13, 16, 5, 0)))

    def test_schedule_type_matches_datetime_sunday_early_and_late(self):
        self.assertTrue(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 13, 0, 0)))
        self.assertTrue(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 16, 5, 0)))
        self.assertTrue(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 16, 25, 0)))
        self.assertFalse(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 20, 25, 0)))
        self.assertFalse(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 14, 13, 25, 0)))

    def test_datetime_matches_schedule_type_sunday_late(self):
        self.assertTrue(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 16, 5, 0)))
        self.assertTrue(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 16, 25, 0)))
        self.assertFalse(ScheduleType.SUNDAY_EARLY_AND_LATE.matches(datetime(2020, 9, 13, 20, 25, 0)))

    def test_datetime_matches_schedule_type_sunday_late_and_night(self):
        self.assertTrue(ScheduleType.SUNDAY_LATE_AND_NIGHT.matches(datetime(2020, 9, 13, 16, 5, 0)))
        self.assertTrue(ScheduleType.SUNDAY_LATE_AND_NIGHT.matches(datetime(2020, 9, 13, 16, 25, 0)))
        self.assertTrue(ScheduleType.SUNDAY_LATE_AND_NIGHT.matches(datetime(2020, 9, 13, 20, 20, 0)))
        self.assertFalse(ScheduleType.SUNDAY_LATE_AND_NIGHT.matches(datetime(2020, 9, 13, 13, 0, 0)))
        self.assertFalse(ScheduleType.SUNDAY_LATE_AND_NIGHT.matches(datetime(2020, 9, 14, 13, 25, 0)))

    def test_datetime_matches_schedule_type_sunday_night(self):
        self.assertTrue(ScheduleType.SUNDAY_NIGHT.matches(datetime(2020, 9, 13, 20, 20, 0)))
        self.assertFalse(ScheduleType.SUNDAY_NIGHT.matches(datetime(2020, 9, 13, 13, 0, 0)))
        self.assertFalse(ScheduleType.SUNDAY_NIGHT.matches(datetime(2020, 9, 14, 20, 20, 0)))

    def test_datetime_matches_schedule_type_sunday_and_monday(self):
        self.assertTrue(ScheduleType.SUNDAY_AND_MONDAY.matches(datetime(2020, 9, 13, 13, 0, 0)))
        self.assertTrue(ScheduleType.SUNDAY_AND_MONDAY.matches(datetime(2020, 9, 13, 20, 20, 0)))
        self.assertTrue(ScheduleType.SUNDAY_AND_MONDAY.matches(datetime(2020, 9, 14, 20, 20, 0)))
        self.assertFalse(ScheduleType.SUNDAY_AND_MONDAY.matches(datetime(2020, 9, 10, 20, 20, 0)))

    def test_datetime_matches_schedule_type_monday(self):
        self.assertTrue(ScheduleType.MONDAY.matches(datetime(2020, 9, 14, 20, 25, 0)))
        self.assertTrue(ScheduleType.MONDAY.matches(datetime(2020, 9, 14, 22, 25, 0)))
        self.assertFalse(ScheduleType.MONDAY.matches(datetime(2020, 9, 13, 20, 25, 0)))

    def test_datetime_matches_schedule_type_thursday(self):
        self.assertTrue(ScheduleType.THURSDAY.matches(datetime(2020, 9, 10, 13, 0, 0)))
        self.assertTrue(ScheduleType.THURSDAY.matches(datetime(2020, 9, 10, 20, 25, 0)))
        self.assertFalse(ScheduleType.THURSDAY.matches(datetime(2020, 9, 13, 20, 25, 0)))
