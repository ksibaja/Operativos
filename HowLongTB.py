import time
from howlongtobeatpy import HowLongToBeat
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

    getHowLongToBeat(elem)

    end_time = time.time()


def getHowLongToBeat(elem):
    #f = open("howLong.txt", "a+", encoding="utf-8")
    doc_ref = db.collection('games').document(elem)

    results = HowLongToBeat(0.0).search(elem)
    try:
        doc_ref.update({
            'timeUrl': str(results[0].game_web_link),
            'fullTime': str(results[0].gameplay_completionist),
            'averTime': str(results[0].gameplay_main),
            'plusTime': str(results[0].gameplay_main_extra),
        })
        #f.write('Tiempo completo ' + str(results[0].gameplay_completionist) + ' tiempo promedio: ' +
        #      str(results[0].gameplay_main) + ' tiempo mas extras: ' + str(results[0].gameplay_main_extra) + '\n')
    except:
        doc_ref.update({
            'Time': 'No existe'
        })
        #f.write('No existe' + '\n')

    #f.close()
