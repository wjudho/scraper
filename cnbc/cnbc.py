import pandas as pd
from bs4 import BeautifulSoup as bs

def extract(page):
    with open("cnbcindo.html", "r") as cnbc:
        soup = bs(cnbc, "html.parser")
        return soup      

def transform(soup):
    body = [x.find('h2').text.replace('\n', '') for x in soup.find_all('article')]





# body > div.container > div.lm_content.mt10 > ul > li:nth-child(1) > article > a > div



c = extract(0)

print(transform(c))

