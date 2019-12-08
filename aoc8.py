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
    layers_data , *ignore = extract_layers(_image_data, width, height)
    l0 = find_layer_with_fewest_n(layers_data, n=0)
    return count_n_m(l0, n=1, m=2)

def extract_layers(image_data, width, height):
    image_size = width * height
    layers_data = list()
    offset = 0
    while offset < len(image_data):
        image_layer = image_data[offset:offset + image_size]
        layers_data.append(image_layer)
        offset += image_size
    layers = list()
    for layer_data in layers_data:
        layer = split_layer(layer_data, width, height)
        layers.append(layer)
    return layers_data, layers

def split_layer(layer_data, width, height):
    layer = list()
    for j in range(height):
        offset = j * width
        layer.append(layer_data[offset:offset + width])
    return layer

def find_layer_with_fewest_n(layers_data, n):
    min_n = +inf
    ln = -1
    i = 0
    for l in layers_data:
        cn = l.count(str(n))
        if cn < min_n:
            min_n = cn
            ln = i
        i += 1
    return layers_data[ln]

def count_n_m(layer_data, n, m):
    return layer_data.count(str(n)) * layer_data.count(str(m))

def solve_2():
    width = 25
    height = 6
    image = decode(_image_data, width, height)
    print_layer(image)
    return 

def decode(image_data, width, height):
    layers_data, layers = extract_layers(_image_data, width, height)
    image_size = width * height
    decoded_image_data = ''
    for pixel in range(image_size):
        color = TRANSPARENT
        for layer_data in layers_data:
            lc = layer_data[pixel]
            if lc != TRANSPARENT:
                image_pixel = lc
                break
        decoded_image_data += image_pixel
    decoded_image = split_layer(decoded_image_data, width, height)
    return decoded_image

def print_layer(layer):
    print('\n'.join(layer))
    printable = ''
    for row in layer:
        printable += row.replace('0', ' ').replace('1', '*') + '\n'
    print()
    print(printable)

########################################################################
# main
########################################################################

if __name__ == '__main__':
    import aocsolver
    aocsolver.AocSolver(day, parse_input, solve_1, solve_2).run()
