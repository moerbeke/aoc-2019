#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 10

########################################################################
# Algorithms
########################################################################

from collections import namedtuple
from math import isclose
from math import pi
from math import atan2

P = namedtuple('P', ['x', 'y'])

EMPTY = '.'
ASTEROID = '#'

_map = None
_v_asteroids = None
_mx = None
_my = None
_dir_asteroids = None

def parse_input(input_str):
    global _map
    global _mx
    global _my
    _map = dict()
    y = 0
    for line in input_str.strip().split('\n'):
        x = 0
        for c in line:
            p = P(x,y)
            if c == EMPTY or c == ASTEROID:
                _map[p] = c
            else:
                raise ValueError("Unknown space: '%s'" % c)
            x += 1
        y += 1
        _mx = x
    _my = y

def reset():
    global _v_asteroids
    global _dir_asteroids
    _v_asteroids = dict()
    _dir_asteroids = dict()
    for p in _map:
        if _map[p] == ASTEROID:
            _v_asteroids[p] = 0
            _dir_asteroids[p] = dict()

def solve_1():
    reset()
    return best_asteroid()[0]

def solve_2():
    reset()
    *ignore, best_asteroid_p = best_asteroid()
    return hit(best_asteroid_p, 200)

def best_asteroid():
    max_v_asteroids = 0
    max_v_asteroids_p = None
    for p in _v_asteroids:
        n = compute_visible_asteroids(p)
        _v_asteroids[p] = n
        if n > max_v_asteroids:
            max_v_asteroids = n
            max_v_asteroids_p = p
    #print("Best asteroid at %d,%d" % (max_v_asteroids_p.x, max_v_asteroids_p.y))
    return max_v_asteroids, max_v_asteroids_p

def compute_visible_asteroids(p0):
    x0 = p0.x
    y0 = p0.y
    n = 0
    # On the right
    n += check_range(p0, range(x0+1, _mx), range(y0, y0+1))
    # Above
    n += check_range(p0, range(x0, x0+1), range(y0-1, -1, -1))
    # On the left
    n += check_range(p0, range(x0-1, -1, -1), range(y0, y0+1))
    # Below
    n += check_range(p0, range(x0, x0+1), range(y0+1, _my))
    # Bottom-right
    n += check_range(p0, range(x0+1, _mx), range(y0+1, _my))
    # Bottom-left
    n += check_range(p0, range(x0-1, -1, -1), range(y0+1, _my))
    # Top-right
    n += check_range(p0, range(x0+1, _mx), range(y0-1, -1, -1))
    # Top-left
    n += check_range(p0, range(x0-1, -1, -1), range(y0-1, -1, -1))
    return n

def check_range(p0, rx, ry):
    x0 = p0.x
    y0 = p0.y
    n = 0
    for x in rx:
        for y in ry:
            d = atan2(-y+y0, x-x0)
            if not d in _dir_asteroids[p0]:
                _dir_asteroids[p0][d] = list()
            n += check_asteroid(P(x,y), p0, d)
    return n

def check_asteroid(p, p0, d):
    n = 0
    if is_asteroid(p):
        if len(_dir_asteroids[p0][d]) == 0:
            n = 1
        _dir_asteroids[p0][d].append(p)
    return n

def is_asteroid(p):
    return p in _v_asteroids

def hit(p0, hits):
    sorted_dirs_0 = list(reversed(sorted(_dir_asteroids[p0].keys())))
    up_index = sorted_dirs_0.index(pi/2)
    sorted_dirs = sorted_dirs_0[up_index:] + sorted_dirs_0[:up_index]
    n = 0
    while n < hits:
        for d in sorted_dirs:
            try:
                p = _dir_asteroids[p0][d].pop(0)
                n += 1
                if n == hits:
                    break
            except IndexError:
                pass
    return 100 * p.x + p.y

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
