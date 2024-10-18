import math 

"""
💎 Exercise-1: count_substrings
Write a function "count_substrings(s: str, subs: str) -> int" that takes 
two strings 's' and 'subs' and returns the number of non-overlapping 
occurrences of the substring 'subs' in the string 's'.

Example:
count_substrings("ababab", "ab") -> 3
count_substrings("aaaaaa", "aa") -> 3
"""

def count_substrings(s: str, subs: str) -> int:
    
    i, j = 0, 0 
    count = 0 

    while i < len(s): 
        while (i < len(s)) and (j < len(subs)) and (s[i] == subs[j]): 
            i += 1
            j += 1
        if j == len(subs): 
            count += 1 
            i -= 1

        j = 0 
        i += 1
    return count 


"""
💎 Exercise-2: find_smallest_divisor
Write a function "find_smallest_divisor(n: int) -> int" that 
takes a positive integer 'n' and returns the smallest prime divisor of 'n'.

Example:
find_smallest_divisor(21) -> 3
find_smallest_divisor(49) -> 7
"""

def find_smallest_divisor(n: int) -> int:
    
    def is_prime(n: int) -> bool:
        if n <= 0: 
            return False 
        if n == 1: 
            return False 
        
        for i in range(2, int(math.sqrt(n))+1):
            if n % i == 0: 
                return False 
        return True
    
    
    for i in range(2, int(math.sqrt(n))+1): 
        if is_prime(i) and n % i == 0: 
            return i 

"""
💎 Exercise-3: check_divisible_by_any
Write a function "check_divisible_by_any(n: int, divisors: str) -> bool" that 
takes a positive integer 'n' and a string 'divisors' containing a sequence of 
space-separated integers, and returns True if 'n' is divisible by 
any of the integers in the 'divisors' string.

Example:
check_divisible_by_any(24, "2 3 5") -> True
check_divisible_by_any(23, "2 3 5") -> False
"""

def check_divisible_by_any(n: int, divisors: str) -> bool:
    
    nums = [int(s) for s in divisors.split(" ")]

    for candidate in nums: 
        if n % candidate == 0: 
            return True 
    return False 


"""
💎 Exercise-4: find_nth_root
Write a function "find_nth_root(x: float, n: int) -> float" that 
takes a float 'x' and an integer 'n' and returns the 'n'-th root 
of 'x' with a precision of up to 3 decimal places.

Example:
find_nth_root(8, 3) -> 2.0
find_nth_root(81, 4) -> 3.0
"""

def find_nth_root(x: float, n: int) -> float:

    left, right = 1.0, x 
    while left <= right: 
        mid = left + (right-left) // 2
        if mid**n == x: 
            return mid 
        elif mid**n > x: 
            right = mid - 1.0
        else: 
            left = mid + 1.0 
    return left 


"""
💎 Exercise-5: collatz_sequence_length
Write a function "collatz_sequence_length(n: int) -> int" that takes a 
positive integer 'n' and returns the number of steps it takes to reach 1 
using the Collatz conjecture. The Collatz conjecture states that for 
any positive integer 'n', if 'n' is even, it should be divided by 2; 
if 'n' is odd, it should be multiplied by 3 and then add 1. Repeat this 
process until 'n' becomes 1.

Example:
collatz_sequence_length(6) -> 8
collatz_sequence_length(27) -> 111
"""

def collatz_sequence_length(n: int) -> int:

    res = 0 
    def dfs(n):
        nonlocal res 
        if n == 1: 
            return 
        res += 1
        if n % 2 == 0: 
            return dfs(n/2)
        return dfs(3*n+1)
    
    dfs(n)
    return res
