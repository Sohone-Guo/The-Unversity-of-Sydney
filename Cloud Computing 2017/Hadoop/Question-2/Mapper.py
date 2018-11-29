#!/usr/bin/python3

import sys


def Mapper():
    """ This mapper select tags and return the tag-owner information.
    Input format: photo_id \t owner \t tags \t date_taken \t place_id \t accuracy
    Output format: tag \t owner
    """
    for line in sys.stdin:
        # Clean input and split it
        parts = line.strip().split("\t")
        if len(parts)==2:
            current_place_url, value = parts[0].strip(), parts[1].strip()
            print(value + "\t" + current_place_url)

if __name__ == "__main__":
    Mapper()
