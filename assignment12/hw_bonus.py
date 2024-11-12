from typing import List, Any, Dict, Tuple, Generator

"""
Exercise-1: Prime Sieve with List Comprehension
Write a function "sieve_of_eratosthenes(n: int) -> List[int]" that implements the Sieve of Eratosthenes to generate all prime numbers less than 'n'. 
Use a list comprehension to generate the initial list of numbers, and another to remove multiples of each prime found.

Example:
sieve_of_eratosthenes(30) -> [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
"""
def sieve_of_eratosthenes(n: int) -> List[int]:
    sieve = [True for _ in range(n)]  
    sieve[:2] = [False, False] 

    for i in range(2, int(n**0.5) + 1): 
        if sieve[i]: 
            for j in range(i*i, n, i): 
                sieve[j] = False 
    return [i for i,v in enumerate(sieve) if v] 


"""
Exercise-2: List Comprehension with Nested Loop and Condition
Write a function "triple_combinations(lst: List[int]) -> List[Tuple[int, int, int]]" that returns all unique triple combinations (i, j, k) 
from the given list that satisfy the condition i < j < k. Use a list comprehension with multiple 'for' clauses and a condition.

Example:
triple_combinations([1, 2, 3, 4]) -> [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
"""
def triple_combinations(lst: List[int]) -> List[Tuple[int, int, int]]:
    return [(i, j, k) for i in lst for j in lst for k in lst if i < j < k]



"""
Exercise-3: Nested Dictionary Comprehension
Write a function "dict_table(n: int) -> Dict[int, Dict[int, int]]" that creates a multiplication table in dictionary form. 
The keys of the outer dictionary are numbers from 1 to 'n'. The values are inner dictionaries. 
In the inner dictionary, the keys are numbers from 1 to 'n' and the values are the products of the outer and inner keys.

Example:
dict_table(3) -> {1: {1: 1, 2: 2, 3: 3}, 2: {1: 2, 2: 4, 3: 6}, 3: {1: 3, 2: 6, 3: 9}}
"""
def dict_table(n: int) -> Dict[int, Dict[int, int]]:
    return { key: {val:val*key for val in range(1, n+1)} for key in range(1, n+1) }



"""
Exercise-4: Generator of Generators
Write a function "generators(n: int) -> Generator[Generator[int]]" that creates a generator which yields 'n' number of generators. 
Each of these generators yields numbers from 1 to 'n'. 

Example:
list(map(list, generators(3))) -> [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
"""
def generators(n: int) -> Generator[Generator[int, None, None], None, None]:
    return ( (i for i in range(1, n + 1)) for _ in range(n) )


"""
Exercise-5: Nested List Comprehension to Compute Cartesian Product
Write a function "cartesian_product(set_a: List[Any], set_b: List[Any]) -> List[Tuple[Any, Any]]" that uses a nested list comprehension to compute the Cartesian product of two sets. The Cartesian product of two sets is the set of all ordered pairs (a, b) where a is in set_a and b is in set_b.

Example:
cartesian_product([1, 2], ['a', 'b']) -> [(1, 'a'), (1, 'b'), (2, 'a'), (2, 'b')]
"""
def cartesian_product(set_a: List[Any], set_b: List[Any]) -> List[Tuple[Any, Any]]:
    return [(i, j) for i in set_a for j in set_b]