import csv
import requests

def populate_movie_ids(rated : dict) -> list:
    csvfile = open('../data/movies.csv', newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    presented_movies = []
    for row in reader:
        # line = [movieId,title,genre]
        movieId = row[0].split(",")[0]
        if not movieId.isnumeric():
            continue
        if int(movieId) not in rated.keys():
            presented_movies.append(int(movieId))
        if len(presented_movies) == 9:
            return presented_movies
    return presented_movies

# Returns a list of movieIds mapped from local ID to
# IMDB movie IDS
def populate_movies(movies : list) -> list:
    csvfile = open('../data/links.csv', newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    mapped = []
    for row in reader:
        # line = [movieId,title,genre]
        line = row[0].split(",")[:-1]
        if not line[0].isnumeric():
            continue
        # check if the current read movieId in movies
        if int(line[0]) in movies:
            mapped.append(line[1])
        if len(mapped) == len(movies):
            return mapped
    return mapped 

# Assumes movie list coming in is formmated with IMDB compat IDS
def collect_movie_data(movies : list):
    movie_data = {}
    for movieId in movies:
        url = f"https://imdb-api.com/en/API/Title/k_oe50pt39/tt{movieId}"
        
        response = requests.request("GET", url)
        
        movie_data[movieId] = response.json()

    return movie_data


if __name__ == '__main__':
    movieIds = populate_movie_ids({1:1})
    imdbIds = populate_movies(movieIds)
    print(collect_movie_data(imdbIds))
