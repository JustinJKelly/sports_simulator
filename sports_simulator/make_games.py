from basketball.models import Game,Team,Player
from nba_api.stats.endpoints import TeamDashboardByOpponent
from datetime import date
import re
from bs4 import BeautifulSoup
import requests 
import copy   
import random


def make_games():
    current = 20200312
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

    for i in range(0,len(team_names),2):
        team_away = team_names[i]
        team_home = team_names[i+1]
        #game = [team_away,team_home]
        #games.append(game)
        #f.write("Away: %s  Home: %s\n" % (team1,team2))
        team_home_id = get_team(team_home.lower())
        team_away_id = get_team(team_away.lower())
        print('Away team: %s %s' % (team_away, team_away_id))
        print('Home team: %s %s' % (team_home, team_home_id))

        matchup_data_home = get_other_data(team_home_id,team_away_id)
        matchup_data_away = get_other_data(team_away_id,team_home_id)
        print(matchup_data_home)

        calculate_stats(matchup_data_home,matchup_data_away,team_home_id,team_away_id)
        return



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

    print("LOOK:",((biases['home_free_throw_percentage_bias'])+home_stats['free_throw_percentage']))
    home_game_stats = {
        'minutes':240,
        'field_goals_percentage': ((biases['home_field_goal_percentage_bias'])+home_stats['field_goal_percentage'])*(random.uniform(0.9, 1.1)),
        'field_goals_attempted': ((biases['home_field_goal_attempt_bias'])+home_stats['field_goals_attempted_per_game'])+random.uniform(-4,5),
        'three_point_percentage': ((biases['home_three_point_pct_bias'])+home_stats['three_point_percentage'])*(random.uniform(0.9, 1.1)),
        'three_point_attempted': ((biases['home_three_point_att_bias'])+home_stats['three_point_attempted_per_game'])+random.uniform(-4,5),
        'free_throws_percentage': (((biases['home_free_throw_percentage_bias'])+home_stats['free_throw_percentage'])*(random.uniform(0.95, 1.05))/2),
        'free_throws_attempted': ((biases['home_free_throw_att_bias'])+home_stats['free_throws_attempted_per_game'])+random.uniform(-5,5),
        'def_rebounds': ((biases['home_def_rebounds_bias'])+home_stats['defensive_rebounds_per_game'])+random.uniform(-7,7),
        'off_rebounds': ((biases['home_off_rebounds_bias'])+home_stats['offensive_rebounds_per_game'])+random.uniform(-2,2),
        'rebounds': ((biases['home_rebounds_bias'])+home_stats['rebounds_per_game'])+random.uniform(-6,6),
        'assists': ((biases['home_assists_bias'])+home_stats['assists_per_game'])+random.uniform(-5,5),
        'steals': ((biases['home_steals_bias'])+home_stats['steals_per_game'])+random.uniform(-2,2),
        'blocks': ((biases['home_blocks_bias'])+home_stats['blocks_per_game'])+random.uniform(-2,2),
        'turnovers': ((biases['home_turnovers_bias'])+home_stats['turnovers_per_game'])+random.uniform(-3,3),
        'personal_fouls': ((biases['home_personal_fouls_bias'])+home_stats['personal_fouls_per_game'])+ random.uniform(-3,3),
        'points': (((biases['home_points_bias']+home_stats['points_per_game'])+(biases['home_points_per_game_bias']+home_stats['points_per_game']))/2)+random.uniform(-7,12),
    }
    home_game_stats['field_goals_made'] = round(home_game_stats['field_goals_attempted']*(home_game_stats['field_goals_percentage']/100))
    home_game_stats['free_throws_made'] = round((home_game_stats['free_throws_percentage']/100)*home_game_stats['free_throws_attempted'])
    home_game_stats['three_points_made'] = round((home_game_stats['three_point_percentage']/100)*home_game_stats['three_point_attempted'])
    print(home_game_stats)

    return


def compute_biases(away_stats,home_stats,matchup_away,matchup_home):
    biases = {
        'home_points_bias':home_stats['points_per_game']-away_stats['opponent_points_per_game'],
        'away_points_bias':away_stats['points_per_game']-home_stats['opponent_points_per_game'],
        #'home_bias':home_stats['home_wins']/home_stats['home_losses'],
        #'away_bias':away_stats['away_wins']/away_stats['away_losses'],
        'home_points_per_game_bias':home_stats['points_per_game']-matchup_home['points_pg'],
        'away_points_per_game_bias':away_stats['points_per_game']-matchup_away['points_pg'],
        #'home_matchup_bias': (home_stats['wins']/home_stats['losses']) / (matchup_home['wins']/matchup_home['losses']),
        #'away_matchup_bias': (away_stats['wins']/away_stats['losses']) / (matchup_away['wins']/matchup_away['losses']),
        'home_field_goal_attempt_bias': home_stats['field_goals_attempted_per_game']-matchup_home['fg_attempted_pg'],
        'away_field_goal_attempt_bias': away_stats['field_goals_attempted_per_game']-matchup_away['fg_attempted_pg'],
        'home_field_goal_percentage_bias': home_stats['field_goal_percentage']-matchup_home['fg_pct'],
        'away_field_goal_percentage_bias': away_stats['field_goal_percentage']-matchup_away['fg_pct'],
        'home_three_point_att_bias': home_stats['three_point_attempted_per_game']-matchup_home['three_pt_att_pg'],
        'away_three_point_att_bias': away_stats['three_point_attempted_per_game']-matchup_away['three_pt_att_pg'],
        'home_three_point_pct_bias': home_stats['three_point_percentage']-matchup_home['three_pt_pct'],
        'away_three_point_pct_bias': away_stats['three_point_percentage']-matchup_away['three_pt_pct'],
        'home_free_throw_att_bias':home_stats['free_throws_attempted_per_game']-matchup_home['free_throw_att_pg'],
        'away_free_throw_att_bias':away_stats['free_throws_attempted_per_game']-matchup_away['free_throw_att_pg'],
        'home_free_throw_percentage_bias':home_stats['free_throw_percentage']-matchup_home['free_throw_pct'],
        'away_free_throw_percentage_bias':away_stats['free_throw_percentage']-matchup_away['free_throw_pct'],
        'home_plus_minus_bias': home_stats['plus_minus']-matchup_home['plus_minus'],
        'away_plus_minus_bias': away_stats['plus_minus']-matchup_away['plus_minus'],
        'home_assists_bias': home_stats['assists_per_game']-matchup_home['ast_pg'],
        'away_assists_bias': away_stats['assists_per_game']-matchup_away['ast_pg'],
        'home_off_rebounds_bias': home_stats['offensive_rebounds_per_game']-matchup_home['orb_pg'],
        'away_off_rebounds_bias': away_stats['offensive_rebounds_per_game']-matchup_away['orb_pg'],
        'home_def_rebounds_bias': home_stats['defensive_rebounds_per_game']-matchup_home['drb_pg'],
        'away_def_rebounds_bias': away_stats['defensive_rebounds_per_game']-matchup_away['drb_pg'],
        'home_rebounds_bias': home_stats['rebounds_per_game']-matchup_home['rb_pg'],
        'away_rebounds_bias': away_stats['rebounds_per_game']-matchup_away['rb_pg'],
        'home_blocks_bias': home_stats['blocks_per_game']-matchup_home['block_pg'],
        'away_blocks_bias': away_stats['blocks_per_game']-matchup_away['block_pg'],
        'home_steals_bias': home_stats['steals_per_game']-matchup_home['steals_pg'],
        'away_steals_bias': away_stats['steals_per_game']-matchup_away['steals_pg'],
        'home_turnovers_bias': home_stats['turnovers_per_game']-matchup_home['turnovers_pg'],
        'away_turnovers_bias': away_stats['turnovers_per_game']-matchup_away['turnovers_pg'],
        'home_personal_fouls_bias': home_stats['personal_fouls_per_game']-matchup_home['personal_fouls_pg'],
        'away_personal_fouls_bias': away_stats['personal_fouls_per_game']-matchup_away['personal_fouls_pg'],
    }
    print("NFIENF:",biases['home_field_goal_percentage_bias'])
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

    if len(team_matchup_2019_2020) > 0:
        team_matchup_2019_2020 = team_matchup_2019_2020[0] #gets data
        #matchup_data['2019-2020 Season'] = {
        matchup_data = {
            'games_played':team_matchup_2019_2020[2],
            'wins':team_matchup_2019_2020[3],
            'losses':team_matchup_2019_2020[4],  
            'win_pct':team_matchup_2019_2020[5], 
            'fg_pct':round(team_matchup_2019_2020[9]*100,1), 
            'fg_attempted_pg':team_matchup_2019_2020[8]/team_matchup_2019_2020[2],
            'block_pg':team_matchup_2019_2020[22]/team_matchup_2019_2020[2],
            'rb_pg':team_matchup_2019_2020[18]/team_matchup_2019_2020[2],
            'steals_pg':team_matchup_2019_2020[21]/team_matchup_2019_2020[2],
            'turnovers_pg':team_matchup_2019_2020[20]/team_matchup_2019_2020[2],
            'personal_fouls_pg':team_matchup_2019_2020[24]/team_matchup_2019_2020[2],
            'orb_pg':team_matchup_2019_2020[16]/team_matchup_2019_2020[2],
            'drb_pg':team_matchup_2019_2020[17]/team_matchup_2019_2020[2],
            'ast_pg':team_matchup_2019_2020[19]/team_matchup_2019_2020[2], 
            'three_pt_att_pg':team_matchup_2019_2020[11]/team_matchup_2019_2020[2],
            'three_pt_pct':round((team_matchup_2019_2020[12])*100,1), 
            'plus_minus':team_matchup_2019_2020[27]/team_matchup_2019_2020[2],
            'free_throw_att_pg':team_matchup_2019_2020[14]/team_matchup_2019_2020[2],
            'free_throw_pct':round((team_matchup_2019_2020[15])*100,1),
            'points_pg':team_matchup_2019_2020[26]/team_matchup_2019_2020[2] 
        }
        print('LOOK2:',matchup_data['free_throw_pct'])
        return matchup_data

    matchup_data={}
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
        }
        
    #print(team_matchup_2019_2020)
    #print(team_matchup_2018_2019)

    return matchup_data









if __name__ == "__main__":
    make_games()