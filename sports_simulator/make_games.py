from basketball.models import Game,Team,Player
from nba_api.stats.endpoints import TeamDashboardByOpponent
from datetime import date
import re
from bs4 import BeautifulSoup
import requests 
import copy   
import random


def make_games():
    current = 20200309
    last = 20200415
    url = "https://www.cbssports.com/nba/schedule/"+str(current)
    response = requests.get(url)

    data = response.text
    soup = BeautifulSoup(data,features='html.parser')
    team_names = []
    games = []

    str_current = str(current)
    print("%s/%s/%s" % (str_current[4:6],str_current[6:],str_current[0:4]))
    #f.write("%s/%s/%s\n" % (str_current[4:6],str_current[6:],str_current[0:4]))

    for span_tag in soup.findAll('span', {'class': 'TeamName'}):
        team_names.append((span_tag.find('a')).string)

    for i in range(1,len(team_names),2):
        team_away = team_names[i-1]
        team_home = team_names[i]
        #game = [team_away,team_home]
        #games.append(game)
        #f.write("Away: %s  Home: %s\n" % (team1,team2))
        team_home_id = get_team(team_home.lower())
        team_away_id = get_team(team_away.lower())
        print('Away team: %s %s' % (team_away, team_away_id))
        print('Home team: %s %s' % (team_home, team_home_id))

        matchup_data_home = get_other_data(team_home_id,team_away_id)
        matchup_data_away = get_other_data(team_away_id,team_home_id)
        print('matchup_away:',matchup_data_away)
        print('matchup_home:',matchup_data_home)

        calculate_stats(matchup_data_home,matchup_data_away,team_home_id,team_away_id)
        #return



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
def calculate_stats(matchup_home,matchup_away,home_id,away_id):

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

    biases = compute_biases(away_stats,home_stats,matchup_away,matchup_home)
    #print(biases['home_field_goal_attempt_bias'])
    #print(home_stats['field_goals_attempted_per_game'])
    ####################SAM' BIAS CALCULATIONS############################
    home_bias_list = get_bias_home(home_id)
    away_bias_list = get_bias_away(away_id)
    #print("LOOK:",((biases['home_free_throw_percentage_bias'])+home_stats['free_throw_percentage']))
    overall_bias_home = ((biases['home_points_bias']+biases['home_points_per_game_bias'])/10)/2
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
        overall_bias_home = (extra+overall_bias_home)/2
    
    #overall_bias_home=1
    #print(biases['home_points_bias'], '  ', biases['home_points_per_game_bias'])
    print("OVERALL BIAS HOME", overall_bias_home)
    home_game_stats = {
        'minutes':240,
        'field_goals_percentage': ((biases['home_field_goal_percentage_bias'])+home_stats['field_goal_percentage'])*(random.uniform(home_bias_list[0], home_bias_list[1]))*overall_bias_home,
        'field_goals_attempted': ((biases['home_field_goal_attempt_bias'])+home_stats['field_goals_attempted_per_game'])+random.uniform(home_bias_list[2],home_bias_list[3])*overall_bias_home,
        'three_point_percentage': ((biases['home_three_point_pct_bias'])+home_stats['three_point_percentage'])*(random.uniform(home_bias_list[4], home_bias_list[5]))*overall_bias_home,
        'three_point_attempted': ((biases['home_three_point_att_bias'])+home_stats['three_point_attempted_per_game'])+random.uniform(home_bias_list[6],home_bias_list[7])*overall_bias_home,
        'free_throws_percentage': (((biases['home_free_throw_percentage_bias'])+home_stats['free_throw_percentage'])*(random.uniform(home_bias_list[8], home_bias_list[9])))*overall_bias_home,
        'free_throws_attempted': ((biases['home_free_throw_att_bias'])+home_stats['free_throws_attempted_per_game'])+random.uniform(home_bias_list[10],home_bias_list[11])*overall_bias_home,
        'def_rebounds': ((biases['home_def_rebounds_bias'])+home_stats['defensive_rebounds_per_game'])+random.uniform(home_bias_list[12],home_bias_list[13])*overall_bias_home,
        'off_rebounds': ((biases['home_off_rebounds_bias'])+home_stats['offensive_rebounds_per_game'])+random.uniform(home_bias_list[14],home_bias_list[15])*overall_bias_home,
        'rebounds': ((biases['home_rebounds_bias'])+home_stats['rebounds_per_game'])+random.uniform(home_bias_list[16],home_bias_list[17])*overall_bias_home,
        'assists': ((biases['home_assists_bias'])+home_stats['assists_per_game'])+random.uniform(home_bias_list[18],home_bias_list[19])*overall_bias_home,
        'steals': ((biases['home_steals_bias'])+home_stats['steals_per_game'])+random.uniform(home_bias_list[20],home_bias_list[21])*overall_bias_home,
        'blocks': ((biases['home_blocks_bias'])+home_stats['blocks_per_game'])+random.uniform(home_bias_list[22],home_bias_list[23])*overall_bias_home,
        'turnovers': ((biases['home_turnovers_bias'])+home_stats['turnovers_per_game'])+random.uniform(home_bias_list[24],home_bias_list[25])*overall_bias_home,
        'personal_fouls': ((biases['home_personal_fouls_bias'])+home_stats['personal_fouls_per_game'])+ random.uniform(home_bias_list[26],home_bias_list[27])*overall_bias_home,
        'points': (((biases['home_points_bias']+home_stats['points_per_game'])+(biases['home_points_per_game_bias']+home_stats['points_per_game']))/2)+random.uniform(home_bias_list[28],home_bias_list[29]),
    }
    home_game_stats['field_goals_made'] = round(home_game_stats['field_goals_attempted']*(home_game_stats['field_goals_percentage']/100))
    home_game_stats['free_throws_made'] = round((home_game_stats['free_throws_percentage']/100)*home_game_stats['free_throws_attempted'])
    home_game_stats['three_points_made'] = round((home_game_stats['three_point_percentage']/100)*home_game_stats['three_point_attempted'])
    print('home_stats:',home_game_stats)
    total_points = (home_game_stats['three_points_made']*3)+((home_game_stats['field_goals_made']-home_game_stats['three_points_made'])*2) + home_game_stats['free_throws_made']
    print('\ntotal points: ', total_points, '\n')

    overall_bias_away = ((biases['away_points_bias']+biases['away_points_per_game_bias'])/10)/2
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

    #overall_bias_away=1
    #print(biases['away_points_bias'], '  ', biases['away_points_per_game_bias'])
    print("OVERALL BIAS AWAY", overall_bias_away)
    away_game_stats = {
        'minutes':240,
        'field_goals_percentage': ((biases['away_field_goal_percentage_bias'])+away_stats['field_goal_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
        'field_goals_attempted': ((biases['away_field_goal_attempt_bias'])+away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])*overall_bias_away,
        'three_point_percentage': ((biases['away_three_point_pct_bias'])+away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
        'three_point_attempted': ((biases['away_three_point_att_bias'])+away_stats['three_point_attempted_per_game'])+random.uniform(-away_bias_list[6],away_bias_list[7])*overall_bias_away,
        'free_throws_percentage': (((biases['away_free_throw_percentage_bias'])+away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
        'free_throws_attempted': ((biases['away_free_throw_att_bias'])+away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away,
        'def_rebounds': ((biases['away_def_rebounds_bias'])+away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away,
        'off_rebounds': ((biases['away_off_rebounds_bias'])+away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away,
        'rebounds': ((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away,
        'assists': ((biases['away_assists_bias'])+away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away,
        'steals': ((biases['away_steals_bias'])+away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away,
        'blocks': ((biases['away_blocks_bias'])+away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away,
        'turnovers': ((biases['away_turnovers_bias'])+away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away,
        'personal_fouls': ((biases['away_personal_fouls_bias'])+away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away,
        'points': (((biases['away_points_bias']+away_stats['points_per_game'])+(biases['away_points_per_game_bias']+away_stats['points_per_game']))/2)+random.uniform(away_bias_list[28],away_bias_list[29]),
    }
    away_game_stats['field_goals_made'] = round(away_game_stats['field_goals_attempted']*(away_game_stats['field_goals_percentage']/100))
    away_game_stats['free_throws_made'] = round((away_game_stats['free_throws_percentage']/100)*away_game_stats['free_throws_attempted'])
    away_game_stats['three_points_made'] = round((away_game_stats['three_point_percentage']/100)*away_game_stats['three_point_attempted'])
    total_points_away = (away_game_stats['three_points_made']*3) + ((away_game_stats['field_goals_made']-away_game_stats['three_points_made'])*2) + away_game_stats['free_throws_made']
    print('away stats:',away_game_stats)
    print('\ntotal points: ', total_points_away, '\n')
    return


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
        1610612749:[0.8, 1.12, -3, 5, 0.75, 1.05, -4, 5, 0.92, 1.02, -5, 9, -3, 5, -3, 6, -3, 6, -3, 3, -2, 2, -2, 3, -2, 1, -3, -3, -10, 10],#MIL
        1610612747:[0.8, 1.15, -4, 6, 0.74, 1.05, -4, 3, 0.91, 1.00, -5, 8, -5, 6, -2, 4, -3, 6, -4, 6, -3, 4, -2, 3, -1, 1, -3, 3, -7, 7], #LAL
        1610612737:[0.7, 1.05, -3, 6, 0.69, 1.02, -4, 6, 0.92, 1.03, -5, 6, -7,3, -2, 2, -6, 3, -3, 2, -2, 1, -1, 1, -3, 2, -3, 3, -4, 10],#ATL
        1610612738:[0.8, 1.1, -4, 4, 0.75, 1.02, -4, 3, 0.92, 1.03, -5, 3, -4, 4, -2, 2, -3, 3, -4, 6, -1, 3, -2, 3, -3, 2, -3, 3, -7, 10],#BOS
        1610612751:[0.78, 1.05, -4, 6, 0.74, 1.1, -4, 5, 0.92, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#BKN
        1610612766:[0.7, 1.04, -3, 4, 0.69, 1.02, -4, 6, 0.92, 1.03, -5, 6, -7, 3, -2, 2, -6, 3, -3, 2, -2, 1, -1, 1, -3, 2, -3, 3, -4, 10],#CHA
        1610612741:[0.78, 1.02, -4, 4, 0.74, 1.04, -4, 5, 0.92, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CHI
        1610612739:[0.78, 1.02, -4, 3, 0.74, 1.05, -4, 4, 0.92, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CLE
        1610612742:[0.85, 1.08, -4, 6, 0.8, 1.08, -4, 6, 0.95, 1.02, -5, 6, -3, 5, -4, 5, -3, 5, -3, 6, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DAL
        1610612743:[0.82, 1.08, -4, 6, 0.78, 1.05, -4, 5, 0.93, 1.02, -5, 5, -3, 4, -4, 4, -3, 4, -3, 4, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DEN
        1610612765:[0.78, 1.02, -4, 4, 0.74, 1.05, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#DET
        1610612744:[0.78, 1.07, -3, 6, 0.72, 1.08, -3, 5, 0.90, 1.02, -2, 2, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#GSW
        1610612745:[0.85, 1.12, -3, 6, 0.82, 1.1, -3, 6, 0.95, 1.02, -2, 4, -3, 4, -3, 4, -3, 4, -3, 5, -2, 4, -2, 2, -2, 4, -3, 3, -7, 12],#HOU
        1610612754:[0.78, 1.1, -3, 6, 0.76, 1.05, -3, 5, 0.92, 1.02, -2, 2, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#IND
        1610612746:[0.78, 1.1, -3, 6, 0.76, 1.05, -3, 5, 0.92, 1.02, -2, 2, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#LAC
        1610612763:[0.77, 1.05, -4, 4, 0.73, 1.05, -4, 2, 0.90, 1.02, -5, 3, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MEM
        1610612748:[0.82, 1.07, -4, 6, 0.82, 1.1, -4, 5, 0.96, 1.02, -5, 5, -3, 4, -4, 5, -3, 4, -3, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIA
        1610612750:[0.75, 1.03, -4, 3, 0.72, 1.02, -4, 3, 0.90, 1.02, -5, 3, -3, 4, -4, 5, -3, 4, -2, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIN
        1610612740:[0.79, 1.06, -4, 5, 0.78, 1.05, -4, 4, 0.93, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NOR
        1610612752:[0.74, 1.02, -4, 3, 0.70, 1.02, -4, 3, 0.89, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NYK
        1610612760:[0.82, 1.1, -4, 4, 0.8, 1.06, -4, 4, 0.92, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#OKC
        1610612753:[0.75, 1.02, -4, 4, 0.75, 1.02, -4, 4, 0.90, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#ORL
        1610612755:[0.85, 1.05, -4, 5, 0.8, 1.04, -4, 4, 0.92, 1.02, -4, 6, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHI
        1610612756:[0.80, 1.02, -4, 3, 0.78, 1.02, -4, 3, 0.90, 1.02, -4, 3, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHX
        1610612757:[0.80, 1.02, -4, 5, 0.78, 1.07, -4, 4, 0.90, 1.02, -4, 3, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#POR
        1610612758:[0.78, 1.04, -4, 3, 0.76, 1.05, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#SAC
        1610612759:[0.78, 1.04, -4, 2, 0.76, 1.05, -4, 2, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2 ,2, -2, 3, -4, 3, -3, 3, -7, 10],#SAS
        1610612761:[0.82, 1.05, -4, 4, 0.76, 1.07, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#TOR
        1610612762:[0.82, 1.08, -4, 4, 0.82, 1.08, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#UTA
        1610612764:[0.82, 1.02, -4, 2, 0.81, 1.08, -4, 2, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10]#WIZ
    }
    return team_list_dist[team_id]

def get_bias_away(team_id):
    team_list_dist = {
        1610612749:[0.78, 1.10, -3, 5, 0.73, 1.05, -4, 5, 0.92, 1.02, -5, 9, -3, 5, -3, 6, -3, 6, -3, 3, -2, 2, -2, 3, -2, 1, -3, -3, -10, 10],#MIL
        1610612747:[0.8, 1.15, -4, 6, 0.72, 1.05, -4, 3, 0.91, 1.00, -5, 8, -5, 6, -2, 4, -3, 6, -4, 6, -3, 4, -2, 3, -1, 1, -3, 3, -7, 7], #LAL
        1610612737:[0.68, 1.05, -3, 6, 0.67, 1.02, -4, 6, 0.92, 1.03, -5, 6, -7,3, -2, 2, -6, 3, -3, 2, -2, 1, -1, 1, -3, 2, -3, 3, -4, 10],#ATL
        1610612738:[0.78, 1.08, -4, 5, 0.73, 1.02, -4, 3, 0.92, 1.03, -5, 3, -4, 4, -2, 2, -3, 3, -4, 6, -1, 3, -2, 3, -3, 2, -3, 3, -7, 10],#BOS
        1610612751:[0.77, 1.05, -4, 6, 0.72, 1.08, -4, 5, 0.92, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#BKN
        1610612766:[0.7, 1.04, -3, 4, 0.68, 1.02, -4, 6, 0.92, 1.03, -5, 6, -7, 3, -2, 2, -6, 3, -3, 2, -2, 1, -1, 1, -3, 2, -3, 3, -4, 10],#CHA
        1610612741:[0.77, 1.02, -4, 4, 0.7, 1.04, -4, 5, 0.92, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CHI
        1610612739:[0.76, 1.02, -4, 4, 0.7, 1.05, -4, 4, 0.92, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#CLE
        1610612742:[0.83, 1.05, -4, 6, 0.78, 1.1, -4, 6, 0.95, 1.02, -5, 6, -3, 5, -4, 5, -3, 5, -3, 6, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DAL
        1610612743:[0.8, 1.08, -4, 4, 0.78, 1.05, -4, 5, 0.93, 1.02, -5, 5, -3, 4, -4, 4, -3, 4, -3, 4, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DEN
        1610612765:[0.76, 1.02, -4, 4, 0.72, 1.05, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#DET
        1610612744:[0.76, 1.07, -3, 6, 0.72, 1.08, -3, 5, 0.90, 1.02, -2, 2, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#GSW
        1610612745:[0.83, 1.12, -3, 6, 0.80, 1.12, -3, 6, 0.95, 1.02, -2, 4, -3, 4, -3, 4, -3, 4, -3, 5, -2, 4, -2, 2, -2, 4, -3, 3, -7, 12],#HOU
        1610612754:[0.76, 1.1, -3, 6, 0.76, 1.05, -3, 5, 0.92, 1.02, -2, 2, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#IND
        1610612746:[0.76, 1.1, -3, 5, 0.76, 1.05, -3, 5, 0.92, 1.02, -2, 2, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#LAC
        1610612763:[0.75, 1.05, -4, 4, 0.7, 1.05, -4, 2, 0.90, 1.02, -5, 3, -3, 4, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MEM
        1610612748:[0.8, 1.08, -4, 6, 0.8, 1.1, -4, 5, 0.96, 1.02, -5, 5, -3, 4, -4, 5, -3, 4, -3, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIA
        1610612750:[0.73, 1.03, -4, 3, 0.7, 1.02, -4, 3, 0.90, 1.02, -5, 3, -3, 4, -4, 5, -3, 4, -2, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIN
        1610612740:[0.76, 1.06, -4, 5, 0.75, 1.05, -4, 4, 0.93, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NOR
        1610612752:[0.7, 1.02, -4, 3, 0.68, 1.02, -4, 3, 0.89, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NYK
        1610612760:[0.8, 1.1, -4, 4, 0.8, 1.06, -3, 3, 0.92, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#OKC
        1610612753:[0.73, 1.02, -4, 4, 0.7, 1.02, -4, 4, 0.90, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#ORL
        1610612755:[0.78, 1.05, -4, 5, 0.74, 1.04, -4, 4, 0.92, 1.02, -4, 6, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHI
        1610612756:[0.76, 1.02, -4, 3, 0.75, 1.02, -4, 3, 0.90, 1.02, -4, 3, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHX
        1610612757:[0.80, 1.06, -4, 5, 0.78, 1.07, -3, 5, 0.90, 1.02, -4, 3, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#POR
        1610612758:[0.75, 1.04, -4, 3, 0.74, 1.05, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#SAC
        1610612759:[0.75, 1.04, -4, 2, 0.75, 1.05, -4, 2, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2 ,2, -2, 3, -4, 3, -3, 3, -7, 10],#SAS
        1610612761:[0.8, 1.05, -4, 4, 0.75, 1.06, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#TOR
        1610612762:[0.8, 1.06, -3, 4, 0.79, 1.06, -4, 4, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#UTA
        1610612764:[0.78, 1.02, -4, 2, 0.78, 1.05, -4, 2, 0.90, 1.02, -5, 5, -3, 7, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10]#WIZ
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