import time
from multiprocessing import Process

''' Classes imports '''
import GetPrices
import HowLongTB
import MetaScore

''' FIREBASE '''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
if not firebase_admin._apps:
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()



if __name__ == '__main__':
    start_time = time.time()

    f = open('repoNamesFew.txt', "r", encoding="utf-8")
    names = f.read().split("\n")
    #f1 = open("metaScore.txt", "w+", encoding="utf-8")
    #f2 = open("howLong.txt", "w+", encoding="utf-8")
    #f3 = open("pricesSteam.txt", "w+", encoding="utf-8")
    #f4 = open("discountSteam.txt", "w+", encoding="utf-8")
    #f5 = open("pricesPlayS.txt", "w+", encoding="utf-8")
    #f6 = open("discountPlayS.txt", "w+", encoding="utf-8")

    #f1.write('')
    #f2.write('')
    #f3.write('')
    #f4.write('')
    #f5.write('')
    #f6.write('')


    #f1.close()
    #f2.close()
    #f3.close()
    #f4.close()
    #f5.close()
    #f6.close()


    for elem in names:
        doc_ref = db.collection('games').document(elem)
        doc_ref.set({
            'Name': elem,
            'Score': '',
            'scoreUrl': '',
            'Time': '',
            'fullTime': '',
            'averTime': '',
            'plusTime': '',
            'timeUrl': '',
            'steamPrice': '',
            'steamDisc': '',
            'steamUrlImage': '',
            'steamUrlGame': '',
            'playPrice': '',
            'playDisc': '',
            'playUrlGame': ''
        })

        print('JUEGO:' + elem)
        p1 = Process(target=GetPrices.work, args=(elem,))
        p2 = Process(target=HowLongTB.work, args=(elem,))
        p3 = Process(target=MetaScore.work, args=(elem,))
        # p4 = Process(target=Scraping.work, args=('x',))

        p1.start()
        p2.start()
        p3.start()
        # p4.start()

        p1.join()
        p2.join()
        p3.join()
        # p4.join()

    print("Done")
    end_time = time.time()

    f.close()
    #f1.close()
    #f2.close()
    #f3.close()
    #f4.close()
    #f5.close()
    #f6.close()
    print("Tiempo total:", end_time - start_time)

