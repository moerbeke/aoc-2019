#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 7

########################################################################
# Algorithms
########################################################################

import itertools

def parse_input(input_str):
    aoc5_parse_input(input_str)

def aoc7_reset():
    return

def solve_1():
    input_signal = 0
    max_output_signal = 0
    phases = [0, 1, 2, 3, 4]
    for phases in list(itertools.permutations(phases)):
        output_signal = run_amps(phases, input_signal)
        if output_signal > max_output_signal:
            max_output_signal = output_signal
    return max_output_signal

def solve_2():
    input_signal = 0
    max_output_signal = 0
    phases = [5, 6, 7, 8, 9]
    for phases in list(itertools.permutations(phases)):
        output_signal = run_amps_closedloop(phases, input_signal)
        if output_signal > max_output_signal:
            max_output_signal = output_signal
    return max_output_signal

def run_amps(phases, input_signal):
    for phase in phases:
        output_signal = run_amp(phase, input_signal)
        input_signal = output_signal
    return output_signal

def run_amp(phase, input_signal):
    return run_program([phase, input_signal])

def run_amps_closedloop(phases, input_signal):
    reset_feedback()
    halt = False
    l = 0
    output_signal, halt = run_amps_firstloop(phases, input_signal)
    assert(not halt)
    while not halt:
        l += 1
        input_signal = output_signal
        output_signal, halt = run_amps_loop(input_signal)
    return output_signal

def run_amps_firstloop(phases, input_signal):
    for i in range(len(phases)):
        output_signal, halt = run_amp_feedback(i, [phases[i], input_signal])
        input_signal = output_signal
    return output_signal, halt

def run_amps_loop(input_signal):
    for i in range(5):
        output_signal, halt = run_amp_feedback(i, [input_signal])
        input_signal = output_signal
    return output_signal, halt

def run_amp_feedback(amp, inputs):
    return run_program_feedback(amp, inputs)

########################################################################
# Intcode computer
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
_suspend = None
_programs = None
_programs_input = None
_ptrs = None

P = namedtuple('P', ['addr', 'value'])

def aoc5_parse_input(input_str):
    global _program
    global _program_0
    _program = [int(i) for i in input_str.strip().split(',')]
    _program_0 = _program.copy()

def reset():
    global _program
    global _halt
    global _suspend
    _program = _program_0.copy()
    _halt = False
    _suspend = False
    set_ptr(0)

def reset_feedback():
    global _programs
    global _ptrs
    global _programs_input
    reset()
    _programs = dict()
    _ptrs = dict()
    _programs_input = dict()

def aoc5_solve_1():
    program_input = 1
    run_program(program_input)
    return _program_output

def aoc5_solve_2():
    program_input = 5
    run_program(program_input)
    return _program_output

def run_program(program_input):
    global _program_input
    reset()
    _program_input = program_input
    while not _halt:
        run_ins()
    return _program_output

def run_program_feedback(n, program_input):
    reset()
    init_program(n, program_input)
    while not _halt and not _suspend:
        run_ins()
    if _suspend:
        save_program(n)
    assert(_ptr <= len(_program))
    return _program_output, _halt

def init_program(n, program_input):
    global _program_input
    if n in _programs:
        #print("---restore %d" % n)
        restore_program(n)
        assert(len(program_input) == 1)  # signal only
    else:
        #print("------init %d" % n)
        _programs_input[n] = _program_input
        _programs[n] = _program
        assert(len(program_input) == 2)  # phase setting, signal
    _program_input = program_input

def save_program(n):
    _ptrs[n] = _ptr

def restore_program(n):
    global _program
    global _ptr
    global _programs_input
    _program = _programs[n]
    _ptr = _ptrs[n]
    _program_input = _programs_input[n]

def run_ins():
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
    global _suspend
    a, *ignore = read_parameters(modal_op_code, 1)
    try:
        _program[a.addr] = _program_input.pop(0)
        #print("<<<  input: %d" % _program[a.addr])
        incr_ptr()
    except IndexError:
        set_ptr(_ptr - 1)
        _suspend = True

def op_output(modal_op_code):
    global _program_output
    a, *ignore = read_parameters(modal_op_code, 1)
    if a.addr is None:
        print("diagnostic code: %d" % a.value)
    else:
        #print(">>> output: %d" % a.value)
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
