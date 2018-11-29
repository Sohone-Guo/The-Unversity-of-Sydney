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
    current_place_url = ""
    tag_number = 0
    tag_count=[]
    for it in data:
        locals = it[0].strip()
        tags = it[1].strip()
        photo_id = it[2].strip()

    # Check that the input is valid
        if locals == "":
            continue
        key = '__'.join([locals,tags])

        if key != current_place_url:
            print('\t'.join(current_place_url.split('__'))+'\t'+str(tag_number))
            current_place_url = key
            tag_number = 1

        else:
            tag_number+=1



if __name__ == "__main__":
    tag_reducer()
