import multiprocessing
import time
import requests

from bs4 import BeautifulSoup


def work(x):
    start_time = time.time()
    # scrapSteamPage()
    # scrapEpicGPage()

    end_time = time.time()
    print("Scraping time:", end_time - start_time)


def scrapSteamPage():
    f = open("repoGames.txt", "w+", encoding="utf-8")
    file = open ('repoNames2.txt', "w+", encoding="utf-8")

    URL = 'https://store.steampowered.com/search/?term='
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='search_resultsRows')
    # print(results.prettify())

    job_elems = results.find_all('a', class_='search_result_row')
    cont = 0

    for job_elem in job_elems:
        title_elem = job_elem.find('span', class_='title').text.strip()
        discount_elem = job_elem.find('div', class_='search_discount').text.strip()
        price_elem = job_elem.find('div', class_='search_price').text.strip()
        if None in (title_elem, discount_elem, price_elem):
            continue
        if discount_elem == '':
            discount_elem = '0%'

        #print('................................................')
        #print(
        #    'Título: ' + title_elem + '\nDescuento: ' + discount_elem + '\nPrecio: ' + price_elem)
        f.write('Titulo: ' + title_elem + ' | Descuento: ' + discount_elem + ' | Precio: ' + (price_elem) +"\n")
        file.write(title_elem + "\n")
        #print()

        cont += 1
    f.close()
    file.close()



'''
################################
Multiprocesos
################################

num_workers = 4


def only_sleep():
    time.sleep(1)


# Run tasks using processes
def multi():
    processes = [
        multiprocessing.Process(target=only_sleep()) for _ in range(num_workers)]
    [process.start() for process in processes]
    [process.join() for process in processes]
'''
