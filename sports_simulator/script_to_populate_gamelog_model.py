from nba_api.stats.endpoints import PlayerGameLog
from nba_api.stats.static import players, teams
from datetime import date
from basketball.models import GameLog

#{'PlayerID': 2544, 'LeagueID': None, 'Season': '2019-20', 'SeasonType': 'Regular Season', 'DateFrom': None, 'DateTo': None}
#'resultSets': [{'name': 'PlayerGameLog', 'headers': ['SEASON_ID', 'Player_ID', 'Game_ID', 'GAME_DATE', 'MATCHUP', 
# 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 
# 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE']

'''player_id = models.ForeignKey(Player, on_delete=models.CASCADE)
    date_time = models.DateField(default=date.today)
    opponent = models.CharField(max_length=4,null=False)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    win_loss = models.CharField(max_length=1) #W or L
    minutes = models.IntegerField(null=False,default=0)
    field_goals_made = models.IntegerField(null=False,default=0)
    field_goals_attempted = models.IntegerField(null=False,default=0)
    three_point_made = models.IntegerField(null=False,default=0)
    three_point_attempted = models.IntegerField(null=False,default=0)
    free_throws_made = models.IntegerField(null=False,default=0)
    free_throws_attempted = models.IntegerField(null=False,default=0)
    rebounds = models.IntegerField(null=False,default=0)
    assists = models.IntegerField(null=False,default=0)
    steals = models.IntegerField(null=False,default=0)
    blocks = models.IntegerField(null=False,default=0)
    turnovers = models.IntegerField(null=False,default=0)
    personal_fouls = models.IntegerField(null=False,default=0)
    points = models.IntegerField(null=False,default=0)
    off_rebounds = models.IntegerField(null=False,default=0)
    def_rebounds = models.IntegerField(null=False,default=0)'''
def populate():
    player_logs = PlayerGameLog(player_id=2544,season='2019-20').get_dict()
    #print((player_logs['resultSets'][0]['headers']))
    #print(len(player_logs['resultSets'][0]['rowSet']))
    for log in player_logs['resultSets'][0]['rowSet']:
        #print(log, "\n")
        game_log = GameLog(player_id=players.find_player_by_id(player_id=log[1]),date_time=get_game_date(log[3]),opponent=get_opponent(log[4]),
                            win_loss=log[5],game_id=log[2],minutes=log[6],field_goals_made=log[7],field_goals_attempted=log[8],
                            three_point_made=log[10], three_point_attempted=log[11],free_throws_made=log[13],
                            free_throws_attempted=log[14],off_rebounds=log[16],def_rebounds=log[17],rebounds=log[18],
                            assists=log[19],steals=log[20],blocks=log[21],turnovers=log[22],personal_fouls=log[23],
                            points=log[24])
        game_log.save()

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
    
def get_opponent(matchup):
    matchup = matchup.split(' ')
    opponent_abv = matchup[2]
    return opponent_abv

if __name__ == "__main__":
    populate()