#!/usr/bin/env python3

########################################################################
# The Advent of Code 2019
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

import aocbase

########################################################################
# Algorithm class
########################################################################

class Aoc4(aocbase.AocBase):

    def __init__(self, read_default_input=True, input_filename=None, input_str=None):
        self._n1 = None
        self._n2 = None
        super().__init__(read_default_input, input_filename, input_str)

    def do_parse_input(self):
        n1, n2 = [int(s) for s in self._input.split('-')]
        self._n1 = n1
        self._n2 = n2

    def do_solve_1(self):
        return self.count_valid_pw()

    def do_solve_2(self):
        return self.count_valid_pw_2()

    def count_valid_pw(self):
        self._valid_pws = list()
        for n in range(self._n1, self._n2 + 1):
            if self.is_valid_pw(n):
                self._valid_pws.append(n)
        return len(self._valid_pws)

    def count_valid_pw_2(self):
        self._valid_pws = list()
        for n in range(self._n1, self._n2 + 1):
            if self.is_valid_pw_2(n):
                self._valid_pws.append(n)
        return len(self._valid_pws)

    def is_valid_pw(self, n):
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
                self.is_six_digit(n) and
                self.is_within_range(n, self._n1, self._n2) and
                self.is_double_adj_digits(n) and
                self.is_non_decr_digits(n))
        return valid

    def is_valid_pw_2(self, n):
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
                self.is_six_digit(n) and
                self.is_within_range(n, self._n1, self._n2) and
                self.is_strict_double_adj_digits(n) and
                self.is_non_decr_digits(n))
        return valid

    def get_digits(self, n):
        d = list()
        remaining = n
        for i in range(0, 6):
            digit = remaining // 10**(5-i)
            d.append(digit)
            remaining = remaining - digit * 10**(5-i)
        return d

    def is_six_digit(self, n):
        return n > 99999 and n < 1000000

    def is_within_range(self, n, a, b):
        return n >= a and n <= b

    def is_double_adj_digits(self, n):
        d = self.get_digits(n)
        valid = False
        for i in range(1, 6):
            if d[i] == d[i-1]:
                valid = True
                break
        return valid

    def is_strict_double_adj_digits(self, n):
        snn = self.successor(str(n))
        reps = [int(snn[i]) for i in range(len(snn)) if i % 2 == 0]
        if 2 in reps:
            valid = True
        else:
            valid = False
        return valid

    def successor(self, element):
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

    def is_non_decr_digits(self, n):
        valid = True
        d = self.get_digits(n)
        for i in range(1, 6):
            if d[i] < d[i-1]:
                valid = False
                break
        return valid


########################################################################
# main
########################################################################

if __name__ == '__main__':
    aocbase.run(Aoc4)
