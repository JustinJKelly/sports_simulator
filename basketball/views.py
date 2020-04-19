from django.shortcuts import redirect, render
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams
from bs4 import BeautifulSoup
import requests
from .models import Player, Game
# importing datetime module 
import datetime
'''
# creating an instance of  
# datetime.date 
d = datetime(2015, 10, 09, 23, 55, 59, 342380) 
'''

from random import seed
from random import randint
from django.http import HttpResponse
from django.contrib import messages

def home(request):
    #print(request.POST['date'])
    if request.method == 'GET':
        game_date = datetime.date.today()
    elif not request.POST['date']:
        messages.add_message(request, messages.ERROR, 'No date specified')
        game_date = datetime.date.today()
    else:
        date_attr = request.POST['date'].split('/')
        #date(year, month, day)
        game_date = datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
        
    games = Game.objects.filter(date=game_date) 
    context = {}
    context['games'] = []

    ''' [ game_id, home_team_abv, away_team_abv, home_team_img, away_team_img, away_team_score,
            home_team_score, top_scorer_home_name, top_scorer_home_points, top_scorer_away_name,
            top_scorer_away_score
        ]
    '''
    for game in games:
        this_game = [
            game.game_id,
            teams.find_team_name_by_id(game.home_team)['abbreviation'],
            teams.find_team_name_by_id(game.away_team)['abbreviation'],
            find_team_image(game.home_team),
            find_team_image(game.away_team),
            game.top_scorer_home,
            players.find_player_by_id(game.top_scorer_home)['full_name'],
            game.top_scorer_home_points,
            game.top_scorer_away,
            players.find_player_by_id(game.top_scorer_away)['full_name'],
            game.top_scorer_away_points,
            game.home_team_score,
            game.away_team_score
        ]
        context['games'].append(this_game)


    return render(request, 'basketball/games.html', context)
    '''url = "https://www.cbssports.com/nba/schedule/"
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

    return render(request, 'basketball/index.html', context)'''

#height,weight,jersey_number,player_age, team_name
#full_name,player_id,points_total,assists_total,rebounds_total,blocks_total
#steals_total, turnovers_total, personal_fouls_total,free_throws_attempted
#free_throws_made,minutes_total,three_point_attempted,three_point_made,
#field_goals_attempted,field_goals_made,games_played,team_id
def player_page(request,id):
    player = Player.objects.get(player_id=id)
    if player == None:
        return render("404 player not found")
    player_image = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{}.png".format(id)

    if player.free_throws_attempted == 0:
        free_throw_percentage = 0
    else:
        free_throw_percentage = round((player.free_throws_made/player.free_throws_attempted)*100,1)

    if player.field_goals_attempted == 0:
        field_goal_percentage = 0
    else:
        field_goal_percentage = round((player.field_goals_made/player.field_goals_attempted)*100,1)
    
    if player.three_point_attempted == 0:
        three_point_percentage = 0
    else:
        three_point_percentage = round((player.three_point_made/player.three_point_attempted)*100,1)
    
    context = {
        "full_name": player.full_name,"player_id":player.player_id,
        "point_per_game":round(player.points_total/player.games_played,1),
        "assists_per_game":round(player.assists_total/player.games_played,1),
        "rebounds_per_game":round(player.rebounds_total/player.games_played,1),
        "blocks_per_game":round(player.blocks_total/player.games_played,1),
        "steals_per_game":round(player.steals_total/player.games_played,1),
        "turnovers_per_game":round(player.turnovers_total/player.games_played,1),
        "personal_fouls_per_game":round(player.personal_fouls_total/player.games_played,1),
        "free_throw_percentage":free_throw_percentage,
        "field_goal_percentage":field_goal_percentage,
        "minutes_per_game":round(player.minutes_total/player.games_played,1),
        "three_point_percentage":three_point_percentage,
        "games_played":player.games_played,"team_image":find_team_image(player.team_id),"player_image":player_image,
        "height":player.height,"weight":player.weight,"jersey_number":player.jersey_number,
        "player_age":player.player_age,"team_name":player.team_name,
        "free_throws_attempted":round(player.free_throws_attempted/player.games_played,1),
        "free_throws_made":round(player.free_throws_made/player.games_played,1),
        "three_point_attempted":round(player.three_point_attempted/player.games_played,1),
        "three_point_made":round(player.three_point_made/player.games_played,1),
        "field_goals_attempted":round(player.field_goals_attempted/player.games_played,1),
        "field_goals_made":round(player.field_goals_made/player.games_played,1),"position":player.position
    }
    return render(request,'basketball/player_page.html',context=context)



''' home_team = models.IntegerField(null=False)
    away_team = models.IntegerField(null=False)
    home_team_name = models.CharField(max_length=35,null=False)
    away_team_name = models.CharField(max_length=35,null=False)
    game_id = models.IntegerField(primary_key=True)
    winning_team_id = models.IntegerField(null=False)
    winner_name = models.CharField(max_length=35,null=False)
    loser_name = models.CharField(max_length=35,null=False)
    losing_team_id = models.IntegerField(null=False)
    home_team_score = models.IntegerField(null=False)
    away_team_score = models.IntegerField(null=False)
    top_scorer_home = models.IntegerField(null=False)
    top_scorer_away = models.IntegerField(null=False)
    attendance = models.IntegerField(null=False)
    date = models.DateField(default=date.today)
    time = models.TimeField(default=None, null=True)
    data = JSONField()'''
def game_page(request, id):
    game = Game.objects.get(game_id=id)

    player_stats = game.data['player_stats']
    team_stats = game.data['team_stats']
    home_team_player_stats = []
    away_team_player_stats = []

    for player in player_stats:
        if player['team_id']==game.home_team:
            if player['comment']=='OK':
                home_team_player_stats.append([
                    player['player_id'],player['name'],player['min'],player['FG_made'],
                    player['FG_attempted'],player['3P_made'],player['3P_attempted'],
                    player['FT_made'],player['FT_attempted'],player['off_rebounds'],
                    player['def_rebounds'],player['off_rebounds']+player['def_rebounds'],
                    player['assists'],player['steals'],player['blocks'],player['turnovers'],
                    player['personal_fouls'],player['points'],player['player_id']
                ])
            else:
                home_team_player_stats.append([
                    player['player_id'],player['name'],'N/A',0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0
                ])
        else:
            if player['comment']=='OK':
                away_team_player_stats.append([
                    player['player_id'],player['name'],player['min'],player['FG_made'],
                    player['FG_attempted'],player['3P_made'],player['3P_attempted'],
                    player['FT_made'],player['FT_attempted'],player['off_rebounds'],
                    player['def_rebounds'],player['off_rebounds']+player['def_rebounds'],
                    player['assists'],player['steals'],player['blocks'],player['turnovers'],
                    player['personal_fouls'],player['points'],player['player_id']
                ])
            else:
                away_team_player_stats.append([
                    player['player_id'],player['name'],'N/A',0,
                    0,0,0,0,0,0,0,0,0,0,0,0,0,0
                ])
                

    home_team_stats = []
    away_team_stats = []
    home_team = 1
    away_team = 1
    if team_stats[0]['team_id']==game.home_team:
        home_team = 0
    else:
        away_team = 0

    home_team_stats= [
        team_stats[home_team]['FG_made'], team_stats[home_team]["FG_attempted"], 
        round((team_stats[home_team]['FG_made']/team_stats[home_team]["FG_attempted"])*100,1),
        team_stats[home_team]['3P_made'], team_stats[home_team]["3P_attempted"], 
        round((team_stats[home_team]['3P_made']/team_stats[home_team]["3P_attempted"])*100,1),
        team_stats[home_team]['FT_made'], team_stats[home_team]["FT_attempted"],
        round((team_stats[home_team]['FT_made']/team_stats[home_team]["FT_attempted"])*100,1),
        team_stats[home_team]['off_rebounds']+team_stats[home_team]["def_rebounds"],
        team_stats[home_team]['off_rebounds'], team_stats[home_team]["def_rebounds"],
        team_stats[home_team]['assists'],team_stats[home_team]['steals'],team_stats[home_team]['blocks'],
        team_stats[home_team]['turnovers'],team_stats[home_team]['personal_fouls']
    ]
    away_team_stats= [
        team_stats[away_team]['FG_made'], team_stats[away_team]["FG_attempted"], 
        round((team_stats[away_team]['FG_made']/team_stats[away_team]["FG_attempted"])*100,1),
        team_stats[away_team]['3P_made'], team_stats[away_team]["3P_attempted"], 
        round((team_stats[away_team]['3P_made']/team_stats[away_team]["3P_attempted"])*100,1),
        team_stats[away_team]['FT_made'], team_stats[away_team]["FT_attempted"],
        round((team_stats[away_team]['FT_made']/team_stats[away_team]["FT_attempted"])*100,1),
        team_stats[away_team]['off_rebounds']+team_stats[away_team]["def_rebounds"],
        team_stats[away_team]['off_rebounds'], team_stats[away_team]["def_rebounds"],
        team_stats[away_team]['assists'],team_stats[away_team]['steals'],team_stats[away_team]['blocks'],
        team_stats[away_team]['turnovers'],team_stats[away_team]['personal_fouls']
    ]
    

    points_by_quarter = game.data["points_by_quarter_id"]
    home_points_by_quarter = points_by_quarter[str(game.home_team)]
    away_points_by_quarter = points_by_quarter[str(game.away_team)]

    #DOESNT HAVE OVERTIME POINTS BY QUARTER
    #AND IT ONLY WANT 10 PLAYERS(SOME GAMES HAVE 12+) CAN JUST do home_team_player_stats[:10]
    context = {
        "home_team_name": game.home_team_name,"game_id":game.game_id,"away_team_name": game.away_team_name,
        "home_team_image":find_team_image(game.home_team),"away_team_image":find_team_image(game.away_team),
        "home_team_score":game.home_team_score,"away_team_score":game.away_team_score,
        "top_scorer_home":game.top_scorer_home,"top_scorer_away":game.top_scorer_away,"attendance":game.attendance,
        "day":game.date.day, "month":game.date.month,"year":game.date.year,
        "home_team_stats":home_team_stats,"away_team_stats":away_team_stats,
        "home_team_player_stats":home_team_player_stats, "away_team_player_stats":away_team_player_stats,
        "top_scorer_home_points":game.top_scorer_home_points,"top_scorer_away_points":game.top_scorer_away_points,
        "top_scorer_home_name":Player.objects.get(player_id=game.top_scorer_home),
        "top_scorer_away_name":Player.objects.get(player_id=game.top_scorer_away),
        "away_points_by_quarter":away_points_by_quarter[:4], "home_points_by_quarter": home_points_by_quarter[:4],
        "home_team_abv":teams.find_team_name_by_id(game.home_team)['abbreviation'],
        "away_team_abv":teams.find_team_name_by_id(game.away_team)['abbreviation'],
        "home_team_record":game.home_team_record, "away_team_record":game.away_team_record
    }

    return render(request,'basketball/game_page.html',context)



def get_game(request):
    #print(request.POST['date'])
    if not request.POST['date']:
        redirect('/index.html')
    else:
        date_attr = request.POST['date'].split('/')
        #date(year, month, day)
        game_date = datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
        
        games = Game.objects.filter(date=game_date) 
        context = {}
        context['games'] = []

        for game in games:
            this_game = [
                game.game_id,
                game.home_team_name,
                game.away_team_name
            ]
            context['games'].append(this_game)
    
        return render(request, 'basketball/index.html', context)



def team_home_page(request):
    return HttpResponse("hello")

def team_page(request,id):
    return HttpResponse("hello")

def standings_page(request):
    return HttpResponse("hello")


def find_team_logos(team1, team2):
    return_list = []

    list_teams = {
        "atlanta":"img/atlanta-hawks.png",
        "boston":"img/boston-celtics.png",
        "brooklyn":"img/brooklyn-nets.png",
        "charlotte":"img/charlotte-hornets.png",
        "chicago":"img/chicago-bulls.png",
        "cleveland":"img/cleveland-cavaliers.png",
        "dallas":"img/dallas-mavericks.png",
        "denver":"img/denver-nuggets.png",
        "detroit":"img/detroit-pistons.png",
        "golden st.":"img/golden-state-warriors.png",
        "houston":"img/houston-rockets.png",
        "indiana":"img/indiana-pacers.png",
        "l.a. clippers":"img/los-angeles-clippers.png",
        "l.a. lakers":"img/los-angeles-lakers.png",
        "memphis":"img/memphis-grizzlies.png",
        "miami":"img/miami-heat.png",
        "milwaukee":"img/milwaukee-bucks.png",
        "minnesota":"img/minnesota-timberwolves.png",
        "new orleans":"img/new-orleans-pelicans.png",
        "new york":"img/new-york-knicks.png",
        "oklahoma city":"img/oklahoma-city-thunder.png",
        "orlando":"img/orlando-magic.png",
        "philadelphia":"img/philadelphia-76ers.png",
        "phoenix":"img/phoenix-suns.png",
        "portland":"img/portland-trail-blazers.png",
        "sacramento":"img/sacramento-kings.png",
        "san antonio":"img/san-antonio-spurs.png",
        "toronto":"img/toronto-raptors.png",
        "utah":"img/utah-jazz.png",
        "washington":"img/washington-wizards.png"
    }
    return_list = [list_teams[team1],list_teams[team2]]

    return return_list



def find_team_image(team_id):
    list_teams = {
        1610612737:"img/atlanta-hawks.png",
        1610612738:"img/boston-celtics.png",
        1610612751:"img/brooklyn-nets.png",
        1610612766:"img/charlotte-hornets.png",
        1610612741:"img/chicago-bulls.png",
        1610612739:"img/cleveland-cavaliers.png",
        1610612742:"img/dallas-mavericks.png",
        1610612743:"img/denver-nuggets.png",
        1610612765:"img/detroit-pistons.png",
        1610612744:"img/golden-state-warriors.png",
        1610612745:"img/houston-rockets.png",
        1610612754:"img/indiana-pacers.png",
        1610612746:"img/los-angeles-clippers.png",
        1610612747:"img/los-angeles-lakers.png",
        1610612763:"img/memphis-grizzlies.png",
        1610612748:"img/miami-heat.png",
        1610612749:"img/milwaukee-bucks.png",
        1610612750:"img/minnesota-timberwolves.png",
        1610612740:"img/new-orleans-pelicans.png",
        1610612752:"img/new-york-knicks.png",
        1610612760:"img/oklahoma-city-thunder.png",
        1610612753:"img/orlando-magic.png",
        1610612755:"img/philadelphia-76ers.png",
        1610612756:"img/phoenix-suns.png",
        1610612757:"img/portland-trail-blazers.png",
        1610612758:"img/sacramento-kings.png",
        1610612759:"img/san-antonio-spurs.png",
        1610612761:"img/toronto-raptors.png",
        1610612762:"img/utah-jazz.png",
        1610612764:"img/washington-wizards.png"
    }
    #print(list_teams[team_id])

    return list_teams[team_id]
