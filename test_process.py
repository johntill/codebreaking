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
    row = assign_type(row)
    # print(row)
    rotors = row[1]
    count_rotors[rotors] += 1
    if count_rotors[rotors] < 21:
        return row

# count_rotors = defaultdict(int)

with open(filename) as f:
    data = csv.reader(f)
    # results = [assign_type(row) for row in data]
    count_rotors = defaultdict(int)
    # results = []
    # for row in data:
    #     row = assign_type(row)
    #     rotors = row[1]
    #     count_rotors[rotors] += 1
    #     if count_rotors[rotors] < 21:
    #         results.append(row)
    results = [append_row(row)for row in data]

print(len(results))

for row in results:
    if row[1] == (4,3,1):
        print(row)
