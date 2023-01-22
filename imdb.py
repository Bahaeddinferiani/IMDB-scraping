import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import json

from unidecode import unidecode
def formatili(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
            return float(x.replace('K', '')) * 1000
    if 'M' in x:
            return float(x.replace('M', '')) * 1000000


start_url = "https://www.imdb.com/search/title/?title_type=feature&genres=sci-fi&explore=genres" #lien
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}
movie_urls = []
movie_reviews_urls= []

response = requests.get(start_url, headers=header) #stocker les données de requete get dans une variable

soup = BeautifulSoup(response.content, 'html.parser')#Beautiful soup permet d'analyser un fichier Html et l'utuliser (Ou xml)
dom = et.HTML(str(soup)) #convertir le traitement de beautifulsoup en xml

movie_urls_list = dom.xpath('//h3[@class="lister-item-header"]/a/@href') #selection du lien de h3 (vers le film)

for i in range(len(movie_urls_list)):
    long_url = "https://www.imdb.com" + movie_urls_list[i] #construction d'url vers chaque film 
    short_url = long_url.split("?")[0]    #ce qui est ecrit apres ? est inutile 
    movie_urls.append(short_url)          #écrire chaque lien vers le film dans le 
for i in range(len(movie_urls)):
    review = movie_urls[i]+'reviews'
    movie_reviews_urls.append(review)

def time_delay():
    time.sleep(random.randint(2, 5))
with open("data.json", "w") as f:
    json.dump([], f)

def write_to_json(new_data, filename='data.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
for i in range(len(movie_urls)):
    response = requests.get(movie_urls[i], headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    dom = et.HTML(str(soup))

    review_response = requests.get(movie_reviews_urls[i], headers=header)
    chorba = BeautifulSoup(review_response.content,'html.parser')
    dom_r = et.HTML(str(chorba))



    title = dom.xpath('//h1[@data-testid="hero-title-block__title"]/text()')[0]
    try:
        year = int(dom.xpath('//a[@class="ipc-link ipc-link--baseAlt ipc-link--inherit-color sc-8c396aa2-1 WIUyh"]/text()')[0])
    except:
        year = 0
    genre = dom.xpath('//span[@class="ipc-chip__text"]/text()')
    try:
        meta = int(dom.xpath('//span[@class="score-meta"]/text()')[0])
    except:
        meta = 0
    try:
       rating = dom.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()')[0] 
    except:
        rating = ""
    try:
        runtime_kemla = dom.xpath('//div[@class="ipc-metadata-list-item__content-container"]/text()')
        runtime = int(runtime_kemla[0])*60+int(runtime_kemla[4])
    except:
        runtime = 0
    try:
        imdb_rating = float(dom.xpath('//span[@class="sc-7ab21ed2-1 jGRxWM"]/text()')[0])
    except:
        imdb_rating = 0
    try:
        votes = formatili(dom.xpath('//div[@class="sc-7ab21ed2-3 dPVcnq"]/text()')[0])
    except:
        votes = 0
    try:
        review = dom_r.xpath('//a[@class="title"]/text()')
    except:
        review = ""
    write_to_json({
        'movie':title,
        'year': year,
        'genre': genre,
        'runtime_mins': runtime,
        'imdb_rating': imdb_rating,
        'metascore': meta,
        'votes': votes,
        "review":review
                   })

    time_delay()
    print("data is written to json file "+str(i))
