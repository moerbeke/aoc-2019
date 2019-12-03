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
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        self._path_ins = list()
        self._path_ins = self._input.strip().split('\n')

    def do_solve_1(self):
        self._path = list()
        for wire in range(0, 2):
            self._path.append(set())
            self.do_path(wire)
        crosses = self._path[0].intersection(self._path[1])
        return self.get_shortest_distance(crosses)

    def do_path(self, wire):
        x, y = 0, 0
        for ins in self._path_ins[wire].split(','):
            x, y = self.move(wire, x, y, ins)

    def move(self, wire, x1, y1, ins):
        direction = ins[0]
        ins_steps = int(ins[1:])
        if direction == 'U':
            x2 = x1
            y2 = y1 + ins_steps
        elif direction == 'D':
            x2 = x1
            y2 = y1 - ins_steps
        elif direction == 'R':
            x2 = x1 + ins_steps
            y2 = y1
        elif direction == 'L':
            x2 = x1 - ins_steps
            y2 = y1
        else:
            assert(False)
        if x2 > x1:
            dx = 1
        elif x2 < x1:
            dx = -1
        else:
            dx = 0
        if y2 > y1:
            dy = 1
        elif y2 < y1:
            dy = -1
        else:
            dy = 0
        x = x1
        y = y1
        while not (x == x2 and y == y2):
            x += dx
            y += dy
            self._path[wire].add((x, y))
        return x2, y2

    def get_shortest_distance(self, crosses):
        return min([abs(x) + abs(y) for x, y in crosses])

    def do_solve_2(self):
        self._path = list()
        self._path_steps = list()
        for wire in range(0, 2):
            self._path.append(set())
            self._path_steps.append(dict())
            self.do_path_steps(wire)
        crosses = self._path[0].intersection(self._path[1])
        return self.get_shortest_distance_steps(crosses)

    def do_path_steps(self, wire):
        x, y = 0, 0
        steps = 0
        for ins in self._path_ins[wire].split(','):
            x, y, steps = self.move_steps(wire, x, y, steps, ins)

    def move_steps(self, wire, x1, y1, steps, ins):
        direction = ins[0]
        ins_steps = int(ins[1:])
        if direction == 'U':
            x2 = x1
            y2 = y1 + ins_steps
        elif direction == 'D':
            x2 = x1
            y2 = y1 - ins_steps
        elif direction == 'R':
            x2 = x1 + ins_steps
            y2 = y1
        elif direction == 'L':
            x2 = x1 - ins_steps
            y2 = y1
        else:
            assert(False)
        if x2 > x1:
            dx = 1
        elif x2 < x1:
            dx = -1
        else:
            dx = 0
        if y2 > y1:
            dy = 1
        elif y2 < y1:
            dy = -1
        else:
            dy = 0
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
