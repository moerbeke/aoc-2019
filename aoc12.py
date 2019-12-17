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

from collections import namedtuple
from blist import blist

C = namedtuple('C', ['x', 'y', 'z'])

_moon_coords_0 = None

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
    #find_cycle(energy)
    #find_cycle(get_state_x)
    #find_cycle(get_state_y)
    #find_cycle(get_state_z)
    return

def simulate(moons, steps):
    for i in range(steps):
        step(moons)

def step(moons):
    n_moons = len(moons)
    for i in range(0, n_moons-1):
        for j in range(i+1, n_moons):
            apply_gravity(moons[i], moons[j])
    for i in range(0, n_moons):
        apply_velocity(moons[i])

def apply_gravity(m1, m2):
    if m1.p.x > m2.p.x:
        m1.decr_vx()
        m2.incr_vx()
    elif m1.p.x < m2.p.x:
        m1.incr_vx()
        m2.decr_vx()
    if m1.p.y > m2.p.y:
        m1.decr_vy()
        m2.incr_vy()
    elif m1.p.y < m2.p.y:
        m1.incr_vy()
        m2.decr_vy()
    if m1.p.z > m2.p.z:
        m1.decr_vz()
        m2.incr_vz()
    elif m1.p.z < m2.p.z:
        m1.incr_vz()
        m2.decr_vz()

def apply_velocity(moon):
    moon.move()

def energy(moons):
    return sum([m.energy() for m in moons])

def find_cycle(state_getter):
    moons = reset()
    states = blist()
    state = state_getter(moons)
    steps = 0
    while not state in states:
        states.append(state)
        step(moons)
        state = state_getter(moons)
        steps += 1
        if steps % 1000 == 0:
            print(steps)
    offset = states.index(state)
    period = len(states) - offset
    assert(states[offset] == state)
    print(state)
    for i in range(period):
        step(moons)
        state = state_getter(moons)
        print(state)
    print(offset, period)
    assert(states[offset] == state_getter(moons))

def get_state_x(moons):
    return [m.p.x for m in moons] + [m.v.x for m in moons]

def get_state_y(moons):
    return [m.p.y for m in moons] + [m.v.y for m in moons]

def get_state_z(moons):
    return [m.p.z for m in moons] + [m.v.z for m in moons]

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
