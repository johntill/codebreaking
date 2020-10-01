import timeit

code_to_test = """


"""

elapsed_time = timeit.timeit(code_to_test, number = 1)#/1000
print(elapsed_time)