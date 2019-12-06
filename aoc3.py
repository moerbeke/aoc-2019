#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 3

########################################################################
# Algorithms
########################################################################

from math import inf

_path_ins = None
_path = None
_path_steps = None
_solved = None

def parse_input(input_str):
    global _path_ins
    global _solved
    _path_ins = input_str.strip().split('\n')
    _solved = False

def solve_1():
    solve_crossed_wires()
    crosses = _path[0].intersection(_path[1])
    return get_shortest_distance(crosses)

def solve_2():
    solve_crossed_wires()
    crosses = _path[0].intersection(_path[1])
    return get_shortest_distance_steps(crosses)

def solve_crossed_wires():
    global _path
    global _path_steps
    global _solved
    if not _solved:
        _path = list()
        _path_steps = list()
        for wire in range(0, 2):
            _path.append(set())
            _path_steps.append(dict())
            do_path(wire)
        _solved = True

def get_shortest_distance(crosses):
    return min([abs(x) + abs(y) for x, y in crosses])

def do_path(wire):
    x, y = 0, 0
    steps = 0
    for ins in _path_ins[wire].split(','):
        x, y, steps = move(wire, x, y, steps, ins)

def move(wire, x1, y1, steps, ins):
    direction = ins[0]
    ins_steps = int(ins[1:])
    x2, y2, dx, dy = get_next_step(x1, y1, direction, ins_steps)
    x = x1
    y = y1
    while not (x == x2 and y == y2):
        x += dx
        y += dy
        steps += 1
        _path[wire].add((x, y))
        _path_steps[wire][(x, y)] = steps
    return x2, y2, steps

def get_next_step(x1, y1, direction, steps):
    x2 = x1
    y2 = y1
    dx = 0
    dy = 0
    if direction == 'U':
        y2 = y1 + steps
        dy = 1
    elif direction == 'D':
        y2 = y1 - steps
        dy = -1
    elif direction == 'R':
        x2 = x1 + steps
        dx = 1
    elif direction == 'L':
        x2 = x1 - steps
        dx = -1
    return x2, y2, dx, dy

def get_shortest_distance_steps(crosses):
    return min([_path_steps[0][(x,y)] + _path_steps[1][(x,y)] for x,y in crosses])

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
