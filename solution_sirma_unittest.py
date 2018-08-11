from collections import namedtuple
from datetime import datetime
import solution_sirma
import unittest


class TestSolution(unittest.TestCase):

    def test_convert_to_datetime_objects_not_null(self):
        date = '2013-11-01'
        expected = datetime.strptime(date, '%Y-%m-%d')
        self.assertEqual(expected, solution_sirma._convert_to_datetime_object(date))

    def test_convert_to_datetime_objects_null(self):
        date = 'NULL'
        expected = datetime.today()
        result = solution_sirma._convert_to_datetime_object(date)
        self.assertEqual(expected.year, result.year)
        self.assertEqual(expected.month, result.month)
        self.assertEqual(expected.day, result.day)

    def test_convert_to_datetime_objects_invalid_date_format(self):
        date = ''
        with self.assertRaisesRegexp(ValueError, "time data '{}' does not match format '%Y-%m-%d'".format(date)):
            solution_sirma._convert_to_datetime_object(date)

    def test_check_overlapping_times_no_overlap(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-05', '%Y-%m-%d')
        d2_start = datetime.strptime('2009-01-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2011-04-27', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 0
        self.assertEqual(expected_overlap, solution_sirma._check_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_start_date(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2013-12-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2015-04-27', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 32
        self.assertEqual(expected_overlap, solution_sirma._check_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_end_date(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2013-10-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2013-12-01', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 31
        self.assertEqual(expected_overlap, solution_sirma._check_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_both_dates_interval1_smaller(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2012-10-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2015-12-01', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 62
        self.assertEqual(expected_overlap, solution_sirma._check_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_both_dates_interval2_bigger(self):
        d1_start = datetime.strptime('2012-10-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2015-12-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 62
        self.assertEqual(expected_overlap, solution_sirma._check_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_interval_contains_mutiple_dates(self):
        interval1_start = datetime.strptime('2009-01-01', '%Y-%m-%d')
        interval1_end = datetime.strptime('2011-04-01', '%Y-%m-%d')
        interval2_start1 = datetime.strptime('2011-03-01', '%Y-%m-%d')
        interval2_end1 = datetime.strptime('2011-04-27', '%Y-%m-%d')
        interval2_start2 = datetime.strptime('2014-01-01', '%Y-%m-%d')
        interval2_end2 = datetime.strptime('2015-04-27', '%Y-%m-%d')
        dates_emp1 = [(interval1_start, interval1_end)]
        dates_emp2 = [(interval2_start1, interval2_end1), (interval2_start2, interval2_end2)]
        expected_overlap = 32
        self.assertEqual(expected_overlap, solution_sirma._check_overlapping_times(dates_emp1, dates_emp2))

    def test_detect_longest_team_mates_working_more_than_once_on_same_project(self):
        interval1_start = datetime.strptime('2009-01-01', '%Y-%m-%d')
        interval1_end = datetime.strptime('2011-04-27', '%Y-%m-%d')
        interval2_start = datetime.strptime('2014-01-01', '%Y-%m-%d')
        interval2_end = datetime.strptime('2015-04-27', '%Y-%m-%d')
        output = solution_sirma._detect_longestteam_mates('pm_table.csv')['100']['projects']['10']
        expected_intervals = [(interval1_start, interval1_end), (interval2_start, interval2_end)]
        self.assertEqual(expected_intervals, output)

    def test_detect_longest_team_mates_mutiple_teammates(self):
        output = solution_sirma._detect_longestteam_mates('pm_table.csv')['100']['teammates']
        expected_teammates =  {'143': 847, '218': 482}
        self.assertEqual(expected_teammates, output)

if __name__ == '__main__':
    unittest.main()