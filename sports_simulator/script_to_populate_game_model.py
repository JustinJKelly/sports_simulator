from nba_api.stats.endpoints import TeamGameLog, BoxScoreTraditionalV2
from nba_api.stats.library.parameters import Season, SeasonTypeAllStar, LeagueIDNullable
from nba_api.stats.static import teams
from datetime import date
from basketball.models import Game

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

    data = TeamGameLog(team_id='1610612745').get_dict()# Houston Rockets
    game_ids=[]
    game_data = []
    this_game = {}
    for game in data['resultSets'][0]['rowSet']:
        #print(game[3], " ", game[2], " ", game[4], " ")
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

        game_ids.append(game[1])
        break

    #print(this_game)

    data2 = BoxScoreTraditionalV2(game_id = game_ids[0]).get_dict()

    #this_game['home_team_player_stats'] = {}
    #this_game['away_team_player_stats'] = {}
    #print('\n\n\n\n\n\n')
    player_stats = []
    team_stats = []
    this_game['all_stats'] = {}

    #['GAME_ID'0, 'TEAM_ID'1, 'TEAM_ABBREVIATION'2, 'TEAM_CITY'3, 'PLAYER_ID'4, 'PLAYER_NAME'5, 'START_POSITION'6,
    #  'COMMENT'7, 'MIN'8, 'FGM'9, 'FGA'10, 'FG_PCT'11, 'FG3M'12, 'FG3A'13, 'FG3_PCT'14, 'FTM'15, 'FTA'16, 'FT_PCT'17, 
    # 'OREB'18, 'DREB'19, 'REB'20, 'AST'21, 'STL'22, 'BLK'23, 'TO'24, 'PF'25, 'PTS'26, 'PLUS_MINUS'27]
    for info in data2['resultSets']:
        if (info['name'] == 'PlayerStats'):
            print('Player Stats:')
            print(print(info['headers']))
            #print(info)
            for player in info['rowSet']:
                #print(player[7], " ",type(player[7]))
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
                else:
                    this_player= {
                        'player_id':player[4],
                        'name':player[5],
                        'comment': player[7]
                    }
                player_stats.append(this_player)

            this_game['all_stats']['player_stats']=player_stats
            #print(player_stats)
            #print('\n\n\n')
        #['GAME_ID'0, 'TEAM_ID'1, 'TEAM_NAME'2, 'TEAM_ABBREVIATION'3, 'TEAM_CITY'4, 'MIN'5, 'FGM'6, 'FGA'7, 'FG_PCT'8, 
        # 'FG3M'9, 'FG3A'10, 'FG3_PCT'11, 'FTM'12, 'FTA'13, 'FT_PCT'14, 'OREB'15, 'DREB'16, 'REB'17, 'AST'18,
        # 'STL'19, 'BLK'20, 'TO'21, 'PF'22, 'PTS'23, 'PLUS_MINUS'24]
        elif (info['name'] == 'TeamStats'):
            print('Team Stats:')
            print(print(info['headers']))
            #print(info)

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


             
             #print(info)
            # Whichever has high points in the winner... duh
            # if(info['rowSet'][0][23] > info['rowSet'][1][23]): # comparing scores
            #     winning_team_id = info['rowSet'][0][1] 
            #     losing_team_id = info['rowSet'][1][1]
            # else: 
            #      winning_team_id = info['rowSet'][1][1]
            #      losing_team_id = info['rowSet'][0][1]
            #print(info['rowSet'][0], "points: ", info['rowSet'][0][23])
            #print(info['rowSet'][1], "points: ", info['rowSet'][1][23])
        
            
        
    this_game['date']=get_date(this_game['date'])
    print(this_game)
    game = Game(home_team_name=this_game['home_team'],away_team_name=this_game['away_team'],
            home_team=this_game['home_team_id'],away_team=this_game['away_team_id'],
            json=this_game['all_stats'],winning_team_id=this_game['winner_id'],
            losing_team_id=this_game["loser_id"],loser_name=this_game["loser_name"],
            winner_name=this_game["winner_name"],home_team_score=this_game['home_team_score'],
            away_team_score=this_game['away_team_score'],date=this_game['date'],attendance=10000,
            top_scorer_home=1,top_scorer_away=1
            #game_id=this_game["game_id"],

    )
    game.save()





    print("end Function")
    
def get_date(this_date):
    items = this_date.split(' ')
    print(items)
    months = {
        'JAN':1,'FEB':2,'MAR':3,"APR":4,"MAY":5,"JUNE":6,"JULY":7,"AUG":8,
        'SEPT':9,"OCT":10,"NOV":11,"DEC":12
    }
    month = months[items[0]]
    items[1]=items[1].replace(',', '')
    day = int(items[1].strip())
    year = int(items[2])
    return date(year, month, day)




if __name__ == "__main__":
    populate()