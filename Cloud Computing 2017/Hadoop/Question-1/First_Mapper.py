#!/usr/bin/python3

import sys

def First_Mapper():
    """ This mapper will output different format dependind on input type
    Input format: place_id \t woeid \t latitude \t longitude \t place_name \t place_type_id \t place_url OR
                  photo_id \t owner \t tags \t date_taken \t place_id \t accuracy
    Output format: place_id#0 \t place_url OR
                   place_id#1 \t user \t date
    """
    for line in sys.stdin:
        # Clean input and split it
        parts = line.strip().split("\t")

        # Check that the line is of the correct format

        if len(parts) == 7:  # The line comes from place.txt
            if int(parts[5].strip())==7:
                print(parts[0].strip() + "#0\t" + ', '.join(parts[4].strip().split(', ')))
				#place_id and locality
            elif int(parts[5].strip())==22:
                print(parts[0].strip() + "#0\t" + ', '.join(parts[4].strip().split(', ')[1:]))
				#place_id and neighbourhood to locality
        elif len(parts) == 6:  # The line comes n0*.txt
            photo_id, place_id = parts[0].strip(), parts[4].strip()
            print(place_id + "#1\t" + photo_id)

if __name__ == "__main__":
    First_Mapper()
