import unittest

import hw_bonus

class TestFunctions(unittest.TestCase):
    # Exercise-1
    def test_memoized_fibonacci(self):
        # self.assertEqual(hw_bonus.memoized_fibonacci(10), 55)
        self.assertEqual(hw_bonus.memoized_fibonacci(20), 6765)
        self.assertEqual(hw_bonus.memoized_fibonacci(0), 0)
        self.assertEqual(hw_bonus.memoized_fibonacci(1), 1)
        self.assertEqual(hw_bonus.memoized_fibonacci(2), 1)

    # Exercise-2
    def test_curry(self):
        def add_three_numbers(a, b, c):
            return a + b + c
        add_five_and_six = hw_bonus.curry(add_three_numbers, 5, 6)
        self.assertEqual(add_five_and_six(7), 18)
        add_five = hw_bonus.curry(add_three_numbers, 5)
        self.assertEqual(add_five(6, 7), 18)

    # Exercise-3
    def test_my_zip(self):
        self.assertEqual(list(hw_bonus.my_zip([1, 2, 3], [4, 5, 6])), [(1, 4), (2, 5), (3, 6)])
        self.assertEqual(list(hw_bonus.my_zip([1, 2], [3, 4], [5, 6])), [(1, 3, 5), (2, 4, 6)])
        self.assertEqual(list(hw_bonus.my_zip([1], [2, 3], [4, 5, 6])), [(1, 2, 4)])

    # Exercise-5
    def test_recursive_flatten(self):
        self.assertEqual(hw_bonus.recursive_flatten([1, [2, [3, 4], 5]]), [1, 2, 3, 4, 5])
        self.assertEqual(hw_bonus.recursive_flatten([[1, 2, [3, 4], 5], [6, 7]]), [1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(hw_bonus.recursive_flatten([1, 2, 3, [4, [5, 6, [7, [8, 9]]]]]), [1, 2, 3, 4, 5, 6, 7, 8, 9])
   
if __name__ == '__main__':
    unittest.main()