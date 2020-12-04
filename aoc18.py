#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 18

########################################################################
# Algorithms
########################################################################

from math import inf
from collections import namedtuple
import copy
import time

P = namedtuple('P', ['x', 'y'])

WALL = '#'
ENTRANCE = '@'
OPEN_PASSAGE = '.'

_path = ''


class Key:

    def __init__(self, pos, key_name):
        self._pos = pos
        self._name = key_name
        self._door = key_name.upper()

    @property
    def door(self):
        return self._door

    @property
    def pos(self):
        return self._pos

    @property
    def name(self):
        return self._name

    @property
    def x(self):
        return self._pos.x

    @property
    def y(self):
        return self._pos.y


class Tmap:
    
    def __init__(self, input_tmap):
        self._map = dict()
        self._tunnel_map = dict()
        if isinstance(input_tmap, str):
            y = 0
            for line in input_tmap.strip().split('\n'):
                x = 0
                for c in line:
                    self._map[P(x,y)] = c
                    x += 1
                self._end_x = x
                y += 1
            self._end_y = y
            self._my_pos = None
            self._keys = dict()
            for p in self._map:
                c = self._map[p]
                if c == ENTRANCE:
                    self._my_pos = p
                    self._tunnel_map[p] = OPEN_PASSAGE
                elif c >= 'a' and c <= 'z':
                    self._keys[p] = Key(p, c)
                    self._tunnel_map[p] = OPEN_PASSAGE
                elif c == OPEN_PASSAGE:
                    self._tunnel_map[p] = OPEN_PASSAGE
                else:
                    self._tunnel_map[p] = WALL
            self._hash_map = dict()
            self._open_doors = list()
        elif isinstance(input_tmap, Tmap):
            self._map = copy.copy(input_tmap._map)
            self._tunnel_map = copy.copy(input_tmap._tunnel_map)
            self._keys = copy.copy(input_tmap._keys)
            self._hash_map = copy.copy(input_tmap._hash_map)
            self._open_doors = copy.copy(input_tmap._open_doors)
            self._end_x = input_tmap._end_x
            self._end_y = input_tmap._end_y
            self._my_pos = input_tmap._my_pos

    @property
    def keys(self):
        return self._keys

    def find_reachable_keys(self):
        global _time_find_keys_clone
        global _time_comp_dist
        hashkey = str(self._my_pos) + str(sorted(self._open_doors))
        if hashkey in self._hash_map:
            print(">>>>>>>>>>>>>> hash FOUND")
            return self._hash_map[hashkey]
        reachable_keys = []
        start = time.process_time()
        dmap = dict()
        _time_find_keys_clone += (time.process_time() - start)
        for p in self._tunnel_map:
            dmap[p] = None
        p0 = self._my_pos
        dmap[p0] = 0
        start = time.process_time()
        self._comp_dist(p0, dmap)
        _time_comp_dist += (time.process_time() - start)
        for p in self._keys:
            if dmap[p] is not None and dmap[p] < inf:
                reachable_keys.append(self._keys[p])
        self._dmap = dmap
        self._hash_map[hashkey] = reachable_keys
        return reachable_keys

    def _comp_dist(self, p0, dmap):
        d = dmap[p0] + 1
        if p0.x > 0:  # go left
            p = P(p0.x-1,p0.y)
            self._try_move(p, d, dmap)
        if p0.x < self._end_x - 1:  # go right
            p = P(p0.x+1,p0.y)
            self._try_move(p, d, dmap)
        if p0.y > 0:  # go up
            p = P(p0.x,p0.y-1)
            self._try_move(p, d, dmap)
        if p0.y < self._end_y - 1:  # go down
            p = P(p0.x,p0.y+1)
            self._try_move(p, d, dmap)

    def _try_move(self, p, d, dmap):
        if dmap[p] == None:
            if self._tunnel_map[p] == OPEN_PASSAGE:
                dmap[p] = d
                self._comp_dist(p, dmap)
            else:
                dmap[p] == inf

    def get_steps_to_key(self, key):
        return self._dmap[key.pos]

    def open_door(self, key):
        for p in self._map:
            if p == key.pos:
                #print("remove key")
                self._map[p] = OPEN_PASSAGE
                self._tunnel_map[p] = OPEN_PASSAGE
                #print(p, self._keys)
                self._open_doors.append(key.door)
                del self._keys[p]
                break
        for p in self._map:
            if self._map[p] == key.door:
                #print("remove door")
                self._map[p] = OPEN_PASSAGE
                self._tunnel_map[p] = OPEN_PASSAGE
                break
        self._my_pos = key.pos

def parse_input(input_str):
    global _original_tmap
    _original_tmap = Tmap(input_str)
    reset()

def reset():
    global _min_length
    _min_length = inf

def solve_1():
    return compute_length_of_shortest_paths(_original_tmap)

def compute_length_of_shortest_paths(tmap):
    '''
    - explore all paths
    - for each path, compute its length
    - while exploring a path, abort as soon as its length is longer than the shortest path
    '''
    current_length = 0
    start = time.process_time()
    scan(tmap)
    print("find_reachable_keys - ellapsed time: %f" % _time_find_reachable_keys)
    print("open_door           - ellapsed time: %f" % _time_open_door)
    print(" open_door_clone    - ellapsed time: %f" % _time_open_door_clone)
    print("Total ellapsed time................. %f" % (time.process_time() - start))
    return _min_length

_time_find_reachable_keys = 0.0
_time_open_door = 0.0
_time_find_keys_clone = 0.0
_time_open_door_clone = 0.0
_time_comp_dist = 0.0

def scan(tmap, current_length=0, level=0):
    #print(" "*level, "scan... remaining keys:", len(tmap.keys), " my pos:", tmap._my_pos)
    global _min_length
    global _path
    global _time_find_reachable_keys
    global _time_open_door
    if len(tmap.keys) == 0:
        print("find_reachable_keys - ellapsed time: %f" % _time_find_reachable_keys)
        print(" find_keys_clone    - ellapsed time: %f" % _time_find_keys_clone)
        print(" comp_dist          - ellapsed time: %f" % _time_comp_dist)
        print("open_door           - ellapsed time: %f" % _time_open_door)
        print(" open_door_clone    - ellapsed time: %f" % _time_open_door_clone)
        #print(" "*level, "all doors open", current_length, _min_length)
        if current_length < _min_length:
            _min_length = current_length
            print(" "*level, "!!!!! shortest_path found", _min_length)
        return
    start = time.process_time()
    next_keys = tmap.find_reachable_keys()
    _time_find_reachable_keys += (time.process_time() - start)
    #print(" "*level, "reachable keys:", [k.name for k in next_keys])
    for key in next_keys:
        #print(" "*level, key.pos, key.name)
        n_steps_to_key = tmap.get_steps_to_key(key)
        if n_steps_to_key + current_length < _min_length:
            _path += key.name
            #print(_path)
            current_length += n_steps_to_key
            #print(" "*level, "open door", key.door, current_length)
            start = time.process_time()
            next_tmap = open_door(key, tmap)
            _time_open_door += (time.process_time() - start)
            scan(next_tmap, current_length, level+1)
            _path = _path[:-1]
            #print(_path)
            current_length -= n_steps_to_key

def open_door(key, tmap):
    global _time_open_door_clone
    start = time.process_time()
    next_tmap = Tmap(tmap)
    _time_open_door_clone += (time.process_time() - start)
    next_tmap.open_door(key)
    return next_tmap

def close_door(key, tmap):
    next_tmap = Tmap(tmap)
    next_tmap.close_door(key)
    return next_tmap

def solve_2():
    return 

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
