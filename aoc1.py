#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 1

########################################################################
# Day 1 algorithms
########################################################################

def reset():
    pass

def parse_input(input_str):
    global _masses
    _masses = [int(m) for m in input_str.strip().split('\n')]

def solve_1():
    f = 0
    for m in _masses:
        f += int(m / 3) - 2
    return f

def solve_2():
    f = 0
    for m in _masses:
        fm = 0
        while True:
            x = int(m / 3) - 2
            if x <= 0:
                break
            fm += x
            m = x
        f += fm
    return f

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
