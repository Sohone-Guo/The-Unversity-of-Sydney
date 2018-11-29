#!/usr/bin/python3

import sys


def read_map_output(file):
    """ Return an iterator for key, value pair extracted from file (sys.stdin).
    Input format:  key \t value
    Output format: (key, value)
    """
    for line in file:
        yield line.strip().split("\t")


def tag_reducer():


    data = read_map_output(sys.stdin)

    for number, place, tag_number in data:
        print(place.split(', ')[0] +'\t'+ number+'\t'+ tag_number)

if __name__ == "__main__":
    tag_reducer()
