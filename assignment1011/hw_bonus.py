"""
💎 Exercise-1: Memoized Fibonacci
Implement a memoized version of the Fibonacci sequence. The function "memoized_fibonacci(n: int) -> int" should return the nth number in the Fibonacci sequence, and it should use a cache to improve performance on subsequent calls.

Example:
memoized_fibonacci(10) -> 55
"""

def memoized_fibonacci(n: int) -> int:
    
    memo = {}
    def fib(n): 
        if n < 2: 
            return n 
        if n in memo: 
            return memo[n]
        memo[n] = fib(n-1) + fib(n-2)
        return memo[n] 
    return fib(n)
    

"""
💎 Exercise-2: Currying Function
Write a function "curry(func, *args)" that implements currying. The function should return a new function that when called will return the result of applying the input function to the provided arguments, followed by the new arguments.

Example:
def add_three_numbers(a, b, c):
    return a + b + c
add_five_and_six = curry(add_three_numbers, 5, 6)
add_five_and_six(7) -> 18
"""

def curry(func, *args):
    def partial(*new_args): 
        return func(*args, *new_args)
    return partial 


"""
💎 Exercise-3: Implement zip() using map() and lambda
Write a function "my_zip(*iterables)" that takes in multiple iterables and returns an iterator that aggregates elements from each of the iterables.

Example:
my_zip([1, 2, 3], [4, 5, 6]) -> [(1, 4), (2, 5), (3, 6)]
"""

def my_zip(*iterables):  
    return map(lambda *args: args, *iterables)


"""
💎 Exercise-4: Caching Decorator
Write a decorator "caching_decorator(func)" that caches the results of the function it decorates.

Example:
@caching_decorator
def expensive_function(x, y):
    # Simulate an expensive function by sleeping
    import time
    time.sleep(5)
    return x + y
"""

def caching_decorator(func):
    
    cache = {}
    def memo(*args): 
        if args in cache: 
            return cache[args]
        cache[args] = func(*args)
        return cache[args]
    return memo 



"""
💎 Exercise-5: Recursive Flattening
Write a function "recursive_flatten(input_list: list) -> list" that takes a nested list and flattens it.

Example:
recursive_flatten([1, [2, [3, 4], 5]]) -> [1, 2, 3, 4, 5]
"""

def recursive_flatten(input_list: list) -> list:
    
    res = []
    def dfs(nums): 
        for el in nums: 
            if isinstance(el, int): 
                res.append(el)
                continue 
            dfs(el)
    
    dfs(input_list)
    return res 



"""
💎 Exercise-6: Decorator for Checking Function Arguments
Write a decorator "check_args(*arg_types)" that checks the types of the arguments passed to the function it decorates.

Example:
@check_args(int, int)
def add(a, b):
    return a + b
"""

def check_args(*arg_types):

    def decorator(func): 
        def wrapper(*args, **kwargs): 
            if len(args) != len(arg_types):
                raise TypeError(f"Function '{func.__name__}' expected {len(arg_types)} arguments")
            
            for a,t in zip(args, arg_types):
                if not isinstance(a, t):
                    raise TypeError(f"Argument {a} of function '{func.__name__}' must be of type {t.__name__}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator
        