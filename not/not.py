from bs4 import BeautifulSoup as bs
import pandas as pd

def extract(page):
    with open('Mobile Graphics Cards - Benchmark List - NotebookCheck.net Tech.html', 'r', encoding='UTF-8', newline='\n') as file:
        soup = bs(file, 'html.parser')
        return soup

def transform(soup):
    products = [product.text for product in soup.find_all('td', class_ = 'specs fullname')]
    fill.append(products)
    return
fill = []
c = extract(0)
transform(c)
df = pd.DataFrame(fill, index=None)
df.to_csv('mob.csv', index=False)
