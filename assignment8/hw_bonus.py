from collections import defaultdict

"""
💎 Exercise-1 (Longest Consecutive Sequence):
Write a function "longest_consecutive(my_list: list[int]) -> int" that takes a 
list of integers and returns the length of the longest consecutive elements 
sequence in the list. The list might be unsorted.

Example:

longest_consecutive([100, 4, 200, 1, 3, 2]) -> 4
"""

def longest_consecutive(my_list: list[int]) -> int:
    s1 = set(my_list)
    max_count = 0 

    for v in my_list:
        x = v
        while v in s1: 
            v += 1 
        max_count = max(max_count, v-x) 

    return max_count 


"""
💎 Exercise-2 (Find missing number):
Write a function "find_missing(my_list: list[int]) -> int" that takes a 
list of integers from 1 to n. The list can be unsorted and have one 
number missing. The function should return the missing number.

Example:

find_missing([1, 2, 4]) -> 3
"""

def find_missing(my_list: list[int]) -> int:

    end = max(my_list)
    res = sum(list(range(end+1))) - sum(my_list) 
    
    return res if res != 0 else None 

                                                                
"""
💎 Exercise-3 (Find duplicate number):
Write a function "find_duplicate(my_list: list[int]) -> int" that takes a list 
of integers where each integer is in the range of 1 to n (n is the size of the list). 
The list can have one number appearing twice and the function should return this number.

Example:

find_duplicate([1, 3, 4, 2, 2]) -> 2
"""

def find_duplicate(my_list: list[int]) -> int:

    for i in range(len(my_list)):
        j= my_list[i]-1 
        while (my_list[i] != i) and (my_list[j] != j+1): 
            my_list[j], my_list[i] = my_list[i], my_list[j] 
    
    for i in range(len(my_list)): 
        if i != my_list[i]-1: 
            return my_list[i]
         
            

"""
💎 Exercise-4 (Group Anagrams):
Write a function "group_anagrams(words: list[str]) -> list[list[str]]" that 
takes a list of strings (all lowercase letters), groups the anagrams together, 
and returns a list of lists of grouped anagrams.

An Anagram is a word or phrase formed by rearranging the letters of 
a different word or phrase, typically using all the original letters exactly once.

group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) 
-> [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
"""

def group_anagrams(words: list[str]) -> list[list[str]]:

    res = defaultdict(list)
    for w in words: 
        word_map = [0]*26 
        for c in w: 
            word_map[ord(c)-ord('a')] += 1
        res[tuple(word_map)].append(w)
    
    return [v for k,v in res.items()]
        
    
