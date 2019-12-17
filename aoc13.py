#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 13

########################################################################
# Algorithms
########################################################################

from collections import namedtuple
from math import inf

import intcode

P = namedtuple('P', ['x', 'y', 'id'])

"""
Tile types:

0 is an empty tile. No game object appears in this tile.
1 is a wall tile. Walls are indestructible barriers.
2 is a block tile. Blocks can be broken by the ball.
3 is a horizontal paddle tile. The paddle is indestructible.
4 is a ball tile. The ball moves diagonally and bounces off objects.
"""
T_EMPTY = 0
T_WALL = 1
T_BLOCK =2
T_PADDLE = 3
T_BALL = 4

_csv_program = None

def parse_input(input_str):
    global _csv_program
    _csv_program = input_str.strip()

def solve_1():
    return count_remaining_blocks()

def solve_2():
    return

def count_remaining_blocks():
    computer = intcode.IntcodeComputer()
    computer.load_program(_csv_program)
    computer.reset()
    play(computer)
    n_blocks = sum([list(line.values()).count(T_BLOCK) for line in _cabinet.values()])
    return n_blocks

def play(computer):
    global _cabinet
    global _x1
    global _y1
    global _x2
    global _y2
    _x1 = +inf
    _y1 = +inf
    _x2 = -inf
    _y2 = -inf
    _cabinet = dict()
    output = list()
    halt_int = False
    while not halt_int:
        halt_int, input_int, output_int = computer.run_program()
        if output_int:
            output.append(computer.pop_output())
    i = 0
    while 3*i < len(output):
        x, y, tile_id = output[i*3:(i+1)*3]
        update_cabinet(x, y, tile_id)
        i += 1
    print_cabinet()

def update_cabinet(x, y, tile_id):
    global _x1
    global _y1
    global _x2
    global _y2
    if x < _x1:
        _x1 = x
    elif x > _x2:
        _x2 = x
    if y < _y1:
        _y1 = y
    elif y > _y2:
        _y2 = y
    if not y in _cabinet:
        _cabinet[y] = dict()
    if tile_id == T_EMPTY:
        _cabinet[y][x] = T_EMPTY
    elif tile_id == T_WALL:
        _cabinet[y][x] = T_WALL
    elif tile_id == T_BLOCK:
        # TODO
        _cabinet[y][x] = T_BLOCK
    elif tile_id == T_PADDLE:
        _cabinet[y][x] = T_PADDLE
    elif tile_id == T_BALL:
        # TODO
        _cabinet[y][x] = T_BALL
    else:
        assert(False)

def print_cabinet():
    #print("(%d,%d) .. (%d,%d)" % (_x1, _y1, _x2, _y2))
    if not -inf in [_x2, _y2] and not inf in [_x1, _y1]:
        for y in range(_y1, _y2+1):
            line = ''
            for x in range(_x1, _x2+1):
                try:
                    if _cabinet[y][x] == T_EMPTY:
                        line += ' '
                    elif _cabinet[y][x] == T_WALL:
                        line += '#'
                    elif _cabinet[y][x] == T_BLOCK:
                        line += '*'
                    elif _cabinet[y][x] == T_PADDLE:
                        line += '='
                    elif _cabinet[y][x] == T_BALL:
                        line += '@'
                    else:
                        assert(False)
                except KeyError:
                    line += ' '
            print(line)
        for i in range(19):
            print()
    else:
        print("cabinet not complete yet")

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
