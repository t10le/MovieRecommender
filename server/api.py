from os import link
import time
from flask import Flask, request
from indexer import *
from signin import *
from tmdb import *

app = Flask(__name__)

# User Specific Data
user_ratings = {}
user_name = ""
password = ""
recommendations = {}
links = {}

db = {}

@app.route('/')
def index():
    return "This is the server index file"

@app.route('/usr-rated', methods=['POST'])
def post_user_rates():
    ratings = request.get_json()
    global user_ratings, recommendations
    user_ratings.update(tmdb_to_movieid(ratings)) #update ratings dict
    update_ratings(user_name, password, user_ratings) # write ratings
    # Run Rating System
    try:
        similar_users = find_sim(user_ratings, db)
        n_movies = find_similar_movies(similar_users,db,user_ratings)
        recommendations = compute_movie_recommendation(n_movies, similar_users, db)
        return {"status" : "success"}
    except:
        return {"status" : "failed"}

@app.route('/signin', methods=['POST'])
def get_signin_data():
    so_data = request.get_json()
    success = sign_in(so_data["userName"], so_data["password"])
    if success is not False:
        global user_ratings, db, user_name, password, recommendations
        user_name = so_data["userName"]
        password = so_data["password"]
        user_ratings = success
        db = parse_ratings('../data/ratings.csv')
        recommendations = {}
        return {"status" : "success"}
    return {"status" : "failed"}

@app.route('/register', methods=['POST'])
def get_register_user():
    register_data = request.get_json()
    success = register_user(register_data["userName"], register_data["password"])
    if success is not False:
        global user_ratings, db, user_name, password, recommendations
        user_name = register_data["userName"]
        password = register_data["password"]
        user_ratings = success
        db = parse_ratings('../data/ratings.csv')
        recommendations = {}
        return {"status" : "success"}

    return {"status" : "failed"}

@app.route('/movies', methods=['GET'])
def get_movies():
    global links
    if not len(links.keys()) > 0:
        links = build_links()
    movieIds = populate_movie_ids(user_ratings)
    imdbIds = populate_movies(movieIds, links)
    
    return { 'movies' : collect_movie_data(imdbIds) }

@app.route('/usr-recommended', methods=['GET'])
def get_recommended_movie_data():
    global recommendations
    if recommendations == {}:
        # Run Rating System
        try:
            similar_users = find_sim(user_ratings, db)
            n_movies = find_similar_movies(similar_users,db,user_ratings)
            recommendations = compute_movie_recommendation(n_movies, similar_users, db)
        except:
            return {"status" : "failed"}
    tmdbIds = populate_movies(list(recommendations.keys()), links)
    return { 'movies' : collect_movie_data(tmdbIds) }

@app.route('/usr-info')
def get_user_info():
    return { "user_name": user_name }





