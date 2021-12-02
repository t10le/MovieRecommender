from typing import *

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




def parse_ratings():
    csvfile = open('/Users/tomtom/Desktop/FinalProject/ml-latest-small/sample.csv', newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    global database
    database = {}
    for row in reader:
        # line = [userId,movieId,rating]
        line = row[0].split(",")[:-1]

        # Skip the first line of the CSV
        if not line[0].isnumeric():
            continue

        userId = int(line[0])
        movieId = int(line[1])
        rating = float(line[2])

        # Create new user in database with its value as the movie/rating
        if userId not in database.keys():
            database[userId] = { movieId : rating }

        # Update the userId with the related movie and rating
        else:
            database[userId][movieId] = rating

def intersect(x:dict,y:dict) -> bool:
    """
    Returns the intersection between two user movie recommendations have at least
    one common movie rated.
    """
    return list(set(x.keys()) & set(y.keys()))

# user_input : {m1 : 1, m2: 2, m3: 3}
# This function will iterate through database and find user matches
# Returns a list of similar users
def find_sim(user_input: dict) -> list:
    
    for user in database.keys():
        check_intersect = intersect(list(user_input), list(database[user]))
        if check_intersect != []:
            calc_sim(user_input, database[user],check_intersect)
    
# x and y have form: {m1 : 1, m2: 2, m3: 3}
def calc_sim(user_in : dict, b : dict, intersect : list):
    pass
    
parse_ratings()
print(intersect({'a':2}, {'z':2, 'b':3}))

