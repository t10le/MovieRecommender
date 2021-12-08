from typing import *
import math
import csv

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


def parse_ratings(csv_name: str):
    csvfile = open(csv_name, newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    database = {}

    next(reader, None)  # Skips header row
    for row in reader:
        # line = [userId,movieId,rating]
        line = row[0].split(",")[:-1]

        userId = int(line[0])
        movieId = int(line[1])
        rating = float(line[2])

        # Create new user in database with its value as the movie/rating
        if userId not in database.keys():
            database[userId] = {movieId: rating}

        # Update the userId with the related movie and rating
        else:
            database[userId][movieId] = rating

    csvfile.close()
    return database


def intersect(x: dict, y: dict) -> list:
    """
    Returns the intersection between two user movie recommendations have at least
    one common movie rated.
    """
    return list(set(x.keys()) & set(y.keys()))


def union(x: list, y: dict) -> list:
    """
    Returns the union between two user movie recommendations
    x: List of similar movies
    y: Dictionary of user ratings
    """
    return list(set(x) | set(y.keys()))

# user_input : {m1 : 1, m2: 2, m3: 3}
# This function will iterate through database and find user matches
# Returns a dict of similar users: {u1: sim_value, u2: sim_value}


def find_sim(user_input: dict, database: dict) -> dict:
    similar_users = {}
    for user in database.keys():
        check_intersect = intersect(user_input, database[user])
        if check_intersect != []:
            sim = calc_sim(user_input, database[user], check_intersect)
            if sim > 0:
                similar_users[user] = sim

    return similar_users

# x and y have form: {m1 : 1, m2: 2, m3: 3}


def calc_sim(user_in: dict, b: dict, intersect: list) -> float:
    usr_avg = 0
    b_avg = 0
    n = len(intersect)

    for sim_movie in intersect:
        usr_avg += user_in[sim_movie]
        b_avg += b[sim_movie]

    # calculated average
    usr_avg = usr_avg / n
    b_avg = b_avg / n

    sim = 0
    denominator1 = 0  # sum of user_in rating squared
    denominator2 = 0  # sum of user b rating squared
    for sim_movie in intersect:
        sim += (user_in[sim_movie] - usr_avg)*(b[sim_movie] - b_avg)
        denominator1 += ((user_in[sim_movie] - usr_avg) ** 2)
        denominator2 += ((b[sim_movie] - b_avg) ** 2)

    if sim <= 0:
        return 0

    return sim / math.sqrt(denominator1 * denominator2)

# Uses the similar_users dictionary to find all the movies
# rated by any of the similar users


def find_similar_movies(similar_users: dict, database: dict, user_in: dict) -> list:
    sim_movies = []
    # build list of all movies that similar user have rated and input user has not
    for user in similar_users.keys():
        user_rated_movies = database[user]
        sim_movies = union(sim_movies, user_rated_movies)

    return [x for x in sim_movies if x not in user_in.keys()]


def compute_movie_recommendation(n_movies: list, similar_users: dict, database: dict):
    """
    Returns a dictionary of estimated movie rating for any movie that the main user has
    not rated yet, based on the set of similar user ratings for that specific movie.
    n_movies:       [3, 6, 7, 8, 10]
    similar_users:  {u1: sim_value, u2: sim_value}
    database:       {u1: {
                        m1: 4,
                        m2: 3,
                        m3: 2,
                        m4: 4
                }}
    """

    movie_recommend = {}
    for movieId in n_movies:
        rating = compute_aggregate(similar_users, database, movieId)
        # Remove zero rated movies
        if rating > 0:
            # populate dict of recommended movies for user_in
            movie_recommend[movieId] = rating

    return get_top_recommended(movie_recommend, 20)


def compute_aggregate(similar_users: dict, database: dict, movieId: int) -> float:
    # get list of userId's who are in similar_users and have rated movieId
    valid_raters = [userId for userId in similar_users.keys(
    ) if movieId in database[userId].keys()]

    # Threshold filtering
    if len(valid_raters) < 2:
        return 0.0

    num = 0
    den = 0

    for userId in valid_raters:
        num += (similar_users[userId] * database[userId][movieId])
        den += similar_users[userId]

    if den > 0:
        return num / den

    return 0.0


def get_top_recommended(recommendations: dict, n: int):
    top_n = sorted(recommendations.items(),
                   key=lambda item: item[1], reverse=True)[:n]
    return dict(top_n)


if __name__ == '__main__':
    database = parse_ratings('../data/ratings.csv')
    user_in = {114709: 2, 4262: 4, 50872: 2,
               6537: 5, 158872: 3, 6365: 4}  # User's movie
    user_in = {1: 4, 2: 4, 3: 2, 4: 4, 5: 2, 6: 2}
    similar_users = find_sim(user_in, database)
    print(similar_users)
    n_movies = find_similar_movies(similar_users, database, user_in)
    recommendations = compute_movie_recommendation(
        n_movies, similar_users, database)
    index = 1
    for movie in recommendations.keys():
        print(
            f"Rank: {index}, Movie: {movie}, Rating: {recommendations[movie]}")
        index += 1
