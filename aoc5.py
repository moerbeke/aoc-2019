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

from collections import namedtuple

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

P = namedtuple('P', ['addr', 'value'])

def parse_input(input_str):
    global _program
    global _program_0
    _program = [int(i) for i in input_str.strip().split(',')]
    _program_0 = _program.copy()

def reset():
    global _program
    global _halt
    _program = _program_0.copy()
    set_ptr(0)
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
    global _program_output
    modal_op_code = _program[_ptr]
    op_code = get_op_code(modal_op_code)
    try:
        op[op_code](modal_op_code)
    except KeyError:
        assert(False)

def op_halt(modal_op_code):
    global _halt
    op_code = get_op_code(modal_op_code)
    assert(op_code == modal_op_code)
    _halt = True

def op_input(modal_op_code):
    a, *ignore = read_parameters(modal_op_code, 1)
    _program[a.addr] = _program_input
    incr_ptr()

def op_output(modal_op_code):
    global _program_output
    a, *ignore = read_parameters(modal_op_code, 1)
    if a.addr is None:
        print("diagnostic code: %d" % a.value)
    else:
        _program_output = a.value
    incr_ptr()

def op_add(modal_op_code):
    a, b, c = read_parameters(modal_op_code, 3)
    _program[c.addr] = a.value + b.value
    incr_ptr()

def op_mul(modal_op_code):
    a, b, c = read_parameters(modal_op_code, 3)
    _program[c.addr] = a.value * b.value
    incr_ptr()

def op_less_than(modal_op_code):
    a, b, c = read_parameters(modal_op_code, 3)
    if a.value < b.value:
        _program[c.addr] = 1
    else:
        _program[c.addr] = 0
    incr_ptr()

def op_equals(modal_op_code):
    a, b, c = read_parameters(modal_op_code, 3)
    if a.value == b.value:
        _program[c.addr] = 1
    else:
        _program[c.addr] = 0
    incr_ptr()

def op_jump_if_true(modal_op_code):
    a, b = read_parameters(modal_op_code, 2)
    if a.value != 0:
        set_ptr(b.value)
    else:
        incr_ptr()

def op_jump_if_false(modal_op_code):
    a, b = read_parameters(modal_op_code, 2)
    if a.value == 0:
        set_ptr(b.value)
    else:
        incr_ptr()

op = {
        OP_HALT:          op_halt,
        OP_INPUT:         op_input,
        OP_OUTPUT:        op_output,
        OP_ADD:           op_add,
        OP_MUL:           op_mul,
        OP_LESS_THAN:     op_less_than,
        OP_EQUALS:        op_equals,
        OP_JUMP_IF_TRUE:  op_jump_if_true,
        OP_JUMP_IF_FALSE: op_jump_if_false,
        }

def read_parameters(modal_op_code, n_params):
    params = list()
    modes = get_parameter_modes(modal_op_code)
    n = 0
    for n in range(n_params):
        incr_ptr()
        params.append(get_modal_param(modes[n]))
    return params

def get_modal_param(p_mode):
    if p_mode == MODE_POSITION:
        p_addr = _program[_ptr]
        p_value = _program[p_addr]
    else:
        p_addr = None
        p_value = _program[_ptr]
    return P(p_addr, p_value)

def get_op_code(modal_op_code):
    n = modal_op_code
    op_code = n % 100
    return op_code

def get_parameter_modes(modal_op_code):
    n = modal_op_code
    n = n // 100
    a_mode = n % 10
    n = n // 10
    b_mode = n % 10
    n = n // 10
    c_mode = n % 10
    return a_mode, b_mode, c_mode

def incr_ptr():
    global _ptr
    _ptr += 1

def set_ptr(p):
    global _ptr
    _ptr = p


########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
