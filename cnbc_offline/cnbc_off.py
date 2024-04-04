from bs4 import BeautifulSoup as bs
import os
import pandas as pd

def extract(page):
    with open("cnbcindo.html", "r") as e:
        soup = bs(e, "html.parser")
        return soup

def transform(soup): 
    divs = soup.find_all('div', class_ = 'xuvV6b BGxR7d')
    for x in divs:
        # images = x.find('img')['src'].replace('\n', '')
        channels = x.find(class_ = 'CEMjEf NUnG9d').text
        #di csv headlines ter-enter kebawah(ada whitespace), jd perlu dihapus spasinya \n
        links = x.find('a', class_ = 'WlydOe')['href']
        headlines = x.find(class_ = 'GI74Re nDgy9d').text.replace('\n', '')
        times = x.find(class_ = 'OSrXXb ZE0LJd').text

        #grab all together, akan mengikuti urutan ini kolomnya
        new = {
            'channels': channels,
            'headlines': headlines,
            'times': times,
            'links': links
        }
        #grab all column into blank list
        news.append(new)
    return
news = []
transform(extract(0))
print(news)

#convert list to dataframe
df = pd.DataFrame(news, index=None)
#save dataframe to csv
df.to_csv('cnbc_off.csv', index=False)

# headlines
# body > div:nth-child(1) > div > a > div > div.iRPxbe > div.mCBkyc.y355M.ynAwRc.MBeuO.nDgy9d
# links
# body > div:nth-child(1) > div > a
# time
# body > div:nth-child(1) > div > a > div > div.iRPxbe > div.OSrXXb.ZE0LJd > span
# kantor berita
# body > div:nth-child(1) > div > a > div > div.iRPxbe > div.CEMjEf.NUnG9d > span


