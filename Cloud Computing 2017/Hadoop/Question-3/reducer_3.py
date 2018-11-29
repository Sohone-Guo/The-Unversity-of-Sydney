#!/usr/bin/python3

import sys


def read_map_output(file):
    for line in file:
        yield line.strip().split("\t", 1)

def check_repeat(x):
    dic = {}
    for t in x:
        if t[0] not in dic:
            dic[t[0]] = int(t[1])
        else:
            dic[t[0]]+=int(t[1])
    return [(k,str(v)) for k, v in dic.items()]
        

def associate_country():

    data = read_map_output(sys.stdin)
    
    place = ""
    total = ''
    total_list = [] #10top
    for key, value in data:
        # Check that the input is valid
        if key == "":
            continue

        # Recreate the key by splitting using #
        key = key.split('#')

        # Check if the place_id is the same as before
        if key[0] != place:

            # Check if the key, value pairs come from place.txt (0) or photo (1)
            if key[1] == "0":
                for i in total_list:
                    total += "{}={}, ".format(i[0], i[1])
                print(total)
                place = key[0]
                number = value
                total = place + "\t" + number+'\t'
                #print(total)
                total_list = []

        else:
            if key[1] == "1":
                try:
                    if len(total_list)<=10:
                        total_list.append((value.strip().split('\t')[0],value.strip().split('\t')[1]))
                        total_list = check_repeat(total_list)
                        total_list = sorted(total_list, key=lambda x: int(x[1]),reverse=True)
                    else:
                        total_list = sorted(total_list, key=lambda x: int(x[1]),reverse=True)
                        if int(total_list[-1][1])<int(value.strip().split('\t')[1]):
                            total_list[-1] = (value.strip().split('\t')[0],value.strip().split('\t')[1])
                            total_list = check_repeat(total_list)
                        total_list = sorted(total_list, key=lambda x: int(x[1]),reverse=True)
                except Exception as e:
                    print('value is :',e,key, value)
                    pass
    for i in total_list:
        total += "{}={}, ".format(i[0], i[1])
    print(total)

if __name__ == "__main__":
    associate_country()
