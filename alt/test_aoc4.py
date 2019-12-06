#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aoc4 as aoc

########################################################################
# Test class
########################################################################

class TestAoc4(unittest.TestCase):

    def setUp(self):
        self.aoc = aoc.Aoc4(read_default_input=False)
        self.tc_1 = [
                (
"""
""", None),
                ("", None),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ("", None),
                ]

    def tearDown(self):
        pass

    def test_is_strict_double_adj_digits(self):
        self.assertTrue(self.aoc.is_strict_double_adj_digits(551234))
        self.assertTrue(self.aoc.is_strict_double_adj_digits(557777))
        self.assertTrue(self.aoc.is_strict_double_adj_digits(558855))
        self.assertTrue(self.aoc.is_strict_double_adj_digits(551255))
        self.assertFalse(self.aoc.is_strict_double_adj_digits(122222))
        self.assertFalse(self.aoc.is_strict_double_adj_digits(123333))
        self.assertFalse(self.aoc.is_strict_double_adj_digits(123444))
        self.assertFalse(self.aoc.is_strict_double_adj_digits(123334))

    @unittest.skip("not implemented yet")
    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aoc.solve_1(t[0]), t[1])

    @unittest.skip("not implemented yet")
    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aoc.solve_2(t[0]), t[1])


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAoc4)
