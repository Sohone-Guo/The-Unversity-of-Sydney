#!/usr/bin/python3

import sys


def tag_mapper():
    """ This mapper select tags and return the tag-owner information.
    Input format: photo_id \t owner \t tags \t date_taken \t place_id \t accuracy
    Output format: tag \t owner
    """
    for line in sys.stdin:
        # Clean input and split it
        try:
            parts = line.strip().split("\t")
            if len(parts)==3:
                place, number,tag_number = parts[0].strip(), parts[1].strip(), parts[2].strip()
                #data = [(i.split('=')[0],int(i.split('=')[1])) for i in tag_number.split(', ')]
                #data = sorted(data, key=lambda x: x[1],reverse=True)[:10]
                #tag_number = ', '.join(['='.join(map(str,i)) for i in data])
                print(number + "\t" + place +"\t"+ tag_number)
        except Exception as e:
            print(e)
            break

if __name__ == "__main__":
    tag_mapper()
