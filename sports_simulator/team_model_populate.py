from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import TeamInfoCommon,TeamPlayerDashboard
from basketball.models import Team, Player
import datetime
import time
'''
    team_name = models.CharField(max_length=40,null=False)
    team_abv = models.CharField(max_length=5,null=False)
    team_wins = models.IntegerField(null=False)
    team_loses = models.IntegerField(null=False)
    conference = models.CharField(max_length=20,null=False)
    division = models.CharField(max_length=20,null=False)
    conference_rank = models.CharField(max_length=2,null=False)
    points_total = models.IntegerField(null=False)
    assists_total = models.IntegerField(null=False)
    offensive_rebounds_total = models.IntegerField(null=False)
    defensive_rebounds_total = models.IntegerField(null=False)
    rebounds_total = models.IntegerField(null=False)
    blocks_total = models.IntegerField(null=False)
    steals_total = models.IntegerField(null=False)
    turnovers_total = models.IntegerField(null=False)
    personal_fouls_total = models.IntegerField(null=False)
    free_throws_made = models.IntegerField(null=False)
    free_throws_attempted = models.IntegerField(null=False)
    three_point_made = models.IntegerField(null=False)
    three_point_attempted = models.IntegerField(null=False)
    field_goals_made = models.IntegerField(null=False)
    field_goals_attempted = models.IntegerField(null=False)
    games_played = models.IntegerField(null=False)
    team_id = models.IntegerField(null=False)
    players = JSONField()

'''
def populate():

    all_teams = teams.get_teams()
    f = open('players_to_add.txt', 'w')

    for team in all_teams:
        time.sleep(2)
        team_info = TeamInfoCommon(team_id=team["id"]).get_dict()['resultSets'][0]['rowSet'][0]
        time.sleep(2)
        stats_info = TeamPlayerDashboard(team_id=team["id"],season='2019-20').get_dict()['resultSets']
        team_overall = stats_info[0]['rowSet'][0]
        player_season_totals = stats_info[1]['rowSet']

        #['Overall', 1610612737, 'Atlanta Hawks', '2019-20', 67, 20, 47, 0.299, 3256.0, 2723, 
        # 6067, 0.449, 805, 2416, 0.333, 1237, 1566, 0.79, 661, 2237, 2898, 1605, 1086.0, 523, 
        # 341, 428, 1548, 1404, 7488, -534.0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
        # 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        team_players={}
        team_players['players'] = []

        for p in player_season_totals:
            if Player.objects.filter(player_id=p[1]):
                team_players['players'].append([p[1],p[2]])
            else:
                print(p[2])
                f.write("%s\n" % p[2])

        '''
        "TeamOverall": [
            "GROUP_SET"0,"TEAM_ID"1,"TEAM_NAME"2,"GROUP_VALUE"3,"GP"4,"W"5,"L"6,"W_PCT"7,"MIN"8,
            "FGM"9,"FGA"10,"FG_PCT"11,"FG3M"12,"FG3A"13,"FG3_PCT"14,"FTM"15,"FTA"16,"FT_PCT"17,
            "OREB"18,"DREB"19,"REB"20,"AST"21,"TOV"22,"STL"23,"BLK"24,"BLKA"25,"PF"26,"PFD"27,
            "PTS"28,
        '''

        team = Team(team_name=(team_info[2]+" "+team_info[3]), team_abv=team_info[4],
                     team_wins=team_info[8],team_loses=team_info[9],conference=team_info[5],
                     division=team_info[6],conference_rank=team_info[11],
                     points_total=team_overall[28],assists_total=team_overall[21],
                     offensive_rebounds_total=team_overall[18],
                     defensive_rebounds_total=team_overall[19],rebounds_total=team_overall[20],
                     blocks_total=team_overall[24],steals_total=team_overall[23],
                     turnovers_total=team_overall[22],personal_fouls_total=team_overall[26],
                     free_throws_made=team_overall[15],free_throws_attempted=team_overall[16],
                     three_point_made=team_overall[12],three_point_attempted=team_overall[13],
                     field_goals_made=team_overall[9],field_goals_attempted=team_overall[10],
                     games_played=team_overall[4],team_id=team["id"],players=team_players
                )

        print(team_info[2]+" "+team_info[3])
        team.save()
    f.close()


if __name__ == '__main__':
    populate()