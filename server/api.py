import time
from flask import Flask, request
from indexer import *
from signin import *
from imdb import *

app = Flask(__name__)

# User Specific Data
global user_ratings
user_ratings = {}
global db

@app.route('/')
def index():
    return "This is the server index file"

@app.route('/usr-rated', methods=['POST'])
def post_user_rates():
    ratings = request.get_json()
    print(ratings)
    return {"status" : "success"}

@app.route('/signin', methods=['POST'])
def get_signin_data():
    so_data = request.get_json()
    success = sign_in(so_data["userName"], so_data["password"])
    print(success)
    if success is not False:
        global user_ratings, db
        user_ratings = success
        db = parse_ratings('../data/ratings.csv')
        return {"status" : "success"}
    return {"status" : "failed"}

@app.route('/register', methods=['POST'])
def get_register_user():
    register_data = request.get_json()
    success = register_user(register_data["userName"], register_data["password"])
    if success is not False:
        global user_ratings, db
        user_ratings = success
        db = parse_ratings('../data/ratings.csv')
        return {"status" : "success"}

    return {"status" : "failed"}

@app.route('/movies', methods=['GET'])
def get_movies():
    movieIds = populate_movie_ids(user_ratings)
    imdbIds = populate_movies(movieIds)
    
    return { 'movies' : collect_movie_data(imdbIds)}






