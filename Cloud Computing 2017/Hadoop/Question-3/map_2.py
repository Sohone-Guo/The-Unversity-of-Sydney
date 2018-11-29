#!/usr/bin/python3

import sys


def tag_mapper():
    """ This mapper select tags and return the tag-owner information.
    Input format: photo_id \t owner \t tags \t date_taken \t place_id \t accuracy
    Output format: tag \t owner
    """
    for line in sys.stdin:
        # Clean input and split it

        parts = line.strip().split("\t")
        if len(parts)==3:
            current_place_url, tags,photo_id = parts[0].strip(), parts[1].strip(),parts[2].strip()
            print(current_place_url+"\t" + tags+ "\t" + photo_id)

if __name__ == "__main__":
    tag_mapper()
