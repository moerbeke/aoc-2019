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
    #return fft_phases(_input_signal, 100)[:8]
    return solve_1_fast()

def solve_1_fast():
    input_signal = _input_signal * 10000
    input_signal = _input_signal
    offset = int(input_signal[:7])
    offset = 0
    output_signal = fast_fft_phases(input_signal, 100)
    o = ''
    for i in output_signal[offset:offset+8]:
        o += str(i)
    return o

def solve_2():
    input_signal = _input_signal * 10000
    offset = int(input_signal[:7])
    #print("Signal length: %d, output offset: %d" % (len(input_signal), offset))
    output_signal = hyperfast_fft_phases(input_signal, offset, 100)
    o = ''
    for i in output_signal[0:8]:
        o += str(i)
    return o

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
    return pattern[1:] + pattern[:1]

def fast_fft_phases(input_signal, n_phases):
    input_signal = [int(i) for i in input_signal]
    for i in range(n_phases):
        #print("phase", i)
        output_signal = fast_fft(input_signal)
        assert(len(output_signal) == len(input_signal))
        #print("phase", i, "\n", output_signal)
        input_signal = output_signal.copy()
    return output_signal

def hyperfast_fft_phases(input_signal, offset, n_phases):
    input_signal = [int(i) for i in input_signal]
    input_signal = input_signal[offset:]  # relevant input signal
    for i in range(n_phases):
        #print("phase", i)
        output_signal = hyperfast_fft(input_signal)
        assert(len(output_signal) == len(input_signal))
        #print("phase", i, "\n", output_signal[:8])
        input_signal = output_signal.copy()
    return output_signal

def hyperfast_fft(input_signal):
    ilen = len(input_signal)
    output_signal = [0] * ilen
    output_signal[ilen - 1] = input_signal[ilen - 1] % 10
    for i in range(ilen - 1):
        k = ilen - 2 - i
        #print("%d/%d" % (k, ilen))
        output_signal[k] = (output_signal[k + 1] + input_signal[k]) % 10
    return output_signal

def fast_fft(input_signal):
    output_signal = list()
    for i in range(len(input_signal)):
        output_signal.append(fast_build_element(i, input_signal))
        #print("position", i)
    return output_signal

def fast_build_element(i, input_signal):
    ilen = len(input_signal)
    o = 0
    if False:
        pattern = _pattern[i]
        plen = len(pattern)
        if i == 0:
            o += sum(input_signal[0:1]) - sum(input_signal[2:3])
            o += sum(input_signal[4:5]) - sum(input_signal[6:7])
            o += sum(input_signal[8:9]) - sum(input_signal[10:11])
            #...
            o += sum(input_signal[k:k+1]) - sum(input_signal[k+2:k+3])  # k < ilen
        elif i == 1:
            o += sum(input_signal[1:3]) - sum(input_signal[5:7])
            o += sum(input_signal[9:11]) - sum(input_signal[13:15])
            o += sum(input_signal[17:19]) - sum(input_signal[21:23])
            #...
            o += sum(input_signal[k:k+2]) - sum(input_signal[k+4:k+6])  # k < ilen
        elif i == 2:
            o += sum(input_signal[2:5]) - sum(input_signal[8:11])
            o += sum(input_signal[14:17]) - sum(input_signal[20:23])
            o += sum(input_signal[26:29]) - sum(input_signal[32:35])
            #...
            o += sum(input_signal[k:k+3]) - sum(input_signal[k+6:k+9])  # k < ilen
        #...
        elif i == ilen - 1:
            o += sum(input_signal[1*i+0: 2*i+1]) - sum(input_signal[ 3*i+2 : 4*i+3])
            o += sum(input_signal[5*i+4: 6*i+5]) - sum(input_signal[ 7*i+6 : 8*i+7])
            o += sum(input_signal[9*i+8:10*i+9]) - sum(input_signal[11*i+10:12*i+11])
    j = 0
    while True:
        a = i * (4*j+1) + 4*j
        if a > ilen:
            break
        b = i * (4*j+2) + (4*j+1)
        b = min(b, ilen)
        o += sum(input_signal[a:b])
        c = i * (4*j+3) + (4*j+2)
        if c > ilen:
            break
        d = i * (4*j+4) + (4*j+3)
        d = min(d, ilen)
        o -= sum(input_signal[c:d])
        j += 1
    o = abs(o) % 10
    return o

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
