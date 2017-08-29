import unittest
import sys
from game import (make_matrix,
                  letter_matrix,
                  print_letter_matrix, 
                  Graph)



class TestMatrix(unittest.TestCase):
    def test_make_matrix(self):
        matrix = 3
        self.assertEqual(make_matrix(matrix), [['11','12','13'],
                                               ['21','22','23'],
                                               ['31','32','33']])
        with self.assertRaises(Exception):
            make_matrix(1)


    def test_letter_matrix(self):
        letters = 'abccdeDuj'
        length = 3
        self.assertEqual(letter_matrix(letters, length=length), ['abc','cde','duj'])
        with self.assertRaises(Exception):
            letter_matrix(letters, length=4)


class TestGraph(unittest.TestCase):
    def setUp(self):
        self._11 = Graph('_11','a')
        self._12 = Graph('_12','b', important=True)
        self._13 = Graph('_13','c')
        self._21 = Graph('_21','c')
        self._22 = Graph('_22','d')
        self._23 = Graph('_23','e', important=True)
        self._31 = Graph('_31','d', important=True)
        self._32 = Graph('_32','u')
        self._33 = Graph('_33','j')
        self._11.arcs = [self._12, self._22, self._21]
        self._12.arcs = [self._11, self._21, self._22, self._13, self._23]
        self._12.arcs = [self._12, self._22, self._23]
        self._21.arcs = [self._11, self._12, self._22, self._32, self._31]
        self._22.arcs = [self._11, self._12, self._13, self._23, self._33, self._32, self._31, self._21]
        self._23.arcs = [self._12, self._13, self._22, self._32, self._33]
        self._31.arcs = [self._21, self._22, self._32]
        self._32.arcs = [self._31, self._21, self._22, self._23, self._33]
        self._33.arcs = [self._32, self._22, self._23]


    def test_search(self):
        max_len = 3
        solns = self._11.search(self._22, max_len)
        self.assertEqual(solns, [[self._11, self._22],
                                 [self._11, self._12, self._22],
                                 [self._11, self._21, self._22]])


    


if __name__ == '__main__':
    unittest.main()
