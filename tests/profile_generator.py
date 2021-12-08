import csv
import random
import ast
from indexerTestVersion import *


def init_movie_dict(reader: csv.reader) -> dict:
    """Returns a dictionary where each key is the movie genre and its value is the list of
    movieIDs within that genre: {'movieGenre': [1,2,3]}.

    # Examples
        >>> init_movie_dict(reader)['Comedy']
        [1,2,5,100]

    :param reader: The csv object parsed from a .csv file using csv module.
    """
    movies_by_genre = {'(no genres listed)': [], 'Action': [], 'Adventure': [], 'Animation': [], 'Children': [], 'Comedy': [], 'Crime': [], 'Documentary': [], 'Drama': [
    ], 'Fantasy': [], 'Film-Noir': [], 'Horror': [], 'IMAX': [], 'Musical': [], 'Mystery': [], 'Romance': [], 'Sci-Fi': [], 'Thriller': [], 'War': [], 'Western': []}

    global movie_lookup
    movie_lookup = {}

    for line in reader:
        movie_lookup[int(line[0])] = line[-1].split('|')
        for key in movies_by_genre.keys():
            if key in line[-1].split('|'):
                movies_by_genre[key].append(line[0])
    return movies_by_genre


def generate_random_preferences() -> list:
    """Return a list of randomly selected movie genres and their weight preference as a tuple: (MovieGenre, Weight).

    # Examples
        >>> generate_random_preferences()
        [('Fantasy', 1), ('Animation', 0), ('Film-Noir', 1), ('Action', 0), ('Adventure', 0),
        ('Thriller', 0), ('Romance', 1), ('Mystery', -1), ('Crime', 0), ('War', 0), ('Children', 1), ('Musical', -1)]
        >>> generate_random_preferences()
        [('Crime', -1), ('Romance', 0), ('Action', 1)]
    """
    # Hard-coded list of genres for better speed to avoid parsing/retrieval for our specific use case.
    genres = ['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama',
              'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

    # == Weight Criteria ==
    #   -1  -> User hates this genre.
    #    0  -> User is neutral for this genre.
    #    1  -> User loves this genre.

    return [(genre, random.randrange(-1, 2))
            for genre in random.sample(genres, k=random.randrange(1, 20))]


def generate_random_movies(genre: str, weight: int, M: int, movies_by_genre: dict) -> list:
    """Return a list of randomly selected movieIds and their ratings as a tuple based on target user weight
    score to represent their preference of genre(s). The count and selection of movies and ratings are
    random, but constrained to selection input 'genre' and upperbound limit input 'm' for max count.

    # Examples
        >>> generate_random_movies('Comedy', 1, 5, movies)
        [(6548, 4), (5074, 5), (1010, 5), (2973, 4)]
        >>> generate_random_movies('Comedy', 0, 5, movies)
        [(26152, 3), (2458, 2), (1261, 2)]
        >>> generate_random_movies('Comedy', -1, 5, movies)
        [(4782, 1)]
        >>> generate_random_movies('Comedy', -1, 5, movies)
        [(7247, 1), (120807, 1), (4204, 1), (8464, 1), (122, 0)]

    :param genre: Selects which key as movie genre set from dictionary to retrieve movies from.
    :param weight: Pick -1, 0 or 1 for user weight or preference of a movie genre.
    :param M: The upperbound limit for how many movies to randomly select from movie genre set.
    :param movies_by_genre: The dictionary containing a list of movieIds in genre
    {'Comedy': [93, 6596, 7193, 118930]}.
    """
    # == Weight Criteria ==
    #   -1  -> User hates this genre.
    #    0  -> User is neutral for this genre.
    #    1  -> User loves this genre.
    score = (4, 6)
    if weight == -1:
        score = (0, 2)
    elif weight == 0:
        score = (2, 4)

    return [(int(movie), random.randrange(score[0], score[1])) for movie in random.sample(movies_by_genre[genre], k=random.randrange(1, M+1))]


def create_user_profile(M: int, rand_genres: list, movies_by_genre: dict) -> dict:
    """Returns a single dictionary containing the target user's movies and their respective rating: {movieID, rating}.

    # Examples
        >>> create_user_profile(3, [('Crime', -1), ('Romance', 0), ('Action', 1)], init_movie_dict(reader))
        {175569: 1, 143559: 0, 165347: 0, 3102: 2,
            4584: 3, 100527: 2, 76743: 5, 122882: 4}

    :param M: The upperbound limit for how many movies to randomly select from movie genre set.
    :param rand_genres: The list of tuples containing randomly selected genres and their random weight preference
    [('Comedy', 1), ('Action', -1)].
    :param movies_by_genre: The dictionary containing a list of movieIds in genre
    {'Comedy': [93, 6596, 7193, 118930]}.
    """
    target_user = {}
    for tupe in rand_genres:
        target_user.update(
            dict(generate_random_movies(tupe[0], tupe[1], M, movies_by_genre)))

    # Embedded genre preference(s) for later retrieval for unittest.
    target_user['metadata'] = rand_genres
    return target_user


def generate_user_profiles(N: int, M: int, movies_by_genre: dict) -> dict:
    """
    # Examples
        >>> generate_user_profiles(1, 3, init_movie_dict(reader))
        {
            0: {714: 1, 8491: 0, 102802: 0, 55844: 1, 7707: 1, 937: 1, 7317: 3, 4772: 3, 764: 2,
            81562: 3, 86781: 2, 4978: 3},
            1: {2727: 2, 4298: 3, 2066: 3, 68159: 3, 2389: 2, 2712: 2}
        }
    :param N: The total number of user profiles to generate.
    :param M: The upperbound limit for how many movies to randomly select from movie genre set.
    :param moves_by_genre: The dictionary containing a list of movieIds in genre
    {'Comedy': [93, 6596, 7193, 118930]}.
    """
    user_profiles = {}
    for user in range(N):
        user_profiles[user] = create_user_profile(
            M, generate_random_preferences(), movies_by_genre)
    return user_profiles


def extract_preferences(preferences: list):
    hate = []
    neutral = []
    love = []
    for tupe in preferences:
        if tupe[1] == -1:
            hate.append(tupe[0])
        elif tupe[1] == 0:
            neutral.append(tupe[0])
        else:
            love.append(tupe[0])
    return (hate, neutral, love)


def generate_recom(users, database):
    shallowCopy_users = dict(users)
    del shallowCopy_users['metadata']
    # print(shallowCopy_users)

    similar_users = find_sim(shallowCopy_users, database)
    n_movies = find_similar_movies(similar_users, database, shallowCopy_users)
    recommendations = compute_movie_recommendation(
        n_movies, similar_users, database)

    return recommendations


def verify_stats(movie_recom: dict, target_user_pref: tuple) -> bool:
    """

    (199, 4.993644307214528)
    (1041, 4.993644307214528)
    (1354, 4.993644307214528)
    (3153, 4.987302636123428)
    (26133, 4.995180595739994)

    :param movie_recom:
    {85: 5.0, 194: 5.0, 5833: 5.0, 78836: 5.0, 26133: 4.995180595739994, 199: 4.993644307214528,
    1041: 4.993644307214528, 1354: 4.993644307214528, 3153: 4.987302636123428, 232: 4.9872886144290565,
    2935: 4.9872886144290565, 3341: 4.9872886144290565, 3475: 4.9872886144290565, 1939: 4.985541787219979,
    5279: 4.985541787219979, 947: 4.980932921643585, 2936: 4.980932921643585, 4419: 4.980932921643585,
    4432: 4.980932921643585, 4433: 4.980932921643585}
    """
    points = 0
    # print(f'This user likes {target_user_pref[2]}')
    for movie in movie_recom.items():
        print(
            f'movieID: {movie[0]}\t EstimatedScore: {movie[1]} \tgenre: {movie_lookup[movie[0]]}')
        if 4 <= movie[1] <= 5 and set(movie_lookup[movie[0]]) & set(target_user_pref[2]):
            points += 1
    # print(len(movie_recom))
    # print(points)
    if points == len(movie_recom):
        return True
    return False


with open('../data/movies.csv', newline='') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    next(reader, None)  # Skips header row
    movies = init_movie_dict(reader)

with open('_userprofiles.txt', 'r') as f:
    users_cache = ast.literal_eval(f.read())

if __name__ == '__main__':
    database = parse_ratings('../data/ratings.csv')

    # Single user check
    userID = 1
    user_preRated = {118894: 2, 95163: 3, 953: 2, 709: 3, 2034: 2, 45431: 2, 6170: 3, 104141: 3,
                     97225: 2, 8535: 3, 3679: 2, 95307: 3, 3086: 3, 1083: 2, 6911: 3, 1035: 2, 2612: 1,
                     3435: 1, 999: 0, 25865: 1, 8236: 0, 1260: 0, 89753: 0, 6515: 0, 48997: 1, 2166: 1,
                     4306: 1, 134853: 1, 65577: 0, 66240: 0, 47404: 1, 5768: 0, 44238: 0, 31150: 1, 829: 0,
                     107408: 0, 7706: 0, 2261: 0, 2395: 1, 1907: 1, 44972: 0, 6252: 0, 77191: 1, 103483: 4,
                     76030: 4, 53280: 5, 66310: 4, 73488: 5}

    # Tuple: (MovieID_Ratings, ListOfPreferences)
    user_1 = (generate_recom(users_cache[userID], database), extract_preferences(
        users_cache[userID]['metadata']))

    movie_suggestions = user_1[0]
    movie_preference = user_1[1]
    print(f'TARGET USER PROFILE: \n{users_cache[userID]}\n\n')
    print(f'TARGET USER TOP20: \n{movie_suggestions}\n\n')
    print(f'TARGET USER PREF: \n{movie_preference}\n\n')

    print(verify_stats(movie_suggestions, movie_preference))
