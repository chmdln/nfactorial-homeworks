import unittest

import hw_bonus

# Your function definitions here...

class TestFunctions(unittest.TestCase):

    def test_sieve_of_eratosthenes(self):
        self.assertEqual(hw_bonus.sieve_of_eratosthenes(30), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
        self.assertEqual(hw_bonus.sieve_of_eratosthenes(50), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47])
        self.assertEqual(hw_bonus.sieve_of_eratosthenes(100), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97])
        self.assertEqual(hw_bonus.sieve_of_eratosthenes(2), [])
        self.assertEqual(hw_bonus.sieve_of_eratosthenes(1), [])

    def test_triple_combinations(self):
        self.assertEqual(hw_bonus.triple_combinations([1, 2, 3, 4, 5]), [(1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5), (3, 4, 5)])
        self.assertEqual(hw_bonus.triple_combinations([5, 6, 7, 8, 9]), [(5, 6, 7), (5, 6, 8), (5, 6, 9), (5, 7, 8), (5, 7, 9), (5, 8, 9), (6, 7, 8), (6, 7, 9), (6, 8, 9), (7, 8, 9)])
        self.assertEqual(hw_bonus.triple_combinations([10, 20, 30, 40]), [(10, 20, 30), (10, 20, 40), (10, 30, 40), (20, 30, 40)])
        self.assertEqual(hw_bonus.triple_combinations([1, 2, 3]), [(1, 2, 3)])
        self.assertEqual(hw_bonus.triple_combinations([1, 2]), [])

    def test_dict_table(self):
        self.assertEqual(hw_bonus.dict_table(3), {1: {1: 1, 2: 2, 3: 3}, 2: {1: 2, 2: 4, 3: 6}, 3: {1: 3, 2: 6, 3: 9}})
        self.assertEqual(hw_bonus.dict_table(5), {1: {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, 2: {1: 2, 2: 4, 3: 6, 4: 8, 5: 10}, 3: {1: 3, 2: 6, 3: 9, 4: 12, 5: 15}, 4: {1: 4, 2: 8, 3: 12, 4: 16, 5: 20}, 5: {1: 5, 2: 10, 3: 15, 4: 20, 5: 25}})
        self.assertEqual(hw_bonus.dict_table(2), {1: {1: 1, 2: 2}, 2: {1: 2, 2: 4}})
        self.assertEqual(hw_bonus.dict_table(4), {1: {1: 1, 2: 2, 3: 3, 4: 4}, 2: {1: 2, 2: 4, 3: 6, 4: 8}, 3: {1: 3, 2: 6, 3: 9, 4: 12}, 4: {1: 4, 2: 8, 3: 12, 4: 16}})
        self.assertEqual(hw_bonus.dict_table(1), {1: {1: 1}})
        self.assertEqual(hw_bonus.dict_table(0), {})

    def test_generators(self):
        self.assertEqual(list(map(list, hw_bonus.generators(3))), [[1, 2, 3], [1, 2, 3], [1, 2, 3]])
        self.assertEqual(list(map(list, hw_bonus.generators(5))), [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
        self.assertEqual(list(map(list, hw_bonus.generators(2))), [[1, 2], [1, 2]])
        self.assertEqual(list(map(list, hw_bonus.generators(4))), [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]])
        self.assertEqual(list(map(list, hw_bonus.generators(1))), [[1]])

    def test_cartesian_product(self):
        self.assertEqual(hw_bonus.cartesian_product([1, 2, 3], ['a', 'b', 'c']), [(1, 'a'), (1, 'b'), (1, 'c'), (2, 'a'), (2, 'b'), (2, 'c'), (3, 'a'), (3, 'b'), (3, 'c')])
        self.assertEqual(hw_bonus.cartesian_product(['x', 'y'], ['A', 'B', 'C']), [('x', 'A'), ('x', 'B'), ('x', 'C'), ('y', 'A'), ('y', 'B'), ('y', 'C')])
        self.assertEqual(hw_bonus.cartesian_product([True, False], [0, 1]), [(True, 0), (True, 1), (False, 0), (False, 1)])
        self.assertEqual(hw_bonus.cartesian_product([1, 2], ['a']), [(1, 'a'), (2, 'a')])
        self.assertEqual(hw_bonus.cartesian_product([], ['a', 'b']), [])

if __name__ == "__main__":
    unittest.main()