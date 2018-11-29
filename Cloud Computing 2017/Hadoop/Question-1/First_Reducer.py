#!/usr/bin/python3

import sys


def read_map_output(file):
    """ Return an iterator for key, value pair extracted from file (sys.stdin).
    Input format:  key \t value
    Output format: (key, value)
    """
    for line in file:
        yield line.strip().split("\t", 1)


def First_Reducer():
    """ This reducer perform reduce side join
        Input format: place_id#0 \t place_url OR
                      place_id#1 \t user \t date
        Output format: user \t date \t place_url
        """

    data = read_map_output(sys.stdin)

    current_place_id = ""
    current_place_url = "NULL"
    for tp_data in data:
        key = tp_data[0]
        value = tp_data[1]
        # Check that the input is valid
        if key == "":
            continue

        # Recreate the key by splitting using #
        key = key.split('#')

        # Check if the place_id is the same as before
        if key[0] != current_place_id:
            # Check if the key, value pairs come from place.txt (0) or photo (1)
            if key[1] == "0":
                current_place_id = key[0]
                current_place_url = value
            else:
                current_place_id = key[0]
                current_place_url = "NULL"

                print(current_place_url + "\t" + value)
        else:
            print(current_place_url + "\t" + value)

if __name__ == "__main__":
    First_Reducer()
