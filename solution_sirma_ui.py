import tkFileDialog
from Tkinter import *

import solution_sirma


def display_common_teammates_parameters():
    """Callback to display "Employee ID #1", "Employee ID #2", "Project ID", "Days worked" of the longest teammates.

    :return:
    """
    filepath = tkFileDialog.askopenfilename()
    struct = solution_sirma.parse_file(filepath)
    employee_struct, longest_teammates = solution_sirma.detect_longest_team_mates(struct)
    emp1 = longest_teammates['employees'][0]
    emp2 = longest_teammates['employees'][1]
    teammates_projects = solution_sirma.get_teammates_projects_and_work_duration(emp1, emp2, employee_struct)
    for index_row, project_name in enumerate(teammates_projects.keys(), start=1):
        for index_col, cell_entry in enumerate([emp1, emp2, project_name, teammates_projects[project_name]]):
            cell = Label(root, text=cell_entry, relief=RAISED, width=20)
            cell.grid(row=index_row, column=index_col)


def prepare_ui(master):
    """Prepare grid-table UI with button for selecting file.

    Used to display the pair of employees working together the most, their common projects and duration.
    :param master: Root window
    :return: None
    """
    column_names = ["Employee ID #1", "Employee ID #2", "Project ID", "Days worked"]
    button = Button(master, text='Select File', command=display_common_teammates_parameters)
    button.grid(row=6, column=1)
    for index, name in enumerate(column_names):
        cell = Label(root, text=name, relief=RAISED, width=20)
        cell.grid(row=0, column=index)


if __name__ == "__main__":
    root = Tk()
    prepare_ui(root)
    root.mainloop()
