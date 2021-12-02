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

    return database

parse_ratings()

