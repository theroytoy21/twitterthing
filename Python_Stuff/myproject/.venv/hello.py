from flask import Flask, render_template
from user_lookup import *
from make_tweets import *
import datetime
from get_tweets_with_bearer_token import *
from sk_test import something, something_else, something_new
from something import *
from firebase_admin import credentials, initialize_app, firestore
import json
# html templates under 'template' folder
app = Flask(__name__)

cred = credentials.Certificate("fbkey.json")
initialize_app(cred, {'storageBucket': 'pizza-41ca7.appspot.com'})
db = firestore.client()

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/test")
def smile():
    return mainfunction()

@app.route('/post/<int:id>')
def show_id(id):
    return f'The id is {id}'

@app.route('/second_page')
def second_page():
    return render_template("index2.html", message = datetime.datetime.today())

@app.route('/prediction')
def prediction():
    myList = predictions()
    num_pos = 0
    num_neg = 0
    for x in myList:
        if int(x) == 0:
            num_neg += 1
        else:
            num_pos += 1
    print('Positive:', num_pos,'| Negative:', num_neg)

    data = {"Number of positive predictions": num_pos,
            "Number of negative predictions": num_neg}
    
    db.collection("output").document("Polarity").set(data)
    return 'hi'

# @app.route("/lookup")
# def lookup_page():
#     return lookup()

# @app.route("/tweet")
# def tweet_page():
#     return tweet()

# 1. make sure in the right file
# 2. .venv/Scripts/activate (sets up ve)
# 3. flask --app hello(name of file) run (runs the server)
# 4. deactivate (turns off ve)

