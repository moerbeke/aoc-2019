#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 17

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

import intcode

P = namedtuple('P', ['x', 'y'])

TURN_LEFT = 0
TURN_RIGHT = 1
TURN = {TURN_LEFT: 'L', TURN_RIGHT: 'R'}

UP = 'N'
DOWN = 'S'
RIGHT = 'E'
LEFT = 'W'

DIRS = [UP, RIGHT, DOWN, LEFT]

OPEN_SPACE = '.'
SCAFFOLD = '#'

VACUUM_ROBOT_DIR = {
        'v': DOWN,
        '^': UP,
        '<': LEFT,
        '>': RIGHT}

VACUUM_ROBOT_SYMBOL = {
        DOWN: 'v',
        UP: '^',
        LEFT: '<',
        RIGHT: '>'}

_scaffolds = None
_max_x = None
_max_y = None

_csv_program = None

def parse_input(input_str):
    global _csv_program
    _csv_program = input_str.strip()

def solve_1():
    return calibrate_cameras()

def solve_2():
    if _scaffolds is None:
        calibrate_cameras()
    notify_robots()
    # Path: R,12,R,4,R,10,R,12,R,6,L,8,R,10,R,12,R,4,R,10,R,12,L,8,R,4,R,4,R,6,R,12,R,4,R,10,R,12,R,6,L,8,R,10,L,8,R,4,R,4,R,6,R,12,R,4,R,10,R,12,R,6,L,8,R,10,L,8,R,4,R,4,R,6
    # From the path, the following functions and routines can be inferred by inspection:
    f_A = 'R,12,R,4,R,10,R,12'
    f_B = 'R,6,L,8,R,10'
    f_C = 'L,8,R,4,R,4,R,6'
    main_routine = 'A,B,A,C,A,B,C,A,B,C'
    new_line = '\n'
    computer = intcode.IntcodeComputer()
    computer.load_program(_csv_program)
    computer.reset()
    computer.write_addr(0, 2)  # wake up the vacuum robot
    for f in [main_routine, f_A, f_B, f_C]:
        for c in f:
            computer.push_input(ord(c))
        computer.push_input(ord(new_line))
    #computer.push_input(ord('y'))  # video feed
    computer.push_input(ord('n'))  # no video feed
    computer.push_input(ord(new_line))
    halt_int = False
    o = ''
    while not halt_int:
        halt_int, input_int, output_int = computer.run_program()
        assert(not input_int)
        if output_int:
            oi = computer.pop_output()
            o += chr(oi)
    print(o)
    dust = oi
    return dust

def calibrate_cameras():
    scaffolds, width = scan_scaffolds()
    calibration_parameters = compute_calibration_parameters(scaffolds, width)
    return calibration_parameters

def scan_scaffolds():
    computer = intcode.IntcodeComputer()
    computer.load_program(_csv_program)
    computer.reset()
    scaffolds = dict()
    halt_int = False
    p = P(0,0)
    ascii_scaffolds = ''
    width = 0
    j = 0
    halt_int = False
    while not halt_int:
        computer.push_input(88)
        halt_int, input_int, output_int = computer.run_program()
        #print(halt_int, input_int, output_int)
        assert(not input_int)
        if output_int:
            ascii_view = computer.pop_output()
        scaffolds[p] = ascii_view
        ascii_scaffolds += chr(ascii_view)
        #print(ascii_view)
        if ascii_view == 10:
            p = P(0, p.y+1)
            if width == 0:
                width = j
        else:
            p = P(p.x+1,p.y)
            j += 1
    return scaffolds, width

def compute_calibration_parameters(scaffolds, width):
    global _scaffolds
    global _max_x
    global _max_y
    _scaffolds = scaffolds
    _max_x = width
    height = len(scaffolds) // width
    _max_y = height
    p = ''
    calibration_parameters = 0
    for j in range(height):
        for i in range(width):
            p += chr(scaffolds[P(i,j)])
            if i > 0 and i < width - 1 and j > 0 and j < height - 1:
                if is_intersection(scaffolds, P(i,j)):
                    calibration_parameters += i * j
        p += '\n'
    print(p)
    return calibration_parameters

def is_intersection(scaffolds, p):
    s = 35
    intersection = (
            scaffolds[p] == s and
            scaffolds[P(p.x-1,p.y)] == s and
            scaffolds[P(p.x+1,p.y)] == s and
            scaffolds[P(p.x,p.y-1)] == s and
            scaffolds[P(p.x,p.y+1)] == s)
    return intersection

def notify_robots():
    candidate_path = compute_candidate_path()
    path = ','.join(candidate_path)
    print(path)

def compute_candidate_path():
    path = list()
    p, d = get_init_pos()
    end = False
    np = None
    while not end:
        p0 = p
        while True:
            np = go_forward(p, d)
            if p == np:
                break
            else:
                p = np
        dist = distance(p, p0)
        if dist != 0:
            path.append(str(dist))
        np = None
        end = is_end(p, d)
        if not end:
            t, d = turn(p, d)
            path.append(TURN[t])
        end = is_end(p, d)
    return path

def distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def is_scaffold(p):
    return p.x >= 0 and p.x < _max_x and p.y >= 0 and p.y < _max_y and chr(_scaffolds[p]) == SCAFFOLD

def is_open_space(p):
    return p.x < 0 or p.x >= _max_x or p.y < 0 or p.y >= _max_y or chr(_scaffolds[p]) == OPEN_SPACE

def turn(p, d):
    if d == UP or d == DOWN:
        assert(is_scaffold(P(p.x-1,p.y)) or is_scaffold(P(p.x+1,p.y)))
        assert(is_open_space(P(p.x-1,p.y)) or is_open_space(P(p.x+1,p.y)))
        if is_scaffold(P(p.x-1,p.y)):
            if d == UP:
                t = TURN_LEFT
            else:
                t = TURN_RIGHT
            d = LEFT
        else:
            if d == UP:
                t = TURN_RIGHT
            else:
                t = TURN_LEFT
            d = RIGHT
    else:
        assert(is_scaffold(P(p.x,p.y-1)) or is_scaffold(P(p.x,p.y+1)))
        assert(is_open_space(P(p.x,p.y-1)) or is_open_space(P(p.x,p.y+1)))
        if is_scaffold(P(p.x,p.y-1)):
            if d == RIGHT:
                t = TURN_LEFT
            else:
                t = TURN_RIGHT
            d = UP 
        else:
            if d == RIGHT:
                t = TURN_RIGHT
            else:
                t = TURN_LEFT
            d = DOWN
    return t, d

def go_forward(p, d):
    if d == UP:
        np = P(p.x,p.y-1)
    elif d == DOWN:
        np = P(p.x,p.y+1)
    elif d == LEFT:
        np = P(p.x-1,p.y)
    elif d == RIGHT:
        np = P(p.x+1,p.y)
    else:
        assert(False)
    if (
            np.x >= 0 and np.x < _max_x and
            np.y >= 0 and np.y < _max_y and
            chr(_scaffolds[np]) == SCAFFOLD):
        p = np
    return p

def is_end(p, d):
    end = (
            (d == LEFT and is_open_space(P(p.x-1,p.y)) and is_open_space(P(p.x,p.y-1)) and is_open_space(P(p.x,p.y+1))) or
            (d == RIGHT and is_open_space(P(p.x+1,p.y)) and is_open_space(P(p.x,p.y-1)) and is_open_space(P(p.x,p.y+1))) or
            (d == UP and is_open_space(P(p.x,p.y-1)) and is_open_space(P(p.x-1,p.y)) and is_open_space(P(p.x+1,p.y))) or
            (d == DOWN and is_open_space(P(p.x,p.y+1)) and is_open_space(P(p.x-1,p.y)) and is_open_space(P(p.x+1,p.y))))
    return end

def get_init_pos():
    for p in _scaffolds:
        if chr(_scaffolds[p]) in VACUUM_ROBOT_DIR:
            p0 = p
            d0 = VACUUM_ROBOT_DIR[chr(_scaffolds[p])]
            break
    return p0, d0

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
