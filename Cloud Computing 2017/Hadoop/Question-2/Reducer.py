#!/usr/bin/python3

import sys


def read_map_output(file):
    """ Return an iterator for key, value pair extracted from file (sys.stdin).
    Input format:  key \t value
    Output format: (key, value)
    """
    for line in file:
        yield line.strip().split("\t", 1)


def Reducer():
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
    #total = []
    total = 0
    data = read_map_output(sys.stdin)

    for value, key in data:
        if total <= 50:
            total+=1
            print(key+'\t'+value)
		
		# Check that the input is valid
        #if len(total)<=50:
        #    total.append((key,int(value)))
        #else:
        #    total = sorted(total,key=lambda tup:tup[1],reverse=True)
        #    if int(value)>total[-1][1]:
         #       total[-1] = (key,int(value))
    #for element in total:
     #   print(element[0]+'\t'+str(element[1]))

if __name__ == "__main__":
    Reducer()
