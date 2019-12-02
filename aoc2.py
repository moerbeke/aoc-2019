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

class Aoc2(aocbase.AocBase):

    def __init__(self, read_default_input=True, input_filename=None, input_str=None):
        self._program = None
        self._ptr = None
        self._halt = None
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        self.reset()

    def reset(self):
        self._program = [int(i) for i in self._input.strip().split(',')]
        self._ptr = 0
        self._halt = False

    def do_solve_1(self):
        self.run(12, 2)
        output = self._program[0]
        return output

    def run(self, noun=None, verb=None):
        if noun is not None and verb is not None:
            self.init(noun, verb)
        while not self._halt:
            self.step()

    def init(self, noun, verb):
        self._program[1] = noun
        self._program[2] = verb

    def step(self):
        op_code = self._program[self._ptr]
        if op_code == 99:
            self._halt = True
        else:
            a = self._program[self._ptr + 1]
            b = self._program[self._ptr + 2]
            c = self._program[self._ptr + 3]
            if op_code == 1:
                self._program[c] = self._program[a] + self._program[b]
            elif op_code == 2:
                self._program[c] = self._program[a] * self._program[b]
            else:
                assert(false)
            self._ptr += 4

    @property
    def state(self):
        return ','.join([str(i) for i in self._program])

    def do_solve_2(self):
        ok = False
        for noun in range(100):
            for verb in range(100):
                self.reset()
                self.run(noun, verb)
                output = self._program[0]
                if output == 19690720:
                    ok = True
                    break
            if ok:
                break
        return 100 * noun + verb

########################################################################
# main
########################################################################

if __name__ == '__main__':
    aocbase.run(Aoc2)
