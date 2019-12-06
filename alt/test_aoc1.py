#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aoc1 as aoc

########################################################################
# Test class
########################################################################

class TestAoc1(unittest.TestCase):

    def setUp(self):
        self.aoc = aoc.Aoc1(read_default_input=False)
        self.tc_1 = [
                (
"""
""", None),
                ("", None),
                ]
        self.tc_2 = [
                ("14", 2),
                ("1969", 966),
                ("100756", 50346),
                ]

    def tearDown(self):
        pass

    @unittest.skip("not implemented yet")
    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aoc.solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aoc.solve_2(t[0]), t[1])


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAoc1)
