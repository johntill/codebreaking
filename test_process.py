import timeit

code_to_test = """
import csv
import re
from collections import defaultdict

filename = 'enigma_results.csv'

def assign_type(row):
    IC = float(row[0])
    rotors = tuple([int(s) for s in re.findall(r'\d+', row[1])])
    settings = [int(s) for s in re.findall(r'\d+', row[2])]
    return IC, rotors, settings

def append_row(row):
    count_rotors[row[1]] += 1
    return assign_type(row)

with open(filename) as f:
    data = csv.reader(f)
    count_rotors = defaultdict(int)
    results = [append_row(row) for row in data if count_rotors[row[1]] < 20]


"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)