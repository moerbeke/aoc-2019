#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest
import os

import testbase
import aocsolver

########################################################################
# Day Nth algorithms example
########################################################################

day = 31

_seq = None

def parse_input(input_str):
    global _seq
    _seq = [int(n) for n in input_str.strip().split('\n')]

def solve_1():
    return sum(_seq)

def solve_2():
    s = 0
    for n in _seq:
        s += n ** 2
    return s

class TestAocBase(unittest.TestCase):

    def setUp(self):
        self._default_input_filename = '31.in'
        self._input_filename_a = '31a.in'
        self._default_seq = [1, 2, 3, 4, 5]
        self._seq_a = [1, 2, 3]
        self._seq_b = [1, 2, 3, 4, 5, 6]
        self.aocsolver = aocsolver.AocSolver(day, parse_input, solve_1, solve_2)

    def tearDown(self):
        if os.path.exists(self._default_input_filename):
            os.remove(self._default_input_filename)
        if os.path.exists(self._input_filename_a):
            os.remove(self._input_filename_a)

    def write_input_file(self, filename, seq):
        with open(filename ,'w') as f:
            f.write('\n'.join([str(n) for n in seq]))

    def test_run_default_input(self):
        self.write_input_file(self._default_input_filename, self._default_seq)
        output_1, output_2 = self.aocsolver.run()
        self.assertEqual(output_1, sum(self._default_seq))
        self.assertEqual(output_2, sum([n*n for n in self._default_seq]))

    def test_input_str(self):
        for seq in [self._seq_a, self._seq_b]:
            seq_str = [str(n) for n in seq]
            self.assertEqual(self.aocsolver.solve_1('\n'.join(seq_str)), sum(seq))
            self.assertEqual(self.aocsolver.solve_2('\n'.join(seq_str)), sum([n*n for n in seq]))


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAocBase)
