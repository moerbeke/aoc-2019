########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

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
OP_ADJ_REL_BASE = 9

MODE_POSITION = 0
MODE_IMMEDIATE = 1
MODE_RELATIVE = 2

Parameter = namedtuple('Parameter', ['addr', 'value'])

class IntcodeComputer:

    def __init__(self):
        self._halt_interrupt = None
        self._input_interrupt = None
        self._output_interrupt = None
        self._program = None
        self._program_0 = None
        self._pc = None
        self._program_input = None
        self._program_output = None
        self._rel_base = None

    def load_program(self, cvs_program):
        pc = 0
        program_ins = [int(i) for i in cvs_program.strip().split(',')]
        self._program = dict()
        for ins in program_ins:
            self._program[pc] = ins
            pc += 1
        self._program_0 = self._program.copy()

    def reset(self):
        self._program = self._program_0.copy()
        self.set_pc(0)
        self.set_rel_base(0)
        self._program_input = list()
        self._program_output = list()
        self.clear_interruptions()

    def run_program(self):
        self.clear_interruptions()
        while not self.is_interrupted():
            self.run_ins()
        return self._halt_interrupt, self._input_interrupt, self._output_interrupt

    def clear_interruptions(self):
        self._halt_interrupt = False
        self._input_interrupt = False
        self._output_interrupt = False

    def is_interrupted(self):
        return self._halt_interrupt or self._input_interrupt or self._output_interrupt

    def push_input(self, input_data):
        self._program_input.append(input_data)

    def pop_output(self):
        try:
            next_output = self._program_output.pop(0)
        except IndexError:
            next_output = None
        return next_output

    def run_ins(self):
        modal_op_code = self._program[self._pc]
        op_code = self.get_op_code(modal_op_code)
        try:
            self.op(op_code)(modal_op_code)
        except KeyError:
            assert(False)

    def op_halt(self, modal_op_code):
        op_code = self.get_op_code(modal_op_code)
        assert(op_code == modal_op_code)
        self._halt_interrupt = True

    def op_input(self, modal_op_code):
        a, *ignore = self.read_parameters(modal_op_code, 1)
        try:
            self._program[a.addr] = self._program_input.pop(0)
            self.incr_pc()
        except IndexError:
            self.set_pc(self._pc - 1)
            self._input_interrupt = True

    def op_output(self, modal_op_code):
        a, *ignore = self.read_parameters(modal_op_code, 1)
        if a.addr is None:
            self._program_output.append(a.value)
        else:
            self._program_output.append(a.value)
        self._output_interrupt = True
        self.incr_pc()

    def op_add(self, modal_op_code):
        a, b, c = self.read_parameters(modal_op_code, 3)
        self._program[c.addr] = a.value + b.value
        self.incr_pc()

    def op_mul(self, modal_op_code):
        a, b, c = self.read_parameters(modal_op_code, 3)
        self._program[c.addr] = a.value * b.value
        self.incr_pc()

    def op_less_than(self, modal_op_code):
        a, b, c = self.read_parameters(modal_op_code, 3)
        if a.value < b.value:
            self._program[c.addr] = 1
        else:
            self._program[c.addr] = 0
        self.incr_pc()

    def op_equals(self, modal_op_code):
        a, b, c = self.read_parameters(modal_op_code, 3)
        if a.value == b.value:
            self._program[c.addr] = 1
        else:
            self._program[c.addr] = 0
        self.incr_pc()

    def op_jump_if_true(self, modal_op_code):
        a, b = self.read_parameters(modal_op_code, 2)
        if a.value != 0:
            self.set_pc(b.value)
        else:
            self.incr_pc()

    def op_jump_if_false(self, modal_op_code):
        a, b = self.read_parameters(modal_op_code, 2)
        if a.value == 0:
            self.set_pc(b.value)
        else:
            self.incr_pc()

    def op_adj_rel_base(self, modal_op_code):
        a, *ignore = self.read_parameters(modal_op_code, 1)
        self.set_rel_base(self._rel_base + a.value)
        self.incr_pc()

    def op(self, op_code):
        return {
            OP_HALT:          self.op_halt,
            OP_INPUT:         self.op_input,
            OP_OUTPUT:        self.op_output,
            OP_ADD:           self.op_add,
            OP_MUL:           self.op_mul,
            OP_LESS_THAN:     self.op_less_than,
            OP_EQUALS:        self.op_equals,
            OP_JUMP_IF_TRUE:  self.op_jump_if_true,
            OP_JUMP_IF_FALSE: self.op_jump_if_false,
            OP_ADJ_REL_BASE:  self.op_adj_rel_base,
            }[op_code]

    def read_parameters(self, modal_op_code, n_params):
        params = list()
        modes = self.get_parameter_modes(modal_op_code)
        n = 0
        for n in range(n_params):
            self.incr_pc()
            params.append(self.get_modal_param(modes[n]))
        return params

    def get_modal_param(self, p_mode):
        if p_mode == MODE_POSITION:
            p_addr = self.read_addr(self._pc)
            p_value = self.read_addr(p_addr)
        elif p_mode == MODE_RELATIVE:
            p_addr = self.read_addr(self._pc) + self._rel_base
            assert(p_addr >= 0)
            p_value = self.read_addr(p_addr)
        elif p_mode == MODE_IMMEDIATE:
            p_addr = None
            p_value = self.read_addr(self._pc)
        else: 
            assert(False)
        return Parameter(p_addr, p_value)

    def read_addr(self, addr):
        try:
            param = self._program[addr]
        except KeyError:
            param = 0
        return param

    def write_addr(self, addr, value):
        self._program[addr] = value

    def get_op_code(self, modal_op_code):
        n = modal_op_code
        op_code = n % 100
        return op_code

    def get_parameter_modes(self, modal_op_code):
        n = modal_op_code
        n = n // 100
        a_mode = n % 10
        n = n // 10
        b_mode = n % 10
        n = n // 10
        c_mode = n % 10
        return a_mode, b_mode, c_mode

    def incr_pc(self):
        self._pc += 1

    def set_pc(self, p):
        self._pc = p

    def set_rel_base(self, b):
        self._rel_base = b
