from nba_api.stats.endpoints import TeamGameLog, BoxScoreTraditionalV2
from nba_api.stats.library.parameters import Season, SeasonTypeAllStar, LeagueIDNullable
#from basketball.models import Game

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

def populate():
    data = TeamGameLog(team_id='1610612745').get_dict()# Houston Rockets
    game_ids=[]
    for game in data['resultSets']:
       # print(game['rowSet'])
       #print(game, "\n\n")
       #count=0
       for games in game['rowSet']:
            # Getting game ID for Houston Rockets
            #print("GameID: ", games[1])
            game_ids.append(games[1])

    #print(game_ids, "\n", len(game_ids)) PRINTING ALL GAME_IDS FOR ROCKETS
    #for games in game_ids:
    data2 = BoxScoreTraditionalV2(game_id = game_ids[0]).get_dict()
#    print(data2)
    for info in data2['resultSets']:
        #print(info, "\n")
        if(info['name'] == 'TeamStats'):
            # Theres not a reliable way to check which team is hosting
             game_id = info['rowSet'][0][0]
            # Whichever has high points in the winner... duh
            # if(info['rowSet'][0][23] > info['rowSet'][1][23]): # comparing scores
            #     winning_team_id = info['rowSet'][0][1] 
            #     losing_team_id = info['rowSet'][1][1]
            # else: 
            #      winning_team_id = info['rowSet'][1][1]
            #      losing_team_id = info['rowSet'][0][1]
            #print(info['rowSet'][0], "points: ", info['rowSet'][0][23])
            #print(info['rowSet'][1], "points: ", info['rowSet'][1][23])
        elif(info['name'] == 'PlayerStats'):
            highestScorerTeam1 = 0
            highestScorerTeam1ID = 0
            highestScorerTeam2 = 0
            highestScorerTeam2ID=0
            for players in info['rowSet'][0][27]:
                if(highestScorerTeam1 < players):
                    highestScorerTeam1 = players
                    highestScorerTeam1ID = info['rowSet'][0][27]
            for players in info['rowSet'][1][27]:
                if highestScorerTeam2 < players:
                    highestScorerTeam2 = info['rowSet'][1][4]
                    highestScorerTeam2ID= info['rowSet'][1][27]
            print(info['rowSet'][0][27])

            





    print("end Function")
    




if __name__ == "__main__":
    populate()