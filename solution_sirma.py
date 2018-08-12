import argparse
from collections import namedtuple
from datetime import datetime
import copy
import csv


def _convert_to_datetime_object(date_string):
    """Take date in string format YYYY-MM-DD and convert it to datetime object.

    If date_string is NULL convert it to datetime object with 'today's' date.
    :param date_string: date in a string format YYYY-MM-DD
    :return: datetime object
    """
    time_format = '%Y-%m-%d'
    if date_string == 'NULL':
        return datetime.today()
    return datetime.strptime(date_string, time_format)


def _check_overlapping_times(dates_1, dates_2):
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


def _parse_file(filepath):
    """Parses csv type file and returns parsed contents in a form suitable for further processing.

    File is having the following format: EmpID, ProjectID, ,
    :param filepath: Path to file
    :return employee_struct: {'EmpID': {'teammates': {}, 'projects': {'10': [(datetime('DateFrom'), datetime('DateTo'))]}}}
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
                    employee_struct[emp_id]= {'projects':{proj_id: [(start, end)]}, 'teammates':{}}
                else:
                    if proj_id not in employee_struct[emp_id]['projects']:
                        employee_struct[emp_id]['projects'][proj_id] = [(start, end)]
                    else:
                        employee_struct[emp_id]['projects'][proj_id].append((start, end))

    except (TypeError, IOError):
        print "Error opening file path '{}'".format(filepath)
    return employee_struct


def _detect_longestteam_mates(struct):
    """Find the pair of employees that worked together the most on the same projects.

    :param struct: Dictionary returned from _parse_file function
    :return employee_struct: Modified employee structure containing 'teammates' key for every employee
    :return  longest_teammates: Dictionary containing the pair of employees that worked together the most and total duration
    """
    longest_teammates = {'days': 0, 'employees': ['', '']}
    employee_struct = copy.deepcopy(struct)
    employee_list = employee_struct.keys()
    for emp_index, emp1 in enumerate(employee_list):
        for emp2 in employee_list[emp_index + 1:]:
            if emp1 != emp2:
                for proj in employee_struct[emp1]['projects']:
                    if proj in employee_struct[emp2]['projects']:
                        overlap = _check_overlapping_times(employee_struct[emp1]['projects'][proj],
                                                           employee_struct[emp2]['projects'][proj])
                        if overlap > 0:
                            if not emp2 in employee_struct[emp1]['teammates']:
                                employee_struct[emp1]['teammates'][emp2] = overlap
                            else:
                                employee_struct[emp1]['teammates'][emp2] += overlap
                            if overlap > longest_teammates['days']:
                                longest_teammates['days'] = overlap
                                longest_teammates['employees'] = [emp1, emp2]
    return employee_struct, longest_teammates

def main(filepath):
    """Main function orchestrating the finding the pair of employees working together and printing it to stdout.

    :param filepath: Path to input file
    :return: 0 if execution successful
    """
    struct = _parse_file(filepath)
    _, longest_teammates = _detect_longestteam_mates(struct)
    print ("The pair of employees working together the most are "
        "'{}','{}', for total of '{}' days.").format(longest_teammates['employees'][0],
                                                     longest_teammates['employees'][1],
                                                     longest_teammates['days'])
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Provide path to file')
    parser.add_argument('-f', type=str, help='Provide path to file')
    args = parser.parse_args()
    main(args.f)
