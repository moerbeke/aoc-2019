#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 6

########################################################################
# Day 6 algorithms
########################################################################

_bodies = None
_centers = None

def parse_input(input_str):
    global _bodies
    global _centers
    _bodies = list()
    _centers = dict()
    for orbit in input_str.strip().split('\n'):
        c, b = orbit.split(')')
        if c not in _bodies:
            _bodies.append(c)
        if b not in _bodies:
            _bodies.append(b)
        _centers[b] = c

def reset():
    return

def solve_1():
    n = 0
    for b in _bodies:
        while True:
            try:
                c = _centers[b]
                n += 1
            except KeyError:
                break
            b = c
    return n

def solve_2():
    you_cs = list()
    b = 'YOU'
    while True:
        try:
            c = _centers[b]
            you_cs.append(c)
        except KeyError:
            break
        b = c
    san_cs = list()
    b = 'SAN'
    while True:
        try:
            c = _centers[b]
            san_cs.append(c)
        except KeyError:
            break
        b = c
    n = 0
    for c in you_cs:
        if c not in san_cs:
            n += 1
        else:
            break
    for c in san_cs:
        if c not in you_cs:
            n += 1
        else:
            break
    return n


########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
