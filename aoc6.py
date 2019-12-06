#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 6

########################################################################
# Algorithms
########################################################################

_centers = None

def parse_input(input_str):
    global _centers
    _centers = dict()
    for orbit in input_str.strip().split('\n'):
        c, b = orbit.split(')')
        _centers[b] = c

def solve_1():
    n = 0
    for b in _centers:
        n += len(get_body_centers(b))
    return n

def solve_2():
    you_cs = get_body_centers('YOU')
    san_cs = get_body_centers('SAN')
    n_you = sum(1 for c in you_cs if c not in san_cs)
    n_san = sum(1 for c in san_cs if c not in you_cs)
    return n_you + n_san

def get_body_centers(b):
    cs = list()
    while True:
        try:
            c = _centers[b]
            cs.append(c)
        except KeyError:
            break
        b = c
    return cs

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
