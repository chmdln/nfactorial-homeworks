import time 
import functools

"""
Exercise-1: First-class Function Operation
Write a function "operation(func, x: int, y: int) -> int" that takes in a function 'func' and two integers, 'x' and 'y'. Apply the function to the two numbers and return the result. 

Example:
def multiply(a, b):
    return a * b
operation(multiply, 5, 3) -> 15
"""

def operation(func, x: int, y: int) -> int:
    res = func(x,y)
    return res 

"""
Exercise-2: Implement Map Function
Write a function "my_map(func, my_list: list) -> list" that mimics the built-in Python 'map' function. It should take a function and a list as input, applying the function to each element of the list.

Example:
my_map(lambda x: x**2, [1, 2, 3, 4]) -> [1, 4, 9, 16]
"""

def my_map(func, my_list: list) -> list:
    res = []
    for el in my_list: 
        res.append(func(el))
    return res 

"""
Exercise-3: Lambda Function with Filter
Write a function "filter_even_numbers(numbers: list) -> list" that uses 'filter' and a lambda function to filter out all even numbers from the list.

Example:
filter_even_numbers([1, 2, 3, 4, 5, 6, 7, 8]) -> [1, 3, 5, 7]
"""

def filter_even_numbers(numbers: list) -> list:
    return list(filter(lambda x: x % 2 == 1, numbers)) 

"""
Exercise-4: Recursive Factorial
Write a function "recursive_factorial(n: int) -> int" that calculates the factorial of a number recursively.

Example:
recursive_factorial(5) -> 120
"""

def recursive_factorial(n: int) -> int:

    def factorial(n):  
        if n == 1: 
            return 1
        return n*factorial(n-1) 
    return factorial(n)
    

"""
Exercise-5: Decorator for Timing
Write a decorator function "timeit_decorator(func)" that prints the time taken by the function to execute.

Example:
@timeit_decorator
def sample_func():
    return [i**2 for i in range(10000)]
"""

def timeit_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs) 
        end_time = time.time()
        execution_time = end_time - start_time  
        print(f"Execution time of function '{func.__name__}': {execution_time}")
        return res 
    return wrapper 


"""
Exercise-6: Function Composition
Write a function "compose(*funcs)" that takes a series of functions and returns a new function that composes them. The returned function should take an input and apply each function to the result of the previous function.

Example:
def double(x):
    return 2 * x
def square(x):
    return x ** 2
new_func = compose(double, square)
new_func(3) -> 36
"""

def compose(*funcs):
    def composition(x): 
        for f in funcs: 
            x = f(x)
        return x 
    return composition 
        

"""
Exercise-7: Partial Application
Write a function "partial(func, *args)" that implements partial application. The function should return a new function that when called will return the result of applying the input function to the provided arguments, followed by the new arguments.

Example:
def add_three_numbers(a, b, c):
    return a + b + c
add_five_and_six = partial(add_three_numbers, 5, 6)
add_five_and_six(7) -> 18
"""

def partial(func, *args):
    def apply(*x): 
        return func(*args, *x)
    return apply 


"""
Exercise-8: Reduce to Compute Factorial
Write a function "factorial_reduce(n: int) -> int" that uses `reduce` to compute the factorial of an integer.

Example:
factorial_reduce(5) -> 120
"""

def factorial_reduce(n: int) -> int:
    return functools.reduce(lambda x, y: x*y, list(range(1,n+1))) 


"""
Exercise-9: Function Memoization
Write a function "memoize(func)" that takes a function and returns a memoized version of the function. The memoized version should cache the results of the function so that the next time it's called with the same arguments, it returns the cached value instead of calculating the result again.

Example:
def expensive_function(x):
    return x ** x  # expensive calculation
memoized_function = memoize(expensive_function)
memoized_function(5)  # -> This will take some time to compute
memoized_function(5)  # -> This will return the cached result
"""

def memoize(func):

    cache = {}
    def memo(*args): 
        if args in cache: 
            return cache[args]
        cache[args] = func(*args)
        return cache[args]
    return memo 



"""
Exercise-10: Custom Reduce Function
Implement your own version of Python's 'reduce' function "my_reduce(func, iterable, initializer=None)".

Example:
my_reduce(lambda x, y: x*y, [1, 2, 3, 4]) -> 24
"""

def my_reduce(func, iterable, initializer=None):
    it = iter(iterable)

    if initializer is None:
        try:
            result = next(it)
        except StopIteration:
            raise TypeError("my_reduce() of empty sequence with no initial value")
    else:
        result = initializer

    for element in it:
        result = func(result, element)
    return result 


"""
Exercise-11: Lambda Function Sort
Write a function "sort_by_last_letter(words: list) -> list" that sorts a list of words in ascending order based on the last letter of each word. Use a lambda function.

Example:
sort_by_last_letter(['apple', 'banana', 'cherry', 'date']) -> ['banana', 'apple', 'date', 'cherry']
"""

def sort_by_last_letter(words: list) -> list:
    return sorted(words, key=lambda x: x[-1])

"""
Exercise-12: Recursive List Reversal
Write a function "recursive_reverse(my_list: list) -> list" that reverses a list using recursion.

Example:
recursive_reverse([1, 2, 3, 4, 5]) -> [5, 4, 3, 2, 1]
"""

def recursive_reverse(my_list: list) -> list:
    
    def dfs(l,r): 
        if l > r: 
            return my_list 
        my_list[l], my_list[r] = my_list[r], my_list[l]
        return dfs(l+1, r-1)
    
    return dfs(0, len(my_list)-1)

"""
Exercise-13: Decorator for Function Counting
Write a decorator function "count_calls(func)" that counts the number of times a function is called.

Example:
@count_calls
def test_function():
    return

test_function()
test_function()
# Output: 'test_function' was called 2 times.
"""

def count_calls(func):
     
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs) 
        wrapper.counter += 1 
        return f"function {func.__name__} was called {wrapper.counter} times"
    
    wrapper.counter = 0 
    return wrapper 



"""
Exercise-14: Use reduce to Find the Maximum Number
Write a function "find_max(numbers: list) -> int" that uses reduce to find the maximum number in a list.

Example:
find_max([1, 2, 3, 4, 5]) -> 5
"""

def find_max(numbers: list) -> int:
    return functools.reduce(lambda x,y: max(x,y), numbers)


"""
Exercise-15: Use filter and lambda to Remove Elements
Write a function "remove_elements(my_list: list, element) -> list" that uses filter and a lambda function to remove all instances of a specific element from a list.

Example:
remove_elements([1, 2, 3, 2, 4, 2, 5], 2) -> [1, 3, 4, 5]
"""

def remove_elements(my_list: list, element):
    return list(filter(lambda x: x != element, my_list))


"""
Exercise-16: Higher-Order Function for Repeats
Write a function "repeat(n: int)" that returns a function. The returned function should take a string input and repeat it `n` times.

Example:
repeat_three_times = repeat(3)
repeat_three_times('hello') -> 'hellohellohello'
"""

def repeat(n: int):
    
    def wrapper(s): 
        return s*n 
    return wrapper 


"""
Exercise-17: Recursive List Sum
Write a function "recursive_sum(my_list: list) -> int" that recursively computes the sum of a list of integers.

Example:
recursive_sum([1, 2, 3, 4, 5]) -> 15
"""

def recursive_sum(my_list: list) -> int:
    
    def dfs(i, s): 
        if not my_list: 
            return 0 
        if i == len(my_list):
            return s 
        s += my_list[i] 
        return dfs(i+1, s)
    
    return dfs(0, 0) 


"""
Exercise-18: Map with Multiple Lists
Write a function "add_two_lists(list1: list, list2: list) -> list" that uses `map` and `lambda` to add together corresponding elements of two lists.

Example:
add_two_lists([1, 2, 3], [4, 5, 6]) -> [5, 7, 9]
"""

def add_two_lists(list1: list, list2: list) -> list:
    return list(map(lambda x,y: x+y, list1, list2))