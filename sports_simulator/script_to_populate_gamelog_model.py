from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static import players

#{'PlayerID': 2544, 'LeagueID': None, 'Season': '2019-20', 'SeasonType': 'Regular Season', 'DateFrom': None, 'DateTo': None}
#'resultSets': [{'name': 'PlayerGameLog', 'headers': ['SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 
# 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
# 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE']
def populate():
    player_logs = PlayerGameLog(player_id=2544,season='2019-20').get_dict()
    print((player_logs['resultSets'][0]['headers']))
    print(len(player_logs['resultSets'][0]['rowSet']))
    for log in player_logs['resultSets'][0]['rowSet']:
        print(log, "\n")
    

if __name__ == "__main__":
    populate()