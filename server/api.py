import time
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return "This is the server index file"

@app.route('/time')
def get_current_time():
    return {'time' : time.time()}

@app.route('/usr-rated', methods=['POST'])
def post_user_rates():
    ratings = request.get_json()
    print(ratings)
    return {"status" : "success"}




