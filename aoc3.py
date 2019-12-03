#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

from math import inf

import aocbase

########################################################################
# Algorithm class
########################################################################

class Aoc3(aocbase.AocBase):

    def __init__(self, read_default_input=True, input_filename=None, input_str=None):
        self._path_ins = None
        self._path = None
        self._path_steps = None
        self._solved = None
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        self._path_ins = self._input.strip().split('\n')
        self._solved = False

    def do_solve_1(self):
        self.solve_crossed_wires()
        crosses = self._path[0].intersection(self._path[1])
        return self.get_shortest_distance(crosses)

    def do_solve_2(self):
        self.solve_crossed_wires()
        crosses = self._path[0].intersection(self._path[1])
        return self.get_shortest_distance_steps(crosses)

    def solve_crossed_wires(self):
        if not self._solved:
            self._path = list()
            self._path_steps = list()
            for wire in range(0, 2):
                self._path.append(set())
                self._path_steps.append(dict())
                self.do_path(wire)
            self._solved = True

    def get_shortest_distance(self, crosses):
        return min([abs(x) + abs(y) for x, y in crosses])

    def do_path(self, wire):
        x, y = 0, 0
        steps = 0
        for ins in self._path_ins[wire].split(','):
            x, y, steps = self.move(wire, x, y, steps, ins)

    def move(self, wire, x1, y1, steps, ins):
        direction = ins[0]
        ins_steps = int(ins[1:])
        x2 = x1
        y2 = y1
        dx = 0
        dy = 0
        if direction == 'U':
            y2 = y1 + ins_steps
            dy = 1
        elif direction == 'D':
            y2 = y1 - ins_steps
            dy = -1
        elif direction == 'R':
            x2 = x1 + ins_steps
            dx = 1
        elif direction == 'L':
            x2 = x1 - ins_steps
            dx = -1
        x = x1
        y = y1
        while not (x == x2 and y == y2):
            x += dx
            y += dy
            steps += 1
            self._path[wire].add((x, y))
            self._path_steps[wire][(x, y)] = steps
        return x2, y2, steps

    def get_shortest_distance_steps(self, crosses):
        return min([self._path_steps[0][(x,y)] + self._path_steps[1][(x,y)] for x,y in crosses])


########################################################################
# main
########################################################################

if __name__ == '__main__':
    aocbase.run(Aoc3)
