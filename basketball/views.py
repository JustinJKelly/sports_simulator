from django.shortcuts import redirect, render, reverse
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players, teams
from bs4 import BeautifulSoup
import requests
from .models import Player, Game, Team, MVPPoll
# importing datetime module 
import datetime
from sports_simulator import views as home_views
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
        print(date_attr)
        game_date = date_attr[2]+date_attr[0]+date_attr[1]#datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
        return redirect('/basketball/games/'+game_date)

        
    games = Game.objects.filter(date=game_date) 
    context = {}
    context['date']='%s/%s/%s' % (game_date.month,game_date.day,game_date.year)
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
            game.away_team_score,
            game.home_team,
            game.away_team
        ]
        context['games'].append(this_game)


    return render(request, 'basketball/games.html', context)


def get_games_date(request,game_date):

    #date(year, month, day)
    print('here')
    try:
        if request.method == 'POST' and request.POST['date']:
            print("here1")
            print(request.POST['date'])
            date_attr = request.POST['date'].split('/')
            return redirect('/basketball/games/'+(date_attr[2]+date_attr[0]+date_attr[1]))
            #game_date = datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
        else:
            print("here2")
            date_attr = str(game_date)
            print(date_attr)
            if len(date_attr) != 8:
                raise TypeError
            game_date = datetime.date(int(date_attr[0:4]),int(date_attr[4:6]),int(date_attr[6:]))

    except:
        messages.add_message(request, messages.ERROR, 'Error in processing the date specified')
        game_date = datetime.date.today()
        return render(request, 'basketball/games.html')

    games = Game.objects.filter(date=game_date) 
    context = {}
    context['date']='%s/%s/%s' % (game_date.month,game_date.day,game_date.year)
    context['games'] = []

    ''' [ game_id, home_team_abv, away_team_abv, home_team_img, away_team_img, away_team_score,
            home_team_score, top_scorer_home_name, top_scorer_home_points, top_scorer_away_name,
            top_scorer_away_score
        ]
    '''
    for game in games:
        this_game = [
            game.game_id,
            Team.objects.get(team_id=game.home_team).team_abv,
            Team.objects.get(team_id=game.away_team).team_abv,
            find_team_image(game.home_team),
            find_team_image(game.away_team),
            game.top_scorer_home,
            Player.objects.get(player_id=game.top_scorer_home).full_name,
            game.top_scorer_home_points,
            game.top_scorer_away,
            Player.objects.get(player_id=game.top_scorer_away).full_name,
            game.top_scorer_away_points,
            game.home_team_score,
            game.away_team_score,
            game.home_team,
            game.away_team
        ]
        context['games'].append(this_game)

    return render(request, 'basketball/games.html',context)
    

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
        "offensive_rebounds_per_game":round(player.offensive_rebounds_total/player.games_played,1),
        "defensive_rebounds_per_game":round(player.defensive_rebounds_total/player.games_played,1),
        "rebounds_per_game":round(player.rebounds_total/player.games_played,1),
        "blocks_per_game":round(player.blocks_total/player.games_played,1),
        "steals_per_game":round(player.steals_total/player.games_played,1),
        "turnovers_per_game":round(player.turnovers_total/player.games_played,1),
        "personal_fouls_per_game":round(player.personal_fouls_total/player.games_played,1),
        "free_throw_percentage":free_throw_percentage,
        "field_goal_percentage":field_goal_percentage,
        "minutes_per_game":round(player.minutes_total/player.games_played,1),
        "three_point_percentage":three_point_percentage,
        "games_played":player.games_played,"team_image":find_team_image(player.team_id),"player_image":player_image, "team_id":player.team_id,
        "height":player.height,"weight":player.weight,"jersey_number":player.jersey_number,
        "player_age":player.player_age,"team_name":player.team_name,
        "free_throws_attempted":round(player.free_throws_attempted/player.games_played,1),
        "free_throws_made":round(player.free_throws_made/player.games_played,1),
        "three_point_attempted":round(player.three_point_attempted/player.games_played,1),
        "three_point_made":round(player.three_point_made/player.games_played,1),
        "field_goals_attempted":round(player.field_goals_attempted/player.games_played,1),
        "field_goals_made":round(player.field_goals_made/player.games_played,1),"position":player.position,
        "injured":player.is_injured
    }

    context['game_log']=[]
    games = (Game.objects.filter(home_team=player.team_id) | Game.objects.filter(away_team=player.team_id)).order_by('-date')
    for game in games:
        player_stats = game.data['player_stats']
        found = False
        this_game_log = []
        for p in player_stats:
            if p['player_id'] == player.player_id:
                found = True
                if p['comment']=='OK':
                    this_game_log = [
                        p['player_id'],p['name'],p['min'],p['FG_made'],
                        p['FG_attempted'],p['3P_made'],p['3P_attempted'],
                        p['FT_made'],p['FT_attempted'],p['off_rebounds'],
                        p['def_rebounds'],p['off_rebounds']+p['def_rebounds'],
                        p['assists'],p['steals'],p['blocks'],p['turnovers'],
                        p['personal_fouls'],p['points'],
                        game.date.month,game.date.day
                    ]
                else:
                    this_game_log = [
                        p['player_id'],p['name'],'N/A',0,
                        0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                        game.date.month,game.date.day
                    ]

                if player.team_id == game.home_team:
                    this_game_log.append(find_team_image(game.away_team))
                    this_game_log.append(game.away_team)
                    this_game_log.append('vs')
                    this_game_log.append(Team.objects.get(team_id=game.away_team).team_abv)
                    if game.winning_team_id == game.home_team:
                        this_game_log.append('W')
                        this_game_log.append(game.home_team_score)
                        this_game_log.append(game.away_team_score)
                    else:
                        this_game_log.append('L')
                        this_game_log.append(game.away_team_score)
                        this_game_log.append(game.home_team_score)

                else:
                    this_game_log.append(find_team_image(game.home_team))
                    this_game_log.append(game.home_team)
                    this_game_log.append('@')
                    this_game_log.append(Team.objects.get(team_id=game.home_team).team_abv)
                    if game.winning_team_id == game.away_team:
                        this_game_log.append('W')
                        this_game_log.append(game.away_team_score)
                        this_game_log.append(game.home_team_score)
                    else:
                        this_game_log.append('L')
                        this_game_log.append(game.home_team_score)
                        this_game_log.append(game.away_team_score)
                break
            #print(this_game_log)
        if not found:
            this_game_log = [
                player.player_id,player.full_name,'N/A',0,
                0,0,0,0,0,0,0,0,0,0,0,0,0,0,
                game.date.month,game.date.day,
            ]
            if player.team_id == game.home_team:
                this_game_log.append(find_team_image(game.away_team))
                this_game_log.append(game.away_team)
                this_game_log.append('vs')
                this_game_log.append(Team.objects.get(team_id=game.away_team).team_abv)
                if game.winning_team_id == game.home_team:
                    this_game_log.append('W')
                    this_game_log.append(game.home_team_score)
                    this_game_log.append(game.away_team_score)
                else:
                    this_game_log.append('L')
                    this_game_log.append(game.away_team_score)
                    this_game_log.append(game.home_team_score)
            else:
                this_game_log.append(find_team_image(game.home_team))
                this_game_log.append(game.home_team),
                this_game_log.append('@')
                this_game_log.append(Team.objects.get(team_id=game.home_team).team_abv)
                if game.winning_team_id == game.away_team:
                    this_game_log.append('W')
                    this_game_log.append(game.away_team_score)
                    this_game_log.append(game.home_team_score)
                else:
                    this_game_log.append('L')
                    this_game_log.append(game.home_team_score)
                    this_game_log.append(game.away_team_score)

            
        this_game_log.append(game.game_id)
        context['game_log'].append(this_game_log)

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
                    player['personal_fouls'],player['points']
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
                    player['personal_fouls'],player['points']
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
    count = 0
    for points in home_points_by_quarter:
        if points > 0:
            count +=1
    num_ots = count-4

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
        "away_points_by_quarter":away_points_by_quarter[:count], "home_points_by_quarter": home_points_by_quarter[:count],
        "home_team_abv":teams.find_team_name_by_id(game.home_team)['abbreviation'],
        "away_team_abv":teams.find_team_name_by_id(game.away_team)['abbreviation'],
        "home_team_record":game.home_team_record, "away_team_record":game.away_team_record,
        "home_team_id":game.home_team,"away_team_id":game.away_team,"num_overtimes":range(1,num_ots+1)
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
    
    divisions = {}
    divisions['Atlantic'] = []
    divisions['Central'] = []
    divisions['Northwest'] = []
    divisions['Pacific'] = []
    divisions['Southeast'] = []
    divisions['Southwest'] = []
    all_teams = Team.objects.all()

    #team_name, team_abv, team_id
    for team in all_teams:
        team_info = [
            team.team_id, 
            team.team_name, 
            team.team_abv,
            find_team_image(team.team_id)
        ]
        #print(find_team_image(team.team_id))
        divisions[team.division].append(team_info)

    context = { 
        'Atlantic':divisions['Atlantic'],
        'Central':divisions['Central'],
        'Northwest':divisions['Northwest'],
        'Pacific':divisions['Pacific'],
        'Southeast':divisions['Southeast'],
        'Southwest':divisions['Southwest']
    }

    return render(request, 'basketball/teams.html',context)



''' team_name,team_abv,team_wins,team_loses,conference,division,conference_rank,
    points_total,assists_total,offensive_rebounds_total,defensive_rebounds_total,
    rebounds_total,blocks_total,steals_total,turnovers_total,personal_fouls_total,
    free_throws_made,free_throws_attempted,three_point_made,three_point_attempted,
    field_goals_made,field_goals_attempted, games_played, team_id, players
'''
def team_page(request,id):
    team = Team.objects.get(team_id=id)

    if not team:
        return HttpResponse("Team DNE")
    else:
        get_players = Player.objects.filter(team_id=id)
        team_players = []

        for p in get_players:
            player = Player.objects.get(player_id=p.player_id)
            if player:
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

                team_players.append(
                    [
                        player.full_name, #"full_name"
                        player.player_id, #"player_id"
                        round(player.points_total/player.games_played,1), #"point_per_game"
                        round(player.assists_total/player.games_played,1), #"assists_per_game"
                        round(player.offensive_rebounds_total/player.games_played,1), #"offensive_rebounds_per_game"
                        round(player.defensive_rebounds_total/player.games_played,1), #"defensive_rebounds_per_game"
                        round(player.rebounds_total/player.games_played,1), #"rebounds_per_game"
                        round(player.blocks_total/player.games_played,1), #"blocks_per_game"
                        round(player.steals_total/player.games_played,1), #"steals_per_game"
                        round(player.turnovers_total/player.games_played,1), #"turnovers_per_game"
                        round(player.personal_fouls_total/player.games_played,1), #"personal_fouls_per_game"
                        round(player.minutes_total/player.games_played,1), #"minutes_per_game"
                        player.games_played, #"games_played"
                        #team_image:find_team_image(team.team_id),
                        player.height, #"height"
                        player.weight, #"weight"
                        player.jersey_number, #"jersey_number"
                        player.player_age, #"player_age"
                        round(player.free_throws_attempted/player.games_played,1), #"free_throws_attempted_per_game"
                        round(player.free_throws_made/player.games_played,1), #"free_throws_made_per_game"
                        free_throw_percentage, #"free_throw_percentage"
                        round(player.three_point_attempted/player.games_played,1), #"three_point_attempted_per_game"
                        round(player.three_point_made/player.games_played,1), #"three_point_made_per_game"
                        three_point_percentage, #"three_point_percentage"
                        round(player.field_goals_attempted/player.games_played,1), #"field_goals_attempted_per_game"
                        round(player.field_goals_made/player.games_played,1), #"field_goals_made_per_game"
                        field_goal_percentage, #"field_goal_percentage"
                        player.position #position
                    ]
                )

        game_log = []
        games = (Game.objects.filter(home_team=team.team_id) | Game.objects.filter(away_team=team.team_id)).order_by('-date')
        for game in games:
            team_stats = game.data['team_stats']
            this_game_log = []
            if team_stats[0]['team_id'] == team.team_id:
                team_index = 0
            else:
                team_index = 1
            
            this_game_log = [
                team_stats[team_index]['FG_made'],team_stats[team_index]['FG_attempted'],
                team_stats[team_index]['3P_made'],team_stats[team_index]['3P_attempted'],
                team_stats[team_index]['FT_made'],team_stats[team_index]['FT_attempted'],
                team_stats[team_index]['off_rebounds'],team_stats[team_index]['def_rebounds'],
                team_stats[team_index]['off_rebounds']+team_stats[team_index]['def_rebounds'],
                team_stats[team_index]['assists'],team_stats[team_index]['steals'],
                team_stats[team_index]['blocks'],team_stats[team_index]['turnovers'],
                team_stats[team_index]['personal_fouls'],team_stats[team_index]['points'],
                game.date.month,game.date.day
            ]

            if team.team_id == game.home_team:
                this_game_log.append(find_team_image(game.away_team))
                this_game_log.append(game.away_team)
                this_game_log.append('vs')
                this_game_log.append(Team.objects.get(team_id=game.away_team).team_abv)
                if game.winning_team_id == game.home_team:
                    this_game_log.append('W')
                    this_game_log.append(game.home_team_score)
                    this_game_log.append(game.away_team_score)
                else:
                    this_game_log.append('L')
                    this_game_log.append(game.away_team_score)
                    this_game_log.append(game.home_team_score)

            else:
                this_game_log.append(find_team_image(game.home_team))
                this_game_log.append(game.home_team)
                this_game_log.append('@')
                this_game_log.append(Team.objects.get(team_id=game.home_team).team_abv)
                if game.winning_team_id == game.away_team:
                    this_game_log.append('W')
                    this_game_log.append(game.away_team_score)
                    this_game_log.append(game.home_team_score)
                else:
                    this_game_log.append('L')
                    this_game_log.append(game.home_team_score)
                    this_game_log.append(game.away_team_score)
                
            this_game_log.append(game.game_id)
            game_log.append(this_game_log)
        
        conference_teams = list(Team.objects.filter(conference=team.conference).order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name'))
        rank = conference_teams.index(team)+1
        context = {
            'team_name':team.team_name,'team_abv':team.team_abv,"team_wins":team.team_wins,"team_losses":team.team_losses,
            'conference':team.conference,'division':team.division,'conference_rank':rank,
            'points_per_game':round(team.points_total/team.games_played,1),
            'assists_per_game':round(team.assists_total/team.games_played,1),
            'offensive_rebounds_per_game':round(team.offensive_rebounds_total/team.games_played,1),
            'defensive_rebounds_per_game':round(team.defensive_rebounds_total/team.games_played,1),
            'rebounds_per_game':round(team.rebounds_total/team.games_played,1),
            'blocks_per_game':round(team.blocks_total/team.games_played,1),
            'steals_per_game':round(team.steals_total/team.games_played,1),
            'turnovers_per_game':round(team.turnovers_total/team.games_played,1),
            'personal_fouls_per_game':round(team.personal_fouls_total/team.games_played,1),
            'free_throws_made_per_game':round(team.free_throws_made/team.games_played,1),
            'free_throws_attempted_per_game':round(team.free_throws_attempted/team.games_played,1),
            'team_free_throw_percentage':round((team.free_throws_made/team.free_throws_made)*100,1),
            'field_goals_made_per_game':round(team.field_goals_made/team.games_played,1),
            'field_goals_attempted_per_game':round(team.field_goals_attempted/team.games_played,1),
            'team_field_goal_percentage':round((team.field_goals_made/team.field_goals_attempted)*100,1),
            'three_point_made_per_game':round(team.three_point_made/team.games_played,1),
            'three_point_attempted_per_game':round(team.three_point_attempted/team.games_played,1),
            'team_three_point_percentage':round((team.three_point_made/team.three_point_attempted)*100,1),
            'games_played':team.games_played,"players":team_players,
            'team_image': find_team_image(team.team_id),'game_log':game_log
        }

    return render(request,'basketball/team_page.html',context)

def standings_page(request):
    all_teams = Team.objects.order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    western = []
    eastern = []

    count_west = 0
    max_wins_west = 0
    losses_west = 0
    count_east = 0
    max_wins_east = 0
    losses_east = 0
    for team in all_teams:
        if team.conference == "West":
            if count_west == 0:
                max_wins_west=team.team_wins
                losses_west = team.team_losses
                print(losses_west)
                games_back = "-"
                count_west += 1
                rank=str(count_west)
            else:
                count_west += 1
                if count_west > 8:
                    games_back = round( (abs(max_wins_west-team.team_wins)+abs(team.team_losses-losses_west))/2 ,1)
                    rank=''
                else:
                    games_back = round( (abs(max_wins_west-team.team_wins)+abs(team.team_losses-losses_west))/2 ,1)
                    rank=str(count_west)
            
            
            western.append([
                team.team_name,
                team.team_wins,
                team.team_losses,
                round((team.team_wins/(team.games_played)),3),
                games_back,
                round((team.points_total/team.games_played),1),
                find_team_image(team.team_id),
                rank,
                team.team_id,
                team.home_wins,
                team.away_wins,
                team.home_losses,
                team.away_losses,
                team.conference_wins,
                team.conference_losses,
                round(team.opponent_points_total/team.games_played,1),
                round(round((team.points_total/team.games_played),1)-round(team.opponent_points_total/team.games_played,1),1),
                team.divisional_wins,
                team.divisional_losses
            ])

        else:
            if count_east == 0:
                max_wins_east=team.team_wins
                losses_east = team.team_losses
                print(losses_east)
                count_east += 1
                games_back = "-"
                rank=str(count_east)
            else:
                count_east += 1
                if count_east > 8:
                    games_back = round( (abs(max_wins_east-team.team_wins)+abs(team.team_losses-losses_east))/2,1)
                    rank=''
                else:
                    games_back = round( (abs(max_wins_east-team.team_wins)+abs(team.team_losses-losses_east))/2,1)
                    print(team.team_name,' ',games_back)
                    rank=str(count_east)
            
            
            eastern.append([
                team.team_name, 
                team.team_wins, 
                team.team_losses,
                round((team.team_wins/(team.games_played)),3),
                games_back, 
                round((team.points_total/team.games_played),1),
                find_team_image(team.team_id),
                rank,
                team.team_id,
                team.home_wins,
                team.away_wins,
                team.home_losses,
                team.away_losses,
                team.conference_wins,
                team.conference_losses,
                round(team.opponent_points_total/team.games_played,1),
                round(round((team.points_total/team.games_played),1)-round(team.opponent_points_total/team.games_played,1),1),
                team.divisional_wins,
                team.divisional_losses
            ])

        #print(western)
        #print(eastern)
        #print('%s %s' % (team.team_name,team.team_wins))
        context = {
            "eastern_teams":eastern,
            "western_teams":western
        }
    return render(request,'basketball/standings.html', context)

def playoffs_page(request):
    all_teams = Team.objects.order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    western = []
    eastern = []

    count_west = 0
    max_wins_west = 0
    losses_west = 0
    count_east = 0
    max_wins_east = 0
    losses_east = 0
    for team in all_teams:
        if team.conference == "West":
            if count_west == 0:
                max_wins_west=team.team_wins
                losses_west = team.team_losses
                print(losses_west)
                games_back = "-"
                count_west += 1
                rank=str(count_west)
            else:
                count_west += 1
                if count_west > 8:
                    games_back = round( (abs(max_wins_west-team.team_wins)+abs(team.team_losses-losses_west))/2 ,1)
                    rank=''
                else:
                    games_back = round( (abs(max_wins_west-team.team_wins)+abs(team.team_losses-losses_west))/2 ,1)
                    rank=str(count_west)
            
            
            western.append([
                team.team_abv,
                team.team_name,
                team.team_id,
                find_team_image(team.team_id)
            ])

        else:
            if count_east == 0:
                max_wins_east=team.team_wins
                losses_east = team.team_losses
                print(losses_east)
                count_east += 1
                games_back = "-"
                rank=str(count_east)
            else:
                count_east += 1
                if count_east > 8:
                    games_back = round( (abs(max_wins_east-team.team_wins)+abs(team.team_losses-losses_east))/2,1)
                    rank=''
                else:
                    games_back = round( (abs(max_wins_east-team.team_wins)+abs(team.team_losses-losses_east))/2,1)
                    print(team.team_name,' ',games_back)
                    rank=str(count_east)
            
            
            eastern.append([
                team.team_abv,
                team.team_name,
                team.team_id,
                find_team_image(team.team_id)
            ])
    post_season_series_west = dict()
    post_season_series_west['round1']={
        'series1':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
        'series2':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
        'series3':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
        'series4':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
    }
    
    first_playoff_date = datetime.date(2020, 4, 17)# first playoff game is scheduled to be 4/18
    for i in range(0,4):
        #print("count: ", i)
        #print("SIZE OF WESTERN OBJ: ", len(western))
        team_id = western[i][2]
#            post_season_series_west['round1']['team_id'] =
        home_team_games = (Game.objects.filter(home_team=team_id) | Game.objects.filter(away_team=team_id)).order_by('date')
        count_games=1
        #post_season_series_west['round1']['series'+str(i+1)] =dict()
        team1_wins = 0
        team2_wins = 0
        for playoff_game in home_team_games:
            if(playoff_game.date > first_playoff_date):
                post_season_series_west['round1']['series'+str(i+1)]['game'+str(count_games)] = str(playoff_game.home_team_score)+"-"+str(playoff_game.away_team_score)
                if playoff_game.home_team_score > playoff_game.away_team_score:
                    team1_wins+=1
                else:
                    team2_wins+=1
                post_season_series_west['round1']['series'+str(i+1)]['matchup']= str(team1_wins)+" : "+str(team2_wins)
                count_games+=1

    post_season_series_east = dict()
    post_season_series_east['round1']={
        'series1':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
        'series2':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
        'series3':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
        'series4':{'matchup':'(0 - 0)', 'revmatchup':'(0 - 0)'},
    }
    first_playoff_date = datetime.date(2020, 4, 17)# first playoff game is scheduled to be 4/18
    for i in range(0,4):
        #print("count: ", i)
        #print("SIZE OF WESTERN OBJ: ", len(western))
        team_id = eastern[i][2]
#            post_season_series_west['round1']['team_id'] =
        home_team_games = (Game.objects.filter(home_team=team_id) | Game.objects.filter(away_team=team_id)).order_by('date')
        count_games=1
        #post_season_series_east['round1']['series'+str(i+1)] =dict()
        team1_wins = 0
        team2_wins = 0
        for playoff_game in home_team_games:
            if(playoff_game.date > first_playoff_date):
                post_season_series_east['round1']['series'+str(i+1)]['game'+str(count_games)] = str(playoff_game.home_team_score)+" - "+str(playoff_game.away_team_score)
                if playoff_game.home_team_score > playoff_game.away_team_score:
                    team1_wins+=1
                else:
                    team2_wins+=1
                post_season_series_east['round1']['series'+str(i+1)]['matchup']= str(team1_wins)+" - "+str(team2_wins)
                count_games+=1

                
        
    print(post_season_series_west,"\n")
    print(post_season_series_east,"\n")
    #print(eastern)
    #print('%s %s' % (team.team_name,team.team_wins))
    context = {
        "eastern_teams":eastern,
        "western_teams":western,
        "west_stats":post_season_series_west,
        "east_stats":post_season_series_east,
    }
    return render(request,'basketball/playoffs.html', context)


def series_page(request, matchup):
    # I pass the two team's IDs as the /basketball/playoff/series/matchup

    # Right now I have the two teams labelled as home_team and away-team
    # This needs to be changed to high_seed/low_seed
    higher_seed_id = int(matchup[0:10])
    lower_seed_id = int(matchup[10:])
    game_number_list = []#number of games should looks like: [1,2,3,4]
    higher_seed_team = Team.objects.filter(team_id=higher_seed_id).first()
    lower_seed_team = Team.objects.filter(team_id=lower_seed_id).first()
    #print(team_away)
    home_team_rank = get_team_playoff_rank(higher_seed_id)# created a hardcoded function please check it out
    away_team_rank = get_team_playoff_rank(lower_seed_id)
    home_team_games = (Game.objects.filter(home_team=higher_seed_id) | Game.objects.filter(away_team=higher_seed_id)).order_by('date')
    first_playoff_date = datetime.date(2020, 4, 17)# first playoff game is scheduled to be 4/18
    playoff_game_data = {}
    series_length= 0
    # getting all playoff games that the higher seeded team has played
    for playoff_game in home_team_games:
        if(playoff_game.date > first_playoff_date and playoff_game.away_team == lower_seed_id):
            # date is either 4/18 or later and the correct "away_team"
            series_length+=1
            playoff_game_data["game" + str(series_length)] = playoff_game
            game_number_list.append(series_length)
            
    home_team_games_scores= []
    away_team_games_scores=[]
    lower_seed_wins = 0
    higher_seed_wins = 0
    num_games = len(playoff_game_data)
    count = 1
    higher_seed_averages={
        'FG':0,'FGP':0,'3FG':0,'3FGP':0,
        'FT':0,'FTP':0,'OREB':0,'DREB':0,
        'REB':0,'AST':0,'STL':0,'BLK':0,
        'TOV':0,'PF':0,'PTS':0
    }
    lower_seed_averages={
        'FG':0,'FGP':0,'3FG':0,'3FGP':0,
        'FT':0,'FTP':0,'OREB':0,'DREB':0,
        'REB':0,'AST':0,'STL':0,'BLK':0,
        'TOV':0,'PF':0,'PTS':0
    }
    #unfortunately have to count backwards
    while num_games > 0:
        #print("Game ", count, ": \n", playoff_game_data[num_games])
        home_team_games_scores.append(playoff_game_data["game"+str(count)].home_team_score)
        away_team_games_scores.append(playoff_game_data["game"+str(count)].away_team_score)
        if playoff_game_data["game"+str(count)].home_team_score > playoff_game_data["game"+str(count)].away_team_score:
            higher_seed_wins+=1
        else:
            lower_seed_wins+=1
        num_games-=1
        count+=1
    while len(home_team_games_scores) < 4:
        home_team_games_scores.append(0)
    while len(away_team_games_scores) < 4:
        away_team_games_scores.append(0)
    #print(higher_seed_wins, "\n", lower_seed_wins)
    
    #print("Game 1: ", playoff_game_data['game1'].data['team_stats'], "\n")
    #print("Game 2: ", playoff_game_data['game2'].data['team_stats'], "\n")
    context=dict()
    context={
        "higher_seed_id":higher_seed_id,
        "lower_seed_id":lower_seed_id,
        "higher_seed_name":higher_seed_team.team_name,
        "lower_seed_name":lower_seed_team.team_name,
        "higher_seed_image":find_team_image(higher_seed_id),
        "lower_seed_image":find_team_image(lower_seed_id),
        "series_length":series_length, 
        "series_games":game_number_list,       
        "higher_seed_abv":higher_seed_team.team_abv,
        "lower_seed_abv":lower_seed_team.team_abv,
        "higher_seed_wins":higher_seed_wins,
        "lower_seed_wins":lower_seed_wins,
        "higher_seed_game_score":home_team_games_scores,
        "lower_seed_game_score":away_team_games_scores,
        "higher_seed_rank":home_team_rank,
        "lower_seed_rank":away_team_rank,
        "playoff_games_data":playoff_game_data,
        "higher_seed_averages":higher_seed_averages,
        "lower_seed_averages":lower_seed_averages
    }
    return render(request, 'basketball/series.html', context)

def mvp_vote(request):
    mvp_poll = MVPPoll.objects.all().first()
    data = mvp_poll.data
    context = {}
    context['players']= []
    for key,values in data:
        context['players'].append([
            key,values['name'],values['team_abv'],find_team_image(values['team_id']),values['team_id']
            
        ])
    
    return render(request,'basketball/mvp_vote.html',context)
    
def mvp_vote_cast(request):
    print('here')
    if request == "POST":
        if not request.POST['player_id']:
            return redirect('basketball/mvp_vote.html')
        else:
            mvp_poll = MVPPoll.objects.all().first()
            data = mvp_poll.data
            
            data[request.POST['player_id']]['votes']+=1
            return reverse(home_views.home)
    else:
        return redirect('basketball/mvp_vote.html')    


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


def get_team_playoff_rank(team_id):
    playoff_teams= {
        1610612747:"1st",#LAL
        1610612746:"2nd",#LAC
        1610612762:"3rd",#UTA
        1610612760:"4th",#OKC
        1610612745:"5th",#HOU
        1610612743:"6th",#DEN
        1610612742:"7th",#DAL
        1610612740:"8th",#NOR
        1610612749:"1st",#MIL
        1610612738:"2nd",#BOS
        1610612761:"3rd",#TOR
        1610612748:"4th",#MIA
        1610612755:"5th",#PHI
        1610612754:"6th",#IND
        1610612751:"7th",#BKN
        1610612764:"8th",#WAS
    }
    return playoff_teams[team_id]

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
        1610612764:"img/washington-wizards.png",
        0:"img/nba_logo.png"
    }
    return list_teams[team_id]
