#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import unittest

import testbase
import aocsolver
import aoc8 as aoc

########################################################################
# Test class
########################################################################

class TestAoc8(unittest.TestCase):

    def setUp(self):
        self.aocsolver = aocsolver.AocSolver(aoc.day, aoc.parse_input, aoc.solve_1, aoc.solve_2)
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
                ]

    def tearDown(self):
        pass

    def test_extract_layers(self):
        input_str = '123456789012'
        expected_layers_data = ['123456', '789012']
        expected_layers = [
                ['123', '456'],
                ['789', '012'],
                ]
        image_data = aoc.parse_input(input_str)
        layers_data, layers = aoc.extract_layers(image_data, width=3, height=2)
        self.assertEqual(layers_data, expected_layers_data)
        self.assertEqual(layers, expected_layers)

    def test_find_layer_with_fewest_n(self):
        layers_data = ['123456', '789012']
        expected_layer_data = layers_data[0]
        layer_data = aoc.find_layer_with_fewest_n(layers_data, 0)
        self.assertEqual(layer_data, expected_layer_data)

    def test_count_n_m(self):
        layer_data = '123456'
        expected_c = 1
        c = aoc.count_n_m(layer_data, 1, 2)
        self.assertEqual(c, expected_c)
        self.assertEqual(aoc.count_n_m('01123456', 1, 2), 2)
        self.assertEqual(aoc.count_n_m('0112345622', 1, 2), 6)

    def test_decode(self):
        input_str = '0222112222120000'
        expected_image = ['01', '10']
        image_data = aoc.parse_input(input_str)
        self.assertEqual(aoc.decode(image_data, 2, 2), expected_image)

    @unittest.skip("not implemented yet")
    def test_solve_1(self):
        for t in self.tc_1:
            self.assertEqual(self.aocsolver.solve_1(t[0]), t[1])

    @unittest.skip("not implemented yet")
    def test_solve_2(self):
        for t in self.tc_2:
            self.assertEqual(self.aocsolver.solve_2(t[0]), t[1])


########################################################################
# Main program
########################################################################

if __name__ == '__main__':
    testbase.run_test(TestAoc8)
