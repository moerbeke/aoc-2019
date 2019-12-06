#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 5

########################################################################
# Algorithms
########################################################################

OP_HALT = 99
OP_ADD = 1
OP_MUL = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JUMP_IF_TRUE = 5
OP_JUMP_IF_FALSE = 6
OP_LESS_THAN = 7
OP_EQUALS = 8

MODE_POSITION = 0
MODE_IMMEDIATE = 1

_program = None
_program_0 = None
_ptr = None
_halt = None
_program_input = None
_program_output = None

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
    program_input = 1
    run_program(program_input)
    return _program_output

def solve_2():
    program_input = 5
    run_program(program_input)
    return _program_output

def run_program(program_input):
    global _program_input
    reset()
    _program_input = program_input
    while not _halt:
        run_ins()

def run_ins():
    global _halt
    global _ptr
    global _program_output
    modal_op_code = _program[_ptr]
    if modal_op_code == OP_HALT:
        _halt = True
    else:
        if modal_op_code == OP_INPUT:
            _ptr += 1
            a_addr = _program[_ptr]
            _program[a_addr] = _program_input
            _ptr += 1
        elif modal_op_code % 10 == OP_OUTPUT:
            op_code, a_mode, *ignore = get_op_parameter_modes(modal_op_code)
            _ptr += 1
            if a_mode == MODE_POSITION:
                a_addr = _program[_ptr]
                a = _program[a_addr]
                _program_output = _program[a_addr]
            else:
                a_addr = None
                a = _program[_ptr]
                print("diagnostic code: %d" % a)
            _ptr += 1
        else:
            op_code, a_mode, b_mode, c_mode = get_op_parameter_modes(modal_op_code)
            _ptr += 1
            if a_mode == MODE_POSITION:
                a_addr = _program[_ptr]
                a = _program[a_addr]
            else:
                a_addr = None
                a = _program[_ptr]
            _ptr += 1
            if b_mode == MODE_POSITION:
                b_addr = _program[_ptr]
                b = _program[b_addr]
            else:
                b_addr = None
                b = _program[_ptr]
            if op_code == OP_ADD:
                _ptr += 1
                assert(c_mode == MODE_POSITION)
                c_addr = _program[_ptr]
                _program[c_addr] = a + b
                _ptr += 1
            elif op_code == OP_MUL:
                _ptr += 1
                assert(c_mode == MODE_POSITION)
                c_addr = _program[_ptr]
                _program[c_addr] = a * b
                _ptr += 1
            elif op_code == OP_LESS_THAN:
                _ptr += 1
                assert(c_mode == MODE_POSITION)
                c_addr = _program[_ptr]
                if a < b:
                    _program[c_addr] = 1
                else:
                    _program[c_addr] = 0
                _ptr += 1
            elif op_code == OP_EQUALS:
                _ptr += 1
                assert(c_mode == MODE_POSITION)
                c_addr = _program[_ptr]
                if a == b:
                    _program[c_addr] = 1
                else:
                    _program[c_addr] = 0
                _ptr += 1
            elif op_code == OP_JUMP_IF_TRUE:
                if a != 0:
                    _ptr = b
                else:
                    _ptr += 1
            elif op_code == OP_JUMP_IF_FALSE:
                if a == 0:
                    _ptr = b
                else:
                    _ptr += 1
            else:
                assert(False)

def get_op_parameter_modes(modal_op_code):
    n = modal_op_code
    op_code = n % 100
    n = n // 100
    a_code = n % 10
    n = n // 10
    b_code = n % 10
    n = n // 10
    c_code = n % 10
    return op_code, a_code, b_code, c_code


########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
