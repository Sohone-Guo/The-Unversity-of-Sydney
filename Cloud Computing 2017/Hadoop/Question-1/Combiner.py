#!/usr/bin/python3

import sys


def read_map_output(file):
    """ Return an iterator for key, value pair extracted from file (sys.stdin).
    Input format:  key \t value
    Output format: (key, value)
    """
    for line in file:
        yield line.split("\t")


def Combiner():
    """ This mapper select tags and return the tag-owner information.

    Note: Unlike normal hadoop which provide the reducer with key and a list of the values
        e.g. tag1, (owner1, owner2...)
    , hadoop streaming instead provide the reducer with sorted (key, value) lines
        e.g. tag1, owner1
             tag1, owner2
             ...

    Furthermore, unlike normal hadoop which calls the reducer for every key,
    in hadoop streaming multiple keys maybe given to the reducer
        e.g. tag1, owner1
             tag1, owner2
             tag2, owner2
             tag2, owner3
             tag3, owner1

    Input format: tag \t owner
    Output format: tag \t {owner=count}
    """

    data = read_map_output(sys.stdin)

    current_place_url = ""
    current_place_number = 0

    for key, value in data:
        # Check that the input is valid
        if key == "":
            continue

        # Check if the place_id is the same as before

        print("{}\t{}".format(key, str(1)))



if __name__ == "__main__":
    Commbiner()
