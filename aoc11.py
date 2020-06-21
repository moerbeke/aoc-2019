#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 11

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

import intcode

P = namedtuple('P', ['x', 'y'])

BLACK = 0
WHITE = 1
COLOR = {BLACK: '.', WHITE: '#'}

TURN_LEFT = 0
TURN_RIGHT = 1
TURN = {TURN_LEFT: 'L', TURN_RIGHT: 'R'}

UP = 'N'
DOWN = 'S'
RIGHT = 'E'
LEFT = 'W'

DIRS = [UP, RIGHT, DOWN, LEFT]

_csv_program = None

def parse_input(input_str):
    global _csv_program
    _csv_program = input_str.strip()

def solve_1():
    return count_panels_to_paint()

def solve_2():
    paint_panel()

def count_panels_to_paint():
    computer = intcode.IntcodeComputer()
    computer.load_program(_csv_program)
    computer.reset()
    return len(run_robot_sw(computer, BLACK))

def run_robot_sw(computer, init_color):
    panels = dict()
    robot_id = 0
    computer.reset()
    halt_int = False
    p = P(0,0)
    direction = UP
    next_color = init_color
    while not halt_int:
        #halt_int, input_int, output_int = computer.run_program(next_color)
        computer.push_input(next_color)
        halt_int, input_int, output_int = computer.run_program()
        assert(not input_int)
        if output_int:
            color = computer.pop_output()
        halt_int, input_int, output_int = computer.run_program()
        assert(not input_int)
        if output_int:
            turn = computer.pop_output()
        panels[p] = color
        p, direction = next_pos(p, direction, turn)
        try:
            next_color = panels[p]
        except KeyError:
            next_color = BLACK
    return panels

def next_pos(p, d, turn):
    di = DIRS.index(d)
    next_x = p.x
    next_y = p.y
    if turn == TURN_LEFT:
        next_d = DIRS[(di-1)%4]
    elif turn == TURN_RIGHT:
        next_d = DIRS[(di+1)%4]
    else:
        assert(False)
    if next_d == UP:
        next_y -= 1
    elif next_d == LEFT:
        next_x -= 1
    elif next_d == DOWN:
        next_y += 1
    elif next_d == RIGHT:
        next_x += 1
    else:
        assert(False)
    return P(next_x,next_y), next_d

def paint_panel():
    computer = intcode.IntcodeComputer()
    computer.load_program(_csv_program)
    panels = run_robot_sw(computer, WHITE)
    print_panel(panels)

def print_panel(panels):
    x1, y1, x2, y2 = get_borders(panels)
    for y in range(y1, y2+1):
        line = ''
        for x in range(x1, x2+1):
            p = P(x,y)
            try:
                pixel_color = panels[p]
                if pixel_color == BLACK:
                    line += '.'
                else:
                    line += '#'
            except KeyError:
                pixel_color = BLACK
                line += ' '
        print(line)

def get_borders(panels):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    for p in panels:
        if p.x < x1:
            x1 = p.x
        elif p.x > x2:
            x2 = p.x
        if p.y < y1:
            y1 = p.y
        elif p.y > y2:
            y2 = p.y
    return x1, y1, x2, y2

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
