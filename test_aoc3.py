#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aocsolver
import aoc3 as aoc

########################################################################
# Test class
########################################################################

class TestAoc3(unittest.TestCase):

    def setUp(self):
        self.aocsolver = aocsolver.AocSolver(aoc.day, aoc.parse_input, aoc.solve_1, aoc.solve_2)
        self.tc_1 = [
                (
"""
R8,U5,L5,D3
U7,R6,D4,L4
""", 6),
                (
"""
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83""", 159),
                (
"""
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""", 135),
                ]
        self.tc_2 = [
                (
"""
R8,U5,L5,D3
U7,R6,D4,L4
""", 30),
                (
"""
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
""", 610),
                (
"""
R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
""", 410),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAoc3)
