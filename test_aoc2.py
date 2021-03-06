#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aocsolver
import aoc2 as aoc

########################################################################
# Test class
########################################################################

class TestAoc2(unittest.TestCase):

    def setUp(self):
        self.aocsolver = aocsolver.AocSolver(aoc.day, aoc.parse_input, aoc.solve_1, aoc.solve_2)
        self.tc_1 = [
                ]
        self.tc_2 = [
                ]

    def tearDown(self):
        pass

    def test_step(self):
        aoc.parse_input('1,9,10,3,2,3,11,0,99,30,40,50')
        aoc.reset()
        self.assertEqual(aoc.state(), '1,9,10,3,2,3,11,0,99,30,40,50')
        aoc.step()
        self.assertEqual(aoc.state(), '1,9,10,70,2,3,11,0,99,30,40,50')

    def test_run(self):
        cases = [
                ('1,0,0,0,99', '2,0,0,0,99'),
                ('2,3,0,3,99', '2,3,0,6,99'),
                ('2,4,4,5,99,0','2,4,4,5,99,9801'),
                ('1,1,1,4,99,5,6,0,99', '30,1,1,4,2,5,6,0,99')]
        for c in cases:
            aoc.parse_input(c[0])
            aoc.reset()
            aoc.run()
            self.assertEqual(aoc.state(), c[1])

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
