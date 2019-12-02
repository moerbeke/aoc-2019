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
        self._ptr = 0
        self._halt = False
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        self.reset()

    def reset(self):
        self._program = [int(i) for i in self._input.strip().split(',')]
        self._ptr = 0
        self._halt = False

    def do_solve_1(self):
        self._program[1] = 12
        self._program[2] = 2
        while not self._halt:
            self.step()
        return self._program[0]

    def step(self):
        op_code = self._program[self._ptr]
        if op_code == 1:
            a = self._program[self._ptr + 1]
            b = self._program[self._ptr + 2]
            c = self._program[self._ptr + 3]
            self._program[c] = self._program[a] + self._program[b]
            self._ptr += 4
        elif op_code == 2:
            a = self._program[self._ptr + 1]
            b = self._program[self._ptr + 2]
            c = self._program[self._ptr + 3]
            self._program[c] = self._program[a] * self._program[b]
            self._ptr += 4
        elif op_code == 99:
            self._halt = True
        else:
            assert(False)

    @property
    def state(self):
        return ','.join([str(i) for i in self._program])

    def do_solve_2(self):
        ok = False
        for noun in range(100):
            for verb in range(100):
                self.reset()
                self._program[1] = noun
                self._program[2] = verb
                while not self._halt:
                    self.step()
                if self._program[0] == 19690720:
                    ok = True
                    break
            if ok:
                break
        if ok:
            return 100 * noun + verb
        else:
            return

########################################################################
# main
########################################################################

if __name__ == '__main__':
    aocbase.run(Aoc2)
