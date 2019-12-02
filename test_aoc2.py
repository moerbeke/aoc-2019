#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aoc2 as aoc

########################################################################
# Test class
########################################################################

class TestAoc2(unittest.TestCase):

    def setUp(self):
        self.aoc = aoc.Aoc2(read_default_input=False)
        self.tc_1 = [
                ("1,0,0,0,99", 2),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ("", None),
                ]

    def tearDown(self):
        pass

    def test_step(self):
        aoc_ = aoc.Aoc2(read_default_input=False, input_str='1,9,10,3,2,3,11,0,99,30,40,50')
        self.assertEqual(aoc_.state, '1,9,10,3,2,3,11,0,99,30,40,50')
        aoc_.step()
        self.assertEqual(aoc_.state, '1,9,10,70,2,3,11,0,99,30,40,50')

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
    testbase.run_test(TestAoc2)
