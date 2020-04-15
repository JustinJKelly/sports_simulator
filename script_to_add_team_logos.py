import requests
from bs4 import BeautifulSoup

teamDict = {1 :"BKN"}# 2: "ATL", 3: "BOS"}

for items in teamDict:
    url = "https://stats.nba.com/media/img/teams/logos/{}_logo.svg".format(teamDict[items])
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    print(soup)
