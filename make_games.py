from basketball.models import Game,Team,Player, Serie, GamePreview
from datetime import date
import re
from bs4 import BeautifulSoup
import requests 
import copy   
import random
import pprint
from datetime import date
import time


def make_playoff_single():
    today = date.today()
    
    for game in GamePreview.objects.all():
        if game.game_date == today:
            print(game.home_team_name)
            print(game.away_team_name)
            print(game.game_date)
            print(game.game_number)
            return_val = calculate_stats(list(),list(),game.lower_seeding_id,game.higher_seeding_id,game.game_date,'away')
    
def make_playoff_games():
    num_wins_higher = 0
    num_wins_lower = 0
    team_away = ""
    team_home = ""
    higher_id = 1610612761
    lower_id = 1610612751
    print('Away team: %s %s' % (team_away, lower_id))
    print('Home team: %s %s' % (team_home, higher_id))
    game_day = 7
    games = 1
    
    while num_wins_higher < 4 and num_wins_lower < 4:
        game_date = date(2020,5,game_day)
        
        if games == 1 or games == 2 or games == 6 or games == 7:
            return_val = calculate_stats(list(),list(),higher_id,lower_id,game_date,'home')
        else:
            return_val = calculate_stats(list(),list(),lower_id,higher_id, game_date,'away')
            
        if return_val == 'higher':
            num_wins_higher += 1
        else:
            num_wins_lower += 1 
            
        print('wins high:',num_wins_higher)
        print('wins low:',num_wins_lower)
        
        game_day += 1
        games += 1
    
  
    return


def make_games():
    current = 20200401
    last = 20200415
    
    team_names = []
    games = []
    while current < 20200416:
        team_names = []
        url = "https://www.cbssports.com/nba/schedule/"+str(current)
        response = requests.get(url)

        data = response.text
        soup = BeautifulSoup(data,features='html.parser')
        str_current = str(current)
        print("%s/%s/%s" % (str_current[4:6],str_current[6:],str_current[0:4]))
        #f.write("%s/%s/%s\n" % (str_current[4:6],str_current[6:],str_current[0:4]))

        for span_tag in soup.findAll('span', {'class': 'TeamName'}):
            team_names.append((span_tag.find('a')).string)
        print(team_names)

        for i in range(0,len(team_names),2):
            #if i == 8 or i == 10:
                team_away = team_names[i]
                team_home = team_names[i+1]
                #game = [team_away,team_home]
                #games.append(game)
                #f.write("Away: %s  Home: %s\n" % (team1,team2))
                team_home_id = get_team(team_home.lower())
                team_away_id = get_team(team_away.lower())
                print('Away team: %s %s' % (team_away, team_away_id))
                print('Home team: %s %s' % (team_home, team_home_id))

                #matchup_data_home = get_other_data(team_home_id,team_away_id)
                #matchup_data_away = get_other_data(team_away_id,team_home_id)
                #print('matchup_away:',matchup_data_away)
                #print('matchup_home:',matchup_data_home)
                curr = str(current)
                game_date = date(int(curr[0:4]),int(curr[4:6]),int(curr[6:]))

            
                #calculate_stats(matchup_data_home,matchup_data_away,team_home_id,team_away_id,game_date)
                calculate_stats(list(),list(),team_home_id,team_away_id,game_date)
                #time.sleep(1)
            #return
        current+=1


'''
        matchup_data['2019-2020 Season'] = {
            'games_played':team_matchup_2019_2020[2],
            'wins':team_matchup_2019_2020[3],
            'losses':team_matchup_2019_2020[4],  
            'win_pct':team_matchup_2019_2020[5], 
            'fg_pct':team_matchup_2019_2020[9], 
            'fg_attempted_pg':team_matchup_2019_2020[8]/team_matchup_2019_2020[2],
            'block_pg':team_matchup_2019_2020[22]/team_matchup_2019_2020[2],
            'steals_pg':team_matchup_2019_2020[21]/team_matchup_2019_2020[2],
            'turnovers_pg':team_matchup_2019_2020[20]/team_matchup_2019_2020[2],
            'personal_fouls_pg':team_matchup_2019_2020[24]/team_matchup_2019_2020[2],
            'rb_pg':team_matchup_2019_2020[18]/team_matchup_2019_2020[2],
            'orb_pg':team_matchup_2019_2020[16]/team_matchup_2019_2020[2],
            'drb_pg':team_matchup_2019_2020[17]/team_matchup_2019_2020[2],
            'ast_pg':team_matchup_2019_2020[19]/team_matchup_2019_2020[2], 
            'three_pt_att_pg':team_matchup_2019_2020[11]/team_matchup_2019_2020[2],
            'three_pt_pct':team_matchup_2019_2020[12], 
            'plus_minus_pts':team_matchup_2019_2020[27],
            'free_throw_att_pg':team_matchup_2019_2020[14]/team_matchup_2019_2020[2],
            'free_throw_pct':team_matchup_2019_2020[15],
            'points_pg':team_matchup_2019_2020[26]/team_matchup_2019_2020[2] 
        }
'''
def calculate_stats(matchup_home,matchup_away,home_id,away_id,game_date,higher_seed):

    team_home = Team.objects.get(team_id=home_id)
    team_away = Team.objects.get(team_id=away_id)
    home_stats = {
        "wins":team_home.home_wins,"losses":team_home.home_losses,
        'points_per_game':round(team_home.points_total/team_home.games_played,1),
        'assists_per_game':round(team_home.assists_total/team_home.games_played,1),
        'offensive_rebounds_per_game':round(team_home.offensive_rebounds_total/team_home.games_played,1),
        'defensive_rebounds_per_game':round(team_home.defensive_rebounds_total/team_home.games_played,1),
        'rebounds_per_game':round(team_home.rebounds_total/team_home.games_played,1),
        'blocks_per_game':round(team_home.blocks_total/team_home.games_played,1),
        'steals_per_game':round(team_home.steals_total/team_home.games_played,1),
        'turnovers_per_game':round(team_home.turnovers_total/team_home.games_played,1),
        'personal_fouls_per_game':round(team_home.personal_fouls_total/team_home.games_played,1),
        'free_throws_made_per_game':round(team_home.free_throws_made/team_home.games_played,1),
        'free_throws_attempted_per_game':round(team_home.free_throws_attempted/team_home.games_played,1),
        'free_throw_percentage':round((team_home.free_throws_made/team_home.free_throws_made)*100,1),
        'field_goals_made_per_game':round(team_home.field_goals_made/team_home.games_played,1),
        'field_goals_attempted_per_game':round(team_home.field_goals_attempted/team_home.games_played,1),
        'field_goal_percentage':round((team_home.field_goals_made/team_home.field_goals_attempted)*100,1),
        'three_point_made_per_game':round(team_home.three_point_made/team_home.games_played,1),
        'three_point_attempted_per_game':round(team_home.three_point_attempted/team_home.games_played,1),
        'three_point_percentage':round((team_home.three_point_made/team_home.three_point_attempted)*100,1),
        'opponent_points_per_game': round((team_home.opponent_points_total/team_home.games_played),1),
        'home_wins':team_home.home_wins,
        'home_losses':team_home.home_losses,
        'plus_minus':round(team_home.points_total/team_home.games_played,1)-round((team_home.opponent_points_total/team_home.games_played),1),
    }

    away_stats = {
        "wins":team_away.away_wins,"losses":team_away.away_losses,
        'points_per_game':round(team_away.points_total/team_away.games_played,1),
        'assists_per_game':round(team_away.assists_total/team_away.games_played,1),
        'offensive_rebounds_per_game':round(team_away.offensive_rebounds_total/team_away.games_played,1),
        'defensive_rebounds_per_game':round(team_away.defensive_rebounds_total/team_away.games_played,1),
        'rebounds_per_game':round(team_away.rebounds_total/team_away.games_played,1),
        'blocks_per_game':round(team_away.blocks_total/team_away.games_played,1),
        'steals_per_game':round(team_away.steals_total/team_away.games_played,1),
        'turnovers_per_game':round(team_away.turnovers_total/team_away.games_played,1),
        'personal_fouls_per_game':round(team_away.personal_fouls_total/team_away.games_played,1),
        'free_throws_made_per_game':round(team_away.free_throws_made/team_away.games_played,1),
        'free_throws_attempted_per_game':round(team_away.free_throws_attempted/team_away.games_played,1),
        'free_throw_percentage':round((team_away.free_throws_made/team_away.free_throws_made)*100,1),
        'field_goals_made_per_game':round(team_away.field_goals_made/team_away.games_played,1),
        'field_goals_attempted_per_game':round(team_away.field_goals_attempted/team_away.games_played,1),
        'field_goal_percentage':round((team_away.field_goals_made/team_away.field_goals_attempted)*100,1),
        'three_point_made_per_game':round(team_away.three_point_made/team_away.games_played,1),
        'three_point_attempted_per_game':round(team_away.three_point_attempted/team_away.games_played,1),
        'three_point_percentage':round((team_away.three_point_made/team_away.three_point_attempted)*100,1),
        'opponent_points_per_game': round((team_away.opponent_points_total/team_away.games_played),1),
        'away_wins':team_away.home_wins,
        'away_losses':team_away.home_losses,
        'plus_minus':round(team_away.points_total/team_away.games_played,1)-round((team_away.opponent_points_total/team_away.games_played),1),
    }

    #biases = compute_biases(away_stats,home_stats,matchup_away,matchup_home)
    #print(biases['home_field_goal_attempt_bias'])
    #print(home_stats['field_goals_attempted_per_game'])
    ####################SAM' BIAS CALCULATIONS############################
    home_bias_list = get_bias_home(home_id)
    away_bias_list = get_bias_away(away_id)
    #print("LOOK:",((biases['home_free_throw_percentage_bias'])+home_stats['free_throw_percentage']))
    '''overall_bias_home = ((biases['home_points_bias']+biases['home_points_per_game_bias'])/10)/2
    if overall_bias_home > 0:
        #overall_bias_home = 1 -overall_bias_home
        overall_bias_home = random.uniform(1.01,1.06)
    else:
        overall_bias_home = random.uniform(0.94,1.00)
    if biases['home_bias'] > 0.5:
        extra = random.uniform(1.0,1.10)
        overall_bias_home = (extra+overall_bias_home)/2
    else:
        extra = random.uniform(0.90,0.97)
        overall_bias_home = (extra+overall_bias_home)/2'''



    home_points_pg = round(team_home.points_total/team_home.games_played,1)
    away_points_pg = round(team_away.points_total/team_away.games_played,1)
    away_opp_point_pg = round(team_away.opponent_points_total/team_away.games_played,1)
    home_opp_point_pg = round(team_home.opponent_points_total/team_home.games_played,1)

    if home_points_pg > away_opp_point_pg:
        overall_bias_home = random.uniform(1.00,1.02)
    else:
        overall_bias_home = random.uniform(0.98,1.00)

    overall_bias_home=1

    #print(biases['home_points_bias'], '  ', biases['home_points_per_game_bias'])
    #print("OVERALL BIAS HOME", overall_bias_home)
    home_game_stats = {
        'minutes':240,
        'field_goals_percentage': (home_stats['field_goal_percentage'])*(random.uniform(home_bias_list[0], home_bias_list[1]))*overall_bias_home,
        'field_goals_attempted': round((home_stats['field_goals_attempted_per_game'])+random.uniform(home_bias_list[2],home_bias_list[3])*overall_bias_home),
        'three_point_percentage': (home_stats['three_point_percentage'])*(random.uniform(home_bias_list[4], home_bias_list[5]))*overall_bias_home,
        'three_point_attempted': round((home_stats['three_point_attempted_per_game'])+random.uniform(home_bias_list[6],home_bias_list[7])*overall_bias_home),
        'free_throws_percentage': ((home_stats['free_throw_percentage'])*(random.uniform(home_bias_list[8], home_bias_list[9])))*overall_bias_home,
        'free_throws_attempted': round((home_stats['free_throws_attempted_per_game'])+random.uniform(home_bias_list[10],home_bias_list[11])*overall_bias_home),
        'def_rebounds': round((home_stats['defensive_rebounds_per_game'])+random.uniform(home_bias_list[12],home_bias_list[13])*overall_bias_home),
        'off_rebounds': round((home_stats['offensive_rebounds_per_game'])+random.uniform(home_bias_list[14],home_bias_list[15])*overall_bias_home),
        #'rebounds': ((biases['home_rebounds_bias'])+home_stats['rebounds_per_game'])+random.uniform(home_bias_list[16],home_bias_list[17])*overall_bias_home,
        'assists': round((home_stats['assists_per_game'])+random.uniform(home_bias_list[18],home_bias_list[19])*overall_bias_home),
        'steals': round((home_stats['steals_per_game'])+random.uniform(home_bias_list[20],home_bias_list[21])*overall_bias_home),
        'blocks': round((home_stats['blocks_per_game'])+random.uniform(home_bias_list[22],home_bias_list[23])*overall_bias_home),
        'turnovers': round((home_stats['turnovers_per_game'])+random.uniform(home_bias_list[24],home_bias_list[25])*overall_bias_home),
        'personal_fouls': round((home_stats['personal_fouls_per_game'])+ random.uniform(home_bias_list[26],home_bias_list[27])*overall_bias_home),
        #'points': (((biases['home_points_bias']+home_stats['points_per_game'])+(biases['home_points_per_game_bias']+home_stats['points_per_game']))/2)+random.uniform(home_bias_list[28],home_bias_list[29]),
    }
    home_game_stats['field_goals_made'] = round(home_game_stats['field_goals_attempted']*(home_game_stats['field_goals_percentage']/100)) 
    home_game_stats['free_throws_made'] = round((home_game_stats['free_throws_percentage']/100)*home_game_stats['free_throws_attempted'])
    home_game_stats['three_point_made'] = round((home_game_stats['three_point_percentage']/100)*home_game_stats['three_point_attempted'])
    home_game_stats['field_goals_percentage'] = round( (home_game_stats['field_goals_made']/home_game_stats['field_goals_attempted'])*100)
    home_game_stats['three_point_percentage'] = round( (home_game_stats['three_point_made']/home_game_stats['three_point_attempted'])*100)
    home_game_stats['free_throw_percentage'] = round( (home_game_stats['free_throws_made']/home_game_stats['free_throws_attempted'])*100)
    home_game_stats['rebounds'] = home_game_stats['off_rebounds']+home_game_stats['def_rebounds']
    total_points_home = (home_game_stats['three_point_made']*3)+((home_game_stats['field_goals_made']-home_game_stats['three_point_made'])*2) + home_game_stats['free_throws_made']


    '''overall_bias_away = ((biases['away_points_bias']+biases['away_points_per_game_bias'])/10)/2
    if overall_bias_away > 0:
        #overall_bias_away = 1 -overall_bias_home
        overall_bias_away = random.uniform(1.01,1.06)
    else:
        overall_bias_away = random.uniform(0.94,1.00)
    if biases['away_bias'] > 0.5:
        extra = random.uniform(1.0,1.10)
        overall_bias_away = (extra+overall_bias_away)/2
    else:
        extra = random.uniform(0.90,0.97)
        overall_bias_away = (extra+overall_bias_away)/2
    overall_bias_away=1'''

    if away_points_pg > home_opp_point_pg:
        overall_bias_away = random.uniform(1.0,1.02)
    else:
        overall_bias_away = random.uniform(0.98,1.00)

    #overall_bias_away=1

    #overall_bias_away=1
    #print(biases['away_points_bias'], '  ', biases['away_points_per_game_bias'])
    #print("OVERALL BIAS AWAY", overall_bias_away)
    away_game_stats = {
        'minutes':240,
        'field_goals_percentage': (away_stats['field_goal_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
        'field_goals_attempted': round((away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])),#*overall_bias_away),
        'three_point_percentage': (away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
        'three_point_attempted': round((away_stats['three_point_attempted_per_game'])+random.uniform(away_bias_list[6],away_bias_list[7])*overall_bias_away),
        'free_throws_percentage': ((away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
        'free_throws_attempted': round((away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away),
        'def_rebounds': round((away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away),
        'off_rebounds': round((away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away),
        #'rebounds': ((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away,
        'assists': round((away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away),
        'steals': round((away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away),
        'blocks': round((away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away),
        'turnovers': round((away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away),
        'personal_fouls': round((away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away),
        #'points': (((biases['away_points_bias']+away_stats['points_per_game'])+(biases['away_points_per_game_bias']+away_stats['points_per_game']))/2)+random.uniform(away_bias_list[28],away_bias_list[29]),
    }
    away_game_stats['field_goals_made'] = round(away_game_stats['field_goals_attempted']*(away_game_stats['field_goals_percentage']/100))
    away_game_stats['free_throws_made'] = round((away_game_stats['free_throws_percentage']/100)*away_game_stats['free_throws_attempted'])
    away_game_stats['three_point_made'] = round((away_game_stats['three_point_percentage']/100)*away_game_stats['three_point_attempted'])
    away_game_stats['field_goals_percentage'] = round( (away_game_stats['field_goals_made']/away_game_stats['field_goals_attempted'])*100,1)
    away_game_stats['three_point_percentage'] = round( (away_game_stats['three_point_made']/away_game_stats['three_point_attempted'])*100,1)
    away_game_stats['free_throw_percentage'] = round( (away_game_stats['free_throws_made']/away_game_stats['free_throws_attempted'])*100,1)  
    away_game_stats['rebounds'] = away_game_stats['off_rebounds']+away_game_stats['def_rebounds']
    total_points_away = (away_game_stats['three_point_made']*3) + ((away_game_stats['field_goals_made']-away_game_stats['three_point_made'])*2) + away_game_stats['free_throws_made']

    num_ots = 0
    '''if total_points_away == total_points_home:
        
        new_results = compute_overtime(away_game_stats,home_game_stats,overall_bias_away,overall_bias_home,biases,away_bias_list,home_bias_list,total_points_away,total_points_home)
        home_game_stats = new_results[1]
        away_game_stats = new_results[0]
        num_ots = new_results[2]
        print("OVERTIME", "  ", num_ots)'''

    #print('home_stats:',home_game_stats)
    #print('\ntotal points: ', total_points_home, '\n')
    #print('away stats:',away_game_stats)
    #print('\ntotal points: ', total_points_away, '\n')

    #print('AWAY')
    combined_away_stats = compute_player_stats(away_game_stats,total_points_away,away_id, 0,False)
    team_away_stats = combined_away_stats[1]
    player_away_stats = combined_away_stats[0]
    #print('HOME')
    combined_home_stats = compute_player_stats(home_game_stats,total_points_home,home_id, team_away_stats['points'],True)
    team_home_stats = combined_home_stats[1]
    player_home_stats = combined_home_stats[0]

    '''if team_home_stats['field_goals_attempted']+team_away_stats['field_goals_attempted'] >= 190:
        v = random.randint(0,11)
        if v > 6:
            print('OVERTIME')
            num_ots = 1'''
    points_by_quarter = compute_points_by_quarter(team_home_stats['points'],team_away_stats['points'],num_ots)
    points_by_quarter_home = points_by_quarter['home_scores']
    points_by_quarter_away = points_by_quarter['away_scores']

    print('Points by quarter home:', points_by_quarter_home)
    print('Points by quarter away:', points_by_quarter_away)

    home = Team.objects.get(team_id=home_id)
    away = Team.objects.get(team_id=away_id)
    
    home_name = home.team_name
    away_name = away.team_name


    #update team stats
    #team_away_stats
    '''
            team_stat['assists']+=player_stat['assists']
            team_stat['off_rebounds']+=player_stat['off_rebounds']
            team_stat['def_rebounds']+=player_stat['def_rebounds']
            team_stat['rebounds']+=(player_stat['off_rebounds']+player_stat['def_rebounds'])
            team_stat['blocks']+=player_stat['blocks']
            team_stat['steals']+=player_stat['steals']
            team_stat['turnovers']+=player_stat['turnovers']
            team_stat['personal_fouls']+=player_stat['personal_fouls']
            team_stat['FT_attempted']+=player_stat['FT_attempted']
            team_stat['FT_made']+=player_stat['FT_made']
            team_stat['FG_attempted']+=player_stat['FG_attempted']
            team_stat['FG_made']+=player_stat['FG_made']
            team_stat['3P_attempted']+=player_stat['3P_attempted']
            team_stat['3P_made']+=player_stat['3P_made']
            team_stat['points']+=player_stat['points']
    '''
    
    
    away.points_total += team_away_stats['points']
    away.assists_total += team_away_stats['assists']
    away.offensive_rebounds_total += team_away_stats['off_rebounds']
    away.defensive_rebounds_total += team_away_stats['def_rebounds']
    away.rebounds_total += team_away_stats['rebounds']
    away.blocks_total += team_away_stats['blocks']
    away.steals_total += team_away_stats['steals']
    away.turnovers_total += team_away_stats['turnovers']
    away.personal_fouls_total += team_away_stats['personal_fouls']
    away.free_throws_made += team_away_stats['FT_made']
    away.free_throws_attempted += team_away_stats['FT_attempted']
    away.three_point_made += team_away_stats['3P_made']
    away.three_point_attempted += team_away_stats['3P_attempted']
    away.field_goals_made += team_away_stats['FG_made']
    away.field_goals_attempted += team_away_stats['FG_attempted']
    away.games_played += 1
    away.opponent_points_total += team_home_stats['points']
    #away.save()

    #team_home_stats
    home.points_total += team_home_stats['points']
    home.assists_total += team_home_stats['assists']
    home.offensive_rebounds_total += team_home_stats['off_rebounds']
    home.defensive_rebounds_total += team_home_stats['def_rebounds']
    home.rebounds_total += team_home_stats['rebounds']
    home.blocks_total += team_home_stats['blocks']
    home.steals_total += team_home_stats['steals']
    home.turnovers_total += team_home_stats['turnovers']
    home.personal_fouls_total += team_home_stats['personal_fouls']
    home.free_throws_made += team_home_stats['FT_made']
    home.free_throws_attempted += team_home_stats['FT_attempted']
    home.three_point_made += team_home_stats['3P_made']
    home.three_point_attempted += team_home_stats['3P_attempted']
    home.field_goals_made += team_home_stats['FG_made']
    home.field_goals_attempted += team_home_stats['FG_attempted']
    home.games_played += 1
    home.opponent_points_total += team_away_stats['points']
    #home.save()


    if team_away_stats['points'] > team_home_stats['points']:
        winner_team_id = away_id
        winning_name = away_name
        losing_name = home_name
        loser_team_id = home_id
        
        #update database
        winner = Team.objects.get(team_id=away_id)
        winner.team_wins += 1
        winner.away_wins += 1

        loser = Team.objects.get(team_id=home_id)
        loser.team_losses += 1
        loser.home_losses += 1

        if loser.conference == winner.conference:
            loser.conference_losses += 1
            winner.conference_wins += 1
        
        if loser.division == winner.division:
            loser.divisional_losses += 1
            winner.divisional_wins += 1

    else:
        winner_team_id = home_id
        winning_name = home_name
        losing_name = away_name
        loser_team_id = away_id

        #update database
        winner = Team.objects.get(team_id=home_id)
        winner.team_wins += 1
        winner.away_wins += 1

        loser = Team.objects.get(team_id=away_id)
        loser.team_losses += 1
        loser.home_losses += 1

        if loser.conference == winner.conference:
            loser.conference_losses += 1
            winner.conference_wins += 1
        
        if loser.division == winner.division:
            loser.divisional_losses += 1
            winner.divisional_wins += 1

    #SAVE TEAMS
    #loser.save()
    #winner.save()

    top_scorer_home_team_score = 0
    top_scorer_home_team_id = 0
    for p in player_home_stats:
        if top_scorer_home_team_score < p['points']:
            top_scorer_home_team_score = p['points']
            top_scorer_home_team_id = p['player_id']

    top_scorer_away_team_score = 0
    top_scorer_away_team_id = 0
    for p in player_away_stats:
        if top_scorer_away_team_score < p['points']:
            top_scorer_away_team_score = p['points']
            top_scorer_away_team_id = p['player_id']

    for p in (player_away_stats+player_home_stats):
        pl = Player.objects.get(player_id=p['player_id'])
        
        pl.assists_total += p['assists']
        pl.offensive_rebounds_total += p['off_rebounds']
        pl.defensive_rebounds_total += p['def_rebounds']
        pl.rebounds_total += p['rebounds']
        pl.blocks_total += p['blocks']
        pl.steals_total += p['steals']
        pl.turnovers_total += p['turnovers']
        pl.personal_fouls_total += p['personal_fouls']
        pl.free_throws_made += p['FT_made']
        pl.free_throws_attempted += p['FT_attempted']
        pl.minutes_total += p['min']
        pl.three_point_made += p['3P_made']
        pl.three_point_attempted += p['3P_attempted']
        pl.field_goals_made += p['FG_made']
        pl.field_goals_attempted += p['FG_attempted']
        if p['comment'] == "OK":
            pl.games_played += 1
        pl.points_total += p['points']
        #SAVE PLAYER
        #pl.save()

    data = {}
    data['points_by_quarter_id'] = {}
    data['points_by_quarter_id'][home_id]=points_by_quarter_home
    data['points_by_quarter_id'][away_id]=points_by_quarter_away
    data['player_stats']=player_home_stats + player_away_stats 
    data['team_stats']=[team_home_stats,team_away_stats]
    this_game_id = (Game.objects.all().order_by('-game_id')[0].game_id+1)

    game = Game(home_team=home_id,away_team=away_id,home_team_name=home_name,away_team_name=away_name, 
                game_id=this_game_id,winning_team_id=winner_team_id,
                winner_name=winning_name,loser_name=losing_name,losing_team_id=loser_team_id,
                home_team_score=team_home_stats['points'],away_team_score=team_away_stats['points'],
                top_scorer_home=top_scorer_home_team_id ,top_scorer_away=top_scorer_away_team_id,
                top_scorer_home_points=top_scorer_home_team_score,top_scorer_away_points=top_scorer_away_team_score,
                date=game_date,home_team_record=(str(home.team_wins)+'-'+str(home.team_losses)),
                away_team_record=(str(away.team_wins)+'-'+str(away.team_losses)),
                data=data, is_playoff=True,playoff_type='QF',is_simulated=True        
            )
    
    
    series = ((Serie.objects.filter(higher_seed_id=home_id,lower_seed_id=away_id)) | (Serie.objects.filter(higher_seed_id=away_id,lower_seed_id=home_id)))[0]
    series.games_played += 1
    if series.game_ids == "":
        series.game_ids = {}
    series.game_ids['game'+str(series.games_played)]=this_game_id
    
    if higher_seed == 'home':
        if winner_team_id == home_id:
            return_val = "higher"
            series.higher_seed_wins+=1
            series.lower_seed_loses+=1
        else:
            return_val = "lower"
            series.higher_seed_loses+=1
            series.lower_seed_wins+=1
    else:
        if winner_team_id == away_id:
            return_val = "higher"
            series.higher_seed_wins+=1
            series.lower_seed_loses+=1
        else:
            return_val = "lower"
            series.higher_seed_loses+=1
            series.lower_seed_wins+=1

    series.save()
    game.save()
    print(return_val)
    return return_val

def sort_func(p):
    return p.points_total/p.games_played

def sort_func2(p):
    return p.is_starter

def compute_player_stats(stats,score,tid, other_team_score,home_var):
    team_players = Player.objects.filter(team_id=tid)
    team_players = sorted(team_players, reverse=True, key=sort_func)
    team_players = sorted(team_players, reverse=True, key=sort_func2)
    team = Team.objects.get(team_id=tid)
    '''
         'minutes':240,
        'field_goals_percentage': ((biases['away_field_goal_percentage_bias'])+away_stats['field_goal_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
        'field_goals_attempted': round(((biases['away_field_goal_attempt_bias'])+away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])*overall_bias_away),
        'three_point_percentage': ((biases['away_three_point_pct_bias'])+away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
        'three_point_attempted': round(((biases['away_three_point_att_bias'])+away_stats['three_point_attempted_per_game'])+random.uniform(-away_bias_list[6],away_bias_list[7])*overall_bias_away),
        'free_throws_percentage': (((biases['away_free_throw_percentage_bias'])+away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
        'free_throws_attempted': round(((biases['away_free_throw_att_bias'])+away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away),
        'def_rebounds': round(((biases['away_def_rebounds_bias'])+away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away),
        'off_rebounds': round(((biases['away_off_rebounds_bias'])+away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away),
        #'rebounds': ((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away,
        'assists': round(((biases['away_assists_bias'])+away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away),
        'steals': round(((biases['away_steals_bias'])+away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away),
        'blocks': round(((biases['away_blocks_bias'])+away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away),
        'turnovers': round(((biases['away_turnovers_bias'])+away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away),
        'personal_fouls': round(((biases['away_personal_fouls_bias'])+away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away),
        #'points': 
        away_game_stats['field_goals_made'] = round(away_game_stats['field_goals_attempted']*(away_game_stats['field_goals_percentage']/100))
        away_game_stats['free_throws_made'] = round((away_game_stats['free_throws_percentage']/100)*away_game_stats['free_throws_attempted'])
        away_game_stats['three_point_made'] = round((away_game_s
    '''


    player_avg = []
    for player in team_players:

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

        players = []
        player_avg.append( {
            "player_name":player.full_name,"player_id":player.player_id,
            "points_per_game":round( (player.points_total/player.games_played) ,4),
            "assists_per_game":round( (player.assists_total/player.games_played) ,4),
            "offensive_rebounds_per_game":round( (player.offensive_rebounds_total/player.games_played) ,4),
            "defensive_rebounds_per_game":round( (player.defensive_rebounds_total/player.games_played) ,4),
            "rebounds_per_game":round( (player.rebounds_total/player.games_played), 4),
            "blocks_per_game":round( (player.blocks_total/player.games_played), 4),
            "steals_per_game":round( (player.steals_total/player.games_played), 4),
            "turnovers_per_game":round( (player.turnovers_total/player.games_played), 4),
            "personal_fouls_per_game":round( (player.personal_fouls_total/player.games_played),4),
            "free_throw_percentage":free_throw_percentage,
            "field_goal_percentage":field_goal_percentage,
            "minutes_per_game":round( (player.minutes_total/player.games_played)/(240), 4),
            "three_point_percentage":three_point_percentage,
            "free_throws_attempted_per_game":round( (player.free_throws_attempted/player.games_played),4),
            "free_throws_made_per_game":round( (player.free_throws_made/player.games_played), 4),
            "three_point_attempted_per_game":round( (player.three_point_attempted/player.games_played), 4),
            "three_point_made_per_game":round( (player.three_point_made/player.games_played), 4),
            "field_goals_attempted_per_game":round( (player.field_goals_attempted/player.games_played), 4),
            "field_goals_made_per_game":round( (player.field_goals_made/player.games_played), 4),
            'minutes':player.minutes_total/player.games_played,
            'games_played':player.games_played,
            'injured':player.is_injured

        })

        if player.player_id == '201939' or player.player_id == 201939: #steph curry has low 3pt so should fix
            player_avg[len(player_avg)-1]["three_point_attempted_per_game"]=9
            player_avg[len(player_avg)-1]["three_point_made_per_game"]=4
            player_avg[len(player_avg)-1]["field_goals_attempted_per_game"]=20
            player_avg[len(player_avg)-1]["field_goals_made_per_game"]=9

    stats_copy = copy.deepcopy(stats)
    #print('PLAYER AVG:',player_avg)
    player_stats = []
    team_stat = {}
    team_stat['team_id']=tid
    name_index = team.team_name.find(' ')
    team_stat['team_name']=team.team_name[name_index+1:]
    team_stat['team_city']=team.team_name[0:name_index]
    team_stat['team_abv']=team.team_abv
    team_stat['assists']=0
    team_stat['off_rebounds']=0
    team_stat['def_rebounds']=0
    team_stat['rebounds']=0
    team_stat['blocks']=0
    team_stat['steals']=0
    team_stat['turnovers']=0
    team_stat['personal_fouls']=0
    team_stat['FT_attempted']=0
    team_stat['FT_made']=0
    team_stat['FG_attempted']=0
    team_stat['FG_made']=0
    team_stat['3P_attempted']=0
    team_stat['3P_made']=0
    team_stat['points']=0


    for player in player_avg:
        if not player['injured']:
            player_stat = {}
            player_stat['name']=player['player_name']
            player_stat['player_id']=player['player_id']
            player_stat['team_id']=tid
            p = Player.objects.get(player_id=player['player_id'])

            off_rebound_min = 0 if (p.offensive_rebounds_total/p.games_played) < 1.2 else 0.5
            off_rebound_max = 2.6 if (p.offensive_rebounds_total/p.games_played) < 1.2 else 1.5
            #if (player['points_per_game'] > 0.2):
            #    player_stat['points'] = player['points_per_game']*(score)*random.uniform(0.7,1.4)
            #else:
            #   player_stat['points'] = player['points_per_game']*(score)*random.uniform(0.8,1.2)
            
            off_rebound_min = 0 if (p.offensive_rebounds_total/p.games_played) < 1.2 else 0.5
            off_rebound_max = 2.6 if (p.offensive_rebounds_total/p.games_played) < 1.2 else 1.5
            def_rebound_min = 0.5 if (p.defensive_rebounds_total/p.games_played) < 3.5 else 0.6
            def_rebound_max = 2 if (p.defensive_rebounds_total/p.games_played) < 3.5 else 1.4
            personal_fouls_min = 0.4 if (p.personal_fouls_total/p.games_played) < 4 else 0.5
            personal_fouls_max = 2 if (p.personal_fouls_total/p.games_played) < 4 else 1.5
            turnovers_min = 0.4 if (p.turnovers_total/p.games_played) < 1.2 else 0.5
            turnovers_max = 2.3 if (p.turnovers_total/p.games_played) < 1.2 else 1.5
            steal_min = 0 if (p.steals_total/p.games_played) < 1.2 else 0.5
            steal_max = 2.3 if (p.steals_total/p.games_played) < 1.2 else 1.5
            
            blocks_min = 0 if (p.steals_total/p.games_played) < 1.2 else 0.5
            blocks_max = 2.2 if (p.steals_total/p.games_played) < 1.2 else 1.5
            assists_min = 0 if (p.steals_total/p.games_played) < 3 else 0.5
            assists_max = 1.8 if (p.steals_total/p.games_played) < 3 else 1.5
            
            if (p.field_goals_attempted/p.games_played) < 5:
                fg_att_min = 0.4
                fg_att_max = 1.6
            elif (p.field_goals_attempted/p.games_played) < 9:
                fg_att_min = 0.6 
                fg_att_max = 1.45
            else:
                fg_att_min = 0.75
                fg_att_max = 1.35
            
            if (p.field_goals_made/p.games_played) < 3:
                fg_made_min = 0.45
                fg_made_max = 1.6
            elif (p.field_goals_made/p.games_played) < 7:
                fg_made_min = 0.7 
                fg_made_max = 1.4
            else:
                fg_made_min = 0.78
                fg_made_max = 1.3
            
            if (p.three_point_attempted/p.games_played) < 3:
                three_pt_att_min = 0 
                three_pt_att_max = 2
            elif (p.three_point_attempted/p.games_played) < 5:
                three_pt_att_min = 0.5 
                three_pt_att_max = 1.5
            elif (p.field_goals_attempted/p.games_played) < 10:
                three_pt_att_min = 0.6 
                three_pt_att_max = 1.35
            else:
                three_pt_att_min = 0.7 
                three_pt_att_max = 1.3
            
            if (p.three_point_made/p.games_played) < 2:
                three_pt_made_min = 0.3
                three_pt_made_max = 1.7
            elif (p.three_point_made/p.games_played) < 5:
                three_pt_made_min = 0.59
                three_pt_made_max = 1.45
            elif (p.three_point_made/p.games_played) < 8:
                three_pt_made_min = 0.67
                three_pt_made_max = 1.35
            else:
                three_pt_made_min = 0.78
                three_pt_made_max = 1.25
                
            if (p.free_throws_made/p.games_played) < 2:
                free_throws_made_min = 0 
                free_throws_made_max = 2.5
            elif (p.free_throws_made/p.games_played) < 5:
                free_throws_made_min = 0.6
                free_throws_made_max = 1.7
            elif (p.free_throws_made/p.games_played) < 8:
                free_throws_made_min = 0.7 
                free_throws_made_max = 1.6
            else:
                free_throws_made_min = 0.75
                free_throws_made_max = 1.45
                
            if (p.free_throws_attempted/p.games_played) < 2:
                free_throws_att_min = 0 
                free_throws_att_max = 2
            elif (p.free_throws_attempted/p.games_played) < 5:
                free_throws_att_min = 0.4
                free_throws_att_max = 1.8
            elif (p.free_throws_attempted/p.games_played) < 8:
                free_throws_att_min = 0.5 
                free_throws_att_max = 1.7
            else:
                free_throws_att_min = 0.6
                free_throws_att_max = 1.5
            
            #playoff_adjustment
            fg_att_max += 0.02
            fg_made_max += 0.025
            free_throws_made_max += 0.025
            free_throws_att_max += 0.025
            three_pt_att_max += 0.015
            three_pt_made_max += 0.015
            
            #nuggets
            if tid == 1610612743:
                fg_att_max -= 0.025
                fg_made_max -= 0.03
                free_throws_made_max -= 0.03
                free_throws_att_max -= 0.03
                three_pt_att_max -= 0.02
                three_pt_made_max -= 0.02
            
            #home team adjustment
            if home_var == True:
                fg_made_max += 0.01
                free_throws_made_max += 0.01
                three_pt_made_max += 0.01
            
            #Lakers
            if tid == 1610612747:
                fg_att_max += 0.04
                fg_made_max += 0.05
                fg_made_min += 0.025
                free_throws_made_max += 0.03
                free_throws_made_min += 0.005
                free_throws_att_max += 0.04
                three_pt_att_max += 0.03
                three_pt_made_max += 0.05
                three_pt_made_min += 0.03
            
            #rockets, Dallas, Heat, Raptors, Clippers, Bucks, Lakers, 76ers, Celtics, OKC, Nuggets
            if tid == 1610612745 or tid == 1610612742 or tid == 1610612748 or tid == 1610612761 or tid == 1610612746 or tid == 1610612749 or tid == 1610612747 or tid == 1610612755 or tid == 1610612738 or tid == 1610612760 or tid == 1610612743:
                free_throws_att_max += 0.1
                free_throws_made_max += 0.1
                three_pt_att_max += 0.06
                three_pt_made_max += 0.12
            
            
            #CLE
            if tid == 1610612739:
                fg_made_min -= 0.04
                
            #Pacers
            if tid == 1610612754:
                fg_att_max += 0.04
                fg_att_min -= 0.03
                fg_made_max += 0.055
                fg_made_min -= 0.01
                free_throws_made_max += 0.1
                free_throws_made_min += 0.04
                free_throws_att_max += 0.1
                free_throws_att_min += 0.04
                three_pt_att_min += 0.03
                three_pt_att_max += 0.05
                three_pt_made_min += 0.07
                three_pt_made_max += 0.15
            
            #Raptors
            if tid == 1610612761:
                fg_att_min -= 0.04
                fg_att_max -= 0.04
                fg_made_min -= 0.02
                fg_made_max -= 0.01
                
            #Heat
            if tid == 1610612748:
                fg_att_max += 0.06
                fg_made_max += 0.06
                free_throws_made_max += 0.032
                free_throws_made_min += 0.01
                free_throws_att_max += 0.04
                free_throws_att_min += 0.01
                three_pt_att_max += 0.05
                three_pt_made_max += 0.03
                
            #Knicks, Hornets, Nets, OKC, Pistons
            if  tid == 1610612752 or tid == 1610612766 or tid == 1610612751 or tid == 1610612760 or tid == 1610612765:
                fg_att_max += 0.1
                fg_att_min += 0.05
                fg_made_max += 0.1
                fg_made_min += 0.05
                free_throws_made_max += 0.1
                free_throws_made_min += 0.05
                free_throws_att_max += 0.1
                free_throws_att_min += 0.05
                three_pt_att_min += 0.05
                three_pt_att_max += 0.1
                three_pt_made_min += 0.05
                three_pt_made_max += 0.1
            
            #OKC
            if tid == 1610612760:
                fg_att_max += 0.035
                fg_att_min += 0.005
                fg_made_max += 0.02
                fg_made_min += 0.01
                free_throws_made_max += 0.03
                free_throws_made_min += 0.01
                
            #Knicks
            if tid == 1610612752:
                fg_made_max += 0.13
                fg_made_min += 0.07
                free_throws_made_max += 0.1
                free_throws_made_min += 0.05
                free_throws_att_max += 0.1
                free_throws_att_min += 0.05
                three_pt_made_min += 0.08
                three_pt_made_max += 0.14
            
            #76ers
            if tid == 1610612755:
                three_pt_made_min += 0.04
                three_pt_made_max += 0.06
                fg_made_min += 0.02
                fg_made_max += 0.03
            
            #rockets, bucks, lakers
            if tid == 1610612745 or tid == 1610612749 or tid == 1610612747:
                three_pt_made_max += 0.06
                fg_made_max += 0.06
                
            #Suns, 76ers, Pelicans, Kings,  Rockets
            if tid == 1610612756 or tid == 1610612755 or tid == 1610612740 or tid == 1610612745:
                fg_att_max -= 0.08
                fg_att_min -= 0.03
                fg_made_max -= 0.06
                fg_made_min -= 0.03
                three_pt_att_min -= 0.05
                three_pt_att_max -= 0.1
                three_pt_made_min -= 0.02
                three_pt_made_max -= 0.07
            
            #Pelicans
            if tid == tid == 1610612740:
                fg_att_max -= 0.07
                fg_att_min -= 0.04
                fg_made_max -= 0.055
                fg_made_min -= 0.03
                three_pt_made_min += 0.01
                three_pt_made_max += 0.03
                three_pt_att_min -= 0.02
                three_pt_att_max -= 0.03
                free_throws_made_min -= 0.03
                
            #Dallas
            if tid == 1610612742:
                fg_att_max += 0.01
                fg_att_min -= 0.04
                fg_made_max += 0.022
                fg_made_min += 0.012
            
            #Kings
            if tid == 1610612758:
                fg_att_max -= 0.07
                fg_att_min -= 0.03
                fg_made_max -= 0.065
                fg_made_min -= 0.02
                three_pt_att_min -= 0.03
                three_pt_att_max -= 0.07
                three_pt_made_min -= 0.02
                three_pt_made_max -= 0.06
                free_throws_made_min += 0.04
                free_throws_made_max += 0.05
                
            # Clippers
            if tid == 1610612746:
                fg_att_max -= 0.1
                fg_att_min -= 0.04
                fg_made_max -= 0.03
                fg_made_min -= 0.02
                three_pt_att_min -= 0.02
                three_pt_att_max -= 0.06
                three_pt_made_min -= 0.01
                three_pt_made_max -= 0.03
            
            #Washington, Celtics, Minnesota, Magic
            if tid == 1610612764 or tid == 1610612738 or tid == 1610612750 or tid == 1610612753:
                fg_att_max -= 0.08
                fg_att_min -= 0.03
                fg_made_max -= 0.07
                fg_made_min -= 0.03
                three_pt_att_min -= 0.03
                three_pt_att_max -= 0.08
                three_pt_made_min -= 0.03
                three_pt_made_max -= 0.7
            
            #Jazz
            if tid == 1610612762:
                fg_att_max += 0.03
                fg_att_min += 0.005
                fg_made_max += 0.012
                fg_made_min += 0.005
                free_throws_made_max += 0.02
                free_throws_att_max += 0.06
                
            #Warriors
            if tid == 1610612744:
                fg_att_max -= 0.15
                fg_att_min -= 0.07
                fg_made_max += 0.02
                fg_made_min -= 0.03
                three_pt_att_min -= 0.04
                three_pt_att_max -= 0.08
                three_pt_made_min += 0.01
                three_pt_made_max += 0.02
            
            #bulls, Nets
            if tid == 1610612741 or tid == 1610612751:
                fg_att_max -= 0.06
                fg_att_min -= 0.07
            
                
            
            if tid == 1610612744: #warriors
                player_stat['min']=round(player['minutes']*random.uniform(0.75,1.28))
            else:
                if player['minutes'] > 25:
                    player_stat['min']=round(player['minutes']*random.uniform(0.92,1.25))
                elif player['minutes'] > 18:
                    player_stat['min']=round(player['minutes']*random.uniform(0.85,1.25))
                elif player['minutes'] > 10:
                    player_stat['min']=round(player['minutes']*random.uniform(0.8,1.35))
                else:
                    player_stat['min']=round(player['minutes']*random.uniform(0.65,1.5))

            if stats_copy['minutes'] >= player_stat['min']:
                stats_copy['minutes'] -= player_stat['min']
            else:
                player_stat['min'] = stats_copy['minutes'] if stats_copy['minutes'] > 0 else 0
                stats_copy['minutes']-=player_stat['min'] 
            
            if stats_copy['minutes'] < 6 and stats_copy['minutes'] > 0:
                player_stat['min'] += stats_copy['minutes']
                stats_copy['minutes'] -= stats_copy['minutes']
            
            if player_stat['min'] > 0:
                player_stat['assists']= round(player['assists_per_game']*random.uniform(assists_min,assists_max))
                if stats_copy['assists'] >= player_stat['assists']:
                    stats_copy['assists'] -= player_stat['assists']
                else:
                    player_stat['assists'] = stats_copy['assists'] if stats_copy['assists'] > 0 else 0
                    stats_copy['assists']-=player_stat['assists']

                player_stat['off_rebounds']= round(player['offensive_rebounds_per_game']*random.uniform(off_rebound_min,off_rebound_max))
                if stats_copy['off_rebounds'] >= player_stat['off_rebounds']:
                    stats_copy['off_rebounds'] -= player_stat['off_rebounds']
                else:
                    player_stat['off_rebounds'] = stats_copy['off_rebounds'] if stats_copy['off_rebounds'] > 0 else 0
                    stats_copy['off_rebounds']-=player_stat['off_rebounds']
                
                player_stat['def_rebounds']= round(player['defensive_rebounds_per_game']*random.uniform(def_rebound_min,def_rebound_max))
                if stats_copy['def_rebounds'] >= player_stat['def_rebounds']:
                    stats_copy['def_rebounds'] -= player_stat['def_rebounds']
                else:
                    player_stat['def_rebounds'] = stats_copy['def_rebounds'] if stats_copy['def_rebounds'] > 0 else 0
                    stats_copy['def_rebounds']-=player_stat['def_rebounds']

                #player_stat['rebounds']=player_stat['defensive_rebounds']+player_stat['offensive_rebounds']

                player_stat['blocks']= round(player['blocks_per_game']*random.uniform(blocks_min,blocks_max))
                if stats_copy['blocks'] >= player_stat['blocks']:
                    stats_copy['blocks'] -= player_stat['blocks']
                else:
                    player_stat['blocks'] = stats_copy['blocks'] if stats_copy['blocks'] > 0 else 0
                    stats_copy['blocks']-=player_stat['blocks']

                player_stat['steals']= round(player['steals_per_game']*random.uniform(steal_min,steal_max))
                if stats_copy['steals'] >= player_stat['steals']:
                    stats_copy['steals'] -= player_stat['steals']
                else:
                    player_stat['steals'] = stats_copy['steals'] if stats_copy['steals'] > 0 else 0
                    stats_copy['steals']-=player_stat['steals']

                player_stat['turnovers']= round(player['turnovers_per_game']*random.uniform(turnovers_min,turnovers_max))
                if stats_copy['turnovers'] >= player_stat['turnovers']:
                    stats_copy['turnovers'] -= player_stat['turnovers']
                else:
                    player_stat['turnovers'] = stats_copy['turnovers'] if stats_copy['turnovers'] > 0 else 0
                    stats_copy['turnovers'] -= player_stat['turnovers']

                player_stat['personal_fouls']=round(player['personal_fouls_per_game']*random.uniform(personal_fouls_min,personal_fouls_max))
                if stats_copy['personal_fouls'] >= player_stat['personal_fouls']:
                    stats_copy['personal_fouls'] -= player_stat['personal_fouls']
                else:
                    player_stat['personal_fouls'] = stats_copy['personal_fouls'] if stats_copy['personal_fouls'] > 0 else 0
                    stats_copy['personal_fouls'] -= player_stat['personal_fouls']

                player_stat['FT_attempted']=round(player['free_throws_attempted_per_game']*random.uniform(free_throws_att_min,free_throws_att_max))
                if stats_copy['free_throws_attempted'] >= player_stat['FT_attempted']:
                    stats_copy['free_throws_attempted'] -= player_stat['FT_attempted']
                else:
                    player_stat['FT_attempted'] = stats_copy['free_throws_attempted'] if stats_copy['free_throws_attempted'] > 0 else 0
                    stats_copy['free_throws_attempted'] -= player_stat['FT_attempted']

                player_stat['FT_made']=round(player['free_throws_made_per_game']*random.uniform(free_throws_made_min,free_throws_made_max))
                if stats_copy['free_throws_made'] >= player_stat['FT_made']:
                    if player_stat['FT_attempted'] < player_stat['FT_made']:
                        player_stat['FT_made'] = player_stat['FT_attempted']
                    stats_copy['free_throws_made'] -= player_stat['FT_made']
                else:
                    if player_stat['FT_attempted'] >= player_stat['FT_made']:
                        player_stat['FT_made'] = stats_copy['free_throws_made'] if stats_copy['free_throws_made'] > 0 else 0
                        stats_copy['free_throws_made'] -= player_stat['FT_made']
                    else:
                        player_stat['FT_made'] = 0

                fg_att_weight = random.uniform(fg_att_min,fg_att_max)
                player_stat['3P_attempted']=round(player['three_point_attempted_per_game']*fg_att_weight)
                if stats_copy['three_point_attempted'] >= player_stat['3P_attempted']:
                    stats_copy['three_point_attempted'] -= player_stat['3P_attempted']
                else:
                    player_stat['3P_attempted'] = stats_copy['three_point_attempted'] if stats_copy['three_point_attempted'] > 0 else 0
                    stats_copy['three_point_attempted'] -= player_stat['3P_attempted']

                fg_made_weight = random.uniform(fg_made_min,fg_made_max)
                player_stat['3P_made']=round(player['three_point_made_per_game']*fg_made_weight)
                if stats_copy['three_point_made'] >= player_stat['3P_made'] and player_stat['3P_attempted'] >= player_stat['3P_made']:
                    stats_copy['three_point_made'] -= player_stat['3P_made']
                else:
                    if player_stat['3P_attempted'] >= player_stat['3P_made']:
                        player_stat['3P_made'] = stats_copy['three_point_made'] if stats_copy['free_throws_attempted'] > 0 else 0
                        stats_copy['three_point_made'] -= player_stat['3P_made'] 
                    else:
                        player_stat['3P_made'] = 0

                player_stat['FG_attempted']=round(player['field_goals_attempted_per_game']*fg_att_weight)-player_stat['3P_attempted']
                if stats_copy['field_goals_attempted'] >= player_stat['FG_attempted']:
                    stats_copy['field_goals_attempted'] -= player_stat['FG_attempted']
                else:
                    player_stat['FG_attempted'] = stats_copy['field_goals_attempted'] if stats_copy['field_goals_attempted'] > 0 else 0
                    stats_copy['field_goals_attempted'] -= player_stat['FG_attempted']


                player_stat['FG_made']=round(player['field_goals_made_per_game']*fg_made_weight)-player_stat['3P_made']
                if stats_copy['field_goals_made'] >= player_stat['FG_made'] and player_stat['FG_attempted'] >= player_stat['FG_made']:
                    stats_copy['field_goals_made'] -= player_stat['FG_made']
                else:
                    if player_stat['FG_attempted'] >= player_stat['FG_made']:
                        player_stat['FG_made'] = stats_copy['field_goals_made'] if stats_copy['field_goals_made'] > 0 else 0
                        stats_copy['field_goals_made'] -= player_stat['FG_made']
                    else:
                        player_stat['FG_made']=0

                player_stat['FG_attempted']+=player_stat['3P_attempted']
                player_stat['FG_made']+=player_stat['3P_made']

                if player_stat['3P_attempted'] > player_stat['FG_attempted']:
                    player_stat['FG_attempted'] = player_stat['3P_attempted']

                #if player_stat['FG_attempted'] < player_stat['FG_made']:
                    #player_stat['FG_attempted']=player_stat['FG_made']

                if player_stat['min'] < 22 and player_stat['min'] > 0:
                    if player_stat['assists'] > player_stat['min']/2.4:
                        player_stat['assists']=round(player_stat['assists']/2)
                    if player_stat['off_rebounds']+player_stat['def_rebounds'] > player_stat['min']/2.4:
                        player_stat['off_rebounds']=round(player_stat['off_rebounds']/2)
                    #if player_stat['def_rebounds'] > player_stat['min']/2:
                        player_stat['def_rebounds']=round(player_stat['def_rebounds']/2)
                        player_stat['rebounds']=player_stat['def_rebounds']+player_stat['off_rebounds']
                    
                    if player_stat['blocks'] > player_stat['min']/3:
                        player_stat['blocks']=round(player_stat['blocks']/3)
                    if player_stat['steals'] > player_stat['min']/3:
                        player_stat['steals']=round(player_stat['steals']/3)
                    if player_stat['turnovers'] > player_stat['min']/3:
                        player_stat['turnovers']=round(player_stat['turnovers']/3)
                    if player_stat['personal_fouls'] > player_stat['min']/3:
                        player_stat['personal_fouls']=round(player_stat['personal_fouls']/3)
                    if player_stat['FT_attempted'] > player_stat['min']/2:
                        player_stat['FT_attempted']=round(player_stat['FT_attempted']/2)
                    if player_stat['FT_made'] > player_stat['min']/2:
                        player_stat['FT_made']=round(player_stat['FT_made']/2)
                    if player_stat['3P_attempted'] > player_stat['min']/2.5:
                        print('3POINT')
                        player_stat['3P_attempted']=round(player_stat['3P_attempted']/2.5)
                    #if player_stat['3P_made'] > player_stat['min']/2.5:
                        player_stat['3P_made']=round(player_stat['3P_made']/2.5)
                    if player_stat['FG_attempted'] > player_stat['min']/2.5:
                        print('FGOAL')
                        player_stat['FG_attempted']=round(player_stat['FG_attempted']/2.5)
                        player_stat['FG_attempted']+=player_stat['3P_attempted']
                    #if player_stat['FG_made']+player_stat['3P_made'] > player_stat['min']/2.5:
                        player_stat['FG_made']=round(player_stat['FG_made']/2.5)
                        player_stat['FG_made']+=player_stat['3P_made']

                player_stat['comment']='OK'
                if player_stat['FG_attempted'] < player_stat['FG_made']:
                    player_stat['FG_attempted']=player_stat['FG_made']

                player_stat['points']=(player_stat['3P_made']*3) + ((player_stat['FG_made']-player_stat['3P_made'])*2) + player_stat['FT_made']
                player_stat['rebounds']=player_stat['off_rebounds']+player_stat['def_rebounds']
                '''if player['games_played'] > 5 and player['minutes']<10:
                    player_stat['minutes']=player['minutes']*random.uniform(0.3,0.5)
                else:
                    player_stat['minutes']=player['minutes']*random.uniform(0.9,1.1)'''
            else:
                player_stat['assists']=0
                player_stat['off_rebounds']=0
                player_stat['def_rebounds']=0
                player_stat['rebounds']=0
                player_stat['blocks']=0
                player_stat['steals']=0
                player_stat['turnovers']=0
                player_stat['personal_fouls']=0
                player_stat['FT_attempted']=0
                player_stat['FT_made']=0
                player_stat['FG_attempted']=0
                player_stat['FG_made']=0
                player_stat['3P_attempted']=0
                player_stat['3P_made']=0
                player_stat['points']=0
                player_stat['min']=0
                player_stat['comment']="NONE"

            team_stat['assists']+=player_stat['assists']
            team_stat['off_rebounds']+=player_stat['off_rebounds']
            team_stat['def_rebounds']+=player_stat['def_rebounds']
            team_stat['rebounds']+=(player_stat['off_rebounds']+player_stat['def_rebounds'])
            team_stat['blocks']+=player_stat['blocks']
            team_stat['steals']+=player_stat['steals']
            team_stat['turnovers']+=player_stat['turnovers']
            team_stat['personal_fouls']+=player_stat['personal_fouls']
            team_stat['FT_attempted']+=player_stat['FT_attempted']
            team_stat['FT_made']+=player_stat['FT_made']
            team_stat['FG_attempted']+=player_stat['FG_attempted']
            team_stat['FG_made']+=player_stat['FG_made']
            team_stat['3P_attempted']+=player_stat['3P_attempted']
            team_stat['3P_made']+=player_stat['3P_made']
            team_stat['points']+=player_stat['points']

            player_stats.append(player_stat)

    if team_stat['points']==other_team_score:
        team_stat['FT_made']+=1
        team_stat['FT_attempted']+=1
        player_stats[0]['FT_made']+=1
        player_stats[0]['FT_attempted']+=1
        team_stat['points']+=1

    #print()
    #pprint.pprint(player_stats)
    #pprint.pprint(team_stat)

    return [player_stats,team_stat]
    '''
    away_game_stats = {
        'minutes':240,
        'field_goals_percentage': ((biases['away_field_goal_percentage_bias'])+away_stats['field_goal_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
        'field_goals_attempted': round(((biases['away_field_goal_attempt_bias'])+away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])*overall_bias_away),
        'three_point_percentage': ((biases['away_three_point_pct_bias'])+away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
        'three_point_attempted': round(((biases['away_three_point_att_bias'])+away_stats['three_point_attempted_per_game'])+random.uniform(-away_bias_list[6],away_bias_list[7])*overall_bias_away),
        'free_throws_percentage': (((biases['away_free_throw_percentage_bias'])+away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
        'free_throws_attempted': round(((biases['away_free_throw_att_bias'])+away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away),
        'def_rebounds': round(((biases['away_def_rebounds_bias'])+away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away),
        'off_rebounds': round(((biases['away_off_rebounds_bias'])+away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away),
        #'rebounds': ((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away,
        'assists': round(((biases['away_assists_bias'])+away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away),
        'steals': round(((biases['away_steals_bias'])+away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away),
        'blocks': round(((biases['away_blocks_bias'])+away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away),
        'turnovers': round(((biases['away_turnovers_bias'])+away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away),
        'personal_fouls': round(((biases['away_personal_fouls_bias'])+away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away),
        #'points': (((biases['away_points_bias']+away_stats['points_per_game'])+(biases['away_points_per_game_bias']+away_stats['points_per_game']))/2)+random.uniform(away_bias_list[28],away_bias_list[29]),
    }
    '''

    '''
        {
  "points_by_quarter_id": {
    "1610612742": [
      33,
      24,
      27,
      29,
      0,
      0,
      0,
      0
    ],
    "1610612743": [
      29,
      21,
      35,
      12,
      0,
      0,
      0,
      0
    ]
  },
  "player_stats": [
 
    {
      "player_id": 1628420,
      "team_id": 1610612743,
      "name": "Monte Morris",
      "min": "17",
      "FG_made": 1,
      "FG_attempted": 6,
      "3P_made": 1,
      "3P_attempted": 3,
      "FT_made": 0,
      "FT_attempted": 0,
      "off_rebounds": 0,
      "def_rebounds": 0,
      "assists": 1,
      "steals": 1,
      "blocks": 0,
      "turnovers": 0,
      "personal_fouls": 0,
      "points": 3,
      "comment": "OK"
    },
    {
      "team_id": 1610612743,
      "player_id": 203943,
      "name": "Noah Vonleh",
      "comment": "DNP - Coach's Decision                  "
    },
  ],
  "team_stats": [
    {
      "team_id": 1610612743,
      "team_name": "Nuggets",
      "team_abv": "DEN",
      "team_city": "Denver",
      "FG_made": 39,
      "FG_attempted": 83,
      "3P_made": 14,
      "3P_attempted": 39,
      "FT_made": 5,
      "FT_attempted": 8,
      "off_rebounds": 3,
      "def_rebounds": 37,
      "assists": 23,
      "steals": 6,
      "blocks": 4,
      "turnovers": 15,
      "personal_fouls": 20,
      "points": 97
    },
    {
      "team_id": 1610612742,
      "team_name": "Mavericks",
      "team_abv": "DAL",
      "team_city": "Dallas",
      "FG_made": 42,
      "FG_attempted": 92,
      "3P_made": 12,
      "3P_attempted": 35,
      "FT_made": 17,
      "FT_attempted": 23,
      "off_rebounds": 13,
      "def_rebounds": 39,
      "assists": 23,
      "steals": 9,
      "blocks": 2,
      "turnovers": 10,
      "personal_fouls": 14,
      "points": 113
    }
  ]
}
    '''
    


def compute_points_by_quarter(total_points_home, total_points_away, num_ots):
    overtime_scores_away=[]
    overtime_scores_home=[]
    if (num_ots>0):
        #for i in range(0,num_ots): --->>>#ONLY ONE OT I hardcoded it
        if total_points_home < total_points_away:
            home_score = random.randint(5,10)
            away_score = random.randint(1,5)+home_score
            overtime_scores_away.append(away_score)
            overtime_scores_home.append(home_score)
            total_points_away -= away_score
            total_points_home -= home_score
        else:
            away_score = random.randint(5,10)
            home_score = random.randint(1,5)+away_score
            overtime_scores_away.append(away_score)
            overtime_scores_home.append(home_score)
            total_points_away -= away_score
            total_points_home -= home_score

    basis_home = int(total_points_home/4)

    quarter_1_home = random.randint(basis_home-6,basis_home+6)
    quarter_2_home = random.randint(basis_home-6,basis_home+6)
    quarter_3_home = random.randint(basis_home-6,basis_home+6)
    quarter_4_home = total_points_home - (quarter_1_home + quarter_2_home + quarter_3_home)
    if quarter_4_home < 18:
        quarter_1_home -= 4
        quarter_2_home -= 4
        quarter_3_home -= 4
        quarter_4_home += 12
    elif quarter_4_home > 32:
        quarter_1_home += 4
        quarter_2_home += 4
        quarter_3_home += 4
        quarter_4_home -= 12

    basis_away = int(total_points_away/4)
    quarter_1_away = random.randint(basis_away-6,basis_away+6)
    quarter_2_away = random.randint(basis_away-6,basis_away+6)
    quarter_3_away = random.randint(basis_away-6,basis_away+6)
    quarter_4_away = total_points_away - (quarter_1_away + quarter_2_away + quarter_3_away)
    if quarter_4_away < 18:
        quarter_1_away -= 4
        quarter_2_away -= 4
        quarter_3_away -= 4
        quarter_4_away += 12
    elif quarter_4_away > 32:
        quarter_1_away += 4
        quarter_2_away += 4
        quarter_3_away += 4
        quarter_4_away -= 12

    if len(overtime_scores_home)>0:
        return  {
                    'home_scores':[[quarter_1_home,quarter_2_home,
                            quarter_3_home,quarter_4_home]+overtime_scores_home],
                    'away_scores':[[quarter_1_away,quarter_2_away,
                            quarter_3_away,quarter_4_away]+overtime_scores_away]
                }

    
    return  {
                'home_scores':[quarter_1_home,quarter_2_home,
                        quarter_3_home,quarter_4_home],
                'away_scores':[quarter_1_away,quarter_2_away,
                        quarter_3_away,quarter_4_away]
            }
    
   

'''def compute_overtime(away_stats,home_stats,overall_bias_away,overall_bias_home,biases,away_bias_list,home_bias_list,points_away,points_home):
    num_ots = 0
    while (points_away == points_home):
        num_ots += 1
        away_stats = {
            'minutes':25+away_stats['minutes'],
            'field_goals_percentage': ((biases['away_field_goal_percentage_bias'])+away_stats['field_goals_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
            'field_goals_attempted': round((((biases['away_field_goals_attempt_bias'])+away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])*overall_bias_away) + away_stats['field_goals_attempted']),
            'three_point_percentage': ((biases['away_three_point_pct_bias'])+away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
            'three_point_attempted': round((((biases['away_three_point_att_bias'])+away_stats['three_point_attempted_per_game'])+random.uniform(-away_bias_list[6],away_bias_list[7])*overall_bias_away ) + away_stats['three_point_attempted']),
            'free_throws_percentage': (((biases['away_free_throw_percentage_bias'])+away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
            'free_throws_attempted': round((((biases['away_free_throw_att_bias'])+away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away) + away_stats['free_throws_attempted']),
            'def_rebounds': round((((biases['away_def_rebounds_bias'])+away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away) + away_stats['def_rebounds']),
            'off_rebounds': round((((biases['away_off_rebounds_bias'])+away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away) +away_stats['off_rebounds']),
            'rebounds': round((((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away) + away_stats['rebounds']),
            'assists': round((((biases['away_assists_bias'])+away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away) + away_stats['assists']),
            'steals': round((((biases['away_steals_bias'])+away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away) + away_stats['steals']),
            'blocks': round((((biases['away_blocks_bias'])+away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away) + away_stats['blocks']),
            'turnovers': round((((biases['away_turnovers_bias'])+away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away) + away_stats['turnovers']),
            'personal_fouls': round((((biases['away_personal_fouls_bias'])+away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away) + away_stats['personal_fouls']),
            #'points': (((biases['away_points_bias']+away_stats['points_per_game'])+(biases['away_points_per_game_bias']+away_stats['points_per_game']))/2)+random.uniform(away_bias_list[28],away_bias_list[29]),
        }
        home_stats = {
            'minutes':5+home_stats['minutes'],
            'field_goals_percentage': ((biases['home_field_goal_percentage_bias'])+home_stats['field_goals_percentage'])*(random.uniform(home_bias_list[0], home_bias_list[1]))*overall_bias_home,
            'field_goals_attempted': (((biases['home_field_goal_attempt_bias'])+home_stats['field_goals_attempted_per_game'])+random.uniform(home_bias_list[2],home_bias_list[3])*overall_bias_home) + home_stats['field_goals_attempted'],
            'three_point_percentage': ((biases['home_three_point_pct_bias'])+home_stats['three_point_percentage'])*(random.uniform(home_bias_list[4], home_bias_list[5]))*overall_bias_home,
            'three_point_attempted': (((biases['home_three_point_att_bias'])+home_stats['three_point_attempted_per_game'])+random.uniform(-home_bias_list[6],home_bias_list[7])*overall_bias_home ) + home_stats['three_point_attempted'],
            'free_throws_percentage': (((biases['home_free_throw_percentage_bias'])+home_stats['free_throw_percentage'])*(random.uniform(home_bias_list[8], home_bias_list[9])))*overall_bias_home,
            'free_throws_attempted': (((biases['home_free_throw_att_bias'])+home_stats['free_throws_attempted_per_game'])+random.uniform(home_bias_list[10],home_bias_list[11])*overall_bias_home) + home_stats['free_throws_attempted'],
            'def_rebounds': (((biases['home_def_rebounds_bias'])+home_stats['defensive_rebounds_per_game'])+random.uniform(home_bias_list[12],home_bias_list[13])*overall_bias_home) + home_stats['def_rebounds'],
            'off_rebounds': (((biases['home_off_rebounds_bias'])+home_stats['offensive_rebounds_per_game'])+random.uniform(home_bias_list[14],home_bias_list[15])*overall_bias_home) +home_stats['off_rebounds'],
            'rebounds': (((biases['home_rebounds_bias'])+home_stats['rebounds_per_game'])+random.uniform(home_bias_list[16],home_bias_list[17])*overall_bias_home) + home_stats['rebounds'],
            'assists': (((biases['home_assists_bias'])+home_stats['assists_per_game'])+random.uniform(home_bias_list[18],home_bias_list[19])*overall_bias_home) + home_stats['assists'],
            'steals': (((biases['home_steals_bias'])+home_stats['steals_per_game'])+random.uniform(home_bias_list[20],home_bias_list[21])*overall_bias_home) + home_stats['steals'],
            'blocks': (((biases['home_blocks_bias'])+home_stats['blocks_per_game'])+random.uniform(home_bias_list[22],home_bias_list[23])*overall_bias_home) + home_stats['blocks'],
            'turnovers': (((biases['home_turnovers_bias'])+home_stats['turnovers_per_game'])+random.uniform(home_bias_list[24],home_bias_list[25])*overall_bias_home) + home_stats['turnovers'],
            'personal_fouls': (((biases['home_personal_fouls_bias'])+home_stats['personal_fouls_per_game'])+ random.uniform(home_bias_list[26],home_bias_list[27])*overall_bias_home) + home_stats['personal_fouls'],
            #'points': (((biases['home_points_bias']+home_stats['points_per_game'])+(biases['home_points_per_game_bias']+home_stats['points_per_game']))/2)+random.uniform(home_bias_list[28],home_bias_list[29]),
        }
        total_points_away = (away_stats['three_points_made']*3) + ((away_stats['field_goals_made']-away_stats['three_points_made'])*2) + away_stats['free_throws_made']
        total_points_home = (home_stats['three_points_made']*3)+((home_stats['field_goals_made']-home_stats['three_points_made'])*2) + home_stats['free_throws_made']
        if total_points_away == total_points_home:
            home_stats['free_throws_made']+=1
            home_stats['free_throws_percentage']=home_stats['free_throws_made']/home_stats['free_throws_attempted']
    
    return [away_stats,home_stats,num_ots]
'''



def compute_biases(away_stats,home_stats,matchup_away,matchup_home):
    biases = {
        'home_points_bias':home_stats['points_per_game']-away_stats['opponent_points_per_game'],
        'away_points_bias':away_stats['points_per_game']-home_stats['opponent_points_per_game'],
        'home_bias':home_stats['home_wins']/(home_stats['home_losses']+home_stats['home_wins']),
        'away_bias':away_stats['away_wins']/(away_stats['away_losses']+away_stats['away_wins']),
        'home_points_per_game_bias':home_stats['points_per_game']-matchup_home['points_pg'],
        'away_points_per_game_bias':away_stats['points_per_game']-matchup_away['points_pg'],
        'home_matchup_bias': (matchup_home['wins']/(matchup_home['losses']+matchup_home['wins'])),
        'away_matchup_bias': (matchup_away['wins']/(matchup_away['losses']+matchup_away['wins'])),
        'home_field_goal_attempt_bias': matchup_home['fg_attempted_pg']-home_stats['field_goals_attempted_per_game'],
        'away_field_goal_attempt_bias': matchup_away['fg_attempted_pg']-away_stats['field_goals_attempted_per_game'],
        'home_field_goal_percentage_bias': matchup_home['fg_pct']-home_stats['field_goal_percentage'],
        'away_field_goal_percentage_bias': matchup_away['fg_pct']-away_stats['field_goal_percentage'],
        'home_three_point_att_bias': matchup_home['three_pt_att_pg']-home_stats['three_point_attempted_per_game'],
        'away_three_point_att_bias': matchup_away['three_pt_att_pg']-away_stats['three_point_attempted_per_game'],
        'home_three_point_pct_bias': matchup_home['three_pt_pct']-home_stats['three_point_percentage'],
        'away_three_point_pct_bias': matchup_away['three_pt_pct']-away_stats['three_point_percentage'],
        'home_free_throw_att_bias':matchup_home['free_throw_att_pg']-home_stats['free_throws_attempted_per_game'],
        'away_free_throw_att_bias':matchup_away['free_throw_att_pg']-away_stats['free_throws_attempted_per_game'],
        'home_free_throw_percentage_bias':matchup_home['free_throw_pct']-home_stats['free_throw_percentage'],
        'away_free_throw_percentage_bias':matchup_away['free_throw_pct']-away_stats['free_throw_percentage'],
        'home_plus_minus_bias': home_stats['plus_minus']-matchup_home['plus_minus'],
        'away_plus_minus_bias': away_stats['plus_minus']-matchup_away['plus_minus'],
        'home_assists_bias': matchup_home['ast_pg']-home_stats['assists_per_game'],
        'away_assists_bias': matchup_away['ast_pg']-away_stats['assists_per_game'],
        'home_off_rebounds_bias': matchup_home['orb_pg']-home_stats['offensive_rebounds_per_game'],
        'away_off_rebounds_bias': matchup_away['orb_pg']-away_stats['offensive_rebounds_per_game'],
        'home_def_rebounds_bias': matchup_home['drb_pg']-home_stats['defensive_rebounds_per_game'],
        'away_def_rebounds_bias': matchup_away['drb_pg']-away_stats['defensive_rebounds_per_game'],
        'home_rebounds_bias': matchup_home['rb_pg']-home_stats['rebounds_per_game'],
        'away_rebounds_bias': matchup_away['rb_pg']-away_stats['rebounds_per_game'],
        'home_blocks_bias': matchup_home['block_pg']-home_stats['blocks_per_game'],
        'away_blocks_bias': matchup_away['block_pg']-away_stats['blocks_per_game'],
        'home_steals_bias': matchup_home['steals_pg']-home_stats['steals_per_game'],
        'away_steals_bias': matchup_away['steals_pg']-away_stats['steals_per_game'],
        'home_turnovers_bias': matchup_home['turnovers_pg']-home_stats['turnovers_per_game'],
        'away_turnovers_bias': matchup_away['turnovers_pg']-away_stats['turnovers_per_game'],
        'home_personal_fouls_bias': matchup_home['personal_fouls_pg']-home_stats['personal_fouls_per_game'],
        'away_personal_fouls_bias': matchup_away['personal_fouls_pg']-away_stats['personal_fouls_per_game'],
    }
    #print("NFIENF:",biases['home_field_goal_percentage_bias'])
    return biases

def get_team(team1):
    list_teams = {
        "atlanta":1610612737,
        "boston":1610612738,
        "brooklyn":1610612751,
        "charlotte":1610612766,
        "chicago":1610612741,
        "cleveland":1610612739,
        "dallas":1610612742,
        "denver":1610612743,
        "detroit":1610612765,
        "golden st.":1610612744,
        "houston":1610612745,
        "indiana":1610612754,
        "l.a. clippers":1610612746,
        "l.a. lakers":1610612747,
        "memphis":1610612763,
        "miami":1610612748,
        "milwaukee":1610612749,
        "minnesota":1610612750,
        "new orleans":1610612740,
        "new york":1610612752,
        "oklahoma city":1610612760,
        "orlando":1610612753,
        "philadelphia":1610612755,
        "phoenix":1610612756,
        "portland":1610612757,
        "sacramento":1610612758,
        "san antonio":1610612759,
        "toronto":1610612761,
        "utah":1610612762,
        "washington":1610612764
    }

    return list_teams[team1]


def get_bias_home(team_id):
    team_list_dist = {
        1610612749:[0.91, 1.18, -4, 5, 0.88, 1.11, -5, 5.5, 0.9, 1.05, -5, 7, -4, 5, -2, 3, -4, 5, -3, 3, -2, 3, -2, 3, -3, 3, -3, 3, -10, 10],#MIL
        1610612747:[0.92, 1.16, -4, 5, 0.88, 1.12, -5, 5.4, 0.87, 1.02, -5, 7, -4, 5, -2, 4, -3, 6, -4, 5, -3, 4, -2, 3, -3, 3, -3, 3, -7, 7], #LAL
        1610612737:[0.88, 1.13, -4, 4.4, 0.87, 1.12, -5.3, 6.5, 0.9, 1.03, -5, 5, -5,4, -3, 3, -6, 3, -3, 3, -3, 2, -2, 2, -3, 3, -3, 3, -4, 10],#ATL
        1610612738:[0.9, 1.14, -4, 5, 0.87, 1.1, -5.2, 5.5, 0.9, 1.03, -5, 6, -4, 4, -2, 2, -3, 3, -4, 6, -2, 3, -2, 3, -3, 2, -3, 3, -7, 10],#BOS
        1610612751:[0.87, 1.12, -4, 4.3, 0.87, 1.1, -5.2, 5, 0.9, 1.02, -5, 5, -4, 5, -3, 4, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#BKN
        1610612766:[0.87, 1.11, -4, 4.2, 0.87, 1.1, -5, 5.3, 0.9, 1.03, -5, 5, -5, 4, -2, 2, -4, 3, -3, 2, -2, 2, -2, 2, -3, 2, -3, 3, -4, 10],#CHA
        1610612741:[0.88, 1.13, -4, 4.4, 0.88, 1.1, -5, 5.3, 0.9, 1.02, -5, 5, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CHI
        1610612739:[0.87, 1.11, -4, 4.2, 0.87, 1.1, -5, 5, 0.9, 1.02, -5, 5, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CLE
        1610612742:[0.91, 1.16, -4, 5.4, 0.9, 1.13, -5, 6, 0.93, 1.02, -5, 6, -3, 5, -4, 5, -3, 5, -3, 6, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DAL
        1610612743:[0.9, 1.13, -4, 5.3, 0.88, 1.13, -5, 6, 0.91, 1.02, -5, 5, -3, 4, -4, 4, -3, 4, -3, 4, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DEN
        1610612765:[0.88, 1.11, -4, 4.3, 0.87, 1.1, -5, 5, 0.88, 1.02, -5, 5, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#DET
        1610612744:[0.89, 1.12, -4, 5, 0.87, 1.12, -5, 5.8, 0.93, 1.05, -3, 3, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#GSW
        1610612745:[0.87, 1.17, -4, 5, 0.89, 1.17, -5, 7.3, 0.93, 1.02, -2, 4, -3, 4, -3, 4, -3, 4, -3, 5, -2, 4, -2, 2, -2, 4, -3, 3, -7, 12],#HOU
        1610612754:[0.9, 1.15, -4, 5.3, 0.88, 1.12, -5, 6.2, 0.9, 1.02, -4, 4, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#IND
        1610612746:[0.91, 1.16, -4, 5, 0.88, 1.12, -5, 6, 0.9, 1.02, -4, 4, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#LAC
        1610612763:[0.9, 1.15, -4, 5, 0.87, 1.1, -5, 5.4, 0.88, 1.02, -5, 5, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MEM
        1610612748:[0.91, 1.16, -4, 5.3, 0.88, 1.15, -5, 5.8, 0.94, 1.02, -5, 5, -3, 4, -4, 5, -3, 4, -3, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIA
        1610612750:[0.88, 1.13, -4, 4.3, 0.87, 1.1, -5, 5, 0.88, 1.02, -5, 4, -3, 4, -4, 5, -3, 4, -2, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIN
        1610612740:[0.88, 1.13, -4, 4.5, 0.87, 1.12, -5, 5, 0.91, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NOR
        1610612752:[0.88, 1.11, -4, 4.1, 0.87, 1.1, -5, 5, 0.87, 1.02, -4, 4, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NYK
        1610612760:[0.89, 1.16, -4, 6, 0.88, 1.13, -5, 5, 0.9, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#OKC
        1610612753:[0.88, 1.12, -4, 4.2, 0.87, 1.1, -5, 5, 0.88, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#ORL
        1610612755:[0.93, 1.2, -4, 5, 0.87, 1.1, -5, 5, 0.9, 1.02, -4, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHI
        1610612756:[0.88, 1.12, -4, 4.4, 0.87, 1.11, -5, 6.2, 0.88, 1.02, -4, 4, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHX
        1610612757:[0.89, 1.12, -4, 4.6, 0.87, 1.13, -5, 6.2, 0.88, 1.02, -4, 4, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#POR
        1610612758:[0.88, 1.11, -4, 5, 0.87, 1.1, -5, 5, 0.88, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#SAC
        1610612759:[0.9, 1.12, -4, 4.5, 0.87, 1.11, -4, 4, 0.88, 1.03, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2 ,2, -2, 3, -4, 3, -3, 3, -7, 10],#SAS
        1610612761:[0.91, 1.17, -4, 5.2, 0.87, 1.12, -5, 6, 0.88, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#TOR
        1610612762:[0.9, 1.14, -4, 5.2, 0.87, 1.13, -5, 5.5, 0.88, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#UTA
        1610612764:[0.88, 1.11, -4, 4.6, 0.87, 1.11, -5, 6, 0.88, 1.02, -5, 5, -3, 4, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10]#WIZ
    }
    return team_list_dist[team_id]

def get_bias_away(team_id):
    team_list_dist = {
        1610612749:[0.9, 1.15, -4, 5, 0.88, 1.11, -5, 5.5, 0.89, 1.05, -5, 7, -3, 5, -3, 4, -3, 4, -3, 3, -2, 2, -2, 3, -2, 1, -3, -3, -10, 10],#MIL
        1610612747:[0.9, 1.15, -4, 5, 0.88, 1.11, -5, 5.4, 0.86, 1.02, -5, 7, -4, 5, -2, 4, -3, 4, -4, 5, -3, 4, -2, 3, -1, 1, -3, 3, -7, 7], #LAL
        1610612737:[0.86, 1.1, -4, 4.4, 0.87, 1.1, -5.3, 6.5, 0.89, 1.03, -5, 5, -7,3, -2, 2, -4, 3, -3, 2, -2, 1, -1, 1, -3, 2, -3, 3, -4, 10],#ATL
        1610612738:[0.88, 1.12, -4, 5, 0.86, 1.1, -5.2, 5.5, 0.89, 1.03, -5, 5, -4, 4, -2, 2, -3, 3, -3, 5, -1, 3, -2, 3, -3, 2, -3, 3, -7, 10],#BOS
        1610612751:[0.86, 1.1, -4, 4.3, 0.85, 1.1, -5, 5, 0.89, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#BKN
        1610612766:[0.86, 1.1, -4, 4.2, 0.85, 1.1, -5, 5.3, 0.89, 1.03, -5, 6, -5, 3, -2, 2, -6, 3, -3, 2, -2, 1, -1, 1, -3, 2, -3, 3, -4, 10],#CHA
        1610612741:[0.89, 1.1, -4, 4.4, 0.86, 1.1, -5, 5.3, 0.89, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CHI
        1610612739:[0.86, 1.1, -4, 4.2, 0.86, 1.1, -5, 5, 0.89, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CLE
        1610612742:[0.89, 1.12, -4, 5.4, 0.87, 1.11, -5, 6, 0.92, 1.02, -5, 6, -3, 5, -4, 5, -3, 5, -3, 6, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DAL
        1610612743:[0.89, 1.1, -4, 5.3, 0.87, 1.11,-5, 6, 0.9, 1.02, -5, 5, -3, 4, -4, 4, -3, 4, -3, 4, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DEN
        1610612765:[0.86, 1.1, -4, 4.3, 0.87, 1.1, -5, 5, 0.87, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#DET
        1610612744:[0.87, 1.1, -4, 4, 0.86, 1.1, -5, 5.8, 0.92, 1.05, -4, 4, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#GSW
        1610612745:[0.86, 1.12, -4, 5, 0.9, 1.12, -5, 7.3, 0.92, 1.02, -4, 6, -3, 4, -3, 4, -3, 4, -3, 5, -2, 4, -2, 2, -2, 4, -3, 3, -7, 12],#HOU
        1610612754:[0.89, 1.12, -4, 5.3, 0.87, 1.11, -5, 6.2, 0.89, 1.02, -3, 3, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#IND
        1610612746:[0.9, 1.12, -4, 5, 0.87, 1.13, -5, 6, 0.89, 1.02, -3, 3, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#LAC
        1610612763:[0.87, 1.11, -4, 5, 0.86, 1.11, -5, 5.4, 0.87, 1.02, -4, 4, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MEM
        1610612748:[0.9, 1.13, -4, 5.3, 0.91, 1.12, -5, 5.8, 0.93, 1.02, -5, 5, -3, 4, -4, 5, -3, 4, -3, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIA
        1610612750:[0.87, 1.1, -4, 4.3, 0.86, 1.1, -5, 5, 0.87, 1.02, -5, 4, -3, 4, -4, 5, -3, 4, -2, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIN
        1610612740:[0.87, 1.1, -4, 4.5, 0.86, 1.12, -5, 5, 0.9, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NOR
        1610612752:[0.86, 1.1, -4, 4.1, 0.86, 1.9, -5, 5, 0.86, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NYK
        1610612760:[0.88, 1.14, -4, 5, 0.88, 1.13, -5, 5, 0.89, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#OKC
        1610612753:[0.87, 1.1, -4, 4.2, 0.85, 1.1, -5, 5, 0.87, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#ORL
        1610612755:[0.88, 1.12, -4, 5, 0.85, 1.1, -4, 4, 0.89, 1.02, -4, 4, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHI
        1610612756:[0.87, 1.11, -4, 4.4, 0.86, 1.1, -5, 5.4, 0.87, 1.02, -4, 3, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHX
        1610612757:[0.88, 1.11, -4, 4.6, 0.87, 1.11, -5, 6.2, 0.87, 1.02, -4, 3, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#POR
        1610612758:[0.87, 1.1, -4, 5, 0.85, 1.1, -5, 5, 0.87, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#SAC
        1610612759:[0.88, 1.1, -4, 4.4, 0.85, 1.11, -4, 4, 0.87, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2 ,2, -2, 3, -4, 3, -3, 3, -7, 10],#SAS
        1610612761:[0.9, 1.14, -4, 5.3, 0.88, 1.12, -5, 6, 0.88, 1.03, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#TOR
        1610612762:[0.89, 1.14, -4, 5.3, 0.88, 1.12, -5, 5.5, 0.87, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#UTA
        1610612764:[0.87, 1.1, -4, 4.6, 0.88, 1.1, -5, 5.8, 0.87, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10]#WIZ
    }
    return team_list_dist[team_id]
            
    

def get_other_data(team,opponent):
    #print("Team:", team)
    #print("Opponent:", opponent)

    team_matchup_2019_2020 = TeamDashboardByOpponent( team_id=team, 
                                            opponent_team_id=opponent,
                                            season='2019-20').get_dict()['resultSets'][3]['rowSet']
                                
    team_matchup_2018_2019 = TeamDashboardByOpponent( team_id=team, 
                                            opponent_team_id=opponent,
                                            season='2018-19').get_dict()['resultSets'][3]['rowSet']
    #print(team_matchup_2018_2019)

    if len(team_matchup_2018_2019) > 0:
        team_matchup_2018_2019 = team_matchup_2018_2019[0] #gets data
        #matchup_data['2018-2019 Season'] = {

        matchup_data = {
            'games_played':team_matchup_2018_2019[2],
            'wins':team_matchup_2018_2019[3],
            'losses':team_matchup_2018_2019[4],  
            'win_pct':team_matchup_2018_2019[5], 
            'fg_pct':round(team_matchup_2018_2019[9]*100,1), 
            'fg_attempted_pg':team_matchup_2018_2019[8]/team_matchup_2018_2019[2],
            'block_pg':team_matchup_2018_2019[22]/team_matchup_2018_2019[2],
            'rb_pg':team_matchup_2018_2019[18]/team_matchup_2018_2019[2],
            'steals_pg':team_matchup_2018_2019[21]/team_matchup_2018_2019[2],
            'turnovers_pg':team_matchup_2018_2019[20]/team_matchup_2018_2019[2],
            'personal_fouls_pg':team_matchup_2018_2019[24]/team_matchup_2018_2019[2],
            'orb_pg':team_matchup_2018_2019[16]/team_matchup_2018_2019[2],
            'drb_pg':team_matchup_2018_2019[17]/team_matchup_2018_2019[2],
            'ast_pg':team_matchup_2018_2019[19]/team_matchup_2018_2019[2], 
            'three_pt_att_pg':team_matchup_2018_2019[11]/team_matchup_2018_2019[2],
            'three_pt_pct':round((team_matchup_2018_2019[12])*100,1), 
            'plus_minus':team_matchup_2018_2019[27]/team_matchup_2018_2019[2],
            'free_throw_att_pg':team_matchup_2018_2019[14]/team_matchup_2018_2019[2],
            'free_throw_pct':round((team_matchup_2018_2019[15])*100,1),
            'points_pg':team_matchup_2018_2019[26]/team_matchup_2018_2019[2] 
        }

    if len(team_matchup_2019_2020) > 0:
        team_matchup_2019_2020 = team_matchup_2019_2020[0] #gets data
        #matchup_data['2019-2020 Season'] = {

        matchup_data['games_played']=matchup_data['games_played']+team_matchup_2019_2020[2]
        matchup_data['wins']=matchup_data['wins']+team_matchup_2019_2020[3]
        matchup_data['losses']=matchup_data['losses']+team_matchup_2019_2020[4]
        matchup_data['win_pct']=(matchup_data['win_pct']+team_matchup_2019_2020[5])/2
        matchup_data['fg_pct']=(matchup_data['fg_pct']+round(team_matchup_2019_2020[9]*100,1))/2
        matchup_data['fg_attempted_pg']=(matchup_data['fg_attempted_pg']+(team_matchup_2019_2020[8]/team_matchup_2019_2020[2]))/2
        matchup_data['block_pg']=(matchup_data['block_pg']+(team_matchup_2019_2020[22]/team_matchup_2019_2020[2]))/2
        matchup_data['rb_pg']=(matchup_data['rb_pg']+(team_matchup_2019_2020[18]/team_matchup_2019_2020[2]))/2
        matchup_data['steals_pg']=(matchup_data['steals_pg']+(team_matchup_2019_2020[21]/team_matchup_2019_2020[2]))/2
        matchup_data['turnovers_pg']=(matchup_data['turnovers_pg']+(team_matchup_2019_2020[20]/team_matchup_2019_2020[2]))/2
        matchup_data['personal_fouls_pg']=(matchup_data['personal_fouls_pg']+(team_matchup_2019_2020[24]/team_matchup_2019_2020[2]))/2
        matchup_data['orb_pg']=(matchup_data['orb_pg']+(team_matchup_2019_2020[16]/team_matchup_2019_2020[2]))/2
        matchup_data['drb_pg']=(matchup_data['drb_pg']+(team_matchup_2019_2020[17]/team_matchup_2019_2020[2]))/2
        matchup_data['ast_pg']=(matchup_data['ast_pg']+(team_matchup_2019_2020[19]/team_matchup_2019_2020[2]))/2
        matchup_data['three_pt_att_pg']=(matchup_data['three_pt_att_pg']+(team_matchup_2019_2020[11]/team_matchup_2019_2020[2]))/2
        matchup_data['three_pt_pct']=(matchup_data['three_pt_pct']+round((team_matchup_2019_2020[12])*100,1))/2
        matchup_data['plus_minus']=(matchup_data['plus_minus']+(team_matchup_2019_2020[27]/team_matchup_2019_2020[2]))/2
        matchup_data['free_throw_att_pg']=(matchup_data['free_throw_att_pg']+(team_matchup_2019_2020[14]/team_matchup_2019_2020[2]))/2
        matchup_data['free_throw_pct']=(matchup_data['free_throw_pct']+(round((team_matchup_2019_2020[15])*100,1)))/2
        matchup_data['points_pg']=(matchup_data['points_pg']+(team_matchup_2019_2020[26]/team_matchup_2019_2020[2]))/2
        #print('LOOK2:',matchup_data['block_pg'])
        #return matchup_data

    '''matchup_data={}
    if len(team_matchup_2018_2019) > 0:
        team_matchup_2018_2019 = team_matchup_2018_2019[0] #gets data
        #matchup_data['2018-2019 Season'] = {
        matchup_data = {
            'games_played':team_matchup_2018_2019[2],
            'wins':team_matchup_2018_2019[3],
            'losses':team_matchup_2018_2019[4],  
            'win_pct':team_matchup_2018_2019[5], 
            'fg_pct':round(team_matchup_2018_2019[9]*100,1), 
            'fg_attempted_pg':team_matchup_2018_2019[8]/team_matchup_2018_2019[2],
            'block_pg':team_matchup_2018_2019[22]/team_matchup_2018_2019[2],
            'rb_pg':team_matchup_2018_2019[18]/team_matchup_2018_2019[2],
            'orb_pg':team_matchup_2018_2019[16]/team_matchup_2018_2019[2],
            'drb_pg':team_matchup_2018_2019[17]/team_matchup_2018_2019[2],
            'ast_pg':team_matchup_2018_2019[19]/team_matchup_2018_2019[2], 
            'three_pt_att_pg':team_matchup_2018_2019[11]/team_matchup_2018_2019[2],
            'three_pt_pct':round((team_matchup_2018_2019[12])*100,1), 
            'plus_minus':team_matchup_2018_2019[27]/team_matchup_2019_2020[2],
            'free_throw_att_pg':team_matchup_2018_2019[14]/team_matchup_2018_2019[2],
            'free_throw_pct':round((team_matchup_2019_2020[15])*100,1),
            'points_pg':team_matchup_2018_2019[26]/team_matchup_2018_2019[2] 
        }'''
        
    #print(team_matchup_2019_2020)
    #print(team_matchup_2018_2019)

    return matchup_data









if __name__ == "__main__":
    make_games()