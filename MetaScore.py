import multiprocessing
import time
import requests
from bs4 import BeautifulSoup
#import Main

''' FIREBASE '''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()



def work(elem):
    start_time = time.time()

    getMetaScore(elem)

    end_time = time.time()


def getMetaScore(elem):
    global urlGame
    global score
    global platf
    global href

    url = 'https://www.metacritic.com/search/all/' + elem + '/results'

    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)

    #f = open("metaScore.txt", "a+", encoding="utf-8")
    doc_ref = db.collection('games').document(elem)

    soup = BeautifulSoup(response.text, 'html.parser')
    search_string = soup.find_all('div', class_='body')

    for p in search_string:
        if p.find('p').text.strip() == 'No search results found.':
            doc_ref.update({
                'Score': 'No existe'
            })
            #f.write('No encontrado en MetaScore' + '\n')
        else:
            platf = 'No definida'
            score = 'No definido'
            try:
                for n in p.find_all('li', class_='result'):
                    href = n.find('a')['href']
                    urlGame = 'https://www.metacritic.com' + href

                    score = n.find('span', class_='metascore_w').text.strip()

                    try:
                        platf = n.find('span', class_='platform').text
                    except:
                        platf = 'No definida'

                    href = n.find('a')['href']
                    urlGame = 'https://www.metacritic.com' + href

                    if score != 'tbd':
                        try:
                            platf = n.find('span', class_='platform').text
                        except:
                            platf = 'No definida'
                        href = n.find('a')['href']
                        urlGame = 'https://www.metacritic.com' + href
                        break

            except:
                unsed = ''

            if score != 'tbd':
                user_agent = {'User-agent': 'Mozilla/5.0'}
                response = requests.get(urlGame, headers=user_agent)

                soup = BeautifulSoup(response.text, 'html.parser')
                score_string = soup.find_all('div', class_=['metascore_summary'])[0].text

                doc_ref.update({
                    'Score': score_string[13:15],
                    'scoreUrl': urlGame
                })
                #f.write(score_string[13:15] + "\n")
            else:
                doc_ref.update({
                    'Score': 'No posee'
                })
                #f.write('No posee' + "\n")

    #f.close()
