# Exercise 1: two-sum
def two_sum(num1, num2): 
    return num1 + num2 

# Exercise 2: reverse-string
def reverse_string(s): 
    return s[::-1]

# Exercise 3: string-length
def get_length(s): 
    return len(s)

# Exercise 4: concatenate-string
def concatenate_strings(s1, s2): 
    return s1 + s2 

# Exercise 5: is-vowel
def is_vowel(char): 
    vowels = set(["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"])
    return char in vowels 

# Exercise 6: swap-first-last
def swap(s):
    n = len(s) 
    if s: 
        split_string = list(s) 
        split_string[0], split_string[n-1] = split_string[n-1], split_string[0]
        return "".join(split_string)
    return s 


# Exercise 7: to-uppercase
def to_upper(s): 
    return s.upper()

# Exercise 8: rectangle-area
def get_area(length, width): 
    return (length + width)*2 

# Exercise 9: is-even
def is_even(num): 
    return num % 2 == 0

# Exercise 10: extract-first-three
def extract(s): 
    return s[:3]

# Exercise 11: string-interpolation
def interpolate(name, age): 
    return f"This is {name}. She is {age} years old."

# Exercise 12: string-slicing
def extract_characters(s): 
    return s[2:6] 

# Exercise 13: type-conversion
def string_to_integer(s): 
    return int(s)

# Exercise 14: string-repetition
def repeat(s): 
    return s*3 

# Exercise 15: calculate-quotient-remainder
def calculate_quotient_remainder(num1, num2): 
    whole = num1 // num2 
    remain = num1 % num2 
    return f"Quotient: {whole}, Remainder: {remain}"

# Exercise 16: float-division
def float_division(num1, num2): 
    return num1/num2

# Exercise 17: string-methods
def count_character(s): 
    unique = set(s)
    return {char: s.count(char) for char in s}

# Exercise 18: escape-sequences
def escape(): 
    s = '''This is a string \"mystring\" with double quotes'''
    return s
    
# Exercise 19: multi-line-string
def multi_line(): 
    s = '''This is a multi-line string
This is a multi-line string'''
    return s

# Exercise 20: exponentiation
def exponentiate(base, exp): 
    return base**exp 

# Exercise 21: exponentiation
def is_pali(s): 
    return s == s[::-1] 

# Exercise 22: check-anagrams
def is_anagram(s1, s2):
    if len(s1) != len(s2): 
        return False 
    s1 = s1.lower()
    s2 = s2.lower()
    return sorted(s1) == sorted(s2)




if __name__ == "__main__":
    print("Exercise 1: Beginning")
    print(two_sum(23, -8))
    print("Exercise 1: End")
    print("\n")

    print("Exercise 2: Beginning")
    print(reverse_string("nFactorial"))
    print("Exercise 2: End")
    print("\n")

    print("Exercise 3: Beginning")
    print(get_length("nFactorial"))
    print("Exercise 3: End")
    print("\n")

    print("Exercise 4: Beginning")
    print(concatenate_strings("nFactorial ", "school"))
    print("Exercise 4: End")
    print("\n")

    print("Exercise 5: Beginning")
    print(is_vowel("i"))
    print(is_vowel("U"))
    print(is_vowel("h"))
    print("Exercise 5: End")
    print("\n")

    print("Exercise 6: Beginning")
    print(swap("nFactorial"))
    print("Exercise 6: End")
    print("\n")

    print("Exercise 7: Beginning")
    print(to_upper("nFactorial"))
    print("Exercise 7: End")
    print("\n")

    print("Exercise 8: Beginning")
    print(get_area(5,89))
    print("Exercise 8: End")
    print("\n")

    print("Exercise 9: Beginning")
    print(is_even(124))
    print(is_even(599))
    print("Exercise 9: End")
    print("\n")

    print("Exercise 10: Beginning")
    print(extract("nFactorial"))
    print(extract("nFa"))
    print(extract("nF"))
    print("Exercise 10: End")
    print("\n")

    print("Exercise 11: Beginning")
    print(interpolate("Anna", "21"))
    print("Exercise 11: End")
    print("\n")

    print("Exercise 12: Beginning")
    print(extract_characters("nFactorial"))
    print("Exercise 12: End")
    print("\n")

    print("Exercise 13: Beginning")
    print(string_to_integer("21"))
    print("Exercise 13: End")
    print("\n")

    print("Exercise 14: Beginning")
    print(repeat("nFactorial"))
    print("Exercise 14: End")
    print("\n")

    print("Exercise 15: Beginning")
    print(calculate_quotient_remainder(10, 5))
    print(calculate_quotient_remainder(33, 2))
    print("Exercise 15: End")
    print("\n")

    print("Exercise 16: Beginning")
    print(float_division(10, 5))
    print(float_division(33, 2))
    print("Exercise 16: End")
    print("\n")

    print("Exercise 17: Beginning")
    print(count_character("dfffaacbb"))
    print("Exercise 17: End")
    print("\n")

    print("Exercise 18: Beginning")
    print(escape())
    print("Exercise 18: End")
    print("\n")

    print("Exercise 19: Beginning")
    print(multi_line())
    print("Exercise 19: End")
    print("\n")

    print("Exercise 20: Beginning")
    print(exponentiate(13,4))
    print("Exercise 20: End")
    print("\n")

    print("Exercise 21: Beginning")
    print(is_pali("catatac"))
    print(is_pali("racercar"))
    print("Exercise 21: End")
    print("\n")

    print("Exercise 22: Beginning")
    print(is_anagram("apple macintosh", "laptop machines"))
    print(is_anagram("rasp", "sfaar"))
    print("Exercise 22: End")
    print("\n")
    
