import csv
import requests

# build dict with movieId : tmdbId pairs
def build_links() -> dict:
    csvfile = open('../data/links.csv', newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    links = {}
    for row in reader:
        # line = [movieId,imdbId,tmdbId]
        line = row[0].split(",")[::2]
        if not line[0].isnumeric() or not line[1].isnumeric():
            continue
        links[int(line[0])] = int(line[1])
    return links

# Gets a list of 6 movieIds which have not been rated
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
        if len(presented_movies) == 6:
            return presented_movies
    return presented_movies

# Returns a list of sorted movieIds mapped from local ID to
# TMDB movie IDS
def populate_movies(movies : list, links : dict) -> list:
    mapped = []
    for movieId in movies:
        if movieId in links:
            mapped.append(links[movieId])

    return mapped

# Assumes movie list coming in is formmated with IMDB compat IDS
def collect_movie_data(movies : list):
    movie_data = {}
    for movieId in movies:
        url = f"https://api.themoviedb.org/3/movie/{movieId}?api_key=253dbcd7c40a74af299b5c8209a7e797"
        
        response = requests.request("GET", url)
        if "title" in response.json():
            movie_data[movieId] = response.json()

    return movie_data

# Converts a dictionary with rating keys as tmdbIds to
# a dictionary with rating keys as movieIds
# ratings: '710': '4'
def tmdb_to_movieid(ratings : dict) -> dict:
    updated = {}
    csvfile = open('../data/links.csv', newline='')
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

    for row in reader:
        # line = [movieId,imdbId,tmdbId]
        line = row[0].split(",")[::2]
        if not line[0].isnumeric():
            continue
        if line[1] in ratings:
            updated[int(line[0])] = int(ratings[line[1]])
        if len(updated) == len(ratings):
            return updated
    
    return updated



if __name__ == '__main__':
    links = build_links()
    movieIds = populate_movie_ids({})
    tmdbIds = populate_movies(movieIds, links)
    print(tmdbIds)
    # diction = collect_movie_data(tmdbIds)
    # print(diction['8844'])

    # print(tmdb_to_movieid({'710': '4', '949': '4', '9087': '1', '9091': '0', '11860': '2', '45325': '4'}))
