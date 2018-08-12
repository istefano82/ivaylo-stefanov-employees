import os
import subprocess
import unittest
from datetime import datetime

import solution_sirma


class TestSolution(unittest.TestCase):

    def test_convert_to_datetime_objects_multiple_date_formats(self):
        dates = ['03/08/06', '03/08/2006', '3/8/06', '3/8/2006', '030806', '03082006', '03Aug06', '03Aug2006',
                 '03-Aug-06', '03-Aug-2006', '3Aug06', '3Aug2006', '3-Aug-06', '3-Aug-2006', '3-August-06',
                 '3-August-2006', '2006/08/03', 'Aug-03-06', 'Aug-03-2006', '2006-08-03', 'August-03-06',
                 'August-03-2006']

        expected_date = datetime(2006, 8, 3, 0, 0)
        for date in dates:
            result = solution_sirma._convert_to_datetime_object(date)
            self.assertEqual(expected_date, result)

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
        with self.assertRaisesRegexp(ValueError, "time data '{}' does not match any of the "
                                                 "supported date formats.'".format(date)):
            solution_sirma._convert_to_datetime_object(date)

    def test_check_overlapping_times_no_overlap(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-05', '%Y-%m-%d')
        d2_start = datetime.strptime('2009-01-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2011-04-27', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 0
        self.assertEqual(expected_overlap, solution_sirma._calculate_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_start_date(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2013-12-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2015-04-27', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 32
        self.assertEqual(expected_overlap, solution_sirma._calculate_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_end_date(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2013-10-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2013-12-01', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 31
        self.assertEqual(expected_overlap, solution_sirma._calculate_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_both_dates_interval1_smaller(self):
        d1_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2012-10-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2015-12-01', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 62
        self.assertEqual(expected_overlap, solution_sirma._calculate_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_on_both_dates_interval2_bigger(self):
        d1_start = datetime.strptime('2012-10-01', '%Y-%m-%d')
        d1_end = datetime.strptime('2015-12-01', '%Y-%m-%d')
        d2_start = datetime.strptime('2013-11-01', '%Y-%m-%d')
        d2_end = datetime.strptime('2014-01-01', '%Y-%m-%d')
        dates_emp1 = (d1_start, d1_end)
        dates_emp2 = (d2_start, d2_end)
        expected_overlap = 62
        self.assertEqual(expected_overlap, solution_sirma._calculate_overlapping_times([dates_emp1], [dates_emp2]))

    def test_check_overlapping_times_overlap_interval_contains_multiple_dates(self):
        interval1_start = datetime.strptime('2009-01-01', '%Y-%m-%d')
        interval1_end = datetime.strptime('2011-04-01', '%Y-%m-%d')
        interval2_start1 = datetime.strptime('2011-03-01', '%Y-%m-%d')
        interval2_end1 = datetime.strptime('2011-04-27', '%Y-%m-%d')
        interval2_start2 = datetime.strptime('2014-01-01', '%Y-%m-%d')
        interval2_end2 = datetime.strptime('2015-04-27', '%Y-%m-%d')
        dates_emp1 = [(interval1_start, interval1_end)]
        dates_emp2 = [(interval2_start1, interval2_end1), (interval2_start2, interval2_end2)]
        expected_overlap = 32
        self.assertEqual(expected_overlap, solution_sirma._calculate_overlapping_times(dates_emp1, dates_emp2))

    def test_detect_longest_team_mates_working_more_than_once_on_same_project(self):
        employee_struct = {'100': {'teammates': {},
                                   'projects': {'10': [(datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                       (datetime(2014, 1, 1, 0, 0), datetime(2015, 4, 27, 0, 0))]}},
                           '143': {'teammates': {},
                                   'projects': {'10': [(datetime(2011, 3, 27, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                       (datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0))],
                                                '12': [(datetime(2013, 11, 1, 0, 0), datetime(2014, 1, 5, 0, 0))]}},
                           '218': {'teammates': {},
                                   'projects': {'10': [(datetime(2012, 5, 16, 0, 0), datetime(2018, 8, 12, 12, 35, 0,
                                                                                              313337))]}}}
        interval1_start = datetime.strptime('2009-01-01', '%Y-%m-%d')
        interval1_end = datetime.strptime('2011-04-27', '%Y-%m-%d')
        interval2_start = datetime.strptime('2014-01-01', '%Y-%m-%d')
        interval2_end = datetime.strptime('2015-04-27', '%Y-%m-%d')
        employee_struct, longest_teammates = solution_sirma.detect_longest_team_mates(employee_struct)
        expected_intervals = [(interval1_start, interval1_end), (interval2_start, interval2_end)]
        expected_teammates = {'days': 879, 'employees': ['100', '143']}
        self.assertEqual(expected_intervals, employee_struct['100']['projects']['10'])
        self.assertEqual(expected_teammates, longest_teammates)

    def test_detect_longest_team_mates_multiple_teammates(self):
        employee_struct = {'100': {'teammates': {},
                                   'projects': {'10': [(datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                       (datetime(2014, 1, 1, 0, 0), datetime(2015, 4, 27, 0, 0))]}},
                           '143': {'teammates': {},
                                   'projects': {'10': [(datetime(2011, 3, 27, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                       (datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0))],
                                                '12': [(datetime(2013, 11, 1, 0, 0), datetime(2014, 1, 5, 0, 0))]}},
                           '218': {'teammates': {},
                                   'projects': {'10': [(datetime(2012, 5, 16, 0, 0), datetime(2018, 8, 12, 12, 35, 0,
                                                                                              313337))]}}}
        employee_struct, _ = solution_sirma.detect_longest_team_mates(employee_struct)
        expected_teammates = {'143': 879, '218': 482}
        self.assertEqual(expected_teammates, employee_struct['100']['teammates'])

    def test_parse_file(self):
        file_contents = '''143, 12, 2013-11-01, 2014-01-05
                            143, 10, 2011-03-27, 2011-04-27
                            143, 10, 2009-01-01, 2011-04-27
                            100, 10, 2009-01-01, 2011-04-27
                            100, 10, 2014-01-01, 2015-04-27'''
        f_path = '/tmp/temp_table'
        with open(f_path, 'w') as f:
            f.write(file_contents)
        expected_employee_struct = {
            '100': {'teammates': {}, 'projects': {'10': [(datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                         (datetime(2014, 1, 1, 0, 0), datetime(2015, 4, 27, 0, 0))]}},
            '143': {'teammates': {}, 'projects': {'10': [(datetime(2011, 3, 27, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                         (datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0))],
                                                  '12': [(datetime(2013, 11, 1, 0, 0), datetime(2014, 1, 5, 0, 0))]}}}
        self.assertEqual(expected_employee_struct, solution_sirma.parse_file(f_path))
        os.remove(f_path)

    def test_main_prints_longest_teammates_to_the_console(self):
        expected = "The pair of employees working together the most are '100','143', for total of '911' days.\n"
        command = 'python solution_sirma.py -f pm_table.csv'
        output = subprocess.check_output(command, shell=True)
        self.assertEqual(expected, output)

    def test_get_teammates_projects_and_work_duration(self):
        employee_struct = {'100': {'teammates': {},
                                   'projects': {'10': [(datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                       (datetime(2014, 1, 1, 0, 0), datetime(2015, 4, 27, 0, 0))],
                                                '15': [(datetime(2009, 1, 1, 0, 0), datetime(2009, 2, 1, 0, 0))]}},
                           '143': {'teammates': {},
                                   'projects': {'10': [(datetime(2011, 3, 27, 0, 0), datetime(2011, 4, 27, 0, 0)),
                                                       (datetime(2009, 1, 1, 0, 0), datetime(2011, 4, 27, 0, 0))],
                                                '15': [(datetime(2009, 1, 1, 0, 0), datetime(2009, 2, 1, 0, 0))]}},
                           '218': {'teammates': {},
                                   'projects': {'10': [(datetime(2012, 5, 16, 0, 0), datetime(2018, 8, 12, 12, 35, 0,
                                                                                              313337))]}}}
        emp1 = '100'
        emp2 = '143'
        result = solution_sirma.get_teammates_projects_and_work_duration(emp1, emp2, employee_struct)
        expected = {'10': 879, '15': 32}
        self.assertEqual(expected, result)

if __name__ == '__main__':
    unittest.main()
