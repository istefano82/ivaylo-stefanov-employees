'''
Script that find the pair of employees working the most on the same projects.

Takes CSV file in the following format: "EmpID, ProjectID, DateFrom, DateTo" as input and prints the result
to the console.
'''


import argparse
import copy
import csv
from collections import namedtuple
from datetime import datetime


def _convert_to_datetime_object(date_string):
    """Take date as string and convert it to datetime object. Supported date formats are listed in Readme.md

    If date_string is NULL convert it to datetime object with today's date.
    If no matching format is found ValueError is raised.
    :param date_string: date in a string format
    :return: datetime object
    """
    time_formats = ['%d/%m/%y', '%d/%m/%Y', '%d%m%y', '%d%m%Y', '%d%b%y', '%d%b%Y',
                    '%d-%b-%y', '%d-%b-%Y', '%d-%B-%y', '%d-%B-%Y', '%y%m%d', '%Y%m%d',
                    '%d-%B-%Y', '%b-%d-%y', '%b-%d-%Y', '%Y-%m-%d', '%Y/%m/%d', '%B-%d-%y', '%B-%d-%Y']
    if date_string == 'NULL':
        return datetime.today()
    for time_format in time_formats:
        try:
            return datetime.strptime(date_string, time_format)
        except ValueError:
            continue
    else:
        raise ValueError("time data '{}' does not match any of the supported date formats.'".format(date_string))


def _calculate_overlapping_times(dates_1, dates_2):
    """Takes two lists of tuples containing start and end dates.

    Return total overlap interval in days between any of the tuples.

    :param dates_1: List of tuples containing datetime objects
    :param dates_2: List of tuples containing datetime objects
    :return total_overlap:
    """
    total_overlap = 0
    for d1_start, d1_end in dates_1:
        for d2_start, d2_end in dates_2:
            range_ = namedtuple('Range', ['start', 'end'])
            r1 = range_(start=d1_start, end=d1_end)
            r2 = range_(start=d2_start, end=d2_end)
            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            total_overlap += max(0, (earliest_end - latest_start).days + 1)
    return total_overlap


def parse_file(filepath):
    """Parses csv type file and returns parsed contents in a form suitable for further processing.

    File is having the following format: EmpID, ProjectID, DateFrom, DateTo
    :param filepath: Path to file
    :return employee_struct: {'EmpID':
                             {'teammates': {}, 'projects': {'10': [(datetime('DateFrom'), datetime('DateTo'))]}}}
    """
    employee_struct = {}
    try:
        with open(filepath, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, skipinitialspace=True)
            for row in csv_reader:
                # catch errors due to empty row in the file
                try:
                    emp_id, proj_id, start, end = row
                except ValueError:
                    continue
                start = _convert_to_datetime_object(start)
                end = _convert_to_datetime_object(end)
                if emp_id not in employee_struct:
                    employee_struct[emp_id] = {'projects': {proj_id: [(start, end)]}, 'teammates': {}}
                else:
                    if proj_id not in employee_struct[emp_id]['projects']:
                        employee_struct[emp_id]['projects'][proj_id] = [(start, end)]
                    else:
                        employee_struct[emp_id]['projects'][proj_id].append((start, end))

    except (TypeError, IOError):
        print "Error opening file path '{}'".format(filepath)
    return employee_struct


def detect_longest_team_mates(struct):
    """Find the pair of employees that worked together the most on the same projects.

    :param struct: Dictionary returned from parse_file function
    :return employee_struct: Modified employee structure containing 'teammates' key for every employee
    :return  longest_teammates: Dictionary containing the pair of employees that worked together the most and total
                                duration
    """
    longest_teammates = {'days': 0, 'employees': ['', '']}
    employee_struct = copy.deepcopy(struct)
    employee_list = employee_struct.keys()
    for emp_index, emp1 in enumerate(employee_list):
        for emp2 in employee_list[emp_index + 1:]:
            if emp1 != emp2:
                for proj in employee_struct[emp1]['projects']:
                    if proj in employee_struct[emp2]['projects']:
                        overlap = _calculate_overlapping_times(employee_struct[emp1]['projects'][proj],
                                                               employee_struct[emp2]['projects'][proj])
                        if overlap > 0:
                            if emp2 not in employee_struct[emp1]['teammates']:
                                employee_struct[emp1]['teammates'][emp2] = overlap
                            else:
                                employee_struct[emp1]['teammates'][emp2] += overlap
                            if employee_struct[emp1]['teammates'][emp2] > longest_teammates['days']:
                                longest_teammates['days'] = employee_struct[emp1]['teammates'][emp2]
                                longest_teammates['employees'] = [emp1, emp2]
    return employee_struct, longest_teammates


def get_teammates_projects_and_work_duration(emp1, emp2, employee_struct):
    """Extract common projects for two employees and the duration they worked in each for.

    :param emp1: employee id string
    :param emp2: employee id string
    :param employee_struct: struct computed from detect_longest_team_mates
    :return: dictionary containing projects employees worked together  and the duration they worked for
    """
    result = {}
    for proj in employee_struct[emp1]['projects']:
        if proj in employee_struct[emp2]['projects']:
            overlap = _calculate_overlapping_times(employee_struct[emp1]['projects'][proj],
                                                   employee_struct[emp2]['projects'][proj])
            if overlap > 0:
                result[proj] = overlap
    return result

def main(filepath):
    """Main function orchestrating the finding the pair of employees working together and printing it to stdout.

    :param filepath: Path to input file
    :return: 0 if execution successful
    """
    struct = parse_file(filepath)
    _, longest_teammates = detect_longest_team_mates(struct)
    print ("The pair of employees working together the most are "
           "'{}','{}', for total of '{}' days.").format(longest_teammates['employees'][0],
                                                        longest_teammates['employees'][1],
                                                        longest_teammates['days'])
    return 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Provide path to file')
    parser.add_argument('-f', type=str, help='Provide path to file')
    args = parser.parse_args()
    main(args.f)
