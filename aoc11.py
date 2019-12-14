#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 11

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

P = namedtuple('P', ['x', 'y'])

BLACK = 0
WHITE = 1
COLOR = {BLACK: '.', WHITE: '#'}

TURN_LEFT = 0
TURN_RIGHT = 1
TURN = {TURN_LEFT: 'L', TURN_RIGHT: 'R'}

UP = 'N'
DOWN = 'S'
RIGHT = 'E'
LEFT = 'W'

DIRS = [UP, RIGHT, DOWN, LEFT]

_csv_program = None

def parse_input(input_str):
    global _csv_program
    _csv_program = input_str.strip()

def solve_1():
    return count_panels_to_paint()

def solve_2():
    paint_panel()

def count_panels_to_paint():
    computer = IntcodeComputer()
    computer.load_program(_csv_program)
    return len(run_robot_sw(computer, BLACK))

def run_robot_sw(computer, init_color):
    panels = dict()
    robot_id = 0
    computer.reset_feedback()
    halt = False
    x = 0
    y = 0
    p = P(x,y)
    direction = UP
    next_color = init_color
    i = 0
    while not halt:
        pinput = [next_color]
        #if i % 1000 == 0:
            #print_panel(panels)
        print("robot scanning at (%2d,%2d), %s [%s]" % (p.x, p.y, direction, COLOR[next_color]))
        output, halt = computer.run_program_feedback(robot_id, pinput)
        color, turn = output
        print("\_> color: %s, turn: %s" % (COLOR[color], TURN[turn]))
        panels[p] = color
        p, direction = next_pos(p, direction, turn)
        try:
            next_color = panels[p]
        except KeyError:
            next_color = BLACK
        pinput = [next_color]
        i += 1
    return panels

def next_pos(p, d, turn):
    di = DIRS.index(d)
    next_x = p.x
    next_y = p.y
    if turn == TURN_LEFT:
        next_d = DIRS[(di-1)%4]
        #print("L?", d, next_d)
    elif turn == TURN_RIGHT:
        next_d = DIRS[(di+1)%4]
        #print("R?", d, next_d)
    else:
        assert(False)
    if next_d == UP:
        next_y -= 1
    elif next_d == LEFT:
        next_x -= 1
    elif next_d == DOWN:
        next_y += 1
    elif next_d == RIGHT:
        next_x += 1
    else:
        assert(False)
    return P(next_x,next_y), next_d

def paint_panel():
    computer = IntcodeComputer()
    computer.load_program(_csv_program)
    panels = run_robot_sw(computer, WHITE)
    print_panel(panels)

def print_panel(panels):
    x1, y1, x2, y2 = get_borders(panels)
    for y in range(y1, y2+1):
        line = ''
        for x in range(x1, x2+1):
            p = P(x,y)
            try:
                pixel_color = panels[p]
                if pixel_color == BLACK:
                    line += '.'
                else:
                    line += '#'
            except KeyError:
                pixel_color = BLACK
                line += ' '
            #if pixel_color == BLACK:
                #line += ' '
            #else:
                #line += '#'
        print(line)

def get_borders(panels):
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    for p in panels:
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
# Intcode computer
########################################################################

from collections import namedtuple
from collections import OrderedDict

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
        self._program = None
        self._program_0 = None
        self._pc = None
        self._halt = None
        self._program_input = None
        self._program_output = None
        self._suspend = None
        self._programs = None
        self._programs_input = None
        self._pcs = None
        self._rel_base = None

    def load_program(self, cvs_program):
        pc = 0
        program_ins = [int(i) for i in cvs_program.strip().split(',')]
        self._program = OrderedDict()
        for ins in program_ins:
            self._program[pc] = ins
            pc += 1
        self._program_0 = self._program.copy()

    def reset(self):
        self._program = self._program_0.copy()
        self._halt = False
        self._suspend = False
        self._program_output = list()
        self.set_pc(0)
        self.set_rel_base(0)

    def reset_feedback(self):
        self.reset()
        self._programs = dict()
        self._pcs = dict()
        self._programs_input = dict()

    def run_program(self, program_input):
        self.reset()
        self._program_input = program_input
        while not self._halt:
            self.run_ins()
        return self._program_output

    def run_program_feedback(self, n, program_input):
        self.reset()
        self.init_program(n, program_input)
        while not self._halt and not self._suspend:
            self.run_ins()
        if self._suspend:
            self.save_program(n)
        assert(self._pc <= len(self._program))
        return self._program_output, self._halt

    def init_program(self, n, program_input):
        #print("input:", program_input)
        assert(len(program_input) == 1)
        if n in self._programs:
            self.restore_program(n)
            #assert(len(program_input) == 1)  # signal only
        else:
            self._programs_input[n] = self._program_input
            self._programs[n] = self._program
            #assert(len(program_input) == 2)  # phase setting, signal
        self._program_input = program_input

    def save_program(self, n):
        self._pcs[n] = self._pc

    def restore_program(self, n):
        self._program = self._programs[n]
        self._pc = self._pcs[n]
        self._program_input = self._programs_input[n]

    def run_ins(self):
        modal_op_code = self._program[self._pc]
        #print(self._pc, "ins:", modal_op_code)
        op_code = self.get_op_code(modal_op_code)
        try:
            self.op(op_code)(modal_op_code)
        except KeyError:
            assert(False)

    def op_halt(self, modal_op_code):
        op_code = self.get_op_code(modal_op_code)
        assert(op_code == modal_op_code)
        self._halt = True

    def op_input(self, modal_op_code):
        a, *ignore = self.read_parameters(modal_op_code, 1)
        try:
            self._program[a.addr] = self._program_input.pop(0)
            self.incr_pc()
        except IndexError:
            self.set_pc(self._pc - 1)
            self._suspend = True

    def op_output(self, modal_op_code):
        a, *ignore = self.read_parameters(modal_op_code, 1)
        if a.addr is None:
            #print("diagnostic code: %d" % a.value)
            self._program_output.append(a.value)
        else:
            #print(">>> output: %d" % a.value)
            #self._program_output = a.value
            self._program_output.append(a.value)
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
        #print("rel_base = %d + %d = %d" % (self._rel_base, a.value, self._rel_base + a.value))
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
            #p_addr = self.read_addr(self._pc + self._rel_base)
            #if p_addr < 0 :
                #print("PC: %d" % self._pc)
                #print("Rel. base: %d" % self._rel_base)
                #print(self.read_addr(self._pc))
                #self.dump()
            #assert(p_addr >= 0)
            p_value = self.read_addr(p_addr)
        elif p_mode == MODE_IMMEDIATE:
            p_addr = None
            p_value = self.read_addr(self._pc)
        else: 
            assert(False)
        return Parameter(p_addr, p_value)

    def read_addr(self, addr):
        try:
            #assert(addr >= 0)
            param = self._program[addr]
        except KeyError:
            param = 0
        return param

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

    def dump(self):
        print("Program dump:")
        print("PC: %d" % self._pc)
        print("Rel. base: %d" % self._rel_base)
        for p in sorted(self._program.keys()):
            print("%d: %4d" % (p, self._program[p]))

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
