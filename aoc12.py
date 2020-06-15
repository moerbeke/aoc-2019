#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 12

########################################################################
# Algorithms
########################################################################

import math
from collections import namedtuple

C = namedtuple('C', ['x', 'y', 'z'])

_moon_coords_0 = None

X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2

class Moon:

    def __init__(self, p):
        self.p = C(p.x, p.y, p.z)
        self.v = C(0,0,0)

    def decr_vx(self):
        self.v = C(self.v.x-1, self.v.y, self.v.z)

    def decr_vy(self):
        self.v = C(self.v.x, self.v.y-1, self.v.z)

    def decr_vz(self):
        self.v = C(self.v.x, self.v.y, self.v.z-1)

    def incr_vx(self):
        self.v = C(self.v.x+1, self.v.y, self.v.z)

    def incr_vy(self):
        self.v = C(self.v.x, self.v.y+1, self.v.z)

    def incr_vz(self):
        self.v = C(self.v.x, self.v.y, self.v.z+1)

    def move(self):
        self.p = C(
                self.p.x + self.v.x,
                self.p.y + self.v.y,
                self.p.z + self.v.z)

    def move_x(self):
        self.p = C(
                self.p.x + self.v.x,
                self.p.y,
                self.p.z)

    def move_y(self):
        self.p = C(
                self.p.x,
                self.p.y + self.v.y,
                self.p.z)

    def move_z(self):
        self.p = C(
                self.p.x,
                self.p.y,
                self.p.z + self.v.z)

    def energy(self):
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return abs(self.p.x) + abs(self.p.y) + abs(self.p.z)

    def kinetic_energy(self):
        return abs(self.v.x) + abs(self.v.y) + abs(self.v.z)

def parse_input(input_str):
    global _moon_coords_0
    _moon_coords_0 = list()
    for line in input_str.strip().split('\n'):
        coords = [c.strip() for c in line[1:-1].split(',')]
        x, y, z = [int(c.split('=')[1]) for c in coords]
        _moon_coords_0.append(C(x,y,z))

def reset():
    moons = list()
    for coords in _moon_coords_0:
        moons.append(Moon(coords))
    return moons

def solve_1():
    moons = reset()
    steps = 1000
    simulate(moons, steps)
    return energy(moons)

def solve_2():
    moons = reset()
    x = find_repeated_state_(X_AXIS, moons)
    y = find_repeated_state_(Y_AXIS, moons)
    z = find_repeated_state_(Z_AXIS, moons)
    xy = abs(x*y) // math.gcd(x, y)
    return abs(xy*z) // math.gcd(xy, z)

def simulate(moons, steps):
    for i in range(steps):
        step(moons)

def find_repeated_state_(axis, moons):
    state_0 = _get_state[axis](moons)
    for i in range(1000000):
        step_(axis, moons)
        state = _get_state[axis](moons)
        if state == state_0:
            return i + 1

def step(moons):
    n_moons = len(moons)
    for i in range(0, n_moons-1):
        for j in range(i+1, n_moons):
            apply_gravity(moons[i], moons[j])
    for i in range(0, n_moons):
        apply_velocity(moons[i])

def step_(axis, moons):
    n_moons = len(moons)
    for i in range(0, n_moons-1):
        for j in range(i+1, n_moons):
            _apply_gravity[axis](moons[i], moons[j])
    for i in range(0, n_moons):
        _apply_velocity[axis](moons[i])

def apply_gravity(m1, m2):
    apply_gravity_x(m1, m2)
    apply_gravity_y(m1, m2)
    apply_gravity_z(m1, m2)

def apply_gravity_x(m1, m2):
    if m1.p.x > m2.p.x:
        m1.decr_vx()
        m2.incr_vx()
    elif m1.p.x < m2.p.x:
        m1.incr_vx()
        m2.decr_vx()

def apply_gravity_y(m1, m2):
    if m1.p.y > m2.p.y:
        m1.decr_vy()
        m2.incr_vy()
    elif m1.p.y < m2.p.y:
        m1.incr_vy()
        m2.decr_vy()

def apply_gravity_z(m1, m2):
    if m1.p.z > m2.p.z:
        m1.decr_vz()
        m2.incr_vz()
    elif m1.p.z < m2.p.z:
        m1.incr_vz()
        m2.decr_vz()

def apply_velocity(moon):
    moon.move()

def apply_velocity_x(moon):
    moon.move_x()

def apply_velocity_y(moon):
    moon.move_y()

def apply_velocity_z(moon):
    moon.move_z()

def energy(moons):
    return sum([m.energy() for m in moons])

def get_state_x(moons):
    return [m.p.x for m in moons] + [m.v.x for m in moons]

def get_state_y(moons):
    return [m.p.y for m in moons] + [m.v.y for m in moons]

def get_state_z(moons):
    return [m.p.z for m in moons] + [m.v.z for m in moons]

_get_state = {
        X_AXIS: get_state_x,
        Y_AXIS: get_state_y,
        Z_AXIS: get_state_z}

_apply_gravity = {
        X_AXIS: apply_gravity_x,
        Y_AXIS: apply_gravity_y,
        Z_AXIS: apply_gravity_z}

_apply_velocity = {
        X_AXIS: apply_velocity_x,
        Y_AXIS: apply_velocity_y,
        Z_AXIS: apply_velocity_z}

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
