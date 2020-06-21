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
from time import sleep

import intcode

Output = namedtuple('Output', ['x', 'y', 'id'])

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

# Cabinet
_display = 0
_screen = dict()

_csv_program = None

def parse_input(input_str):
    global _csv_program
    _csv_program = input_str.strip()

def solve_1():
    return count_remaining_blocks()

def solve_2():
    return beat_the_game()

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
    print_screen(_cabinet)

def beat_the_game():
    computer = intcode.IntcodeComputer()
    computer.load_program(_csv_program)
    computer.reset()
    computer.write_addr(0, 2)  # play for free
    output_len = 3
    output = [None] * output_len
    next_output_index = 0
    halt_int = False
    while not halt_int:
        halt_int, input_int, output_int = computer.run_program()
        if output_int:
            output[next_output_index] = computer.pop_output()
            if next_output_index == output_len - 1:
                parse_output(output)
                next_output_index = 0
            else:
                next_output_index += 1
        elif input_int:
            if _ball_x < _paddle_x:
                input_data = -1
            elif _ball_x > _paddle_x:
                input_data = 1
            else:
                input_data = 0
            computer.push_input(input_data)
    return _display

def parse_output(output):
    x, y, tile_id = output
    update_screen = False
    if x == -1 and y == 0:
        new_display = tile_id
        global _display
        if new_display != _display:
            _display = new_display
            update_screen = True
    else:
        global _screen
        if y not in _screen:
            _screen[y] = dict()
        _screen[y][x] = tile_id
        if tile_id == T_BALL:
            global _ball_x
            _ball_x = x
            update_screen = True
        elif tile_id == T_PADDLE:
            global _paddle_x
            _paddle_x = x
    if update_screen:
        print_screen(_screen, _display)

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
        _cabinet[y][x] = T_BLOCK
    elif tile_id == T_PADDLE:
        _cabinet[y][x] = T_PADDLE
    elif tile_id == T_BALL:
        _cabinet[y][x] = T_BALL
    else:
        assert(False)

def print_screen(screen, display=None):
    #sleep(.04)
    y_range = [y for y in screen]
    y1 = min(y_range)
    y2 = max(y_range)
    x_range = [x for x in screen[y1]]
    x1 = min(x_range)
    x2 = max(x_range)
    if not display is None:
        print(chr(27) + "[2J")  # clear screen
        print("                +----------+")
        print("   SCORE >>>>>> | %8d |" % display)
        print("                +----------+")
    for y in range(y1, y2+1):
        line = ''
        for x in range(x1, x2+1):
            try:
                if screen[y][x] == T_EMPTY:
                    line += ' '
                elif screen[y][x] == T_WALL:
                    line += '#'
                elif screen[y][x] == T_BLOCK:
                    line += '*'
                elif screen[y][x] == T_PADDLE:
                    line += '='
                elif screen[y][x] == T_BALL:
                    line += '@'
                else:
                    assert(False)
            except KeyError:
                line += ' '
        print(line)
    print()

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
