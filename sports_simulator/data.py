from nba_api.stats.endpoints import WinProbabilityPBP,TeamDashboardByOpponent
from basketball.models import Game, Team
from datetime import date
from nba_api.stats.library.parameters import Season

''' "WinProbPBP": [
            "GAME_ID",
            "EVENT_NUM",
            "HOME_PCT",
            "VISITOR_PCT",
            "HOME_PTS",
            "VISITOR_PTS",
            "HOME_SCORE_MARGIN",
            "PERIOD",
            "SECONDS_REMAINING",
            "HOME_POSS_IND",
            "HOME_G",
            "DESCRIPTION",
            "LOCATION",
            "PCTIMESTRING",
            "ISVISIBLE"
        ]'''
'''def get_data():
    games = Game.objects.all()

    count = 1
    for game in games:
        print(game)
        this_game_id = "00" + str(game.game_id)
        print(this_game_id)
        data = WinProbabilityPBP(this_game_id).get_dict()['resultSets'][0]['rowSet']
        print(len(data))
        #print(data)
        print("home win % ",data[2500][2])
        print("away win % ",data[2500][3])
        #break
        if count == 15:
         break
        count += 1'''

'''
['GROUP_SET', 'GROUP_VALUE', 'GP'2, 'W'3, 'L'4, 'W_PCT'5, 'MIN'6, 'FGM'7, 'FGA'8, 'FG_PCT'9,
 'FG3M'10, 'FG3A'11, 'FG3_PCT'12, 'FTM'13, 'FTA'14, 'FT_PCT'15, 'OREB'16, 'DREB'17, 
 'REB'18, 'AST'19, 'TOV'20, 'STL'21, 'BLK'22, 'BLKA'23, 'PF'24, 
'PFD'25, 'PTS'26, 'PLUS_MINUS'27, 'GP_RANK', 'W_RANK', 'L_RANK', 'W_PCT_RANK', 'MIN_RANK', 'FGM_RANK', 
'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 
'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 
'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PTS_RANK', 'PLUS_MINUS_RANK', 'CFID', 'CFPARAMS']

'''
def get_other_data():
    f = open('team_matchups.txt','w')
    for team in Team.objects.all():
        this_team_id = team.team_id
        #f.write('%s: %s\n' % ("TEAM",team.team_name))
        print("Team:", team.team_name)
        for opp_team in Team.objects.all():
            if opp_team.team_id != this_team_id:
                f.write('%s: %s\n' % ("TEAM",team.team_name))
                f.write('%s %s\n' % ("OPPONENT",opp_team.team_name))
                print("Opponent:", opp_team.team_name)
                team_matchup_2019_2020 = TeamDashboardByOpponent( team_id=this_team_id, 
                                                        opponent_team_id=opp_team.team_id,
                                                        season='2019-20').get_dict()['resultSets'][3]['rowSet']
                                            
                team_matchup_2018_2019 = TeamDashboardByOpponent( team_id=this_team_id, 
                                                        opponent_team_id=opp_team.team_id,
                                                        season='2018-19').get_dict()['resultSets'][3]['rowSet']
                #print(team_matchup_2018_2019)
                if len(team_matchup_2018_2019) > 0:
                    team_matchup_2018_2019 = team_matchup_2018_2019[0]
                    f.write('%s\n' % ( '2018-2019 Season'))
                    f.write('%s %s\n' % ('Games Played:',team_matchup_2018_2019[2]))
                    f.write('%s %s\n' % ('Wins:',team_matchup_2018_2019[3]))
                    f.write('%s %s\n' % ('Losses:',team_matchup_2018_2019[4]))
                    f.write('%s %s\n' % ('Win %:',team_matchup_2018_2019[5]))
                    f.write('%s %s\n' % ('FG %:',team_matchup_2018_2019[9]))
                    f.write('%s %.3f\n' % ('FG Attempted PG:',team_matchup_2018_2019[8]/team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('BLK PG',team_matchup_2018_2019[22]/team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('RB PG:',team_matchup_2018_2019[18]//team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('ORB PG:',team_matchup_2018_2019[16]//team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('DRB PG:',team_matchup_2018_2019[17]//team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('AST PG:',team_matchup_2018_2019[19]//team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('3PT Attempted PG:',team_matchup_2018_2019[11]//team_matchup_2018_2019[2]))
                    f.write('%s %s\n' % ('3PT %:',team_matchup_2018_2019[12]))
                    f.write('%s %s\n' % ('Plus-Minus(Points):',team_matchup_2018_2019[27]))
                    f.write('%s %.3f\n' % ('FT Attempted PG',team_matchup_2018_2019[14]/team_matchup_2018_2019[2]))
                    f.write('%s %.3f\n' % ('Points PG',team_matchup_2018_2019[26]/team_matchup_2018_2019[2]))
                else:
                    f.write("No matchups\n")
                
                #print(team_matchup_2019_2020)
                #print(team_matchup_2018_2019)
                if len(team_matchup_2019_2020)>0:
                    team_matchup_2019_2020 = team_matchup_2019_2020[0]
                    f.write('\n%s\n' % ( '2019-2020 Season'))
                    f.write('%s %s\n' % ('Games Played:',team_matchup_2019_2020[2]))
                    f.write('%s %s\n' % ('Wins:',team_matchup_2019_2020[3]))
                    f.write('%s %s\n' % ('Losses:',team_matchup_2019_2020[4]))
                    f.write('%s %s\n' % ('Win %:',team_matchup_2019_2020[5]))
                    f.write('%s %s\n' % ('FG %:',team_matchup_2019_2020[9]))
                    f.write('%s %.3f\n' % ('FG Attempted PG:',team_matchup_2019_2020[8]/team_matchup_2019_2020[2],))
                    f.write('%s %.3f\n' % ('BLK PG',team_matchup_2019_2020[22]/team_matchup_2019_2020[2]))
                    f.write('%s %.3f\n' % ('RB PG:',team_matchup_2019_2020[18]//team_matchup_2019_2020[2]))
                    f.write('%s %.3f\n' % ('ORB PG:',team_matchup_2019_2020[16]//team_matchup_2019_2020[2]))
                    f.write('%s %.3f\n' % ('DRB PG:',team_matchup_2019_2020[17]//team_matchup_2019_2020[2]))
                    f.write('%s %.3f\n' % ('AST PG:',team_matchup_2019_2020[19]//team_matchup_2019_2020[2]))
                    f.write('%s %.3f\n' % ('3PT Attempted PG:',team_matchup_2019_2020[11]//team_matchup_2019_2020[2]))
                    f.write('%s %s\n' % ('3PT %:',team_matchup_2019_2020[12]))
                    f.write('%s %s\n' % ('Plus-Minus(Points):',team_matchup_2019_2020[27]))
                    f.write('%s %.3f\n' % ('FT Attempted PG',team_matchup_2019_2020[14]/team_matchup_2019_2020[2]))
                    f.write('%s %.3f\n\n' % ('Points PG',team_matchup_2019_2020[26]/team_matchup_2019_2020[2]))
                else:
                    f.write("No matchups\n\n")
'''
Team PPG
Team APG
Team RPG(ORB & DRB)
Team BLKSPG
Team FG%
Team FGA
Team 3FG%
Team 3FGA
Team SPG
Team #AllStars(we can hardcode this)
Team Height
Team Rankings
Player Points
Player Rebounds
Player assists
Player BLKS
Player FG%
Player 3FG%
Player Steals

'''
        


if __name__ == "__main__":
    #get_data()
    get_other_data()
