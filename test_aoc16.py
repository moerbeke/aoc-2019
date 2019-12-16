#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aocsolver
import aoc16 as aoc

########################################################################
# Test class
########################################################################

class TestAoc16(unittest.TestCase):

    def setUp(self):
        self.aocsolver = aocsolver.AocSolver(aoc.day, aoc.parse_input, aoc.solve_1, aoc.solve_2)
        self.tc_1 = [
                (
"""
""", None),
                ("", None),
                ]
        self.tc_2 = [
                ("03036732577212944063491565474664", '84462026'),
                ]

    def tearDown(self):
        pass

    def test_compute_pattern(self):
        # base pattern: 0, 1, 0, -1
        self.assertEqual(aoc.compute_pattern(0), [1, 0, -1, 0])
        self.assertEqual(aoc.compute_pattern(1), [0, 1, 1, 0, 0, -1, -1, 0])
        self.assertEqual(aoc.compute_pattern(2), [0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1, 0])

    def test_build_element(self):
        signal = '12345678'
        aoc.parse_input(signal)
        self.assertEqual(aoc.build_element(0, signal), '4')
        self.assertEqual(aoc.build_element(1, signal), '8')
        self.assertEqual(aoc.build_element(2, signal), '2')

    def test_fft_1(self):
        signal = ['12345678',
                '48226158',
                '34040438',
                '03415518',
                '01029498']
        for i in range(len(signal) - 1):
            input_signal = signal[i]
            aoc.parse_input(input_signal)
            expected_output_signal = signal[i+1]
            output_signal = aoc.fft(input_signal)
            self.assertEqual(output_signal, expected_output_signal)

    def test_fft_phases(self):
        signal = [
                ('80871224585914546619083218645595', '24176176'),
                ('19617804207202209144916044189917', '73745418'),
                ('69317163492948606335995924319873', '52432133')
                ]
        for s in signal:
            input_signal = s[0]
            aoc.parse_input(input_signal)
            expected_output_signal_8 = s[1]
            output_signal = aoc.fft_phases(input_signal, n_phases=100)
            self.assertEqual(output_signal[:8], expected_output_signal_8)

    @unittest.skip("not implemented yet")
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
    testbase.run_test(TestAoc16)
