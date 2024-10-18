from collections import defaultdict

"""
Exercise-1: Count unique elements
Write a function "count_unique_elements(my_list: list) -> int" that takes a 
list of integers and returns the number of unique elements in the list.

Example:
count_unique_elements([1, 2, 3, 1, 2, 4, 5, 4]) -> 5
"""

def count_unique_elements(my_list: list) -> int:
    unique = set()
    for el in my_list: 
        if el not in unique: 
            unique.add(el)
    return len(unique)

"""
Exercise-2: Remove duplicates
Write a function "remove_duplicates(my_list: list) -> list" that takes a list of integers and 
removes all duplicates, returning the new list with unique elements in their original order.

Example:
remove_duplicates([1, 2, 3, 1, 2, 4, 5, 4]) -> [1, 2, 3, 4, 5]
"""

def remove_duplicates(my_list: list) -> list:
    unique = set()
    res = []
    for el in my_list:
        if el not in unique: 
            res.append(el) 
            unique.add(el)
    return res 

"""
Exercise-3: Reverse a list
Write a function "reverse_list(my_list: list) -> list" that takes a list of integers and 
returns a new list with the elements in reverse order.

Example:
reverse_list([1, 2, 3, 4, 5]) -> [5, 4, 3, 2, 1]
"""

def reverse_list(my_list: list) -> list:
    l,r = 0, len(my_list)-1 
    while l < r: 
        my_list[l], my_list[r] = my_list[r], my_list[l]
        l += 1
        r -= 1 
    return my_list 

"""
Exercise-4: Find the maximum value in a list
Write a function "max_value(my_list: list) -> int" that takes a 
list of integers and returns the maximum value in the list.

Example:
max_value([1, 2, 3, 4, 5]) -> 5
"""

def max_value(my_list: list) -> int:
    res = -float('inf')
    for v in my_list: 
        if res < v: 
            res = v 
    return res 


"""
Exercise-5: Find the minimum value in a list
Write a function "min_value(my_list: list) -> int" that takes a 
list of integers and returns the minimum value in the list.

Example:
min_value([1, 2, 3, 4, 5]) -> 1
"""

def min_value(my_list: list) -> int:
    res = float('inf')
    for v in my_list: 
        if v < res: 
            res = v 
    return res 

"""
Exercise-6: Sum all values in a list
Write a function "sum_values(my_list: list) -> int" that takes a 
list of integers and returns the sum of all values in the list.

Example:
sum_values([1, 2, 3, 4, 5]) -> 15
"""

def sum_values(my_list: list) -> int:
    return sum(v for v in my_list)

"""
Exercise-7: Find the average of a list
Write a function "average(my_list: list) -> float" that takes a 
list of integers and returns the average value of the list.

Example:
average([1, 2, 3, 4, 5]) -> 3.0
"""

def average(my_list: list) -> float:
    return sum(v for v in my_list)/len(my_list)

"""
Exercise-8: Find the index of an element in a list
Write a function "find_index(my_list: list, element: int) -> int" that takes a 
list of integers and an element, and returns the index of the first occurrence of 
the element in the list. If the element is not in the list, return -1.

Example:
find_index([1, 2, 3, 4, 5], 3) -> 2
find_index([1, 2, 3, 4, 5], 6) -> -1
"""

def find_index(my_list: list, element: int) -> int:
    for index, val in enumerate(my_list): 
        if val == element: 
            return index 
    return -1 

"""
Exercise-9: Check if a list is sorted
Write a function "is_sorted(my_list: list) -> bool" that takes a list
of integers and returns True if the list is sorted in non-descending 
order (i.e., each element is greater than or equal to the previous element), 
False otherwise.

Example:
is_sorted([1, 2, 3, 4, 5]) -> True
is_sorted([1, 3, 2, 4, 5]) -> False
"""

def is_sorted(my_list: list) -> bool:
    if len(my_list) < 2: 
        return True 
    
    for i in range(1, len(my_list)): 
        if not (my_list[i] >= my_list[i-1]): 
            return False 
    return True 

"""
Exercise-10: Count the frequency of an element in a list
Write a function "count_frequency(my_list: list, element: int) -> int" that 
takes a list of integers and an element, and returns the number of 
times the element appears in the list.

Example:
count_frequency([1, 2, 3, 4, 5, 1, 2, 3], 3) -> 2
"""

def count_frequency(my_list: list, element: int) -> int:
    return sum(1 if v == element else 0 for v in my_list)

"""
Exercise-11: Find the mode of a list
Write a function "find_mode(my_list: list) -> int" that takes a list of 
integers and returns the mode (i.e., the value that appears most frequently) 
of the list. If there are multiple modes, return any of them.

Example:
find_mode([1, 2, 3, 4, 5, 1, 2, 2, 3]) -> 2
"""

def find_mode(my_list: list) -> int:
    
    cache = defaultdict(int)
    curr_max, curr_count = None, -float('inf')

    for el in my_list: 
        cache[el] += 1
        if cache[el] > curr_count: 
            curr_count = cache[el]
            curr_max = el 
    
    return curr_max 

"""
Exercise-12: Remove all occurrences of an element in a list
Write a function "remove_all(my_list: list, element: int) -> list" 
that takes a list of integers and an element, and returns a new list 
with all occurrences of the element removed.

Example:
remove_all([1, 2, 3, 4, 5, 1, 2, 3], 3) -> [1, 2, 4, 5, 1, 2]
"""

def remove_all(my_list: list, element: int) -> list:
    res = []
    for el in my_list: 
        if el != element:  
            res.append(el)
    return res 

"""
Exercise-13: Rotate a list to the left by k positions
Write a function "rotate_left(my_list: list, k: int) -> list" that takes a 
list of integers and an integer k, and returns a new list with the elements rotated k positions to the left.

Example:
rotate_left([1, 2, 3, 4, 5], 2) -> [3, 4, 5, 1, 2]
"""

def rotate_left(my_list: list, k: int) -> list:
    
    def rotate(nums, l,r): 
        while l < r: 
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
        return nums 
    
    n = len(my_list)
    rotate(my_list, 0, k-1)
    rotate(my_list, k, n-1)
    rotate(my_list, 0, n-1)

    return my_list 



"""
Exercise-14: Rotate a list to the right by k positions
Write a function "rotate_right(my_list: list, k: int) -> list" that 
takes a list of integers and an integer k, and returns a new list 
with the elements rotated k positions to the right.

Example:
rotate_right([1, 2, 3, 4, 5], 2) -> [4, 5, 1, 2, 3]
"""

def rotate_right(my_list: list, k: int) -> list:
    
    def rotate(nums, l,r): 
        while l < r: 
            nums[l], nums[r] = nums[r], nums[l]
            l += 1
            r -= 1
        return nums 
    
    n = len(my_list)
    rotate(my_list, 0, n-k-1)
    rotate(my_list, n-k, n-1)
    rotate(my_list, 0, n-1)

    return my_list

"""
Exercise-15: Find the intersection of two lists
Write a function "find_intersection(list1: list, list2: list) -> list" that 
takes two lists of integers and returns a new list with the elements that are present in both lists.

Example:
find_intersection([1, 2, 3, 4], [3, 4, 5, 6]) -> [3, 4]
"""

def find_intersection(list1: list, list2: list) -> list:
    s1 = set(list1)
    s2 = set(list2)
    
    return [el for el in s2 if el in s1 ]

"""
Exercise-16: Find the union of two lists
Write a function "find_union(list1: list, list2: list) -> list" that takes 
two lists of integers and returns a new list with the elements that are 
present in either list (i.e., the union of the lists).

Example:
find_union([1, 2, 3, 4], [3, 4, 5, 6]) -> [1, 2, 3, 4, 5, 6]
"""

def find_union(list1: list, list2: list) -> list:
    s = set(list1)
    for el in list2: 
        if el not in s: 
            s.add(el)
    return list(s) 

"""
Exercise-17: Find the difference of two lists
Write a function "find_difference(list1: list, list2: list) -> list" that takes 
two lists of integers and returns a new list with the elements that are 
present in the first list but not the second list.
Assume that list does not contain duplicates.

Example:
find_difference([1, 2, 3, 4], [3, 4, 5, 6]) -> [1, 2]
"""

def find_difference(list1: list, list2: list) -> list:
    s2 = set(list2)
    return [el for el in list1 if el not in s2]
    
