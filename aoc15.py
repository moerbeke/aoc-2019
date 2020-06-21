#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 15

########################################################################
# Algorithms
########################################################################

from collections import namedtuple
from math import inf

import intcode

P = namedtuple('P', ['x', 'y'])

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

ST_WALL = 0
ST_PATH = 1
ST_OXYGEN = 2

WALL = '#'
PATH = '.'
OXYGEN = '@'

DIRS = [NORTH, SOUTH, WEST, EAST]

_computer = None
_csv_program = None
_map = None
_d_map = None
_p0 = P(0,0)
_droid_position = _p0

class FoundInterrupt(Exception):
    pass

def parse_input(input_str):
    global _csv_program
    _csv_program = input_str.strip()

def solve_1():
    return find_oxygen_distance()

def solve_2():
    return

def find_oxygen_distance():
    '''
    Strategy: create a map of distances exploring the area following a spiral.

    Example of result map

    x = (0,0)
    # = wall
    . = path
    @ oxygen

       ## 
      #..#.
     ###...#
    #...x..#
     #....#
      ##.#
       #.@

    d = 0
    while oxygen not found
        d += 1
        sq_n = Find squares at distance d
        if oxygen in sq_n
            distance = d
            stop

    Find squares at distance d
        for each square at distance d-1
            Go to square
            scan uncharted adjacent squares: for each uncharted adjacent square:
                if square is path or oxygen
                    set distance = d
                else
                    set distance = +inf
                if square is oxygen
                    save oxygen position

    Go to square
        go from target square to current square, just using the distance map
    '''
    global _map
    global _d_map
    global _computer
    _computer = intcode.IntcodeComputer()
    _computer.load_program(_csv_program)
    _computer.reset()
    d = 0
    p = _p0
    _map = dict()
    _d_map = dict()
    _map[p] = PATH
    _d_map[p] = 0
    oxygen_found = False
    while not oxygen_found:
        d += 1
        oxygen_found = find_sq_distant(d)
    return d

def find_sq_distant(target_d):
    # Go p0 ->  p | d(p,p0) = d
    outer_circle = [p for p in _d_map if _d_map[p] == target_d - 1]
    oxygen_found = False
    for p in outer_circle:
        # Go to point in circle
        goto(_p0, p)
        # Scan uncharted adjacent points
        oxygen_found = scan_around(p)
        print_map()
        #print_d_map()
        # Go back to p0
        goto(p, _p0)
        if oxygen_found:
            break
    return oxygen_found

def goto(p1, p2):
    p1_d = _d_map[p1]
    p2_d = _d_map[p2]
    assert(p1_d < inf and p2_d < inf)
    if p1_d != 0:
        # Go to (0,0)
        goto_origin(p1)
    if p2_d != 0:
        # Goto p2
        goto_target(p2)

def goto_origin(p1):
    if p1 == _p0:
        return
    d = _d_map[p1]
    current_point = p1
    path = list()
    while d > 0:
        next_points = [
                P(current_point.x,current_point.y-1),
                P(current_point.x,current_point.y+1), 
                P(current_point.x-1,current_point.y), 
                P(current_point.x+1,current_point.y)]
        next_point = [p for p in next_points if p in _d_map and _d_map[p] < d][0]
        next_cmd = get_dir(current_point, next_point)
        path.append(next_cmd)
        current_point = next_point
        d -= 1
    seq = path
    for cmd in seq:
        status = run_repair_droid_cycle(cmd)
        assert(status == ST_PATH)

def goto_target(p2):
    if p2 == _p0:
        return
    d = _d_map[p2]
    current_point = p2
    path = list()
    while d > 0:
        next_points = [
                P(current_point.x,current_point.y-1),
                P(current_point.x,current_point.y+1), 
                P(current_point.x-1,current_point.y), 
                P(current_point.x+1,current_point.y)]
        next_point = [p for p in next_points if p in _d_map and _d_map[p] < d][0]
        next_cmd = get_dir(current_point, next_point)
        path.append(next_cmd)
        current_point = next_point
        d -= 1
    assert(len(path) > 0)
    seq = reverse(path)
    for cmd in seq:
        status = run_repair_droid_cycle(cmd)
        assert(status == ST_PATH)

def scan_around(source_p):
    oxygen_found = False
    next_d = _d_map[source_p] + 1
    points_to_scan = [P(source_p.x,source_p.y-1), P(source_p.x,source_p.y+1), P(source_p.x-1,source_p.y), P(source_p.x+1,source_p.y)]
    points_to_scan = [p for p in points_to_scan if not p in _d_map]
    for p in points_to_scan:
        cmd = get_dir(source_p, p)
        status_code = run_repair_droid_cycle(cmd)
        if status_code == ST_WALL:
            add_map(p, WALL)
            _d_map[p] = inf
        elif status_code == ST_PATH:
            add_map(p, PATH)
            _d_map[p] = next_d
            run_repair_droid_cycle(reverse_dir(cmd))
        elif status_code == ST_OXYGEN:
            add_map(p, OXYGEN)
            _d_map[p] = next_d
            run_repair_droid_cycle(reverse_dir(cmd))
            oxygen_found = True
        else:
            assert(False)
    return oxygen_found

def run_repair_droid_cycle(cmd):
    '''
    Search cycle

      - Accept a movement command via an input instruction.
      - Send the movement command to the repair droid.
      - Wait for the repair droid to finish the movement operation.
      - Report on the status of the repair droid via an output instruction.
    '''
    _computer.push_input(cmd)
    halt_int, input_int, output_int = _computer.run_program()
    if output_int:
        status_code = _computer.pop_output()
        if status_code in [ST_PATH, ST_OXYGEN]:
            update_droid_position(cmd)
    return status_code

def update_droid_position(cmd):
    global _droid_position
    p1 = _droid_position
    if cmd == NORTH:
        x2 = p1.x
        y2 = p1.y - 1
    elif cmd == SOUTH:
        x2 = p1.x
        y2 = p1.y + 1
    elif cmd == WEST:
        x2 = p1.x - 1
        y2 = p1.y
    elif cmd == EAST:
        x2 = p1.x + 1
        y2 = p1.y
    else:
        assert(False)
    _droid_position = P(x2, y2)
    #print(">>> (%d, %d)" % (x2, y2))

def reverse(seq):
    return [reverse_dir(cmd) for cmd in reversed(seq)]

def reverse_dir(cmd):
    reversed_cmd = None
    if cmd == NORTH:
        reversed_cmd = SOUTH
    elif cmd == SOUTH:
        reversed_cmd = NORTH
    elif cmd == WEST:
        reversed_cmd = EAST
    elif cmd == EAST:
        reversed_cmd = WEST
    else:
        assert(False)
    return reversed_cmd

def get_dir(p1, p2):
    if p2.x == p1.x:
        if p2.y == p1.y - 1:
            d = NORTH
        elif p2.y == p1.y + 1:
            d = SOUTH
        else:
            assert(False)
    elif p2.y == p1.y:
        if p2.x == p1.x - 1:
            d = WEST
        elif p2.x == p1.x + 1:
            d = EAST
        else:
            assert(False)
    else:
        assert(False)
    return d

def add_map(p, t):
    _map[p] = t

def print_map():
    x1, y1, x2, y2 = get_borders()
    print("_______________________________________________________________________")
    print(x1, y1, x2, y2)
    for y in range(y1, y2+1):
        line = ''
        for x in range(x1, x2+1):
            p = P(x,y)
            if p == _p0:
                line += 'x'
            else:
                try:
                    line += _map[p]
                except KeyError:
                    line += '?'
        print(line)
    print("-----------------------------------------------------------------------")
    try:
        o = [p for p in _map if _map[p] == OXYGEN][0]
        print("Oxygen found at ", o)
    except IndexError:
        pass

def print_d_map():
    x1, y1, x2, y2 = get_borders()
    print("_______________________________________________________________________")
    print(x1, y1, x2, y2)
    for y in range(y1, y2+1):
        line = ''
        for x in range(x1, x2+1):
            line += print_p(P(x,y))
        print(line)
    print("-----------------------------------------------------------------------")

def print_p(p):
    try:
        d = _d_map[p]
        if d < 10:
            c = str(d)
        elif d < 36:
            c = chr(ord('A') + d - 10)
        elif d < 62:
            c = chr(ord('a') + d - 36)
        elif d < 72:
            c = str(d - 62)
        elif d < 98:
            c = chr(ord('A') + d - 72)
        elif d < 124:
            c = chr(ord('a') + d - 98)
        elif d < inf:
            c = '-'
        else:
            c = '#'
    except KeyError:
        c = '?'
    return c

def get_borders():
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    for p in _map:
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
