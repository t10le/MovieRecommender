"""
DATASTRUCTURE:

    {
        u1: {
            m1: 4,
            m2: 3,
            m3: 2,
            m4: 4
        },
        u2: {
            m1: 4,
            m2: 3,
            m3: 2,
            m4: 4
        },
        u3: {
            m1: 4,
            m2: 3,
            m3: 2,
            m4: 4
        }
    }
"""
import csv

def parse_ratings() -> dict:
    csvfile = open('../ml-latest-small/ratings.csv', newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        print(row[0].split(","))

parse_ratings()

