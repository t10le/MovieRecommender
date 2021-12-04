import csv
import random


def init_movie_dict(reader: csv.reader) -> dict:
    """Returns a dictionary where each key is the movie genre and its value is the list of
    movieIDs within that genre: {'movieGenre': [1,2,3]}.

    ## Examples
        >>> init_movie_dict(reader)['Comedy']
        [1,2,5,100]

    :param reader: The csv object parsed from a .csv file using csv module.
    """
    movies_by_genre = {'(no genres listed)': [], 'Action': [], 'Adventure': [], 'Animation': [], 'Children': [], 'Comedy': [], 'Crime': [], 'Documentary': [], 'Drama': [
    ], 'Fantasy': [], 'Film-Noir': [], 'Horror': [], 'IMAX': [], 'Musical': [], 'Mystery': [], 'Romance': [], 'Sci-Fi': [], 'Thriller': [], 'War': [], 'Western': []}

    for line in reader:
        for key in movies_by_genre.keys():
            if key in line[-1].split('|'):
                movies_by_genre[key].append(line[0])
    return movies_by_genre


def generate_random_preferences() -> list:
    """Return a list of randomly selected movie genres and their weight preference as a tuple: (MovieGenre, Weight).

    ## Examples
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

    ## Examples
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
    :param movies_by_genre: The dictionary containing a list of movieIds in genre;
        {'Comedy': [93, 6596, 7193, 118930]}
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


with open('../data/movies.csv', newline='') as f:
    reader = csv.reader(f, delimiter=',', quotechar='|')
    next(reader, None)  # Skips header row
    movies = init_movie_dict(reader)

    # Single user
    target_user = {}
    random_genres = generate_random_preferences()
    for tupe in random_genres:
        target_user.update(
            dict(generate_random_movies(tupe[0], tupe[1], 3, movies)))


if __name__ == '__main__':
    # print(generate_random_movies('Comedy', 1, 5, movies))
    # print(generate_random_preferences())
    print(target_user)
