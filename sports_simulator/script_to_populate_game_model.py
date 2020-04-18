from nba_api.stats.endpoints import TeamGameLog, BoxScoreTraditionalV2,BoxScoreSummaryV2, Scoreboard
from nba_api.stats.library.parameters import Season, SeasonTypeAllStar, LeagueIDNullable
from nba_api.stats.static import teams
from datetime import date
from basketball.models import Game
import random

"""
    home_team = models.IntegerField(null=False)
    away_team = models.IntegerField(null=False)
    game_id = models.IntegerField(primary_key=True)
    winning_team_id = models.IntegerField(null=False)
    losing_team_id = models.IntegerField(null=False)
    home_team_score = models.IntegerField(null=False)
    away_team_score = models.IntegerField(null=False)
    top_scorer_home = models.IntegerField(null=False)
    top_scorer_away = models.IntegerField(null=False)
    attendance = models.IntegerField(null=False)
    date_time = models.DateTimeField(null=False)
"""

"""
    'BoxScoreTraditionalV2': { "data_sets": {
    "PlayerStats": ["GAME_ID",
            "TEAM_ID",
            "TEAM_ABBREVIATION",
            "TEAM_CITY",
            "PLAYER_ID",
            "PLAYER_NAME",
            "START_POSITION",
            "COMMENT",
            "MIN",
            "FGM",
            "FGA",
            "FG_PCT",
            "FG3M",
            "FG3A",
            "FG3_PCT",
            "FTM",
            "FTA",
            "FT_PCT",
            "OREB",
            "DREB",
            "REB",
            "AST",
            "STL",
            "BLK",
            "TO",
            "PF",
            "PTS",
            "PLUS_MINUS"],
    "TeamStats": ["GAME_ID","TEAM_ID","TEAM_NAME","TEAM_ABBREVIATION",
                  "TEAM_CITY","MIN", "E_OFF_RATING","OFF_RATING",
                  "E_DEF_RATING","DEF_RATING","E_NET_RATING",
                  "NET_RATING", "AST_PCT","AST_TOV","AST_RATIO",
                  "OREB_PCT","DREB_PCT","REB_PCT","E_TM_TOV_PCT",
                  "TM_TOV_PCT","EFG_PCT","TS_PCT","USG_PCT",
                  "E_USG_PCT","E_PACE","PACE","PACE_PER40","POSS","PIE"]
    }
"""
'''ATL	Atlanta Hawks
"BKN":"Brooklyn Nets"
"BOS":"Boston Celtics"
"CHA":"Charlotte Hornets"
"CHI":"Chicago Bulls"
"CLE":"Cleveland Cavaliers"
"DAL":"Dallas Mavericks"
"DEN":"Denver Nuggets"
"DET":"Detroit Pistons"
"GSW":"Golden State Warriors"
"HOU":"Houston Rockets"
"IND":"Indiana Pacers"
"LAC":"Los Angeles Clippers"
"LAL":"Los Angeles Lakers"
"MEM":"Memphis Grizzlies"
"MIA":"Miami Heat"
"MIL":"Milwaukee Bucks"
"MIN":"Minnesota Timberwolves"
"NOP":"New Orleans Pelicans"
"NYK":"New York Knicks"
"OKC":"Oklahoma City Thunder"
"ORL":"Orlando Magic"
"PHI":"Philadelphia 76ers"
"PHX":"Phoenix Suns"
"POR":"Portland Trail Blazers"
"SAC":"Sacramento Kings"
"SAS":"San Antonio Spurs"
"TOR":"Toronto Raptors"
"UTA":"Utah Jazz"
"WAS":"Washington Wizards"'''
def populate():
    abv_to_name = {
        "ATL":"Atlanta Hawks","BKN":"Brooklyn Nets","BOS":"Boston Celtics","CHA":"Charlotte Hornets","CHI":"Chicago Bulls",
        "CLE":"Cleveland Cavaliers","DAL":"Dallas Mavericks","DEN":"Denver Nuggets","DET":"Detroit Pistons","GSW":"Golden State Warriors",
        "HOU":"Houston Rockets","IND":"Indiana Pacers","LAC":"Los Angeles Clippers","LAL":"Los Angeles Lakers","MEM":"Memphis Grizzlies",
        "MIA":"Miami Heat","MIL":"Milwaukee Bucks","MIN":"Minnesota Timberwolves","NOP":"New Orleans Pelicans","NYK":"New York Knicks",
        "OKC":"Oklahoma City Thunder","ORL":"Orlando Magic","PHI":"Philadelphia 76ers","PHX":"Phoenix Suns","POR":"Portland Trail Blazers",
        "SAC":"Sacramento Kings","SAS":"San Antonio Spurs","TOR":"Toronto Raptors","UTA":"Utah Jazz","WAS":"Washington Wizards"
    }

    count = 1
    all_teams = teams.get_teams()
    for t in all_teams:
        #data = TeamGameLog(team_id='1610612745').get_dict()# Houston Rockets
        data = TeamGameLog(team_id=t['id']).get_dict()# Houston Rockets
        game_data = {}
        count = 0
        for game in data['resultSets'][0]['rowSet']:
            count += 1
            if count == 2:
                return
            this_game = {}
            home_team_player_scores = {}
            away_team_player_scores = {}
            #print(game[3], " ", game[2], " ", game[4], " ")

            if game[1] not in game_data:
                this_game['game_id']=game[1]
                this_game['date'] = game[2]
                this_game['matchup'] = game[3]
                if 'home_team' not in this_game:
                    matchup = game[3]
                    l = matchup.split(' ')
                    if '@' in l:
                        this_game['home_team']=abv_to_name[l[2]]
                        this_game['away_team']=abv_to_name[l[0]]
                        this_game['home_team_id'] = teams.find_team_by_abbreviation(l[2])['id']
                        this_game['away_team_id'] = teams.find_team_by_abbreviation(l[0])['id']
                    else:
                        this_game['home_team']=abv_to_name[l[0]]
                        this_game['away_team']=abv_to_name[l[2]]
                        this_game['home_team_id'] = teams.find_team_by_abbreviation(l[0])['id']
                        this_game['away_team_id'] = teams.find_team_by_abbreviation(l[2])['id']

                data2 = BoxScoreTraditionalV2(game_id = game[1]).get_dict()['resultSets']
                #print(data2)

                player_stats = []
                team_stats = []
                this_game['all_stats'] = {}

                data3 = BoxScoreSummaryV2(game_id=game[1]).get_dict()['resultSets']
                print(len(data3))
                game_info = data3[4]['rowSet'] #GameInfo
                print(game_info)
                this_game['attendance']=game_info[0][1]
                game_lineScore = data3[5]['rowSet'] #linescore
                season_series = data3[8]['rowSet']
                if game_lineScore[0][3]==this_game['home_team_id']:
                    this_game['home_team_record']=game_lineScore[0][7]
                    this_game['away_team_record']=game_lineScore[1][7]
                else:
                    this_game['home_team_record']=game_lineScore[1][7]
                    this_game['away_team_record']=game_lineScore[0][7]

                this_game['all_stats']['points_by_quarter_id']={
                    game_lineScore[0][3]: [game_lineScore[0][x] for x in range(8,16)],
                    game_lineScore[1][3]: [game_lineScore[1][x] for x in range(8,16)]
                }

                """
                    game_lineScore[0][3]:{
                        'pts_1st':game_lineScore[0][8],
                        'pts_2nd':game_lineScore[0][9],
                        'pts_3rd':game_lineScore[0][10],
                        'pts_4th':game_lineScore[0][11],
                        'pts_ot1':game_lineScore[0][12],
                        'pts_ot2':game_lineScore[0][13],
                        'pts_ot3':game_lineScore[0][14],
                        'pts_ot4':game_lineScore[0][15]
                    },
                    game_lineScore[1][3]: {
                        'pts_1st':game_lineScore[1][8],
                        'pts_2nd':game_lineScore[1][9],
                        'pts_3rd':game_lineScore[1][10],
                        'pts_4th':game_lineScore[1][11],
                        'pts_ot1':game_lineScore[1][12],
                        'pts_ot2':game_lineScore[1][13],
                        'pts_ot3':game_lineScore[1][14],
                        'pts_ot4':game_lineScore[1][15]
                    }"""

                #['GAME_ID'0, 'TEAM_ID'1, 'TEAM_ABBREVIATION'2, 'TEAM_CITY'3, 'PLAYER_ID'4, 'PLAYER_NAME'5, 'START_POSITION'6,
                #  'COMMENT'7, 'MIN'8, 'FGM'9, 'FGA'10, 'FG_PCT'11, 'FG3M'12, 'FG3A'13, 'FG3_PCT'14, 'FTM'15, 'FTA'16, 'FT_PCT'17, 
                # 'OREB'18, 'DREB'19, 'REB'20, 'AST'21, 'STL'22, 'BLK'23, 'TO'24, 'PF'25, 'PTS'26, 'PLUS_MINUS'27]
                for info in data2:
                    if (info['name'] == 'PlayerStats'):

                        for player in info['rowSet']:
                            if not player[7]:
                                this_player = {
                                    'player_id':player[4],
                                    'team_id':player[1],
                                    'points':player[26],
                                    'name':player[5],
                                    'min':player[8].split(':')[0],
                                    'FG_made':player[9],
                                    'FG_attempted':player[10],
                                    '3P_made':player[12],
                                    '3P_attempted':player[13],
                                    'FT_made':player[15],
                                    'FT_attempted':player[16],
                                    'off_rebounds':player[18],
                                    'def_rebounds':player[19],
                                    'assists':player[21],
                                    'steals':player[22],
                                    'blocks':player[23],
                                    'turnovers':player[24],
                                    'personal_fouls':player[25],
                                    'comment':'OK'
                                }
                                if this_game['home_team_id']==player[1]:
                                    home_team_player_scores[player[4]]=[player[26],player[5]]
                                else:
                                    away_team_player_scores[player[4]]=[player[26],player[5]]
                            else:
                                this_player= {
                                    'player_id':player[4],
                                    'name':player[5],
                                    'comment': player[7]
                                }
                            player_stats.append(this_player)
                        
                        max_value_home=max(home_team_player_scores.values())
                        max_value_away=max(away_team_player_scores.values())
                        this_game['top_scorer_home']=[k for k, v in home_team_player_scores.items() if v == max_value_home][0]
                        this_game['top_scorer_away']=[k for k, v in away_team_player_scores.items() if v == max_value_away][0]
                        this_game['top_scorer_home_points']=max_value_home[0]
                        this_game['top_scorer_away_points']=max_value_away[0]
                        
                        this_game['all_stats']['player_stats']=player_stats

                    #['GAME_ID'0, 'TEAM_ID'1, 'TEAM_NAME'2, 'TEAM_ABBREVIATION'3, 'TEAM_CITY'4, 'MIN'5, 'FGM'6, 'FGA'7, 'FG_PCT'8, 
                    # 'FG3M'9, 'FG3A'10, 'FG3_PCT'11, 'FTM'12, 'FTA'13, 'FT_PCT'14, 'OREB'15, 'DREB'16, 'REB'17, 'AST'18,
                    # 'STL'19, 'BLK'20, 'TO'21, 'PF'22, 'PTS'23, 'PLUS_MINUS'24]
                    elif (info['name'] == 'TeamStats'):

                        for team in info['rowSet']:
                            this_team = {
                                'team_id':team[1],
                                'team_name':team[2],
                                'team_abv':team[3],
                                'team_city':team[4],
                                'FG_made':team[6],
                                'FG_attempted':team[7],
                                '3P_made':team[9],
                                '3P_attempted':team[10],
                                'FT_made':team[12],
                                'FT_attempted':team[13],
                                'off_rebounds':team[15],
                                'def_rebounds':team[16],
                                'assists':team[18],
                                'steals':team[19],
                                'blocks':team[20],
                                'turnovers':team[21],
                                'personal_fouls':team[22],
                                'points':team[23]
                            }
                            if this_team['team_id']==this_game['home_team_id']:
                                this_game['home_team_score']=this_team['points']
                            else:
                                this_game['away_team_score']=this_team['points']

                            team_stats.append(this_team)
                        
                        this_game['all_stats']['team_stats']=team_stats

                        if team_stats[0]['points']>team_stats[1]['points']:
                            this_game['winner_id']=team_stats[0]['team_id']
                            this_game['winner_name']="%s %s" % (team_stats[0]['team_city'], team_stats[0]['team_name'])
                            this_game['loser_id']=team_stats[1]['team_id']
                            this_game['loser_name']="%s %s" % (team_stats[1]['team_city'], team_stats[1]['team_name'])
                        else:
                            this_game['winner_id']= team_stats[1]['team_id']
                            this_game['winner_name']="%s %s" % (team_stats[1]['team_city'], team_stats[1]['team_name'])
                            this_game['loser_id']=team_stats[0]['team_id']
                            this_game['loser_name']="%s %s" % (team_stats[0]['team_city'], team_stats[0]['team_name'])

                #print(this_game)
                print("Winning id:",this_game['winner_id'])
                print("Losing id:",this_game['loser_id'])                  
                    
                this_game['date']=get_game_date(this_game['date'])
                #print(this_game)
                print("Winning id:",this_game['winner_id'])
                print("Losing id:",this_game['loser_id'])
                game = Game(home_team_name=this_game['home_team'],away_team_name=this_game['away_team'],
                        home_team=this_game['home_team_id'],away_team=this_game['away_team_id'],
                        data=this_game['all_stats'],winning_team_id=this_game['winner_id'],
                        losing_team_id=this_game["loser_id"],loser_name=this_game["loser_name"],
                        winner_name=this_game["winner_name"],home_team_score=this_game['home_team_score'],
                        away_team_score=this_game['away_team_score'],date=this_game['date'],attendance=this_game['attendance'],#attendance=get_attendance(this_game['home_team_id']),
                        top_scorer_home=this_game['top_scorer_home'],top_scorer_away=this_game['top_scorer_away'],
                        game_id=this_game["game_id"],home_team_record=this_game['home_team_record'],
                        away_team_record=this_game['away_team_record'],top_scorer_home_points=this_game['top_scorer_home_points'],
                        top_scorer_away_points=this_game['top_scorer_away_points']
                )

                game_data[this_game['game_id']]= this_game
                game.save()
                print(this_game['game_id'])
                this_game={}
        
    
def get_game_date(this_date):
    items = this_date.split(' ')
    #print(items)
    months = {
        'JAN':1,'FEB':2,'MAR':3,"APR":4,"MAY":5,"JUNE":6,"JULY":7,"AUG":8,
        'SEPT':9,"OCT":10,"NOV":11,"DEC":12
    }
    month = months[items[0]]
    items[1]=items[1].replace(',', '')
    day = int(items[1].strip())
    year = int(items[2])
    return date(year, month, day)


def get_attendance(team_id):
    team_attendance = {
        1610612737:18118,1610612738:18624,1610612751:17732,1610612766:19077,1610612741:20917,1610612739:19432,
        1610612742:19200,1610612743:19520,1610612765:20491,1610612744:18064,1610612745:18055,1610612754:17923,
        1610612746:19068,1610612747:19068,1610612763:17794,1610612748:19600,1610612749:17500,1610612750:18978,
        1610612740:16867,1610612752:19812,1610612760:18203,1610612753:18846,1610612755:20478,1610612756:18055,
        1610612757:19441,1610612758:17583,1610612759:18418,1610612761:19800,1610612762:18306,1610612764:20536
    }

    max_attendance=team_attendance[team_id]
    r1 = random.randint(0, 2500)
    return (max_attendance-r1)




if __name__ == "__main__":
    populate()