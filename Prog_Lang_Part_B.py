##########################################################
# Question 1
print("\n\nQuestion 1\n\n")
##########################################################

fibonacci = lambda n, a=0, b=1: [a] + fibonacci(n - 1, b, a + b) if n > 0 else []
print("The first 10 numbers in the Fibonacci sequence are:")
print(fibonacci(10))

##########################################################
# Question 2
print("\n\nQuestion 2\n\n")
##########################################################

concat_strings = lambda lst: lst[0] if len(lst) == 1 else lst[0] + ' ' + concat_strings(lst[1:])
example_str_list = ["These", "were", "separate", "strings"]
print(f"Original list of strings: {example_str_list}")
print(f"String after running concat_strings: {concat_strings(example_str_list)}")

##########################################################
# Question 3
print("\n\nQuestion 3\n\n")


##########################################################

def cumulative_sum_of_squares(lst):
    return list(map(lambda sublist: sum(map(lambda x: x ** 2, filter(lambda y: y % 2 == 0, sublist))), lst))


example_list_of_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9, 10]]
print(f"Original list of lists: {example_list_of_lists}")
print(
    f"Result set of accumulated even number squares of each list: {cumulative_sum_of_squares(example_list_of_lists)}")

##########################################################
# Question 4
print("\n\nQuestion 4\n\n")


##########################################################


def cumulative_operation(operation):
    return lambda sequence: sequence[0] if len(sequence) == 1 else operation(sequence[0],
                                                                             cumulative_operation(operation)(
                                                                                 sequence[1:]))


factorial = lambda n: cumulative_operation(lambda x, y: x * y)(range(1, n + 1))
exponential = lambda base, exp: cumulative_operation(lambda x, y: x * y)([base] * exp)

print(f"Factorial of 5 is {factorial(5)}")
print(f"2 exponent 4 is {exponential(2, 4)}")

##########################################################
# Question 5
print("\n\nQuestion 5\n\n")
##########################################################
from functools import reduce

sum_squared = reduce(lambda acc, x: acc + x, map(lambda y: y ** 2, filter(lambda z: z % 2 == 0, [1, 2, 3, 4, 5, 6])))

print(f"Sum of square 2^2 + 4^2 + 6^2 = 4 + 16 + 36 = {sum_squared}")

##########################################################
# Question 6
print("\n\nQuestion 6\n\n")
##########################################################


count_palindromes = lambda lst: list(
    map(lambda sublist: reduce(lambda acc, s: acc + 1, filter(lambda x: x == x[::-1], sublist), 0), lst))

example_list_of_lists_of_palindromes = [["abab", "aabbaa", "aaaaa"], ["YGH", "aaab", "SkibididibikS"],
                                        ["Hello", "world", "aaabaaa"]]

print(f"Original list of lists: {example_list_of_lists_of_palindromes}")
print(f"Number of palindromes in each list: {count_palindromes(example_list_of_lists_of_palindromes)}")

##########################################################
# Question 7
print("\n\nQuestion 7\n\n")
##########################################################
print("Text based question, answer is written as a comment in the code.")
'''
Lazy evaluation is a programming concept where an expression will not be evaluated until its value is actually needed.
This is usually done for increased efficiency especially when working with large datasets.

The function 'generate_values()' uses the 'yield' keyword, so this means it is a generator. The generator provides
values only when required rather than generating all values at once.

Eager evaluation is the more common approach of computing all values upfront.
'generate_values()' is called and converted into a list, then the generator produces all values (1, 2, 3) at once
and then prints "Generating values...". Then, the squared_values variable will compute the square of each value in the 
'values' list, printing the following:
"Squaring 1"
"Squaring 2"
"Squaring 3"
All values are evaluated as soon as they are encountered.


On the contrary, lazy evaluation occurs when only the values that are needed are computed.
In this part, 'generate_values()' is passed straight into the list comprehension without converting to a list.
Then, the generator produces values one at a time while the list comprehension iterates over it.
For each value the generator produces (1, 2, 3), the 'square(x)' function is then called, printing the following:
"Squaring 1"
"Squaring 2"
"Squaring 3"
Once the generator starts producing values, only then will the program print "Generating values..." and each value
is squared only when it's needed in the list comprehension.

The main differences between the two are:
Memory usage:       In eager evaluation the entire list is created and stored in memory, while in lazy evaluation only
                    the necessary values are kept in memory.
                    
Value generation:   In eager evaluation all values are generated at once, while in lazy evaluation they are generated 
                    one by one.

Efficiency:         Eager evaluation executes all operations immediately regardless of whether we need the results or 
                    not, while lazy evaluation is more efficient for operations where not all values are used.

'''

##########################################################
# Question 8
print("\n\nQuestion 8\n\n")
##########################################################


get_primes_desc = lambda lst: sorted([x for x in lst if x > 1 and all(x % i != 0 for i in range(2, int(x ** 0.5) + 1))],
                                     reverse=True)

example_list_of_primes = [1, 2, 3, 7, 15, 8, 23, 11, 19, 17]
print(f"Original list of primes: {example_list_of_primes}")
print(f"Primes sorted by descending order: {get_primes_desc(example_list_of_primes)}")
