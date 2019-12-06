#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest
import os

import testbase
import aocbase

########################################################################
# Test class
########################################################################

class Aoc31(aocbase.AocBase):

    def __init__(self, read_default_input=True, input_filename=None, input_str=None):
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        self._seq = [int(n) for n in self._input.strip().split('\n')]

    def do_solve_1(self):
        return sum(self._seq)

    def do_solve_2(self):
        s = 0
        for n in self._seq:
            s += n ** 2
        return s

class TestAocBase(unittest.TestCase):

    def setUp(self):
        self._default_input_filename = '31.in'
        self._input_filename_a = '31a.in'
        self._default_seq = [1, 2, 3, 4, 5]
        self._seq_a = [1, 2, 3]
        self._seq_b = [1, 2, 3, 4, 5, 6]

    def tearDown(self):
        if os.path.exists(self._default_input_filename):
            os.remove(self._default_input_filename)
        if os.path.exists(self._input_filename_a):
            os.remove(self._input_filename_a)

    def write_input_file(self, filename, seq):
        with open(filename ,'w') as f:
            f.write('\n'.join([str(n) for n in seq]))

    def test_use_default_input(self):
        with self.assertRaises(FileNotFoundError):
            aoc = Aoc31()
        self.write_input_file(self._default_input_filename, self._default_seq)
        aoc = Aoc31()
        self.assertEqual(aoc.solve_1(), sum(self._default_seq))
        self.assertEqual(aoc.solve_2(), sum([n*n for n in self._default_seq]))

    def test_use_default_input_solve_part_2_only(self):
        self.write_input_file(self._default_input_filename, self._default_seq)
        aoc = Aoc31()
        self.assertEqual(aoc.solve_2(), sum([n*n for n in self._default_seq]))

    def test_use_then_override_default_input(self):
        self.write_input_file(self._default_input_filename, self._default_seq)
        # Default input
        aoc = Aoc31(read_default_input=True)
        self.assertEqual(aoc.solve_1(), sum(self._default_seq))
        self.assertEqual(aoc.solve_2(), sum([n*n for n in self._default_seq]))
        # Solve self._seq_a, which overrides default input
        seq_str = [str(n) for n in self._seq_a]
        self.assertEqual(aoc.solve_1('\n'.join(seq_str)), sum(self._seq_a))
        self.assertEqual(aoc.solve_2('\n'.join(seq_str)), sum([n*n for n in self._seq_a]))
        # Solve self._seq_b, which overrides default input
        seq_str = [str(n) for n in self._seq_b]
        self.assertEqual(aoc.solve_1('\n'.join(seq_str)), sum(self._seq_b))
        self.assertEqual(aoc.solve_2('\n'.join(seq_str)), sum([n*n for n in self._seq_b]))

    def test_no_default_input(self):
        aoc = Aoc31(read_default_input=False)
        # No input provided - cannot solve
        with self.assertRaises(ValueError):
            aoc.solve_1()
        with self.assertRaises(ValueError):
            aoc.solve_2()
        # Solve self._seq_a
        seq_str = [str(n) for n in self._seq_a]
        self.assertEqual(aoc.solve_1('\n'.join(seq_str)), sum(self._seq_a))
        self.assertEqual(aoc.solve_2('\n'.join(seq_str)), sum([n*n for n in self._seq_a]))
        # Solve self._seq_b
        seq_str = [str(n) for n in self._seq_b]
        self.assertEqual(aoc.solve_1('\n'.join(seq_str)), sum(self._seq_b))
        self.assertEqual(aoc.solve_2('\n'.join(seq_str)), sum([n*n for n in self._seq_b]))

    def test_too_many_inputs(self):
        with self.assertRaises(ValueError):
            aoc = Aoc31(read_default_input=True, input_filename='')
        with self.assertRaises(ValueError):
            aoc = Aoc31(read_default_input=True, input_str='')
        with self.assertRaises(ValueError):
            aoc = Aoc31(read_default_input=False, input_filename='', input_str='')

    def test_input_filename(self):
        # Explicit input file provided
        self.write_input_file(self._input_filename_a, self._seq_a)
        aoc = Aoc31(read_default_input=False, input_filename=self._input_filename_a)
        self.assertEqual(aoc.solve_1(), sum(self._seq_a))
        self.assertEqual(aoc.solve_2(), sum([n*n for n in self._seq_a]))
        # Solve self._seq_b, which overrides the provided input
        seq_str = [str(n) for n in self._seq_b]
        self.assertEqual(aoc.solve_1('\n'.join(seq_str)), sum(self._seq_b))
        self.assertEqual(aoc.solve_2('\n'.join(seq_str)), sum([n*n for n in self._seq_b]))

    def test_input_str(self):
        # Explicit input string provided
        seq_str = [str(n) for n in self._seq_a]
        aoc = Aoc31(read_default_input=False, input_str='\n'.join(seq_str))
        self.assertEqual(aoc.solve_1(), sum(self._seq_a))
        self.assertEqual(aoc.solve_2(), sum([n*n for n in self._seq_a]))
        # Solve self._seq_b, which overrides the provided input
        seq_str = [str(n) for n in self._seq_b]
        self.assertEqual(aoc.solve_1('\n'.join(seq_str)), sum(self._seq_b))
        self.assertEqual(aoc.solve_2('\n'.join(seq_str)), sum([n*n for n in self._seq_b]))


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAocBase)
