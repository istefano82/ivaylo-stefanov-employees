import argparse
from collections import namedtuple
from datetime import datetime
import csv
import os


def _convert_to_datetime_object(date_string):
    '''Take date in string format YYYY-MM-DD and convert it to datetime object.

    If date_string is NULL convert it to datetime object with 'today's' date.'''
    time_format = '%Y-%m-%d'
    if date_string == 'NULL':
        return datetime.today()
    return datetime.strptime(date_string, time_format)
    
def _check_overlapping_times(dates_1, dates_2):
    '''Takes two lists of tuples containing start and end dates.

    Return total overlap interval in days between any of the tuples.
    '''
    total_overlap = 0
    for d1_start, d1_end in dates_1:
        for d2_start, d2_end in dates_2:
            range_ = namedtuple('Range', ['start', 'end'])
            r1 = range_(start=d1_start, end=d1_end)
            r2 = range_(start=d2_start, end=d2_end)
            latest_start = max(r1.start, r2.start)
            earliest_end = min(r1.end, r2.end)
            total_overlap += (earliest_end - latest_start).days + 1
    return max(0, total_overlap)

def _detect_longestteam_mates(filepath):
    employee_struct = {}
    try:
        with open(filepath, 'rb') as csvfile:
            csv_reader = csv.reader(csvfile, skipinitialspace=True)
            for row in csv_reader:
                # catchg errors due to empty row in the file
                try:
                    emp_id, proj_id, start, end = row
                except ValueError:
                    continue
                start = _convert_to_datetime_object(start)
                end = _convert_to_datetime_object(end)
                if emp_id not in employee_struct:
                       # @TODO check case where employee has been working mutiple times on same project
                    employee_struct[emp_id] = {proj_id: [(start, end)], 'teammates':{}}
                else:
                    if proj_id not in employee_struct[emp_id]:
                        employee_struct[emp_id][proj_id] = [(start, end)]
                    else:
                        employee_struct[emp_id][proj_id].append((start, end))

    except (TypeError, IOError):
        print "Error opening file path '{}'".format(filepath)

    employee_list = employee_struct.keys()
    for emp_index, emp1 in enumerate(employee_list):
        for emp2 in employee_list[emp_index + 1:]:
            if emp1 != emp2:
                for proj in emp1:
                    # @TODO add condition to check for overlapping dates
                    if proj in emp2:
                        overlap = _check_overlapping_times(employee_struct[emp1][proj_id], employee_struct[emp2][proj_id])
                        if overlap > 0:
                            if not emp2 in employee_struct[emp1]['teammates']:
                                employee_struct[emp1]['teammates'][emp2] = overlap
                            else:
                                employee_struct[emp1]['teammates'][emp2] += overlap
                            print emp1 + ': ',  employee_struct[emp1]
    return  employee_struct
'''
    for emp1 in employee_struct.keys():
        for emp2 in employee_struct.keys():
            if emp1 != emp2:
                for proj in emp1:
                    # @TODO add condition to check for overlapping dates
                    if proj in emp2:
                        print "======================================="
                        print emp1 + ': ',  employee_struct[emp1], emp2 + ': ' ,employee_struct[emp2]
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Provide path to file')
    parser.add_argument('-f', type=str, help='Provide path to file')
    args = parser.parse_args()
    _detect_longestteam_mates(args.f)
