# ivaylo-stefanov-employees

Write an application that takes a text file with EmpID, ProjectID, DateFrom, DateTo columns,
That finds and prints the pair of employees working together the most on the same projects.

Requirements:
Python version 2.7

How to use via command line:
1. Clone the repository - https://github.com/istefano82/ivaylo-stefanov-employees
2. Navigate to the directory where the project is cloned
3. Execute:</br>
  % python solution_sirma.py -f <path to file></br>
Assert following is printed in the console:</br>
  "The pair of employees working together the most are <employee_1>, <employee_2>, for total of <num_days> days."

How to use via user interface:
1. Execute:</br>
  % python solution_sirma_ui.py
2. Click the "Select File" and choose your input file
Assert gridtable showing the longest working teammates, their common projects, and duration the worked on them.

Supported date formats:

Note: Be consistent with the dates you use! Do not mix ddmmyy with mmddyy!

No.	Format	                Example</br>
1	dd/mm/yy	            03/08/06 </br>
2	dd/mm/yyyy	            03/08/2006</br>
3	d/m/yy	                3/8/06</br>
4	d/m/yyyy	            3/8/2006</br>
5	ddmmyy	                030806</br>
6	ddmmyyyy	            03082006</br>
7	ddmmmyy	                03Aug06</br>
8	ddmmmyyyy	            03Aug2006</br>
9	dd-mmm-yy	            03-Aug-06</br>
10	dd-mmm-yyyy	            03-Aug-2006</br>
11	dmmmyy	                3Aug06</br>
12	dmmmyyyy	            3Aug2006</br>
13	d-mmm-yy	            3-Aug-06</br>
14	d-mmm-yyyy	            3-Aug-2006</br>
15	d-mmmm-yy	            3-August-06</br>
16	d-mmmm-yyyy	            3-August-2006</br>
17	yyyy/mm/dd	            2006/08/03</br>
18	mmm-dd-yy	            Aug-03-06</br>
19	mmm-dd-yyyy	            Aug-03-2006</br>
20	yyyy-mm-dd	            2006-08-03</br>
21  mmmm-d-yyyy	            August-03-06</br>
22  mmmm-d-yyyy	            Aug-03-06</br>
