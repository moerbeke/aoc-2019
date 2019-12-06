#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 2

########################################################################
# Algorithms
########################################################################

_program = None
_program_0 = None
_ptr = None
_halt = None

def parse_input(input_str):
    global _program
    global _program_0
    _program = [int(i) for i in input_str.strip().split(',')]
    _program_0 = _program.copy()

def reset():
    global _program
    global _ptr
    global _halt
    _program = _program_0.copy()
    _ptr = 0
    _halt = False

def solve_1():
    reset()
    run(12, 2)
    output = _program[0]
    return output

def run(noun=None, verb=None):
    if noun is not None and verb is not None:
        init(noun, verb)
    while not _halt:
        step()

def init(noun, verb):
    _program[1] = noun
    _program[2] = verb

def step():
    global _ptr
    global _halt
    op_code = _program[_ptr]
    if op_code == 99:
        _halt = True
    else:
        a = _program[_ptr + 1]
        b = _program[_ptr + 2]
        c = _program[_ptr + 3]
        if op_code == 1:
            _program[c] = _program[a] + _program[b]
        elif op_code == 2:
            _program[c] = _program[a] * _program[b]
        else:
            assert(false)
        _ptr += 4

def state():
    return ','.join([str(i) for i in _program])

def solve_2():
    ok = False
    for noun in range(100):
        for verb in range(100):
            reset()
            run(noun, verb)
            output = _program[0]
            if output == 19690720:
                ok = True
                break
        if ok:
            break
    return 100 * noun + verb

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
