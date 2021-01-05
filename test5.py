import timeit

code_to_test = """
key = [3,2,1,4,0]
key_len = len(key)
num_long_col = 4


long_columns = set(key[:num_long_col])
# align = count = 0

for _ in range(1):
    for x in range(key_len-1):
        i, j = key[x], key[x+1]
        k, l = (j, i) if i > j else (i, j)
        columns = set(range(k,l))
        number_of_columns = len(long_columns & columns)

        print(number_of_columns)


"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)