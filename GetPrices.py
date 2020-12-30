from multiprocessing import Process
import time
import requests
from bs4 import BeautifulSoup

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

    p1 = Process(target=getSteamPrices(elem))
    p2 = Process(target=getPlayStationPrices(elem))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    end_time = time.time()


def getSteamPrices(elem):
    url = 'https://store.steampowered.com/search/?term=' + elem

    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)

    #f = open("pricesSteam.txt", "a+", encoding="utf-8")
    #f2 = open("discountSteam.txt", "a+", encoding="utf-8")
    doc_ref = db.collection('games').document(elem)

    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find(id='search_resultsRows')

    first_elem = results.find('a', class_='search_result_row', href=True)
    discount = first_elem.find('div', class_='search_discount')
    price = first_elem.find('div', class_='search_price')
    urlGame = first_elem['href']
    #print(urlGame)

    ''' URL IMAGE'''
    res = requests.get(urlGame, headers=user_agent)
    soupImage = BeautifulSoup(res.content, 'html.parser')
    try:
        resul = soupImage.find('img', class_='game_header_image_full')
        imageUrl = resul['src']
    except:
        try:
            resulDiv = soupImage.find('div', class_='img_ctn')
            imageUrl = resulDiv.find('img')['src']
        # print(imageUrl)
        except:
            imageUrl = ''


    doc_ref.update({
        'steamUrlGame': urlGame,
        'steamUrlImage': imageUrl,
        'steamPrice': str(price.text.strip())
    })
    #f.write(str(price.text.strip()) + '\n')

    if discount.text.strip() == '':
        doc_ref.update({
            'steamDisc': str(0)
        })
        #f2.write(str(0) + '\n')
    else:
        doc_ref.update({
            'steamDisc': str(discount.text.strip())
        })
        #f2.write(str(discount.text.strip()) + '\n')

    #f.close()
    #f2.close()


def getPlayStationPrices(elem):
    global price
    global discount
    global cont

    url = 'https://store.playstation.com/es-cr/grid/search-game/1?direction=asc&query=' + elem + '&sort=release_date'

    user_agent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=user_agent)

    #f = open("pricesPlayS.txt", "a+", encoding="utf-8")
    #f2 = open("discountPlayS.txt", "a+", encoding="utf-8")
    doc_ref = db.collection('games').document(elem)

    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', class_='grid-cell-container')
    urlGame = ''

    for n in results:
        game = n.find_all('div', class_='grid-cell__body')
        cont = 0
        for g in game:
            text = g.find_all('span')
            for t in text:
                if t.text.strip() == elem:
                    try:
                        cont += 1
                        urlGame = g.find('a', class_='internal-app-link', href=True)['href']
                        price = g.find('h3', class_='price-display__price').text.strip()
                        doc_ref.update({
                            'playPrice': str(price),
                            'playUrlGame': 'https://store.playstation.com' + urlGame
                        })
                        #f.write(str(price) + '\n')

                        try:
                            discount = g.find('div', class_='price').text.strip()
                        except:
                            discount = 0

                        doc_ref.update({
                            'playDisc': str(discount)
                        })
                        #f2.write(str(discount) + '\n')

                    except:
                        doc_ref.update({
                            'playPrice': 'No existe',
                            'playDisc': 'No existe'
                        })
                        #f.write('No existe' + '\n')
                        #f2.write('No existe' + '\n')
                    break


        res = n.find('div', class_='grid-cell__body')
        if cont == 0:
            try:
                price = res.find('h3', class_='price-display__price').text.strip()
                urlGame = res.find('a', class_='internal-app-link', href=True)['href']
                doc_ref.update({
                    'playPrice': str(price),
                    'playUrlGame': 'https://store.playstation.com/' + urlGame
                })
                #f.write(str(price) + '\n')
                try:
                    discount = res.find('div', class_='price').text.strip()
                except:
                    discount = 0

                doc_ref.update({
                    'playDisc': str(discount)
                })
                #f2.write(str(discount) + '\n')

            except:
                doc_ref.update({
                    'playPrice': 'No existe',
                    'playDisc': 'No existe'
                })
                #f.write('No existe' + '\n')
                #f2.write('No existe' + '\n')
        elif cont > 1:
            doc_ref.update({
                'playPrice': 'No existe',
                'playDisc': 'No existe'
            })
            #f.write('No existe' + '\n')
            #f2.write('No existe' + '\n')

    if results == []:
        doc_ref.update({
            'playPrice': 'No existe',
            'playDisc': 'No existe'
        })
        #f.write('No existe' + '\n')
        #f2.write('No existe' + '\n')

    #f.close()
    #f2.close()
