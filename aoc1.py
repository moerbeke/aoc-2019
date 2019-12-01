#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import aocbase

########################################################################
# Algorithm class
########################################################################

class Aoc1(aocbase.AocBase):

    def __init__(self, read_default_input=True, input_filename=None, input_str=None):
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        self._masses = [int(m) for m in self._input.strip().split('\n')]

    def do_solve_1(self):
        f = 0
        for m in self._masses:
            f += int(m / 3) - 2
        return f

    def do_solve_2(self):
        f = 0
        for m in self._masses:
            fm = 0
            while True:
                x = int(m / 3) - 2
                if x <= 0:
                    break
                fm += x
                m = x
            f += fm
        return f

########################################################################
# main
########################################################################

if __name__ == '__main__':
    aocbase.run(Aoc1)
