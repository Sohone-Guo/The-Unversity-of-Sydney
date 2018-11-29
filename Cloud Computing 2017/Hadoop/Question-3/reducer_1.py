#!/usr/bin/python3

import sys
import re 


def read_map_output(file):
    """ Return an iterator for key, value pair extracted from file (sys.stdin).
    Input format:  key \t value
    Output format: (key, value)
    """
    for line in file:
        yield line.strip().split("\t", 1)


def associate_country():

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
            try:
                # if parent place or year in the tags
                tag = value.split('\t')[0].lower()
                # first if years in the tags:
                if len(re.findall('[0-9]{4}',tag)) == 0:
                    name = current_place_url.lower().replace(" ", "").strip().split(',')
                    name_little =[] 
                    k = [name_little.extend(i.split(' ')) for i in current_place_url.lower().split(', ')]
                    if tag not in name and tag not in name_little:
                        print(current_place_url + "\t" + value)
            except Exception as e:
                print(e)
                break
        
if __name__ == "__main__":
    associate_country()
