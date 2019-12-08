#!/usr/bin/env python3

########################################################################
# Advent of Code 2019 - solver
#
# Copyright (C) 2019 Antonio Ceballos Roa
########################################################################

day = 8

########################################################################
# Algorithms
########################################################################

from math import inf

TRANSPARENT = '2'
WHITE = '1'
BLACK = '0'

_image_data = None

def parse_input(input_str):
    global _image_data
    _image_data = input_str.strip()
    return _image_data

def solve_1():
    width = 25
    height = 6
    layers = extract_layers(_image_data, width, height)
    l0 = find_layer_with_fewest_n(layers, n=0)
    return count_n_m(l0, n=1, m=2)

def extract_layers(image_data, width, height):
    image_size = width * height
    layers = list()
    offset = 0
    while offset < len(image_data):
        layer = image_data[offset:offset + image_size]
        layers.append(layer)
        offset += image_size
    return layers

def split_layer(layer, width, height):
    layer_rows = list()
    for j in range(height):
        offset = j * width
        layer_rows.append(layer[offset:offset + width])
    return layer_rows

def find_layer_with_fewest_n(layers, n):
    min_n = +inf
    ln = -1
    i = 0
    for layer in layers:
        cn = layer.count(str(n))
        if cn < min_n:
            min_n = cn
            ln = i
        i += 1
    return layers[ln]

def count_n_m(layer, n, m):
    return layer.count(str(n)) * layer.count(str(m))

def solve_2():
    width = 25
    height = 6
    image = decode(_image_data, width, height)
    print_layer(image, width, height)
    return 

def decode(image_data, width, height):
    layers = extract_layers(_image_data, width, height)
    image_size = width * height
    decoded_image = ''
    for pixel in range(image_size):
        color = TRANSPARENT
        for layer in layers:
            lc = layer[pixel]
            if lc != TRANSPARENT:
                image_pixel = lc
                break
        decoded_image += image_pixel
    return decoded_image

def print_layer(layer, width, height):
    layer_rows = split_layer(layer, width, height)
    printable = ''
    for row in layer_rows:
        printable += row.replace('0', ' ').replace('1', '*') + '\n'
    print()
    print(printable)

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
