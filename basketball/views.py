from .models import Player, Game, Team, MVPVote,  Serie, GamePreview
import datetime
from sports_simulator import views as home_views
from .forms import MVPVoteForm, SeriesForm
from pytz import timezone, utc
import pprint
import django_tables2 as tables
from django_tables2 import RequestConfig, A
from django.shortcuts import redirect, render


'''
# creating an instance of  
# datetime.date 
d = datetime(2015, 10, 09, 23, 55, 59, 342380) 
'''

from random import randint
from django.http import HttpResponse
from django.contrib import messages


def home(request):
    if request.method == 'GET':
        #game_date = get_pst_time()
        game_date = datetime.datetime.now().date()
        game_year = str(game_date.year)
        game_month = str(game_date.month) if game_date.month > 9 else '0'+str(game_date.month)
        game_day = str(game_date.day) if game_date.day > 9 else '0'+str(game_date.day)
        return redirect('/basketball/games/'+('%s%s%s' % (game_year,game_month,game_day)))
    elif not request.POST['date']:
        messages.add_message(request, messages.ERROR, 'No date specified')
        game_date = datetime.date.today()
    else:
        date_attr = request.POST['date'].split('/')
        #date(year, month, day)
        #print(date_attr)
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

def get_pst_time():
    date = datetime.datetime.now(tz=utc)
    date = date.astimezone(timezone('US/Pacific')).date()
    return date

def get_games_date(request,game_date):
    
    #date(year, month, day)
    try:
        if request.method == 'POST' and request.POST['date']:
            date_attr = request.POST['date'].split('/')
            
            return redirect('/basketball/games/'+(date_attr[2]+date_attr[0]+date_attr[1]))
            #game_date = datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
            
        else:
            date_attr = str(game_date)
            if len(date_attr) != 8:
                raise TypeError
            game_date = datetime.date(int(date_attr[0:4]),int(date_attr[4:6]),int(date_attr[6:]))

    except:
        messages.add_message(request, messages.ERROR, 'Error in processing the date specified')
        game_date = datetime.date.today()
        return render(request, 'basketball/games.html')

    #today = get_pst_time()
    today = datetime.datetime.now().date()
    #print(today)
    #print(game_date)
    context = {}
    context['games'] = []
    context['date']='%s/%s/%s' % (game_date.month,game_date.day,game_date.year)
    if today < game_date or (today <= game_date and datetime.datetime.now().hour < 14):
        game_previews = GamePreview.objects.filter(game_date=game_date)
        for game in game_previews:
            previous_playoff_games = (Game.objects.filter(home_team=game.home_team_id,away_team=game.away_team_id,date__gte=datetime.date(2020,5,1))
                            | Game.objects.filter(away_team=game.home_team_id,home_team=game.away_team_id,date__gte=datetime.date(2020,5,1))).order_by('date')
            
            home_series_wins = 0
            away_series_wins = 0
            for g in previous_playoff_games:
                if g.winning_team_id == game.home_team_id:
                    home_series_wins += 1
                else:
                    away_series_wins += 1
                    
            series = (Serie.objects.filter(higher_seed_id=game.home_team_id,lower_seed_id=game.away_team_id)
                            | Serie.objects.filter(higher_seed_id=game.away_team_id,lower_seed_id=game.home_team_id))[0]
     
            this_game = [
                game.home_team_name,
                game.away_team_name,
                game.votes_home_team,
                game.votes_home_away,
                game.game_preview_id,
                find_team_image(game.home_team_id),
                find_team_image(game.away_team_id),
                Team.objects.get(team_id=game.higher_seeding_id).team_abv,
                Team.objects.get(team_id=game.lower_seeding_id).team_abv,
                series.higher_seed_wins,
                series.lower_seed_wins,
                game.higher_seeding_id,
                game.lower_seeding_id,
                Team.objects.get(team_id=game.home_team_id).team_abv,
                Team.objects.get(team_id=game.away_team_id).team_abv,
                game.home_team_id,
                game.away_team_id
            ]
            context['games'].append(this_game)
        
        return render(request, 'basketball/game_previews.html',context)
            
    else:
        games = Game.objects.filter(date=game_date) 
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
    try:
         player = Player.objects.get(player_id=id)
    except:
        return render(request,"error_request.html")
    
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

def series_vote_results(request):
                
    series = Serie.objects.all()
    context = {}
    count = 1
    for serie in series:
        name_l = 'labels'+str(count)
        name_d = 'data'+str(count)
        data = [
            serie.votes_higher_seed+1,
            serie.votes_lower_seed+1
        ]
        labels = [
            serie.higher_seed_name,
            serie.lower_seed_name
        ]
        context[name_l]=labels
        context[name_d]=data
        count +=1
    
    #pprint.pprint(context)
    return render(request,'basketball/series_votes_results.html', context)
    #return HttpResponse("Thanks")

def series_vote(request):
    if request.method == 'POST':
        #print(request.POST)
        form = SeriesForm(request.POST)
        if form.is_valid():
            name = 'form'
            count = 1
            while name in request.POST:
                items = request.POST[name].split(' ')
                series = Serie.objects.get(series_id=int(items[1]))
                if int(items[0])==series.higher_seed_id:
                    series.votes_higher_seed+=1
                    series.save()
                else:
                    series.votes_lower_seed+=1
                    series.save()
                name = 'form'+str(count)
                count += 1
            return redirect('/basketball/series_vote_results')
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data')
            formset = SeriesForm()
            return render(request,'basketball/vote_for_series.html',{'form':formset})
        #return HttpResponse("Thanks")
    
    formset = SeriesForm()
    return render(request,'basketball/vote_for_series.html',{'form':formset})


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
    
    if id > 9223372036854775807:
        return render(request,"error_request.html")
    
    if id < 10000:
        return preview_game_page(request,id,True)
    
    game = Game.objects.filter(game_id=id)
    if len(game) == 0:
        return render(request,"error_request.html")
    
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
        "home_team_abv": Team.objects.get(team_id=game.home_team).team_abv,
        "away_team_abv": Team.objects.get(team_id=game.away_team).team_abv,
        "home_team_record":game.home_team_record, "away_team_record":game.away_team_record,
        "home_team_id":game.home_team,"away_team_id":game.away_team,"num_overtimes":range(1,num_ots+1),
        "date": '%s/%s/%s' % (game.date.month,game.date.day,game.date.year)
    }

    return render(request,'basketball/game_page.html',context)

def preview_game_page(request,id,add_form):
    if id > 9223372036854775807:
        return render(request,"error_request.html")
    game = GamePreview.objects.get(game_preview_id=id)
    print(game)
    if game.game_date < datetime.datetime.now().date() or (game.game_date < datetime.datetime.now().date() and datetime.datetime.now().hour > 14): #get_pst_time():
        print("here")
        return render(request,"error_request.html")
     
    #previous_playoff_games = (Game.objects.filter(home_team=game.home_team_id,away_team=game.away_team_id,date__gte=datetime.date(2020,5,1))
                            #| Game.objects.filter(away_team=game.home_team_id,home_team=game.away_team_id,date__gte=datetime.date(2020,5,1))).order_by('date')
            
    #home_series_wins = 0
    #away_series_wins = 0
    #for g in previous_playoff_games:
    #    if g.winning_team_id == game.home_team_id:
    #        home_series_wins += 1
    #    else:
    #        away_series_wins += 1
    
    previous_games = (Game.objects.filter(home_team=game.home_team_id,away_team=game.away_team_id)
                            | Game.objects.filter(away_team=game.home_team_id,home_team=game.away_team_id)).order_by('-date')
    
    previous_game_scores = []
    for g in previous_games:
        previous_game_scores.append([g.home_team_score,
                                     g.away_team_score,
                                     Team.objects.get(team_id=g.home_team).team_abv,
                                     Team.objects.get(team_id=g.away_team).team_abv,
                                     game.home_team_id,
                                     game.away_team_id,
                                     g.game_id,
                                     '%s/%s/%s' % (g.date.month,g.date.day,g.date.year),
                                     find_team_image(g.home_team),
                                     find_team_image(g.away_team)
        ]),

        
    team_away = Team.objects.get(team_id=game.away_team_id)
    away_abv = team_away.team_abv
    away_team_stats = [ 
        team_away.team_name,team_away.team_abv,
        team_away.team_wins,team_away.team_losses,
        round(team_away.points_total/team_away.games_played,1),
        round(team_away.assists_total/team_away.games_played,1),
        round(team_away.offensive_rebounds_total/team_away.games_played,1),
        round(team_away.defensive_rebounds_total/team_away.games_played,1),
        round(team_away.rebounds_total/team_away.games_played,1),
        round(team_away.blocks_total/team_away.games_played,1),
        round(team_away.steals_total/team_away.games_played,1),
        round(team_away.turnovers_total/team_away.games_played,1),
        round(team_away.personal_fouls_total/team_away.games_played,1),
        round(team_away.free_throws_made/team_away.games_played,1),
        round(team_away.free_throws_attempted/team_away.games_played,1),
        round((team_away.free_throws_made/team_away.free_throws_attempted)*100,1),
        round(team_away.field_goals_made/team_away.games_played,1),
        round(team_away.field_goals_attempted/team_away.games_played,1),
        round((team_away.field_goals_made/team_away.field_goals_attempted)*100,1),
        round(team_away.three_point_made/team_away.games_played,1),
        round(team_away.three_point_attempted/team_away.games_played,1),
        round((team_away.three_point_made/team_away.three_point_attempted)*100,1),
        round((team_away.points_total/team_away.games_played),1),
        team_away.games_played,
    ]
    
    team_home = Team.objects.get(team_id=game.home_team_id)
    home_abv = team_home.team_abv
    home_team_stats = [ 
        team_home.team_name,team_home.team_abv,
        team_home.team_wins,team_home.team_losses,
        round(team_home.points_total/team_home.games_played,1),
        round(team_home.assists_total/team_home.games_played,1),
        round(team_home.offensive_rebounds_total/team_home.games_played,1),
        round(team_home.defensive_rebounds_total/team_home.games_played,1),
        round(team_home.rebounds_total/team_home.games_played,1),
        round(team_home.blocks_total/team_home.games_played,1),
        round(team_home.steals_total/team_home.games_played,1),
        round(team_home.turnovers_total/team_home.games_played,1),
        round(team_home.personal_fouls_total/team_home.games_played,1),
        round(team_home.free_throws_made/team_home.games_played,1),
        round(team_home.free_throws_attempted/team_home.games_played,1),
        round((team_home.free_throws_made/team_home.free_throws_attempted)*100,1),
        round(team_home.field_goals_made/team_home.games_played,1),
        round(team_home.field_goals_attempted/team_home.games_played,1),
        round((team_home.field_goals_made/team_home.field_goals_attempted)*100,1),
        round(team_home.three_point_made/team_home.games_played,1),
        round(team_home.three_point_attempted/team_home.games_played,1),
        round((team_home.three_point_made/team_home.three_point_attempted)*100,1),
        round((team_home.points_total/team_home.games_played),1),
        team_home.games_played,
    ]
    
    series = (Serie.objects.filter(higher_seed_id=game.home_team_id,lower_seed_id=game.away_team_id)
                            | Serie.objects.filter(higher_seed_id=game.away_team_id,lower_seed_id=game.home_team_id))[0]
     
    context={}
    context['away_team_stats']=away_team_stats
    context['home_team_stats']=home_team_stats
    context['higher_seed_wins']=series.higher_seed_wins
    context['lower_seed_wins']=series.lower_seed_wins
    context['higher_seed_abv']=series.higher_seed_abv
    context['lower_seed_abv']=series.lower_seed_abv
    context['higher_seed_id']=series.higher_seed_id
    context['lower_seed_id']=series.lower_seed_id
    context['prev_games']=previous_game_scores
    context['home_team_id']=game.home_team_id
    context['away_team_id']=game.away_team_id
    context['home_abv']=home_abv
    context['away_abv']=away_abv
    context['home_team_image']=find_team_image(game.home_team_id)
    context['away_team_image']=find_team_image(game.away_team_id)
    context['home_team_name']=game.home_team_name
    context['away_team_name']=game.away_team_name
    context['date']='%s/%s/%s' % (game.game_date.month,game.game_date.day,game.game_date.year)
    context['game_id']=game.game_preview_id
    context['game_number']=game.game_number
    context['is_necessary'] = game.is_necessary
    
    return render(request,'basketball/game_preview.html',context)


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
    list_teams = {
        1610612737:True,
        1610612738:True,
        1610612751:True,
        1610612766:True,
        1610612741:True,
        1610612739:True,
        1610612742:True,
        1610612743:True,
        1610612765:True,
        1610612744:True,
        1610612745:True,
        1610612754:True,
        1610612746:True,
        1610612747:True,
        1610612763:True,
        1610612748:True,
        1610612749:True,
        1610612750:True,
        1610612740:True,
        1610612752:True,
        1610612760:True,
        1610612753:True,
        1610612755:True,
        1610612756:True,
        1610612757:True,
        1610612758:True,
        1610612759:True,
        1610612761:True,
        1610612762:True,
        1610612764:True,
    }
    if id not in list_teams:
        return render(request,"error_request.html")
    team = Team.objects.get(team_id=id)

    if not team:
        return render(request,"error_request.html")
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
            'team_image': find_team_image(team.team_id),'game_log':game_log,
            'team_id':team.team_id
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
                #print(losses_west)
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
                #print(losses_east)
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
                    #print(team.team_name,' ',games_back)
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
    context = {}

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
                #print(losses_west)
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
                #print(losses_east)
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
                    #print(team.team_name,' ',games_back)
                    rank=str(count_east)
            
            
            eastern.append([
                team.team_abv,
                team.team_name,
                team.team_id,
                find_team_image(team.team_id)
            ])
    
    matchups_west = [
        [western[0],western[7]],[western[3],western[4]],
        [western[2],western[5]],[western[1],western[6]]
    ]
    matchups_east = [
        [eastern[0],eastern[7]],[eastern[3],eastern[4]],
        [eastern[2],eastern[5]],[eastern[1],eastern[6]]
    ]
    
    context['west']= {}
    context['west']['round1']= {}
    context['west']['round1']['series1']= {}
    context['west']['round1']['series2']= {}
    context['west']['round1']['series3']= {}
    context['west']['round1']['series4']= {}
    #round1 West
    for i in range(1,5):
        previous_playoff_games = (Game.objects.filter(home_team=matchups_west[i-1][0][2],away_team=matchups_west[i-1][1][2],date__gte=datetime.date(2020,5,1))
                        | Game.objects.filter(away_team=matchups_west[i-1][0][2],home_team=matchups_west[i-1][1][2],date__gte=datetime.date(2020,5,1))).order_by('date')
        
        series = Serie.objects.filter(higher_seed_id=matchups_west[i-1][0][2],lower_seed_id=matchups_west[i-1][1][2])[0]
        context['west']['round1']['series'+str(i)]['series_id']=series.series_id
        context['west']['round1']['series'+str(i)]['higher_seed_wins']=series.higher_seed_wins
        context['west']['round1']['series'+str(i)]['higher_seed_losses']=series.higher_seed_loses
        context['west']['round1']['series'+str(i)]['lower_seed_wins']=series.lower_seed_wins
        context['west']['round1']['series'+str(i)]['lower_seed_losses']=series.lower_seed_loses
        
        count=1
        game_str='game'
        for game in previous_playoff_games:
            context['west']['round1']['series'+str(i)]['game'+str(count)]={}
            context['west']['round1']['series'+str(i)]['game'+str(count)]['id']=game.game_id
            #print(matchups_west[i][0][2])
            if matchups_west[i-1][0][2] == game.home_team:
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.home_team_score
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.away_team_score
            else:
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.away_team_score
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.home_team_score
                
            count += 1
    
    context['east']= {}
    context['east']['round1']= {}
    context['east']['round1']['series1']= {}
    context['east']['round1']['series2']= {}
    context['east']['round1']['series3']= {}
    context['east']['round1']['series4']= {}
    #round1 east
    for i in range(1,5):
        
        previous_playoff_games = (Game.objects.filter(home_team=matchups_east[i-1][0][2],away_team=matchups_east[i-1][1][2],date__gte=datetime.date(2020,5,1),is_playoff=True)
                        | Game.objects.filter(away_team=matchups_east[i-1][0][2],home_team=matchups_east[i-1][1][2],date__gte=datetime.date(2020,5,1),is_playoff=True)).order_by('date')
        
        series = Serie.objects.filter(higher_seed_id=matchups_east[i-1][0][2],lower_seed_id=matchups_east[i-1][1][2])[0]
        context['east']['round1']['series'+str(i)]['series_id']=series.series_id
        context['east']['round1']['series'+str(i)]['higher_seed_wins']=series.higher_seed_wins
        context['east']['round1']['series'+str(i)]['higher_seed_losses']=series.higher_seed_loses
        context['east']['round1']['series'+str(i)]['lower_seed_wins']=series.lower_seed_wins
        context['east']['round1']['series'+str(i)]['lower_seed_losses']=series.lower_seed_loses
        
        count = 1
        game_str='game'+str(count)
        for game in previous_playoff_games:
            context['east']['round1']['series'+str(i)]['game'+str(count)]={}
            context['east']['round1']['series'+str(i)]['game'+str(count)]['series_id']=game.game_id
            if matchups_east[i-1][0][2] == game.home_team:
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.home_team_score
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.away_team_score
            else:
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.away_team_score
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.home_team_score
                
            count += 1    
                
        
    #print(context['east'],"\n")
    #print(context['west'],"\n")

    context['eastern_teams']=eastern
    context['western_teams']=western

    return render(request,'basketball/playoffs.html', context)



def series_page(request, id):
    
    if id > 9223372036854775807:
        return render(request,"error_request.html")
    
    series_check = Serie.objects.filter(series_id=id)
    if len(series_check) == 0:
        return render(request,"error_request.html")

    series = Serie.objects.get(series_id=id)
    count=1
    game_score = 'game_score'
    game_str = 'game'
    higher_seed_scores = []
    lower_seed_scores = []
    
    # getting all playoff games that the higher seeded team has played
    context={}
    higher_seed_stats=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    lower_seed_stats=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    if series.game_ids != "": 
        for key,this_game_id in series.game_ids.items(): #need to have game1,game2,... in series model
            context[game_score+str(count)] = ' '
            game = Game.objects.get(game_id=this_game_id)
            context[game_str+str(count)] = game.game_id
            if game.home_team == series.higher_seed_id:
                lower_seed_scores.append(game.away_team_score)     
                higher_seed_scores.append(game.home_team_score)

            else:
                lower_seed_scores.append(game.home_team_score)     
                higher_seed_scores.append(game.away_team_score)
            count+=1
            
            team_stats = game.data['team_stats']
            higher_seed_team = 1
            lower_seed_team = 1
            if team_stats[0]['team_id']==series.higher_seed_id:
                higher_seed_team = 0
            else:
                lower_seed_team = 0

            higher_seed_stats[0] += team_stats[higher_seed_team]['FG_made']
            higher_seed_stats[1] += team_stats[higher_seed_team]["FG_attempted"]
            higher_seed_stats[2] += team_stats[higher_seed_team]['3P_made']
            higher_seed_stats[3] += team_stats[higher_seed_team]["3P_attempted"]
            higher_seed_stats[4] += team_stats[higher_seed_team]['FT_made']
            higher_seed_stats[5] += team_stats[higher_seed_team]["FT_attempted"]
            higher_seed_stats[6] += (team_stats[higher_seed_team]['off_rebounds']+team_stats[higher_seed_team]["def_rebounds"])
            higher_seed_stats[7] += team_stats[higher_seed_team]['off_rebounds']
            higher_seed_stats[8] += team_stats[higher_seed_team]["def_rebounds"]
            higher_seed_stats[9] += team_stats[higher_seed_team]['assists']
            higher_seed_stats[10] += team_stats[higher_seed_team]['steals']
            higher_seed_stats[11] += team_stats[higher_seed_team]['blocks']
            higher_seed_stats[12] += team_stats[higher_seed_team]['turnovers']
            higher_seed_stats[13] += team_stats[higher_seed_team]['personal_fouls']
            higher_seed_stats[14] += team_stats[higher_seed_team]['points']

            lower_seed_stats[0] += team_stats[lower_seed_team]['FG_made']
            lower_seed_stats[1] += team_stats[lower_seed_team]["FG_attempted"]
            lower_seed_stats[2] += team_stats[lower_seed_team]['3P_made']
            lower_seed_stats[3] += team_stats[lower_seed_team]["3P_attempted"]
            lower_seed_stats[4] += team_stats[lower_seed_team]['FT_made']
            lower_seed_stats[5] += team_stats[lower_seed_team]["FT_attempted"]
            lower_seed_stats[6] += (team_stats[lower_seed_team]['off_rebounds']+team_stats[lower_seed_team]["def_rebounds"])
            lower_seed_stats[7] += team_stats[lower_seed_team]['off_rebounds']
            lower_seed_stats[8] += team_stats[lower_seed_team]["def_rebounds"]
            lower_seed_stats[9] += team_stats[lower_seed_team]['assists']
            lower_seed_stats[10] += team_stats[lower_seed_team]['steals']
            lower_seed_stats[11] += team_stats[lower_seed_team]['blocks']
            lower_seed_stats[12] += team_stats[lower_seed_team]['turnovers']
            lower_seed_stats[13] += team_stats[lower_seed_team]['personal_fouls']
            lower_seed_stats[14] += team_stats[lower_seed_team]['points']
        
        if series.games_played > 0:    
            for i in range(0,len(higher_seed_stats)):
                higher_seed_stats[i]/=series.games_played
                higher_seed_stats[i]=round(higher_seed_stats[i],1)
                lower_seed_stats[i]/=series.games_played
                lower_seed_stats[i]=round(lower_seed_stats[i],1)
        
    #home_team_stats.append(round((home_team_stats[home_team]['FG_made']/team_stats[home_team]["FG_attempted"])*100,1))
    #round((team_stats[home_team]['3P_made']/team_stats[home_team]["3P_attempted"])*100,1),
    #round((team_stats[home_team]['FT_made']/team_stats[home_team]["FT_attempted"])*100,1),
    
    higher_seed_teams = Team.objects.filter(conference=Team.objects.get(team_id=series.higher_seed_id).conference).order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    higher_seed_rank = 1
    for t in higher_seed_teams:
        if t.team_id == series.higher_seed_id:
            break
        else:
            higher_seed_rank += 1
            
    lower_seed_teams = Team.objects.filter(conference=Team.objects.get(team_id=series.lower_seed_id).conference).order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    lower_seed_rank = 1
    for t in lower_seed_teams:
        if t.team_id == series.lower_seed_id:
            break
        else:
            lower_seed_rank += 1

    context["higher_seed_id"]=series.higher_seed_id
    context["lower_seed_id"]=series.lower_seed_id
    context["higher_seed_name"]=series.higher_seed_name
    context["lower_seed_name"]=series.lower_seed_name
    context["higher_seed_image"]=find_team_image(series.higher_seed_id)
    context["lower_seed_image"]=find_team_image(series.lower_seed_id)    
    context["higher_seed_abv"]=series.higher_seed_abv
    context["lower_seed_abv"]=series.lower_seed_abv
    context["higher_seed_wins"]=series.higher_seed_wins
    context["lower_seed_wins"]=series.lower_seed_wins
    context["higher_seed_losses"]=series.higher_seed_loses
    context["lower_seed_losses"]=series.lower_seed_loses
    context["higher_seed_rank"]=higher_seed_rank
    context["lower_seed_rank"]=lower_seed_rank
    context["higher_seed_stats"]=higher_seed_stats
    context["lower_seed_stats"]=lower_seed_stats
    context["games_played"]=series.games_played
    context['lower_seed_scores']=lower_seed_scores
    context['higher_seed_scores']=higher_seed_scores
    context['series_id']=series.series_id
        
    return render(request, 'basketball/series.html', context)


def mvp_vote(request):
    if request.method == 'POST':
        form = MVPVoteForm(request.POST)
        #print(form.data)
        if form.is_valid():
            mvp_player = MVPVote.objects.get(player_id=form.data['VOTE_FOR_MVP'])
            #print(mvp_player)
            mvp_player.votes+=1
            mvp_player.save()
                    
            return redirect('/basketball/mvp_results')
    #return render(request,'basketball/mvp_vote.html',context)
    form = MVPVoteForm()
    #print(form.CHOICES)
    labels=[]
    data=[]
    
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')[3:]
    other_votes = 0
    for p in mvp_poll:
        other_votes += p.votes
        if p.votes == 0:
            break
    
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')[:3]
    
    for player in mvp_poll:
        labels.append(player.player_name)
        data.append(player.votes)
    labels.append('Other')
    data.append(other_votes)
    return render(request,'basketball/mvp_vote.html', {"form":form,'labels': labels,'data': data, })  

def mvp_results(request):
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')
    labels=[]
    data=[]
    
    for player in mvp_poll[:10]:
        labels.append(player.player_name)
        data.append(player.votes)
    
    other_votes = 0
    for player in mvp_poll[10:]:
        other_votes += player.votes
        if player.votes == 0:
            break
        
    labels.append('Other')
    data.append(other_votes)
    
    rest = []
    for player in mvp_poll:
        team_id = Player.objects.get(player_id=player.player_id).team_id
        team_image=find_team_image(team_id)
        rest.append([player.player_name,player.team_abv,team_id,str(player.votes),str(team_image),player.player_id])
        
    return render(request,'basketball/mvp_votes_results.html',context={
                                                                    'top_players':rest,
                                                                    'labels': labels,
                                                                    'data': data    })
    

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

def sort_func(p):
    return p.points_total/p.games_played


class PlayerTable(tables.Table):
    name = tables.LinkColumn('player_page',args=[A('player_id')],attrs={"th":{"id":"first_col"},"td":{"id":"first_col"}})
    team_abv = tables.Column(verbose_name="Team",orderable=False)
    GP = tables.Column()
    MIN = tables.Column()
    PTS = tables.Column()
    FGM = tables.Column()
    FGA = tables.Column()
    FGP = tables.Column(verbose_name="FG%")
    TPM = tables.Column()
    TPA = tables.Column(verbose_name="3PA")
    TPP = tables.Column(verbose_name="3P%")
    FTA = tables.Column()
    FTM = tables.Column()
    FTP = tables.Column(verbose_name="FT%")
    ORB = tables.Column()
    DRB = tables.Column()
    RB = tables.Column()
    AST = tables.Column()
    BLK = tables.Column()
    STL = tables.Column()
    TO = tables.Column()
    PF = tables.Column()
    
    class Meta:
        attrs = {"class": "table-sm table-striped table-light"}

class PlayerTableMobile(tables.Table):
    name = tables.LinkColumn('player_page',args=[A('player_id')],attrs={"th":{"id":"first_col"},"td":{"id":"first_col"}})
    team_abv = tables.Column(verbose_name="Team",orderable=False)
    GP = tables.Column(verbose_name="GP")
    MIN = tables.Column()
    PTS = tables.Column()
    FGM = tables.Column()
    FGA = tables.Column()
    FGP = tables.Column(verbose_name="FG%")
    TPM = tables.Column(verbose_name="3PM")
    TPA = tables.Column(verbose_name="3PA")
    TPP = tables.Column(verbose_name="3P%")
    FTA = tables.Column()
    FTM = tables.Column()
    FTP = tables.Column(verbose_name="FT%")
    ORB = tables.Column()
    DRB = tables.Column()
    RB = tables.Column()
    AST = tables.Column()
    BLK = tables.Column()
    STL = tables.Column()
    TO = tables.Column()
    PF = tables.Column()
    
    class Meta:
        attrs = {"class": "table-sm table-striped table-light","border-collapse": "separate"}
    
def stats_leaders(request):
    players = Player.objects.all()
    players = sorted(players, reverse=True, key=sort_func)
    
    context = {}
    context["players"] = []
    
    for player in players:
        if player.games_played > 1:
            player_stats = {}
            player_stats['MIN']=round(player.minutes_total/player.games_played,1)
            player_stats['PTS']=round(player.points_total/player.games_played,1)
            player_stats['FGA']=round(player.field_goals_attempted/player.games_played,1)
            player_stats['FGM']=round(player.field_goals_made/player.games_played,1)
            if player.field_goals_attempted > 0:
                player_stats['FGP']=round((player.field_goals_made/player.field_goals_attempted)*100,1)
            else:
                player_stats['FGP']=0.0
            player_stats['FTA']=round(player.free_throws_attempted/player.games_played,1)
            player_stats['FTM']=round(player.free_throws_made/player.games_played,1)
            if player.free_throws_attempted > 0:
                player_stats['FTP']=round((player.free_throws_made/player.free_throws_attempted)*100,1)
            else:
                player_stats['FTP']=0.0
            player_stats['TPA']=round(player.three_point_attempted/player.games_played,1)
            player_stats['TPM']=round(player.three_point_made/player.games_played,1)
            if player.three_point_attempted > 0:
                player_stats['TPP']=round((player.three_point_made/player.three_point_attempted)*100,1)
            else:
                player_stats['TPP']=0.0
            player_stats['AST']=round(player.assists_total/player.games_played,1)
            player_stats['BLK']=round(player.blocks_total/player.games_played,1)
            player_stats['STL']=round(player.steals_total/player.games_played,1)
            player_stats['TO']=round(player.turnovers_total/player.games_played,1)
            player_stats['PF']=round(player.personal_fouls_total/player.games_played,1)
            player_stats['ORB']=round(player.offensive_rebounds_total/player.games_played,1)
            player_stats['DRB']=round(player.defensive_rebounds_total/player.games_played,1)
            player_stats['RB']=round((player.defensive_rebounds_total+player.offensive_rebounds_total)/player.games_played,1)
            player_stats['player_id']=player.player_id
            player_stats['team_id'] = player.team_id
            player_stats['name'] = player.full_name
            player_stats['GP'] = player.games_played
            if player.team_id == 0:
                player_stats['team_abv']="FA"
            else:
                player_stats['team_abv'] = Team.objects.get(team_id=player.team_id).team_abv

            #player_stats['name'] = player_stats['name'] + " " + player_stats['team_abv']
            context['players'].append(player_stats)
            
    table=PlayerTable(context['players'])
    RequestConfig(request,paginate={"per_page": 100}).configure(table)
    context['table']=table
    
    return render(request,"basketball/stat_leaders.html",context)

'''

MOBILE


'''


def stats_leaders_mobile(request):
    players = Player.objects.all()
    players = sorted(players, reverse=True, key=sort_func)
    
    context = {}
    context["players"] = []
    
    for player in players:
        if player.games_played > 1:
            player_stats = {}
            player_stats['MIN']=round(player.minutes_total/player.games_played,1)
            player_stats['PTS']=round(player.points_total/player.games_played,1)
            player_stats['FGA']=round(player.field_goals_attempted/player.games_played,1)
            player_stats['FGM']=round(player.field_goals_made/player.games_played,1)
            if player.field_goals_attempted > 0:
                player_stats['FGP']=round((player.field_goals_made/player.field_goals_attempted)*100,1)
            else:
                player_stats['FGP']=0.0
            player_stats['FTA']=round(player.free_throws_attempted/player.games_played,1)
            player_stats['FTM']=round(player.free_throws_made/player.games_played,1)
            if player.free_throws_attempted > 0:
                player_stats['FTP']=round((player.free_throws_made/player.free_throws_attempted)*100,1)
            else:
                player_stats['FTP']=0.0
            player_stats['TPA']=round(player.three_point_attempted/player.games_played,1)
            player_stats['TPM']=round(player.three_point_made/player.games_played,1)
            if player.three_point_attempted > 0:
                player_stats['TPP']=round((player.three_point_made/player.three_point_attempted)*100,1)
            else:
                player_stats['TPP']=0.0
            player_stats['AST']=round(player.assists_total/player.games_played,1)
            player_stats['BLK']=round(player.blocks_total/player.games_played,1)
            player_stats['STL']=round(player.steals_total/player.games_played,1)
            player_stats['TO']=round(player.turnovers_total/player.games_played,1)
            player_stats['PF']=round(player.personal_fouls_total/player.games_played,1)
            player_stats['ORB']=round(player.offensive_rebounds_total/player.games_played,1)
            player_stats['DRB']=round(player.defensive_rebounds_total/player.games_played,1)
            player_stats['RB']=round((player.defensive_rebounds_total+player.offensive_rebounds_total)/player.games_played,1)
            player_stats['player_id']=player.player_id
            player_stats['team_id'] = player.team_id
            player_stats['name'] = player.full_name
            player_stats['GP'] = player.games_played
            player_stats['a'] = ' '
            player_stats['b'] = ' '
            player_stats['c'] = ' '
            player_stats['d'] = ' '
            player_stats['e'] = ' '
        
            if player.team_id == 0:
                player_stats['team_abv']="FA"
            else:
                player_stats['team_abv'] = Team.objects.get(team_id=player.team_id).team_abv

            #player_stats['name'] = player_stats['name'] + " " + player_stats['team_abv']
            context['players'].append(player_stats)
        
    table=PlayerTableMobile(context['players'])
    RequestConfig(request,paginate={"per_page": 25}).configure(table)
    context['table']=table
    
    return render(request,"basketball/stat_leaders_mobile.html",context)

def team_page_mobile(request,id):
    list_teams = {
        1610612737:True,
        1610612738:True,
        1610612751:True,
        1610612766:True,
        1610612741:True,
        1610612739:True,
        1610612742:True,
        1610612743:True,
        1610612765:True,
        1610612744:True,
        1610612745:True,
        1610612754:True,
        1610612746:True,
        1610612747:True,
        1610612763:True,
        1610612748:True,
        1610612749:True,
        1610612750:True,
        1610612740:True,
        1610612752:True,
        1610612760:True,
        1610612753:True,
        1610612755:True,
        1610612756:True,
        1610612757:True,
        1610612758:True,
        1610612759:True,
        1610612761:True,
        1610612762:True,
        1610612764:True,
    }
    if id not in list_teams:
        return render(request,"error_request.html")
    team = Team.objects.get(team_id=id)

    if not team:
        return render(request,"error_request.html")
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
            'team_image': find_team_image(team.team_id),'game_log':game_log,
            'team_id':team.team_id
        }

    return render(request,'basketball/team_page_mobile.html',context)


def playoffs_page_mobile(request):
    all_teams = Team.objects.order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    western = []
    eastern = []
    context = {}

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
                #print(losses_west)
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
                #print(losses_east)
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
                    #print(team.team_name,' ',games_back)
                    rank=str(count_east)
            
            
            eastern.append([
                team.team_abv,
                team.team_name,
                team.team_id,
                find_team_image(team.team_id)
            ])
    
    matchups_west = [
        [western[0],western[7]],[western[3],western[4]],
        [western[2],western[5]],[western[1],western[6]]
    ]
    matchups_east = [
        [eastern[0],eastern[7]],[eastern[3],eastern[4]],
        [eastern[2],eastern[5]],[eastern[1],eastern[6]]
    ]
    
    context['west']= {}
    context['west']['round1']= {}
    context['west']['round1']['series1']= {}
    context['west']['round1']['series2']= {}
    context['west']['round1']['series3']= {}
    context['west']['round1']['series4']= {}
    #round1 West
    for i in range(1,5):
        previous_playoff_games = (Game.objects.filter(home_team=matchups_west[i-1][0][2],away_team=matchups_west[i-1][1][2],date__gte=datetime.date(2020,5,1))
                        | Game.objects.filter(away_team=matchups_west[i-1][0][2],home_team=matchups_west[i-1][1][2],date__gte=datetime.date(2020,5,1))).order_by('date')
        
        series = Serie.objects.filter(higher_seed_id=matchups_west[i-1][0][2],lower_seed_id=matchups_west[i-1][1][2])[0]
        context['west']['round1']['series'+str(i)]['series_id']=series.series_id
        context['west']['round1']['series'+str(i)]['higher_seed_wins']=series.higher_seed_wins
        context['west']['round1']['series'+str(i)]['higher_seed_losses']=series.higher_seed_loses
        context['west']['round1']['series'+str(i)]['lower_seed_wins']=series.lower_seed_wins
        context['west']['round1']['series'+str(i)]['lower_seed_losses']=series.lower_seed_loses
        
        count=1
        game_str='game'
        for game in previous_playoff_games:
            context['west']['round1']['series'+str(i)]['game'+str(count)]={}
            context['west']['round1']['series'+str(i)]['game'+str(count)]['id']=game.game_id
            #print(matchups_west[i][0][2])
            if matchups_west[i-1][0][2] == game.home_team:
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.home_team_score
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.away_team_score
            else:
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.away_team_score
                context['west']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.home_team_score
                
            count += 1
    
    context['east']= {}
    context['east']['round1']= {}
    context['east']['round1']['series1']= {}
    context['east']['round1']['series2']= {}
    context['east']['round1']['series3']= {}
    context['east']['round1']['series4']= {}
    #round1 east
    for i in range(1,5):
        
        previous_playoff_games = (Game.objects.filter(home_team=matchups_east[i-1][0][2],away_team=matchups_east[i-1][1][2],date__gte=datetime.date(2020,5,1),is_playoff=True)
                        | Game.objects.filter(away_team=matchups_east[i-1][0][2],home_team=matchups_east[i-1][1][2],date__gte=datetime.date(2020,5,1),is_playoff=True)).order_by('date')
        
        series = Serie.objects.filter(higher_seed_id=matchups_east[i-1][0][2],lower_seed_id=matchups_east[i-1][1][2])[0]
        context['east']['round1']['series'+str(i)]['series_id']=series.series_id
        context['east']['round1']['series'+str(i)]['higher_seed_wins']=series.higher_seed_wins
        context['east']['round1']['series'+str(i)]['higher_seed_losses']=series.higher_seed_loses
        context['east']['round1']['series'+str(i)]['lower_seed_wins']=series.lower_seed_wins
        context['east']['round1']['series'+str(i)]['lower_seed_losses']=series.lower_seed_loses
        
        count = 1
        game_str='game'+str(count)
        for game in previous_playoff_games:
            context['east']['round1']['series'+str(i)]['game'+str(count)]={}
            context['east']['round1']['series'+str(i)]['game'+str(count)]['series_id']=game.game_id
            if matchups_east[i-1][0][2] == game.home_team:
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.home_team_score
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.away_team_score
            else:
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_higher_seed']=game.away_team_score
                context['east']['round1']['series'+str(i)]['game'+str(count)]['score_lower_seed']=game.home_team_score
                
            count += 1    
                
        
    #print(context['east'],"\n")
    #print(context['west'],"\n")

    context['eastern_teams']=eastern
    context['western_teams']=western

    return render(request,'basketball/playoffs_mobile.html', context)



def series_page_mobile(request, id):
    
    if id > 9223372036854775807:
        return render(request,"error_request.html")
    
    
    series_check = Serie.objects.filter(series_id=id)
    if len(series_check) == 0:
        return render(request,"error_request.html")

    series = Serie.objects.get(series_id=id)
    count=1
    game_score = 'game_score'
    game_str = 'game'
    higher_seed_scores = []
    lower_seed_scores = []
    
    # getting all playoff games that the higher seeded team has played
    context={}
    higher_seed_stats=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    lower_seed_stats=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    
    if series.game_ids != "": 
        for key,this_game_id in series.game_ids.items(): #need to have game1,game2,... in series model
            context[game_score+str(count)] = ' '
            game = Game.objects.get(game_id=this_game_id)
            context[game_str+str(count)] = game.game_id
            if game.home_team == series.higher_seed_id:
                lower_seed_scores.append(game.away_team_score)     
                higher_seed_scores.append(game.home_team_score)

            else:
                lower_seed_scores.append(game.home_team_score)     
                higher_seed_scores.append(game.away_team_score)
            count+=1
            
            team_stats = game.data['team_stats']
            higher_seed_team = 1
            lower_seed_team = 1
            if team_stats[0]['team_id']==series.higher_seed_id:
                higher_seed_team = 0
            else:
                lower_seed_team = 0

            higher_seed_stats[0] += team_stats[higher_seed_team]['FG_made']
            higher_seed_stats[1] += team_stats[higher_seed_team]["FG_attempted"]
            higher_seed_stats[2] += team_stats[higher_seed_team]['3P_made']
            higher_seed_stats[3] += team_stats[higher_seed_team]["3P_attempted"]
            higher_seed_stats[4] += team_stats[higher_seed_team]['FT_made']
            higher_seed_stats[5] += team_stats[higher_seed_team]["FT_attempted"]
            higher_seed_stats[6] += (team_stats[higher_seed_team]['off_rebounds']+team_stats[higher_seed_team]["def_rebounds"])
            higher_seed_stats[7] += team_stats[higher_seed_team]['off_rebounds']
            higher_seed_stats[8] += team_stats[higher_seed_team]["def_rebounds"]
            higher_seed_stats[9] += team_stats[higher_seed_team]['assists']
            higher_seed_stats[10] += team_stats[higher_seed_team]['steals']
            higher_seed_stats[11] += team_stats[higher_seed_team]['blocks']
            higher_seed_stats[12] += team_stats[higher_seed_team]['turnovers']
            higher_seed_stats[13] += team_stats[higher_seed_team]['personal_fouls']
            higher_seed_stats[14] += team_stats[higher_seed_team]['points']

            lower_seed_stats[0] += team_stats[lower_seed_team]['FG_made']
            lower_seed_stats[1] += team_stats[lower_seed_team]["FG_attempted"]
            lower_seed_stats[2] += team_stats[lower_seed_team]['3P_made']
            lower_seed_stats[3] += team_stats[lower_seed_team]["3P_attempted"]
            lower_seed_stats[4] += team_stats[lower_seed_team]['FT_made']
            lower_seed_stats[5] += team_stats[lower_seed_team]["FT_attempted"]
            lower_seed_stats[6] += (team_stats[lower_seed_team]['off_rebounds']+team_stats[lower_seed_team]["def_rebounds"])
            lower_seed_stats[7] += team_stats[lower_seed_team]['off_rebounds']
            lower_seed_stats[8] += team_stats[lower_seed_team]["def_rebounds"]
            lower_seed_stats[9] += team_stats[lower_seed_team]['assists']
            lower_seed_stats[10] += team_stats[lower_seed_team]['steals']
            lower_seed_stats[11] += team_stats[lower_seed_team]['blocks']
            lower_seed_stats[12] += team_stats[lower_seed_team]['turnovers']
            lower_seed_stats[13] += team_stats[lower_seed_team]['personal_fouls']
            lower_seed_stats[14] += team_stats[lower_seed_team]['points']
        
        if series.games_played > 0:    
            for i in range(0,len(higher_seed_stats)):
                higher_seed_stats[i]/=series.games_played
                higher_seed_stats[i]=round(higher_seed_stats[i],1)
                lower_seed_stats[i]/=series.games_played
                lower_seed_stats[i]=round(lower_seed_stats[i],1)
        
    #home_team_stats.append(round((home_team_stats[home_team]['FG_made']/team_stats[home_team]["FG_attempted"])*100,1))
    #round((team_stats[home_team]['3P_made']/team_stats[home_team]["3P_attempted"])*100,1),
    #round((team_stats[home_team]['FT_made']/team_stats[home_team]["FT_attempted"])*100,1),
    
    higher_seed_teams = Team.objects.filter(conference=Team.objects.get(team_id=series.higher_seed_id).conference).order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    higher_seed_rank = 1
    for t in higher_seed_teams:
        if t.team_id == series.higher_seed_id:
            break
        else:
            higher_seed_rank += 1
            
    lower_seed_teams = Team.objects.filter(conference=Team.objects.get(team_id=series.lower_seed_id).conference).order_by('-team_wins','team_losses','-divisional_wins','divisional_losses','-conference_wins','conference_losses','team_name')
    lower_seed_rank = 1
    for t in lower_seed_teams:
        if t.team_id == series.lower_seed_id:
            break
        else:
            lower_seed_rank += 1

    context["higher_seed_id"]=series.higher_seed_id
    context["lower_seed_id"]=series.lower_seed_id
    context["higher_seed_name"]=series.higher_seed_name
    context["lower_seed_name"]=series.lower_seed_name
    context["higher_seed_image"]=find_team_image(series.higher_seed_id)
    context["lower_seed_image"]=find_team_image(series.lower_seed_id)    
    context["higher_seed_abv"]=series.higher_seed_abv
    context["lower_seed_abv"]=series.lower_seed_abv
    context["higher_seed_wins"]=series.higher_seed_wins
    context["lower_seed_wins"]=series.lower_seed_wins
    context["higher_seed_losses"]=series.higher_seed_loses
    context["lower_seed_losses"]=series.lower_seed_loses
    context["higher_seed_rank"]=higher_seed_rank
    context["lower_seed_rank"]=lower_seed_rank
    context["higher_seed_stats"]=higher_seed_stats
    context["lower_seed_stats"]=lower_seed_stats
    context["games_played"]=series.games_played
    context['lower_seed_scores']=lower_seed_scores
    context['higher_seed_scores']=higher_seed_scores
    context['series_id']=series.series_id
        
    return render(request, 'basketball/series_mobile.html', context)


def standings_page_mobile(request):
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
                #print(losses_west)
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
                #print(losses_east)
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
                    #print(team.team_name,' ',games_back)
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
    return render(request,'basketball/standings_mobile.html', context)


def team_home_page_mobile(request):
    
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

    return render(request, 'basketball/teams_mobile.html',context)


def home_mobile(request):
    if request.method == 'GET':
        game_date = datetime.datetime.now().date()
        game_year = str(game_date.year)
        game_month = str(game_date.month) if game_date.month > 9 else '0'+str(game_date.month)
        game_day = str(game_date.day) if game_date.day > 9 else '0'+str(game_date.day)
        return redirect('/basketball/games_mobile/'+('%s%s%s' % (game_year,game_month,game_day)))
    elif not request.POST['date']:
        messages.add_message(request, messages.ERROR, 'No date specified')
        game_date = datetime.datetime.now().date()
    else:
        date_attr = request.POST['date'].split('/')
        #date(year, month, day)
        #print(date_attr)
        game_date = date_attr[2]+date_attr[0]+date_attr[1]#datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
        return redirect('/basketball/games_mobile/'+game_date)

        
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


    return render(request, 'basketball/games_mobile.html', context)


def get_games_date_mobile(request,game_date):
    
    #date(year, month, day)
    try:
        if request.method == 'POST' and request.POST['date']:
            date_attr = request.POST['date'].split('/')
            
            return redirect('/basketball/games_mobile/'+(date_attr[2]+date_attr[0]+date_attr[1]))
            #game_date = datetime.date(int(date_attr[2]),int(date_attr[0]),int(date_attr[1]))
            
        else:
            date_attr = str(game_date)
            if len(date_attr) != 8:
                raise TypeError
            game_date = datetime.date(int(date_attr[0:4]),int(date_attr[4:6]),int(date_attr[6:]))

    except:
        messages.add_message(request, messages.ERROR, 'Error in processing the date specified')
        game_date = datetime.date.today()
        return render(request, 'basketball/games_mobile.html')

    #today = get_pst_time()
    today = datetime.datetime.now().date()
    #print(today)
    #print(game_date)
    context = {}
    context['games'] = []
    context['date']='%s/%s/%s' % (game_date.month,game_date.day,game_date.year)
    if today < game_date or (today <= game_date and datetime.datetime.now().hour < 14):
        game_previews = GamePreview.objects.filter(game_date=game_date)
        for game in game_previews:
            previous_playoff_games = (Game.objects.filter(home_team=game.home_team_id,away_team=game.away_team_id,date__gte=datetime.date(2020,5,1))
                            | Game.objects.filter(away_team=game.home_team_id,home_team=game.away_team_id,date__gte=datetime.date(2020,5,1))).order_by('date')
            
            home_series_wins = 0
            away_series_wins = 0
            for g in previous_playoff_games:
                if g.winning_team_id == game.home_team_id:
                    home_series_wins += 1
                else:
                    away_series_wins += 1
            
            series = (Serie.objects.filter(higher_seed_id=game.home_team_id,lower_seed_id=game.away_team_id)
                            | Serie.objects.filter(higher_seed_id=game.away_team_id,lower_seed_id=game.home_team_id))[0]        
            
            this_game = [
                game.home_team_name,
                game.away_team_name,
                game.votes_home_team,
                game.votes_home_away,
                game.game_preview_id,
                find_team_image(game.home_team_id),
                find_team_image(game.away_team_id),
                Team.objects.get(team_id=game.higher_seeding_id).team_abv,
                Team.objects.get(team_id=game.lower_seeding_id).team_abv,
                series.higher_seed_wins,
                series.lower_seed_wins,
                game.higher_seeding_id,
                game.lower_seeding_id,
                Team.objects.get(team_id=game.home_team_id).team_abv,
                Team.objects.get(team_id=game.away_team_id).team_abv,
                game.home_team_id,
                game.away_team_id
            ]
            context['games'].append(this_game)
        
        return render(request, 'basketball/game_previews_mobile.html',context)
            
    else:
        games = Game.objects.filter(date=game_date) 
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

        return render(request, 'basketball/games_mobile.html',context)
    

#height,weight,jersey_number,player_age, team_name
#full_name,player_id,points_total,assists_total,rebounds_total,blocks_total
#steals_total, turnovers_total, personal_fouls_total,free_throws_attempted
#free_throws_made,minutes_total,three_point_attempted,three_point_made,
#field_goals_attempted,field_goals_made,games_played,team_id
def player_page_mobile(request,id):
    try:
         player = Player.objects.get(player_id=id)
    except:
        return render(request,"error_request.html")
    
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

    return render(request,'basketball/player_page_mobile.html',context=context)


def preview_game_page_mobile(request,id,add_form):
    
    game = GamePreview.objects.filter(game_preview_id=id)
    if len(game) == 0:
        return render(request,"error_request.html")
    
    
    game = GamePreview.objects.get(game_preview_id=id)
    #print(game.game_date, ' ', datetime.datetime.now().date())
    if game.game_date < datetime.datetime.now().date() or (game.game_date < datetime.datetime.now().date() and datetime.datetime.now().hour > 14): #get_pst_time():
        return render(request,"error_request.html")
     
    previous_playoff_games = (Game.objects.filter(home_team=game.home_team_id,away_team=game.away_team_id,date__gte=datetime.date(2020,5,1))
                            | Game.objects.filter(away_team=game.home_team_id,home_team=game.away_team_id,date__gte=datetime.date(2020,5,1))).order_by('date')
            
    home_series_wins = 0
    away_series_wins = 0
    for g in previous_playoff_games:
        if g.winning_team_id == game.home_team_id:
            home_series_wins += 1
        else:
            away_series_wins += 1
    
    previous_games = (Game.objects.filter(home_team=game.home_team_id,away_team=game.away_team_id)
                            | Game.objects.filter(away_team=game.home_team_id,home_team=game.away_team_id)).order_by('-date')
    
    previous_game_scores = []
    for g in previous_games:
        previous_game_scores.append([g.home_team_score,
                                     g.away_team_score,
                                     Team.objects.get(team_id=g.home_team).team_abv,
                                     Team.objects.get(team_id=g.away_team).team_abv,
                                     game.home_team_id,
                                     game.away_team_id,
                                     g.game_id,
                                     '%s/%s/%s' % (g.date.month,g.date.day,g.date.year),
                                     find_team_image(g.home_team),
                                     find_team_image(g.away_team)
        ]),

        
    team_away = Team.objects.get(team_id=game.away_team_id)
    away_abv = team_away.team_abv
    away_team_stats = [ 
        team_away.team_name,team_away.team_abv,
        team_away.team_wins,team_away.team_losses,
        round(team_away.points_total/team_away.games_played,1),
        round(team_away.assists_total/team_away.games_played,1),
        round(team_away.offensive_rebounds_total/team_away.games_played,1),
        round(team_away.defensive_rebounds_total/team_away.games_played,1),
        round(team_away.rebounds_total/team_away.games_played,1),
        round(team_away.blocks_total/team_away.games_played,1),
        round(team_away.steals_total/team_away.games_played,1),
        round(team_away.turnovers_total/team_away.games_played,1),
        round(team_away.personal_fouls_total/team_away.games_played,1),
        round(team_away.free_throws_made/team_away.games_played,1),
        round(team_away.free_throws_attempted/team_away.games_played,1),
        round((team_away.free_throws_made/team_away.free_throws_attempted)*100,1),
        round(team_away.field_goals_made/team_away.games_played,1),
        round(team_away.field_goals_attempted/team_away.games_played,1),
        round((team_away.field_goals_made/team_away.field_goals_attempted)*100,1),
        round(team_away.three_point_made/team_away.games_played,1),
        round(team_away.three_point_attempted/team_away.games_played,1),
        round((team_away.three_point_made/team_away.three_point_attempted)*100,1),
        round((team_away.points_total/team_away.games_played),1),
        team_away.games_played,
    ]
    
    team_home = Team.objects.get(team_id=game.home_team_id)
    home_abv = team_home.team_abv
    home_team_stats = [ 
        team_home.team_name,team_home.team_abv,
        team_home.team_wins,team_home.team_losses,
        round(team_home.points_total/team_home.games_played,1),
        round(team_home.assists_total/team_home.games_played,1),
        round(team_home.offensive_rebounds_total/team_home.games_played,1),
        round(team_home.defensive_rebounds_total/team_home.games_played,1),
        round(team_home.rebounds_total/team_home.games_played,1),
        round(team_home.blocks_total/team_home.games_played,1),
        round(team_home.steals_total/team_home.games_played,1),
        round(team_home.turnovers_total/team_home.games_played,1),
        round(team_home.personal_fouls_total/team_home.games_played,1),
        round(team_home.free_throws_made/team_home.games_played,1),
        round(team_home.free_throws_attempted/team_home.games_played,1),
        round((team_home.free_throws_made/team_home.free_throws_attempted)*100,1),
        round(team_home.field_goals_made/team_home.games_played,1),
        round(team_home.field_goals_attempted/team_home.games_played,1),
        round((team_home.field_goals_made/team_home.field_goals_attempted)*100,1),
        round(team_home.three_point_made/team_home.games_played,1),
        round(team_home.three_point_attempted/team_home.games_played,1),
        round((team_home.three_point_made/team_home.three_point_attempted)*100,1),
        round((team_home.points_total/team_home.games_played),1),
        team_home.games_played,
    ]
    
    series = (Serie.objects.filter(higher_seed_id=game.home_team_id,lower_seed_id=game.away_team_id)
                            | Serie.objects.filter(higher_seed_id=game.away_team_id,lower_seed_id=game.home_team_id))[0]
    
    context={}
    context['away_team_stats']=away_team_stats
    context['home_team_stats']=home_team_stats
    context['higher_seed_wins']=series.higher_seed_wins
    context['lower_seed_wins']=series.lower_seed_wins
    context['higher_seed_abv']=series.higher_seed_abv
    context['lower_seed_abv']=series.lower_seed_abv
    context['higher_seed_id']=series.higher_seed_id
    context['lower_seed_id']=series.lower_seed_id
    context['prev_games']=previous_game_scores
    context['home_team_id']=game.home_team_id
    context['away_team_id']=game.away_team_id
    context['home_abv']=home_abv
    context['away_abv']=away_abv
    context['home_team_image']=find_team_image(game.home_team_id)
    context['away_team_image']=find_team_image(game.away_team_id)
    context['home_team_name']=game.home_team_name
    context['away_team_name']=game.away_team_name
    context['date']='%s/%s/%s' % (game.game_date.month,game.game_date.day,game.game_date.year)
    context['game_id']=game.game_preview_id
    context['game_number']=game.game_number
    context['is_necessary'] = game.is_necessary
    
    return render(request,'basketball/game_preview_mobile.html',context)


def game_page_mobile(request, id):
    
    if id > 9223372036854775807:
        return render(request,"error_request.html")
    
    if id < 10000:
        return preview_game_page_mobile(request,id,True)
    
    game = Game.objects.filter(game_id=id)
    if len(game) == 0:
        return render(request,"error_request.html")
    
    
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
        "home_team_abv":Team.objects.get(team_id=game.home_team).team_abv,
        "away_team_abv":Team.objects.get(team_id=game.away_team).team_abv,
        "home_team_record":game.home_team_record, "away_team_record":game.away_team_record,
        "home_team_id":game.home_team,"away_team_id":game.away_team,"num_overtimes":range(1,num_ots+1),
        "date": '%s/%s/%s' % (game.date.month,game.date.day,game.date.year)
    }

    return render(request,'basketball/game_page_mobile.html',context)



def mvp_vote_mobile(request):
    if request.method == 'POST':
        form = MVPVoteForm(request.POST)
        #print(form.data)
        if form.is_valid():
            mvp_player = MVPVote.objects.get(player_id=form.data['VOTE_FOR_MVP'])
            #print(mvp_player)
            mvp_player.votes+=1
            mvp_player.save()
                    
            return redirect('/basketball/mvp_results')
    #return render(request,'basketball/mvp_vote.html',context)
    form = MVPVoteForm()
    #print(form.CHOICES)
    labels=[]
    data=[]
    
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')[3:]
    other_votes = 0
    for p in mvp_poll:
        other_votes += p.votes
        if p.votes == 0:
            break
    
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')[:3]
    
    for player in mvp_poll:
        labels.append(player.player_name)
        data.append(player.votes)
    labels.append('Other')
    data.append(other_votes)
    return render(request,'basketball/mvp_vote_mobile.html', {"form":form,'labels': labels,'data': data, })  


def mvp_results_mobile(request):
    mvp_poll = MVPVote.objects.all().order_by('-votes','-points_pg')
    labels=[]
    data=[]
    
    for player in mvp_poll[:10]:
        labels.append(player.player_name)
        data.append(player.votes)
    
    other_votes = 0
    for player in mvp_poll[10:]:
        other_votes += player.votes
        if player.votes == 0:
            break
        
    labels.append('Other')
    data.append(other_votes)
    
    rest = []
    for player in mvp_poll:
        team_id = Player.objects.get(player_id=player.player_id).team_id
        team_image=find_team_image(team_id)
        rest.append([player.player_name,player.team_abv,team_id,str(player.votes),str(team_image),player.player_id])
        
    return render(request,'basketball/mvp_votes_results_mobile.html',context={
                                                                    'top_players':rest,
                                                                    'labels': labels,
                                                                    'data': data    })

def series_vote_results_mobile(request):
                
    series = Serie.objects.all()
    context = {}
    count = 1
    for serie in series:
        name_l = 'labels'+str(count)
        name_d = 'data'+str(count)
        data = [
            serie.votes_higher_seed+1,
            serie.votes_lower_seed+1
        ]
        labels = [
            serie.higher_seed_name,
            serie.lower_seed_name
        ]
        context[name_l]=labels
        context[name_d]=data
        count +=1
    
    #pprint.pprint(context)
    return render(request,'basketball/series_votes_results_mobile.html', context)

def series_vote_mobile(request):
    if request.method == 'POST':
        form = SeriesForm(request.POST)
        if form.is_valid():
            name = 'form'
            count = 1
            while name in request.POST:
                items = request.POST[name].split(' ')
                series = Serie.objects.get(series_id=int(items[1]))
                if int(items[0])==series.higher_seed_id:
                    series.votes_higher_seed+=1
                    series.save()
                else:
                    series.votes_lower_seed+=1
                    series.save()
                name = 'form'+str(count)
                count += 1
            return redirect('/basketball/series_vote_results_mobile')
        else:
            messages.add_message(request, messages.ERROR, 'Error in processing form data')
            formset = SeriesForm()
            return render(request,'basketball/vote_for_series_mobile.html',{'form':formset})
        #return HttpResponse("Thanks")
    
    formset = SeriesForm()
    return render(request,'basketball/vote_for_series_mobile.html',{'form':formset})



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
        1610612753:"8th",#ORL
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
