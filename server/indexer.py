from typing import *
import math
import csv


def parse_ratings(csv_name: str) -> dict:
    """Returns a dictionary containing {UserID: {MovieID: Rating}}.
    Note that each userID is a sub-dictionary containing their selection
    of movieIDs and their relative rating.

    ## Example
        >>> parse_ratings('../data/ratings.csv')
        {605: {1: 4.0, 2: 3.5, 28: 4.0, 73: 3.0, ...}
        # Return output is too long for example, hence (...)

    ## Data Structure
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

    :param csv_name: The CSV object loaded from ratings.csv
    """
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
    Returns the intersection between target user and another potentially 
    similar user's movie recommendations that have at least one common 
    movie rated.

    ## Example
        >>> intersect({1:5, 40: 2}, {40: 3, 2:0, 1337: 5})
        [40]

    :param x: Dictionary of movieIDs and user ratings {MovieID: Rating}.
    :param y: Dictionary of movieIDs and user ratings {MovieID: Rating}.
    """
    return list(set(x.keys()) & set(y.keys()))


def union(x: list, y: dict) -> list:
    """
    Returns the union between two user movie recommendations.

    ## Example
        >>> union([1,2,3], {1:2, 4:4, 69:0})
        [1, 2, 3, 4, 69]

    :param x: List of similar movieIDs.
    :param y: Dictionary of movieIDs and user ratings {MovieID: Rating}.
    """
    return list(set(x) | set(y.keys()))


def find_sim(user_input: dict, database: dict) -> dict:
    """Returns the similarity matrix or vector containing only the
    similar users to target user profile with similarity scores greater
    than 0.

    ## Example
        >>> find_sim({114709: 2, 4262: 4, 50872: 2,
            6537: 5, 158872: 3, 6365: 4}, parse_ratings('../data/ratings.csv'))
        {15: 1.0, 18: 0.49999999999999994, 28: 1.0, 103: 1.0, 200: 1.0, 210: 1.0, 
        298: 0.9449111825230682, 354: 0.24019223070763066, 365: 1.0, 380: 0.5, 
        438: 1.0, 452: 1.0, 489: 1.0, 561: 0.05263157894736842}

    :param user_input: The user's selection of userIDs and their similarity score relative
    to the target user. 
    :param database: The MovieLens database containing other user profiles with their 
    relative selection of movieIDs and relative ratings {MovieID: Rating}.
    """
    similar_users = {}
    for user in database.keys():
        check_intersect = intersect(user_input, database[user])
        if check_intersect != []:
            sim = calc_sim(user_input, database[user], check_intersect)
            if sim > 0:
                similar_users[user] = sim

    return similar_users


def calc_sim(user_in: dict, b: dict, intersect: list) -> float:
    """Returns the similarity score between the target user and another user
    based on their user profiles containing their choice of movieIDs and ratings
    in the form of {MovieID: Rating}.

    ## Example
        >>> calc_sim({1: 3, 2: 0, 55: 0}, {1:5, 55:3}, [1, 55])
        1.0

    :param user_in: The target user profile for their selection of movieIDs and
    relative ratings {MovieID: Rating}.
    :param b: Another user profile different from target user containing their 
    selection of movie IDs and relative ratings {MovieID: Rating}.
    :param intersect: The intersection of movieIDs between target user and
    another user.
    """
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


def find_similar_movies(similar_users: dict, database: dict, user_in: dict) -> list:
    """Returns a list of similar movieIDs based the union between the target user 
    choice of movieIDs and other similar user's choice of movieIDs.

    ## Example
        >>> find_similar_movies({1: [2, 34, 55], 2: [2, 44]}, parse_ratings('../data/ratings.csv'), {2: 2, 35: 5})
        [1024, 1, 1025, 3, 2048, 1029, 6, 1030, ...]
        # Return output is too long, hence (...)

    :param similar_users: The dictionary of similar user profiles {UserID: [MovieID]}.
    :param database: The MovieLens database {UserID: {MovieID: Rating}}. 
    :param user_in: The target user profile {MovieID: Rating}.
    """
    sim_movies = []
    # build list of all movies that similar user have rated and input user has not
    for user in similar_users.keys():
        user_rated_movies = database[user]
        sim_movies = union(sim_movies, user_rated_movies)

    return [x for x in sim_movies if x not in user_in.keys()]


def compute_movie_recommendation(n_movies: list, similar_users: dict, database: dict):
    """Returns a dictionary of estimated movie rating for any movie that the main user 
    has not rated yet, based on the set of similar user ratings for that specific movie.

    ## Example
        >>> compute_movie_recommendation([3,6,7,10], {55: 1.0, 4: 2.4}, parse_ratings('../data/ratings.csv'))
        {123: 3.0, 69: 5.0}

    :param n_movies: The list of similar movieIDs [MovieID].
    :param similar_users: The dictionary of similar user profiles {UserID: [MovieID]}.
    :param database: The MovieLens database {UserID: {MovieID: Rating}}.  
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
    """Returns the computed aggregate weighted-sum function given the similar user's
    similarity score and their ratings per movieID for a movieID that the target user
    has yet to rate.

    ## Example
        >>> compute_aggregate({15: 1.0, 18: 0.49999999999999994, 28: 1.0, 103: 1.0, 200: 1.0}
        , parse_ratings('../data/ratings.csv'), 18)
        0.0

    :param similar_users: The dictionary of similar user profiles {UserID: [MovieID]}.
    :param database: The MovieLens database {UserID: {MovieID: Rating}}.  
    :param movieId: The movieID as an integer between 1 and 193609.
    """
    # get list of userId's who are in similar_users and have rated movieId
    valid_raters = [userId for userId in similar_users.keys(
    ) if movieId in database[userId].keys()]

    # Threshold filtering
    K = 2
    if len(valid_raters) < K:
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
    """Returns the top 20 movieIDs and their rating sorted in descending order.

    ## Example
        >>> get_top_recommended({123: 3.0, 69: 5.0}, 20)
        {69: 5.0, 123: 3.0}

    :param recommendations: The dictionary of recommended movieIDs and their relative rating
    {MovieID: Rating}.
    """
    top_n = sorted(recommendations.items(),
                   key=lambda item: item[1], reverse=True)[:n]
    return dict(top_n)


if __name__ == '__main__':
    database = parse_ratings('../data/ratings.csv')
    user_in = {114709: 2, 4262: 4, 50872: 2,
               6537: 5, 158872: 3, 6365: 4}  # User's movie
    # user_in = {1: 4, 2: 4, 3: 2, 4: 4, 5: 2, 6: 2}
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
