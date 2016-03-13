import requests as req					#to establish connection
from bs4 import BeautifulSoup as BS	#to process data from html
import pandas as pd

url = 'http://espn.go.com/nba/teams'

r = req.get(url)
soup = BS(r.text,'html.parser')

tables = soup.find_all('ul', class_='medium-logos')
teams = []
#print (tables)

prefix_1 = []
prefix_2 = []
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        prefix_1.append(url.split('/')[-2])
        prefix_2.append(url.split('/')[-1])


dic = {'prefix_2': prefix_2, 'prefix_1': prefix_1}
teams = pd.DataFrame(dic, index=teams)
teams.index.name = 'name'

f = open('teams.csv','wt')
f.write(teams.to_csv())
f.close

print(teams)