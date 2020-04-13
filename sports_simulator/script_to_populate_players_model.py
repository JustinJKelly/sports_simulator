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

#Player Model (full_name,player_id,point_per_game,assists_per_game,rebounds_per_game,blocks_per_game,
# steals_per_game,turnovers_per_game,personal_fouls_per_game,free_throw_percentage,field_goal_percentage,
# minutes_per_game,three_point_percentage,games_played,team_id)

#this should only run once, re-run when needed but should
#delete database entries before re-run
#Format of data
#['PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']
def populate():
    players_ = players.get_players()
    count = 0

    for p in players_:
        if p['is_active']:
            time.sleep(3)
            player_stats_current_year = playercareerstats.PlayerCareerStats(player_id=p['id']).get_dict()['resultSets'][0]['rowSet']
            year_array = None

            for year_stats in player_stats_current_year:
                if year_stats[1]=='2019-20':
                    year_array=year_stats

            #player_name = players.find_player_by_id(year_array[0])
            #print(year_array)

            if year_array != None:
                if year_array[6]>5:
                    player = Player(full_name=p['full_name'],player_id=year_array[0],point_per_game=round(year_array[26]/year_array[6],1),
                        assists_per_game=year_array[21]/year_array[6],rebounds_per_game=year_array[20]/year_array[6],
                        blocks_per_game=year_array[23]/year_array[6],steals_per_game=year_array[22]/year_array[6],
                        turnovers_per_game=year_array[24]/year_array[6],personal_fouls_per_game=year_array[25]/year_array[6],
                        free_throw_percentage=year_array[17]*100,field_goal_percentage=year_array[11]*100,
                        minutes_per_game=year_array[8]/year_array[6],three_point_percentage=year_array[14]*100,
                        games_played=year_array[6],team_id=year_array[3]
                    )

                    player.save()
                    print(p['full_name'])


if __name__ == "__main__":
    populate()
