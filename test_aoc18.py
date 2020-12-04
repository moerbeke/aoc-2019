#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aocsolver
import aoc18 as aoc

########################################################################
# Test class
########################################################################
'''
                (
"""
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""", 136),
'''

class TestAoc18(unittest.TestCase):

    def setUp(self):
        self.aocsolver = aocsolver.AocSolver(aoc.day, aoc.parse_input, aoc.solve_1, aoc.solve_2)
        self.tc_1 = [
                (
"""
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
""", 86),
                (
"""
########################
#...............b.C.D.f#
#.######################
#.....@.a.B.c.d.A.e.F.g#
########################
""", 132),
                (
"""
########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
""", 81),
                (
"""
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
""", 136),
                ]
        self.tc_2 = [
                (
"""
""", None),
                ]

    def tearDown(self):
        pass

    def test_solve_1(self):
        i = 0
        for t in self.tc_1:
            print("Test case #%d" % i)
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])
            i += 1

    @unittest.skip("not implemented yet")
    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAoc18)
