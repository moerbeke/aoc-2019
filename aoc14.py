#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 14

########################################################################
# Algorithms
########################################################################

from collections import namedtuple

Ch = namedtuple('Ch', ['n', 'ch'])
Reaction = namedtuple('Reaction', ['output', 'inputs'])

_target_input_ch = 'ORE'
_target_input_n = None
_reactions_0 = None
_remains_0 = None
_reactions = None
_remains = None

def parse_input(input_str):
    global _reactions_0
    global _remains_0
    _reactions_0 = dict()
    _remains_0 = dict()
    _remains_0[_target_input_ch] = 0
    for line in input_str.strip().split('\n'):
        inputs, output = line.strip().split('=>')
        inputs = inputs.strip().split(',')
        inputs = [i.split() for i in inputs]
        inputs = [Ch(int(i[0]), i[1]) for i in inputs]
        output = output.split()
        output = Ch(int(output[0]), output[1])
        _reactions_0[output.ch] = {'output': output, 'inputs': inputs}
        _remains_0[output.ch] = 0

def reset():
    global _target_input_n
    global _reactions
    global _remains
    _target_input_n = 0
    _reactions = _reactions_0.copy()
    _remains = _remains_0.copy()

def solve_1():
    reset()
    compute_input_amount(Ch(1, 'FUEL'))
    return _target_input_n

def compute_input_amount(output):
    output_still_to_be_obtained = use_remains_if_exist(output)
    if output_still_to_be_obtained.n > 0:
        do_reaction(output_still_to_be_obtained)

def use_remains_if_exist(output):
    current_remains = _remains[output.ch]
    new_remains = current_remains - output.n
    if new_remains >= 0:
        _remains[output.ch] = new_remains
        output_still_to_be_obtained = 0
    else:
        _remains[output.ch] = 0
        output_still_to_be_obtained = -new_remains
    return Ch(output_still_to_be_obtained, output.ch)

def do_reaction(output):
    global _target_input_n
    direct_inputs = produce_inputs(output)
    for i in direct_inputs:
        if i.ch == _target_input_ch:
            _target_input_n += i.n
        else:
            compute_input_amount(i)

def produce_inputs(output):
    reaction = _reactions[output.ch]
    scale = compute_scale(output.n, reaction['output'].n)
    _remains[output.ch] += reaction['output'].n * scale - output.n
    scaled_inputs = list()
    for i in reaction['inputs']:
        scaled_inputs.append(Ch(i.n*scale, i.ch))
    return scaled_inputs

def compute_scale(target, base):
    if base >= target:
        scale = 1
    else:
        scale = target // base
        if target % base > 0:
            scale += 1
    return scale

def solve_2():
    # Approach: binary search of the solution, based on the algorithm for Part 1.
    available_ORE = 1e+12
    fuel_lower_bound = 1  # known from Part 1
    fuel_upper_bound = 3628800  # proven true: requires 1106573746307 ~= 1.1e+12
    fuel_upper_bound = 3628800*int(1e+12)  # test cases require more
    max_fuel = 0
    while fuel_upper_bound - fuel_lower_bound > 1:
        fuel_range = fuel_upper_bound + fuel_lower_bound
        target_fuel = (fuel_range + (fuel_range % 2)) // 2
        target_fuel = fuel_range // 2
        reset()
        compute_input_amount(Ch(target_fuel, 'FUEL'))
        if _target_input_n >= available_ORE:
            fuel_upper_bound = target_fuel
        else:
            fuel_lower_bound = target_fuel
            max_fuel = fuel_lower_bound
    return max_fuel

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
