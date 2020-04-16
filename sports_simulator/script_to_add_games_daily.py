from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from bs4 import BeautifulSoup
import requests
import re

f = open("hrefs.txt", "w")

def check(href):
    if href != None:
        f.write(href)
        f.write("\n")
    return not re.compile("/game/{{ game.id }}/")

def get_score(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for tag in soup.findAll('div', {'class': 'game-summary-team__points'}):
        print(tag.string)

def get_old_games():
    f = open("hrefs.txt", "w")
    url = 'https://stats.nba.com/scores/03/10/2020'
    data = requests.get(url)
    plain_text = data.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    #for game_link in soup.find_all(href=check):
    for game_link in soup.findAll('a'):
        #if game_link.string == "Box Score":
        if game_link.get("href") != None:
            f.write(game_link.get("href"))
            f.write("\n")
            print(game_link.get("href"))
            #get_score(game_link.get("href"))
    f.close()
    

if __name__ == "__main__":
    f = open("hrefs.txt", "w")
    get_old_games()



