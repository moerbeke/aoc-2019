#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 4

########################################################################
# Algorithms
########################################################################

_n1 = None
_n2 = None

def parse_input(input_str):
    global _n1
    global _n2
    n1, n2 = [int(s) for s in input_str.split('-')]
    _n1 = n1
    _n2 = n2

def solve_1():
    return count_valid_pw()

def solve_2():
    return count_valid_pw_2()

def count_valid_pw():
    _valid_pws = list()
    for n in range(_n1, _n2 + 1):
        if is_valid_pw(n):
            _valid_pws.append(n)
    return len(_valid_pws)

def count_valid_pw_2():
    _valid_pws = list()
    for n in range(_n1, _n2 + 1):
        if is_valid_pw_2(n):
            _valid_pws.append(n)
    return len(_valid_pws)

def is_valid_pw(n):
    """
    Rules for a valid password:

    - It is a six-digit number.
    - The value is within the range given in your puzzle input.
    - Two adjacent digits are the same (like 22 in 122345).
    - Going from left to right, the digits never decrease;
      they only ever increase or stay the same (like 111123 or 135679).

    Other than the range rule, the following are true:

    - 111111 meets these criteria (double 11, never decreases).
    - 223450 does not meet these criteria (decreasing pair of digits 50).
    - 123789 does not meet these criteria (no double).
    """
    valid = (
            is_six_digit(n) and
            is_within_range(n, _n1, _n2) and
            is_double_adj_digits(n) and
            is_non_decr_digits(n))
    return valid

def is_valid_pw_2(n):
    """
    Rules for a valid password:

    - It is a six-digit number.
    - The value is within the range given in your puzzle input.
    - Two adjacent digits are the same (like 22 in 122345).
    - Going from left to right, the digits never decrease;
      they only ever increase or stay the same (like 111123 or 135679).

    Additional detail:

    - The two adjacent matching digits are not part of a larger group of matching digits.

    Given this additional criterion, but still ignoring the range rule, the following are now true:

    - 112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
    - 123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
    - 111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
    """
    valid = (
            is_six_digit(n) and
            is_within_range(n, _n1, _n2) and
            is_strict_double_adj_digits(n) and
            is_non_decr_digits(n))
    return valid

def get_digits(n):
    d = list()
    remaining = n
    for i in range(0, 6):
        digit = remaining // 10**(5-i)
        d.append(digit)
        remaining = remaining - digit * 10**(5-i)
    return d

def is_six_digit(n):
    return n > 99999 and n < 1000000

def is_within_range(n, a, b):
    return n >= a and n <= b

def is_double_adj_digits(n):
    d = get_digits(n)
    valid = False
    for i in range(1, 6):
        if d[i] == d[i-1]:
            valid = True
            break
    return valid

def is_strict_double_adj_digits(n):
    snn = successor(str(n))
    reps = [int(snn[i]) for i in range(len(snn)) if i % 2 == 0]
    if 2 in reps:
        valid = True
    else:
        valid = False
    return valid

def successor(element):
    s = ''
    i = 0
    while i < len(element):
        c = element[i]
        n = 1
        while i+n < len(element) and element[i+n] == c:
            n += 1
        s += str(n) + c
        i += n
    return s

def is_non_decr_digits(n):
    valid = True
    d = get_digits(n)
    for i in range(1, 6):
        if d[i] < d[i-1]:
            valid = False
            break
    return valid


########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
