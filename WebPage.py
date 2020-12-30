# helloTest.py
# at the end point / call method hello which returns "hello world"
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import time

''' FIREBASE '''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

currentGame = {}

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html', header='Proyecto Paralelismo', sub_header='WebScraping',
                           gameList=getGames(), site_title="WebScraping Project")

@app.route("/game/<name>")
def game(name):
    gameElem = searchGame(name)
    discPlay = gameElem['playDisc']
    discSteam = gameElem['steamDisc']
    if discPlay == '0' or discPlay == 'No existe':
        discPlay = 'No está en Oferta'
    else:
        discPlay = 'Esta en Oferta'

    if discSteam == '0' or discSteam == 'No existe':
        discSteam = 'No está en oferta'
    else:
        discSteam = 'Esta en Oferta'

    return render_template('game.html', header='Proyecto Paralelismo', sub_header='WebScraping',
                           site_title="WebScraping Project", gameName = name, game = gameElem,
                           playD = discPlay, steamD = discSteam, discS=discSteam, discP=discPlay)


#########################################################
#########################################################
@app.route("/gamed", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        name = request.form['name']
        return redirect(url_for("game", name=name))
    else:
        return render_template('game.html', site_title="WebScraping Project")


def validate(elem):
    if elem == 'No está en oferta':
        return False
    else:
        return True
        

def searchGame(name):
    game_ref = db.collection('games').document(name)
    game = game_ref.get().to_dict()
    print(game)
    return game


def getGames():
    gamesList = []
    games_ref = db.collection('games')
    games = games_ref.stream()
    #print(json.dumps(games))

    for game in games:
        #print(json.dumps(game))
        #print('{}'.format(game.to_dict()))
        gamesList.append(game.to_dict())
    #print(gamesList)
    return gamesList

