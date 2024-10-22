"""
Exercise-1: Find missing elements
Write a function "missing_elements(my_list: list) -> list" that takes a
sorted list of integers and returns a list of missing integers in the range of the list.

Example:
missing_elements([1, 2, 4, 6, 7]) -> [3, 5]
"""

def missing_elements(my_list: list) -> list:
    res = []

    if len(my_list) < 2: 
        return res 

    for i in range(1, len(my_list)): 
        s,e = my_list[i-1], my_list[i]
        if e - s > 1: 
            res.extend(range(s+1, e))
    return res
         
        

"""
Exercise-2: Count occurrences
Write a function "count_occurrences(my_list: list) -> dict" that takes a
list of integers and returns a dictionary where keys are unique integers
from the list and values are their counts in the list.

Example:
count_occurrences([1, 2, 3, 1, 2, 4, 5, 4]) -> {1: 2, 2: 2, 3: 1, 4: 2, 5: 1}
"""

def count_occurrences(my_list: list) -> dict:
    res = {}

    for num in my_list: 
        res[num] = res.get(num, 0) + 1  
    return res 



"""
Exercise-4: Common elements
Write a function "common_elements(list1: list, list2: list) -> list" that takes two
lists of integers and returns a list of unique common elements.

Example:
common_elements([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]) -> [3, 4, 5]
"""

def common_elements(list1: list, list2: list) -> list:
    res = []
    visited = {}

    for num in list1: 
        if num not in visited: 
            visited[num] = 1 
    
    for num in list2: 
        if num in visited and visited[num] == 1: 
            res.append(num)
            visited[num] = 0 
    return res 


"""
Exercise-5: Character frequency
Write a function "char_frequency(my_string: str) -> dict" that takes a
string and returns a dictionary with the frequency of each character in the string.

Example:
char_frequency('hello world') -> {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
"""

def char_frequency(my_string: str) -> dict:
    res = {}
    for char in my_string: 
        res[char] = res.get(char, 0) + 1 
    return res 

"""
Exercise-6: Unique words
Write a function "unique_words(my_string: str) -> int" that takes a
string and returns the number of unique words in the string.

Example:
unique_words('hello world hello') -> 2
"""

def unique_words(my_string: str) -> int:
    if not my_string: 
        return 0 

    unique = set()
    words = my_string.split(" ")

    for w in words: 
        if (w != '') and (w not in unique): 
            unique.add(w)
    return len(unique)


"""
Exercise-7: Word frequency
Write a function "word_frequency(my_string: str) -> dict" that takes a
string and returns a dictionary with the frequency of each word in the string.

Example:
word_frequency('hello world hello') -> {'hello': 2, 'world': 1}
"""

def word_frequency(my_string: str) -> dict:
    res = {}

    if not my_string: 
        return res 
    
    words = my_string.split(" ")
    for w in words: 
        if (w != ""): 
            res[w] = res.get(w, 0) + 1 
    return res 

"""
Exercise-8: Count elements in range
Write a function "count_in_range(my_list: list, start: int, end: int) -> int" that
takes a list of integers and two integers as range boundaries and
returns the count of unique elements within that range in the list.

Example:
count_in_range([1, 2, 3, 4, 5, 4, 3, 2, 1], 2, 4) -> 3
"""

def count_in_range(my_list: list, start: int, end: int) -> int:
    unique = set(range(start, end+1))
    res = 0 

    for num in my_list: 
        if num in unique: 
            res += 1
            unique.remove(num)
    return res 



"""
Exercise-9: Swap dictionary keys and values
Write a function "swap_dict(d: dict) -> dict" that takes a dictionary
and returns a new dictionary where keys become values and values become keys.
if you face duplicates, the first key should be saved.

Example:
swap_dict({1: 'a', 2: 'b', 3: 'c'}) -> {'a': 1, 'b': 2, 'c': 3}
"""

def swap_dict(d: dict) -> dict:
    res = {}

    for key, val in d.items(): 
        if val not in res: 
            res[val] = key 
    return res 

"""
Exercise-10: Subset check
Write a function "is_subset(set1: set, set2: set) -> bool" that takes two
sets and returns True if set2 is a subset of set1, and False otherwise.

Example:
is_subset({1, 2, 3, 4, 5}, {3, 4, 5}) -> True
"""

def is_subset(set1: set, set2: set) -> bool:
    '''
    Using Python's built-in function: 

    def is_subset(set1: set, set2: set) -> bool:
        return set2.issubset(set1)
    
    '''

    for el in set2: 
        if el not in set1: 
            return False 
    return True 



"""
Exercise-11: Intersection of lists
Write a function "list_intersection(list1: list, list2: list) -> list" that takes two
lists and returns a list of unique elements that are in both lists.

Example:
list_intersection([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]) -> [3, 4, 5]
"""

def list_intersection(list1: list, list2: list) -> list:
    res = []
    visited = {}

    for num in list1: 
        if num not in visited: 
            visited[num] = 1 
    
    for num in list2: 
        if num in visited and visited[num] == 1: 
            res.append(num)
            visited[num] = 0 
    return res 


"""
Exercise-12: Union of lists
Write a function "list_union(list1: list, list2: list) -> list" that takes two
lists and returns a list of unique elements that are in either of the lists.

Example:
list_union([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]) -> [1, 2, 3, 4, 5, 6, 7]
"""

def list_union(list1: list, list2: list) -> list:
    s1 = set(list1) 

    for el in list2: 
        if el not in s1: 
            s1.add(el)
    return list(s1)



"""
Exercise-13: Most frequent element
Write a function "most_frequent(my_list: list) -> int" that takes a
list of integers and returns the most frequent element in the list.

Example:
most_frequent([1, 2, 3, 1, 2, 4, 5, 4, 1]) -> 1
"""

def most_frequent(my_list: list) -> int:
    res, max_count = None, -float('inf')
    counts = {}

    for num in my_list: 
        counts[num] = counts.get(num, 0) + 1 
        if counts[num] > max_count: 
            res = num 
            max_count = counts[num]
    return res 


"""
Exercise-14: Least frequent element
Write a function "least_frequent(my_list: list) -> int" that takes a
list of integers and returns the least frequent element in the list.

Example:
least_frequent([1, 2, 3, 1, 2, 4, 5, 4, 1]) -> 3
"""

def least_frequent(my_list: list) -> int:
    res = {}

    for val in my_list: 
        res[val] = res.get(val, 0) + 1 
    return min(res, key=res.get) 

