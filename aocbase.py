#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import abc
import argparse

class AocBase(abc.ABC):
    """Abstract base class for every day's AoC puzzle"""

    def __init__(self, read_default_input=True, input_filename=None, input_str=None):
        # Deduce the day from the class name, assuming class names like Aoc1, Aoc2, ..., Aoc25.
        self._day = int(self.__class__.__name__[3:])
        # Read input if default or explicitly provided.
        if read_default_input:
            if input_filename is None and input_str is None:
                self._input = self._read_file('%d.in' % self._day)
            else:
                raise ValueError("input_filename and input_str cannot be set if read_default_input is True.")
        else:
            if input_filename is not None and input_str is not None:
                raise ValueError("input_filename and input_str cannot be both set.")
            if input_filename is not None:
                self._input = self._read_file(input_filename)
            elif input_str is not None:
                self._input = input_str
            else:
                self._input = None  # to be explicitly set later
        # Parse input, if it was provided
        self._input_parsed = False
        if self._input is not None:
            self.parse_input()

    @property
    def day(self):
        return self._day

    @property
    def input(self):
        return self._input

    def parse_input(self, input_str=None):
        parse = False
        if input_str is not None:
            self._input = input_str
            parse = True
        elif not self._input_parsed:
            if self._input is None:
                raise ValueError("No input provided - cannot parse it")
            parse = True
        if parse:
            self.do_parse_input()
            self._input_parsed = True

    def solve_1(self, input_str=None):
        if input_str is not None:
            self._input = input_str
            self.parse_input(input_str)
        else:
            self.parse_input()
        return self.do_solve_1()

    def solve_2(self, input_str=None):
        if input_str is not None:
            self._input = input_str
            self.parse_input(input_str)
        else:
            self.parse_input()
        return self.do_solve_2()

    def _read_file(self, filename):
        """Read a file and returns its contents as a multiline string.
        """
        with open(filename, 'r') as f:
            contents = f.read()
        return contents.strip()

    @abc.abstractmethod
    def do_parse_input(self):
        pass

    @abc.abstractmethod
    def do_solve_1(self):
        pass

    @abc.abstractmethod
    def do_solve_2(self):
        pass

def parse_cmd_line_args():
    parser = argparse.ArgumentParser()
    part_group = parser.add_mutually_exclusive_group()
    part_group.add_argument("-p1", "--part-1-only", help="solve part 1 only", action="store_true")
    part_group.add_argument("-p2", "--part-2-only", help="solve part 2 only", action="store_true")
    args = parser.parse_args()
    return args

def run(AocClass):
    args = parse_cmd_line_args()
    aoc = AocClass()
    print("\n===== AoC_2019 day #%d =====\n" % aoc.day)
    if not args.part_2_only:
        # Part 1
        output_1 = aoc.solve_1()
        print("Answer 1:", output_1)
    if not args.part_1_only:
        # Part 2
        output_2 = aoc.solve_2()
        print("Answer 2:", output_2)

