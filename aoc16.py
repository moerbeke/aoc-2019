#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 16

########################################################################
# Algorithms
########################################################################

_input_signal = None
_pattern = None

def parse_input(input_str):
    global _input_signal
    global _pattern
    _input_signal = input_str.strip()
    _pattern = list()
    for i in range(len(_input_signal)):
        _pattern.append(compute_pattern(i))

def reset():
    return

def solve_1():
    return fft_phases(_input_signal, 100)[:8]

# TODO uncomputable
def solve_2():
    return
    global _pattern
    input_signal = _input_signal * 10000
    for i in range(len(input_signal)):
        _pattern.append(compute_pattern(i))
    offset = int(input_signal[:7])
    return fft_phases(input_signal, 100)[offset:offset+8]

def fft_phases(input_signal, n_phases):
    for i in range(n_phases):
        output_signal = fft(input_signal)
        input_signal = output_signal
    return output_signal

def fft(input_signal):
    output_signal = ''
    for i in range(len(input_signal)):
        output_signal += build_element(i, input_signal)
    return output_signal

def build_element(i, input_signal):
    pattern = _pattern[i]
    plen = len(pattern)
    o = 0
    for i in range(len(input_signal)):
        n = int(input_signal[i])
        o += n * pattern[i % plen]
    o = abs(o) % 10
    return str(o)

def compute_pattern(i):
    base_pattern = [0, 1, 0, -1]  # base pattern
    pattern = []
    for n in base_pattern:
        for j in range(i+1):
            pattern.append(n)
    pattern = pattern[1:] + pattern[0:]
    pattern = pattern[0:len(base_pattern)*(i+1)]
    return pattern

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
