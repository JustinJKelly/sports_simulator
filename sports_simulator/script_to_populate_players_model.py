from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd
import time
from basketball.models import Player

import django
django.setup()

#need for CommonPlayerInfo requests
header = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://stats.nba.com',
}

 
#full_name,player_id,point_total,assists_total,rebounds_total,blocks_total
#steals_total, turnovers_total, personal_fouls_total,free_throws_attempted
#free_throws_made,minutes_total,three_point_attempted,three_point_made,
#field_goals_attempted,field_goals_made,games_played,team_id

#this should only run once, re-run when needed but should
#delete database entries before re-run
#Format of data
#['PLAYER_ID'0, 'SEASON_ID'1, 'LEAGUE_ID'2, 'TEAM_ID'3, 'TEAM_ABBREVIATION'4, 'PLAYER_AGE'5, 'GP'6, 'GS'7, 'MIN'8,
# 'FGM'9, 'FGA'10, 'FG_PCT'11, 'FG3M'12, 'FG3A'13, 'FG3_PCT'14, 'FTM'15, 'FTA'16, 'FT_PCT'17, 'OREB'18, 'DREB'19,
#  'REB'20, 'AST'21, 'STL'22, 'BLK'23, 'TOV'24, 'PF'25, 'PTS'26]
def populate():
    f = open("players_added.txt", "w")
    f1 = open("players_not_added.txt", "w")
    players_ = players.get_players()
    count = 0

    for p in players_:
        if p['is_active']:
            time.sleep(8)
            player = commonplayerinfo.CommonPlayerInfo(player_id=p["id"]).get_dict()['resultSets'][0]['rowSet'][0]
            player_stats_current_year = playercareerstats.PlayerCareerStats(player_id=p['id']).get_dict()['resultSets'][0]['rowSet']
            year_array = None

            for year_stats in player_stats_current_year:
                if year_stats[1]=='2019-20':
                    year_array=year_stats

            #player_name = players.find_player_by_id(year_array[0])
            #print(year_array)

            if year_array != None:
                if year_array[6]>0:
                    player = Player(full_name=p['full_name'],player_id=year_array[0],points_total=year_array[26],
                        assists_total=year_array[21],rebounds_total=year_array[20],blocks_total=year_array[23],
                        steals_total=year_array[22],turnovers_total=year_array[24],personal_fouls_total=year_array[25],
                        free_throws_attempted=year_array[16],free_throws_made=year_array[15],minutes_total=year_array[8],
                        three_point_attempted=year_array[13],three_point_made=year_array[12],field_goals_attempted=year_array[10],
                        field_goals_made=year_array[9],games_played=year_array[6],team_id=player[16],height=player[10],
                        weight=player[11],position=player[14],jersey_number=player[13],player_age=int(year_array[5]),
                        team_name=player[20]+" "+player[17],offensive_rebounds_total=year_array[18],
                        defensive_rebounds_total=year_array[19]
                    )

                    player.save()
                    print(p['full_name'])
                    s = p['full_name'] + "\n"
                    f.write(s)
                #else:
                    #s = p['full_name'] + "\n"
                    #f1.write(s)
            else:
                s = p['full_name'] + "\n"
                f1.write(s)
    f.close()
    f1.close()

#['PERSON_ID'0, 'FIRST_NAME'1, 'LAST_NAME'2, 'DISPLAY_FIRST_LAST'3, 'DISPLAY_LAST_COMMA_FIRST'4, 
#'DISPLAY_FI_LAST'5, 'BIRTHDATE'6, 'SCHOOL'7, 'COUNTRY'8, 'LAST_AFFILIATION'9, 'HEIGHT'10, 'WEIGHT'11, 
#'SEASON_EXP'12, 'JERSEY'13, 'POSITION'14, 'ROSTERSTATUS'15, 'TEAM_ID'16, 'TEAM_NAME'17, 'TEAM_ABBREVIATION'18, 
#'TEAM_CODE'19, 'TEAM_CITY'20, 'PLAYERCODE'21, 'FROM_YEAR'22, 'TO_YEAR'23, 'DLEAGUE_FLAG'24, 'NBA_FLAG'25, 
#'GAMES_PLAYED_FLAG'26, 'DRAFT_YEAR'27, 'DRAFT_ROUND'28, 'DRAFT_NUMBER'29]
#1629027
def test(parameter):

    player = commonplayerinfo.CommonPlayerInfo(player_id=parameter)
    print(len(player.get_dict()['resultSets'][0]['rowSet'][0]))
    print(player.get_dict()['resultSets'][0]['rowSet'])
if __name__ == "__main__":
    #test()
    populate()
