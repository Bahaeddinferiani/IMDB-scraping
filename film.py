import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import time
import random
import json
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"}

url = "https://www.imdb.com/title/tt9114286/reviews"
def write_to_json(new_data, filename='reviews.json'):
    with open(filename, 'r+') as file:
        file_data = json.load(file)
        file_data.append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)
response = requests.get(url, headers=header)
soup = BeautifulSoup(response.content, 'html.parser')
dom = et.HTML(str(soup))
try:
    review = dom.xpath('//div[@class="text show-more__control"]/descendant-or-self::text()')
except:
    review = ""

def time_delay():
    time.sleep(random.randint(2, 5))
with open("reviews.json", "w") as f:
    json.dump([], f)
time_delay()
for i in range(len(review)):
    write_to_json(review[i])

