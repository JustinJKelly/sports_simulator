from django.shortcuts import render
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
from bs4 import BeautifulSoup
import requests

from random import seed
from random import randint

def home(request):
    url = "https://www.cbssports.com/nba/schedule/"
    response = requests.get(url)

    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    team_names = []
    games = []

    for span_tag in soup.findAll('span', {'class': 'TeamName'}):
        team_names.append((span_tag.find('a')).string)

    for i in range(0,len(team_names),2):
        team1 = team_names[i]
        team2 = team_names[i+1]
        team_logos = find_team_logos(team1.lower(),team2.lower())
        game = [team1,team2]
        game += team_logos
        games.append(game)

    for game in games:
        print(game)

    context = {
        "games": games
    }
    return render(request, 'basketball/index.html', context)


def find_team_logos(team1, team2):
    return_list = []

    list_teams = [
        "atlanta","boston","brooklyn","charlotte","chicago","cleveland","dallas","denver",
        "detroit","golden","houston","indiana","l.a. clippers","l.a. lakers","memphis","miami","milwaukee",
        "minnesota","new orleans","new york","oklahoma city","orlando","philadelphia","phoenix","portland",
        "sacramento","san antonio","toronto","utah","washington"
    ]
    list_teams_logo = [
        "atlanta-hawks","boston-celtics","brooklyn-nets","charlotte-bobcats","chicago-bulls",
        "cleveland-cavaliers","dallas-mavericks","denver-nuggets","detroit-pistons","golden-state-warriors",
        "houston-rockets","indiana-pacers","los-angeles-clippers","los-angeles-lakers","memphis-grizzlies",
        "miami-heat","milwaukee-bucks","minnesota-timberwolves","new-orleans-pelicans","new-york-knicks",
        "oklahoma-city-thunder","orlando-magic","philadelphia-76ers","phoenix-suns","portland-trail-blazers",
        "sacramento-kings","san-antonio-spurs","toronto-raptors","utah-jazz","washington-wizards"
    ]

    for i in range(0,len(list_teams)):
        if list_teams[i]==team1:
            img_file = "img/"+list_teams_logo[i]+".png"
            return_list.append(img_file)
        elif list_teams[i]==team2:
            img_file = "img/"+list_teams_logo[i]+".png"
            return_list.append(img_file)
    return return_list

