from basketball.models import Game,Team,Player
from datetime import date
import re
import random
import pprint
import copy


def make_playoff_games():
    current = 20200418
    higher_seed_wins = 0
    lower_seed_wins = 0
    games_count = 0
    hundred =0
    series_data = {
        'higher_seed_series_wins':0,
        'lower_seed_series_wins':0,
        'game_seven':0,
        'higher_seed_sweeps':0,
        'lower_seed_sweeps':0
    }
    low_seed = "New Orleans"
    high_seed = "L.A. Lakers"
    is_hundred = False
    
    while hundred < 100:
        games_count=0
        higher_seed_wins=0
        lower_seed_wins=0
        hundred+=1
        while games_count < 7 and (higher_seed_wins < 4) and lower_seed_wins < 4:# plays seven games
            games_count+=1
            if games_count < 3 :
                team_home_id = get_team(high_seed.lower())
                home_team_name = high_seed
                team_away_id = get_team(low_seed.lower())
                away_team_name = low_seed
                print('Away team: %s %s' % (low_seed, team_away_id))
                print('Home team: %s %s' % (high_seed, team_home_id))
            elif games_count >= 3 and games_count < 6:
                team_home_id = get_team(low_seed.lower())
                home_team_name = high_seed
                team_away_id = get_team(high_seed.lower())
                away_team_name = low_seed
                print('Away team: %s %s' % (high_seed, team_away_id))
                print('Home team: %s %s' % (low_seed, team_home_id))
            else:
                team_home_id = get_team(high_seed.lower())
                home_team_name = high_seed
                team_away_id = get_team(low_seed.lower())
                away_team_name = low_seed
                print('Away team: %s %s' % (low_seed, team_away_id))
                print('Home team: %s %s' % (high_seed, team_home_id))
            curr = str(current)
            
            game_date = date(int(curr[0:4]),int(curr[4:6]),int(curr[6:]))
            #current+=1
            
            # game_info contains all relevant information about the game calculated 
            game_info = calculate_stats(team_home_id,team_away_id,game_date)
            if games_count < 3:
                if game_info[team_away_id] < game_info[team_home_id]:
                    higher_seed_wins+=1
                else:
                    lower_seed_wins+=1
            elif games_count >=3 and games_count < 6:
                if game_info[team_away_id] > game_info[team_home_id]:
                    higher_seed_wins+=1
                else:
                    lower_seed_wins+=1
            else:
                if game_info[team_away_id] < game_info[team_home_id]:
                    higher_seed_wins+=1
                else:
                    lower_seed_wins+=1
                
            print("AWAY: ", temp[team_away_id], "\n")
            print("HOME: ", temp[team_home_id], "\n")
            print("Lakers: ", higher_seed_wins,"\n")
            print("Pelicans: ", lower_seed_wins,"\n")
        if(higher_seed_wins > lower_seed_wins):
            series_data['higher_seed_series_wins']+=1
            if lower_seed_wins == 0:
                series_data['higher_seed_sweeps']+=1
            elif lower_seed_wins == 3:
                series_data['game_seven']+=1
        else:
            series_data['lower_seed_series_wins']+=1
            if higher_seed_wins ==0:
                series_data['lower_seed_sweeps']+=1
            elif higher_seed_wins==3:
                series_data['game_seven']+=1
    print(" 100 Series Stats")
    print("HIGHER SEED ", high_seed, " series wins: ", series_data['higher_seed_series_wins'], "\n")
    print("Higher seed sweeps: ", series_data['higher_seed_sweeps'], "\n")
    print("LOWER SEED ", low_seed, " series wins: ", series_data['lower_seed_series_wins'], "\n")
    print("Lower seed sweeps: ", series_data['lower_seed_sweeps'], "\n")
    print("Game Sevens: ", series_data['game_seven'])
          




def calculate_stats(home_id,away_id,game_date):
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

    # GETTING BIAS LIST/MATRIX 
    home_bias_list = get_bias_home(home_id)
    away_bias_list = get_bias_away(away_id)
   

    home_points_pg = round(team_home.points_total/team_home.games_played,1)
    away_points_pg = round(team_away.points_total/team_away.games_played,1)
    away_opp_point_pg = round(team_away.opponent_points_total/team_away.games_played,1)
    home_opp_point_pg = round(team_home.opponent_points_total/team_home.games_played,1)

    if home_points_pg > away_opp_point_pg:
        overall_bias_home = random.uniform(1.00,1.05)# slightly increase home team scoring
    else:
        overall_bias_home = random.uniform(0.98,1.00)# slightly decrease away team scoring



    # COMPUTING HOME TEAM STATS
    home_game_stats = {
        'minutes':240,
        'field_goals_percentage': (home_stats['field_goal_percentage'])*(random.uniform(home_bias_list[0], home_bias_list[1]))*overall_bias_home,
        'field_goals_attempted': round((home_stats['field_goals_attempted_per_game'])+random.uniform(home_bias_list[2],home_bias_list[3])*overall_bias_home),
        'three_point_percentage': (home_stats['three_point_percentage'])*(random.uniform(home_bias_list[4], home_bias_list[5]))*overall_bias_home,
        'three_point_attempted': round((home_stats['three_point_attempted_per_game'])+random.uniform(home_bias_list[6],home_bias_list[7])*overall_bias_home),
        'free_throws_percentage': ((home_stats['free_throw_percentage'])*(random.uniform(home_bias_list[8], home_bias_list[9])))*overall_bias_home,
        'free_throws_attempted': round((home_stats['free_throws_attempted_per_game'])+random.uniform(home_bias_list[10],home_bias_list[11])*overall_bias_home),
        'def_rebounds': round((home_stats['defensive_rebounds_per_game'])+random.uniform(home_bias_list[12],home_bias_list[13])*overall_bias_home),
        'off_rebounds': round((home_stats['offensive_rebounds_per_game'])+random.uniform(home_bias_list[14],home_bias_list[15])*overall_bias_home),
        #'rebounds': ((biases['home_rebounds_bias'])+home_stats['rebounds_per_game'])+random.uniform(home_bias_list[16],home_bias_list[17])*overall_bias_home,
        'assists': round((home_stats['assists_per_game'])+random.uniform(home_bias_list[18],home_bias_list[19])*overall_bias_home),
        'steals': round((home_stats['steals_per_game'])+random.uniform(home_bias_list[20],home_bias_list[21])*overall_bias_home),
        'blocks': round((home_stats['blocks_per_game'])+random.uniform(home_bias_list[22],home_bias_list[23])*overall_bias_home),
        'turnovers': round((home_stats['turnovers_per_game'])+random.uniform(home_bias_list[24],home_bias_list[25])*overall_bias_home),
        'personal_fouls': round((home_stats['personal_fouls_per_game'])+ random.uniform(home_bias_list[26],home_bias_list[27])*overall_bias_home),
        #'points': (((biases['home_points_bias']+home_stats['points_per_game'])+(biases['home_points_per_game_bias']+home_stats['points_per_game']))/2)+random.uniform(home_bias_list[28],home_bias_list[29]),
    }


    home_game_stats['field_goals_made'] = round(home_game_stats['field_goals_attempted']*(home_game_stats['field_goals_percentage']/100)) 
    home_game_stats['free_throws_made'] = round((home_game_stats['free_throws_percentage']/100)*home_game_stats['free_throws_attempted'])
    home_game_stats['three_point_made'] = round((home_game_stats['three_point_percentage']/100)*home_game_stats['three_point_attempted'])
    home_game_stats['field_goals_percentage'] = round( (home_game_stats['field_goals_made']/home_game_stats['field_goals_attempted'])*100)
    home_game_stats['three_point_percentage'] = round( (home_game_stats['three_point_made']/home_game_stats['three_point_attempted'])*100)
    home_game_stats['free_throw_percentage'] = round( (home_game_stats['free_throws_made']/home_game_stats['free_throws_attempted'])*100)
    home_game_stats['rebounds'] = home_game_stats['off_rebounds']+home_game_stats['def_rebounds']
    total_points_home = (home_game_stats['three_point_made']*3)+((home_game_stats['field_goals_made']-home_game_stats['three_point_made'])*2) + home_game_stats['free_throws_made']

    #pprint.pprint(home_game_stats)


    if away_points_pg > home_opp_point_pg:
        overall_bias_away = random.uniform(1.0,1.02)# slightly boost away team scoring
    else:
        overall_bias_away = random.uniform(0.95,1.00)# slightly decrease away team scoring.


    #overall_bias_away=1

    # COMPUTING AWAY TEAM STATS
    away_game_stats = {
        'minutes':240,
        'field_goals_percentage': (away_stats['field_goal_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
        'field_goals_attempted': round((away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])),#*overall_bias_away),
        'three_point_percentage': (away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
        'three_point_attempted': round((away_stats['three_point_attempted_per_game'])+random.uniform(away_bias_list[6],away_bias_list[7])*overall_bias_away),
        'free_throws_percentage': ((away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
        'free_throws_attempted': round((away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away),
        'def_rebounds': round((away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away),
        'off_rebounds': round((away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away),
        #'rebounds': ((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away,
        'assists': round((away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away),
        'steals': round((away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away),
        'blocks': round((away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away),
        'turnovers': round((away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away),
        'personal_fouls': round((away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away),
        #'points': (((biases['away_points_bias']+away_stats['points_per_game'])+(biases['away_points_per_game_bias']+away_stats['points_per_game']))/2)+random.uniform(away_bias_list[28],away_bias_list[29]),
    }
    away_game_stats['field_goals_made'] = round(away_game_stats['field_goals_attempted']*(away_game_stats['field_goals_percentage']/100))
    away_game_stats['free_throws_made'] = round((away_game_stats['free_throws_percentage']/100)*away_game_stats['free_throws_attempted'])
    away_game_stats['three_point_made'] = round((away_game_stats['three_point_percentage']/100)*away_game_stats['three_point_attempted'])
    away_game_stats['field_goals_percentage'] = round( (away_game_stats['field_goals_made']/away_game_stats['field_goals_attempted'])*100,1)
    away_game_stats['three_point_percentage'] = round( (away_game_stats['three_point_made']/away_game_stats['three_point_attempted'])*100,1)
    away_game_stats['free_throw_percentage'] = round( (away_game_stats['free_throws_made']/away_game_stats['free_throws_attempted'])*100,1)  
    away_game_stats['rebounds'] = away_game_stats['off_rebounds']+away_game_stats['def_rebounds']
    total_points_away = (away_game_stats['three_point_made']*3) + ((away_game_stats['field_goals_made']-away_game_stats['three_point_made'])*2) + away_game_stats['free_throws_made']

    #print('AWAY')
    # CALLING COMPUTE PLAYER STATS TO DISTRIBUTE STATS
    combined_away_stats = compute_player_stats(away_game_stats,total_points_away,away_id, 0)
    team_away_stats = combined_away_stats[1]
    player_away_stats = combined_away_stats[0]
    #print('HOME')
    combined_home_stats = compute_player_stats(home_game_stats,total_points_home,home_id, team_away_stats['points'])
    team_home_stats = combined_home_stats[1]
    player_home_stats = combined_home_stats[0]

    # CALLING COMPUTE POINTS BY QUARTER
    num_ots = 0
    points_by_quarter = compute_points_by_quarter(team_home_stats['points'],team_away_stats['points'],num_ots)
    points_by_quarter_home = points_by_quarter['home_scores']
    points_by_quarter_away = points_by_quarter['away_scores']

    print('Points by quarter home:', points_by_quarter_home)
    print('Points by quarter away:', points_by_quarter_away)

    home = Team.objects.get(team_id=home_id)
    away = Team.objects.get(team_id=away_id)
    
    home_name = home.team_name
    away_name = away.team_name

    # UPDATING AWAY TEAM STATS WE DONT WANT TO DO THIS YET

    """
        team_stat['assists']+=player_stat['assists']
        team_stat['off_rebounds']+=player_stat['off_rebounds']
        team_stat['def_rebounds']+=player_stat['def_rebounds']
        team_stat['rebounds']+=(player_stat['off_rebounds']+player_stat['def_rebounds'])
        team_stat['blocks']+=player_stat['blocks']
        team_stat['steals']+=player_stat['steals']
        team_stat['turnovers']+=player_stat['turnovers']
        team_stat['personal_fouls']+=player_stat['personal_fouls']
        team_stat['FT_attempted']+=player_stat['FT_attempted']
        team_stat['FT_made']+=player_stat['FT_made']
        team_stat['FG_attempted']+=player_stat['FG_attempted']
        team_stat['FG_made']+=player_stat['FG_made']
        team_stat['3P_attempted']+=player_stat['3P_attempted']
        team_stat['3P_made']+=player_stat['3P_made']
        team_stat['points']+=player_stat['points']
        
        away.points_total += team_away_stats['points']
        away.assists_total += team_away_stats['assists']
        away.offensive_rebounds_total += team_away_stats['off_rebounds']
        away.defensive_rebounds_total += team_away_stats['def_rebounds']
        away.rebounds_total += team_away_stats['rebounds']
        away.blocks_total += team_away_stats['blocks']
        away.steals_total += team_away_stats['steals']
        away.turnovers_total += team_away_stats['turnovers']
        away.personal_fouls_total += team_away_stats['personal_fouls']
        away.free_throws_made += team_away_stats['FT_made']
        away.free_throws_attempted += team_away_stats['FT_attempted']
        away.three_point_made += team_away_stats['3P_made']
        away.three_point_attempted += team_away_stats['3P_attempted']
        away.field_goals_made += team_away_stats['FG_made']
        away.field_goals_attempted += team_away_stats['FG_attempted']
        away.games_played += 1
        away.opponent_points_total += team_home_stats['points']
        away.save()
    """
    #UPDATING HOME TEAM STATS WE DONT WANT TO DO THIS YET
    """
        home.points_total += team_home_stats['points']
        home.assists_total += team_home_stats['assists']
        home.offensive_rebounds_total += team_home_stats['off_rebounds']
        home.defensive_rebounds_total += team_home_stats['def_rebounds']
        home.rebounds_total += team_home_stats['rebounds']
        home.blocks_total += team_home_stats['blocks']
        home.steals_total += team_home_stats['steals']
        home.turnovers_total += team_home_stats['turnovers']
        home.personal_fouls_total += team_home_stats['personal_fouls']
        home.free_throws_made += team_home_stats['FT_made']
        home.free_throws_attempted += team_home_stats['FT_attempted']
        home.three_point_made += team_home_stats['3P_made']
        home.three_point_attempted += team_home_stats['3P_attempted']
        home.field_goals_made += team_home_stats['FG_made']
        home.field_goals_attempted += team_home_stats['FG_attempted']
        home.games_played += 1
        home.opponent_points_total += team_away_stats['points']
        home.save()
    """

        # UPDATING GAME METADATA
    if team_away_stats['points'] > team_home_stats['points']:
        winner_team_id = away_id
        winning_name = away_name
        losing_name = home_name
        loser_team_id = home_id
        
        #update database
        winner = Team.objects.get(team_id=away_id)
        winner.team_wins += 1
        winner.away_wins += 1

        loser = Team.objects.get(team_id=home_id)
        loser.team_losses += 1
        loser.home_losses += 1

        # DONT HAVE TO WORRY ABOUT CONFERENCE WINS
        '''
        if loser.conference == winner.conference:
            loser.conference_losses += 1
            winner.conference_wins += 1
        
        if loser.division == winner.division:
            loser.divisional_losses += 1
            winner.divisional_wins += 1
        '''

    else:
        winner_team_id = home_id
        winning_name = home_name
        losing_name = away_name
        loser_team_id = away_id

        #update database
        winner = Team.objects.get(team_id=home_id)
        winner.team_wins += 1
        winner.away_wins += 1

        loser = Team.objects.get(team_id=away_id)
        loser.team_losses += 1
        loser.home_losses += 1
        
        # DONT HAVE TO WORRY ABOUT CONFERENCE WINS ANYMORE
        '''
        if loser.conference == winner.conference:
            loser.conference_losses += 1
            winner.conference_wins += 1
        
        if loser.division == winner.division:
            loser.divisional_losses += 1
            winner.divisional_wins += 1
        '''

    #SAVE TEAMS
    #loser.save() DONT SAVE YET
    # winner.save() DONT SAVE YET

    
    # GAME METADATA: TOP SCORERS
    top_scorer_home_team_score = 0
    top_scorer_home_team_id = 0
    for p in player_home_stats:
        if top_scorer_home_team_score < p['points']:
            top_scorer_home_team_score = p['points']
            top_scorer_home_team_id = p['player_id']

    top_scorer_away_team_score = 0
    top_scorer_away_team_id = 0
    for p in player_away_stats:
        if top_scorer_away_team_score < p['points']:
            top_scorer_away_team_score = p['points']
            top_scorer_away_team_id = p['player_id']

    #UPDATING/ SAVING NEW GAME TO PLAYER MODEL
    # NOT SAVING YET, NO NEED

    """
    for p in (player_away_stats+player_home_stats):
        pl = Player.objects.get(player_id=p['player_id'])
        
        player_stat['assists']=0
        player_stat['off_rebounds']=0
        player_stat['def_rebounds']=0
        player_stat['rebounds']=0
        player_stat['blocks']=0
        player_stat['steals']=0
        player_stat['turnovers']=0
        player_stat['personal_fouls']=0
        player_stat['FT_attempted']=0
        player_stat['FT_made']=0
        player_stat['FG_attempted']=0
        player_stat['FG_made']=0
        player_stat['3P_attempted']=0
        player_stat['3P_made']=0
        player_stat['points']=0
        player_stat['min']=0
        player_stat['comment']="NONE"
        
        
        pl.assists_total += p['assists']
        pl.offensive_rebounds_total += p['off_rebounds']
        pl.defensive_rebounds_total += p['def_rebounds']
        pl.rebounds_total += p['rebounds']
        pl.blocks_total += p['blocks']
        pl.steals_total += p['steals']
        pl.turnovers_total += p['turnovers']
        pl.personal_fouls_total += p['personal_fouls']
        pl.free_throws_made += p['FT_made']
        pl.free_throws_attempted += p['FT_attempted']
        pl.minutes_total += p['min']
        pl.three_point_made += p['3P_made']
        pl.three_point_attempted += p['3P_attempted']
        pl.field_goals_made += p['FG_made']
        pl.field_goals_attempted += p['FG_attempted']
        if p['comment'] == "OK":
            pl.games_played += 1
        pl.points_total += p['points']
        #SAVE PLAYER
        pl.save()
    """

    data = {}
    data['points_by_quarter_id'] = {}
    data['points_by_quarter_id'][home_id]=points_by_quarter_home
    data['points_by_quarter_id'][away_id]=points_by_quarter_away
    data['player_stats']=player_home_stats + player_away_stats 
    data['team_stats']=[team_home_stats,team_away_stats]
    #print(data['points_by_quarter_id'][home_id])
    #print(data['points_by_quarter_id'][away_id])
    #print(data['team_stats'])
    # SAVING GAME DATA NOT NECESSARY YET
    '''
        game = Game(home_team=home_id,away_team=away_id,home_team_name=home_name,away_team_name=away_name, 
                game_id=(Game.objects.all().order_by('-game_id')[0].game_id+1),winning_team_id=winner_team_id,
                winner_name=winning_name,loser_name=losing_name,losing_team_id=loser_team_id,
                home_team_score=team_home_stats['points'],away_team_score=team_away_stats['points'],
                top_scorer_home=top_scorer_home_team_id ,top_scorer_away=top_scorer_away_team_id,
                top_scorer_home_points=top_scorer_home_team_score,top_scorer_away_points=top_scorer_away_team_score,
                date=game_date,home_team_record=(str(home.team_wins)+'-'+str(home.team_losses)),
                away_team_record=(str(away.team_wins)+'-'+str(away.team_losses)),
                data=data         
            )
    '''
    #game.save() DONT SAVE YET
    # need to return data
    return data

def sort_func(p):
    return p.points_total/p.games_played

def sort_func2(p):
    return p.is_starter

def compute_player_stats(stats,score,tid, other_team_score):
    team_players = Player.objects.filter(team_id=tid)
    team_players = sorted(team_players, reverse=True, key=sort_func)# sort by points/game
    team_players = sorted(team_players, reverse=True, key=sort_func2)# sort by is_starter
    team = Team.objects.get(team_id=tid)
    '''
         'minutes':240,
        'field_goals_percentage': ((biases['away_field_goal_percentage_bias'])+away_stats['field_goal_percentage'])*(random.uniform(away_bias_list[0], away_bias_list[1]))*overall_bias_away,
        'field_goals_attempted': round(((biases['away_field_goal_attempt_bias'])+away_stats['field_goals_attempted_per_game'])+random.uniform(away_bias_list[2],away_bias_list[3])*overall_bias_away),
        'three_point_percentage': ((biases['away_three_point_pct_bias'])+away_stats['three_point_percentage'])*(random.uniform(away_bias_list[4], away_bias_list[5]))*overall_bias_away,
        'three_point_attempted': round(((biases['away_three_point_att_bias'])+away_stats['three_point_attempted_per_game'])+random.uniform(-away_bias_list[6],away_bias_list[7])*overall_bias_away),
        'free_throws_percentage': (((biases['away_free_throw_percentage_bias'])+away_stats['free_throw_percentage'])*(random.uniform(away_bias_list[8], away_bias_list[9])))*overall_bias_away,
        'free_throws_attempted': round(((biases['away_free_throw_att_bias'])+away_stats['free_throws_attempted_per_game'])+random.uniform(away_bias_list[10],away_bias_list[11])*overall_bias_away),
        'def_rebounds': round(((biases['away_def_rebounds_bias'])+away_stats['defensive_rebounds_per_game'])+random.uniform(away_bias_list[12],away_bias_list[13])*overall_bias_away),
        'off_rebounds': round(((biases['away_off_rebounds_bias'])+away_stats['offensive_rebounds_per_game'])+random.uniform(away_bias_list[14],away_bias_list[15])*overall_bias_away),
        #'rebounds': ((biases['away_rebounds_bias'])+away_stats['rebounds_per_game'])+random.uniform(away_bias_list[16],away_bias_list[17])*overall_bias_away,
        'assists': round(((biases['away_assists_bias'])+away_stats['assists_per_game'])+random.uniform(away_bias_list[18],away_bias_list[19])*overall_bias_away),
        'steals': round(((biases['away_steals_bias'])+away_stats['steals_per_game'])+random.uniform(away_bias_list[20],away_bias_list[21])*overall_bias_away),
        'blocks': round(((biases['away_blocks_bias'])+away_stats['blocks_per_game'])+random.uniform(away_bias_list[22],away_bias_list[23])*overall_bias_away),
        'turnovers': round(((biases['away_turnovers_bias'])+away_stats['turnovers_per_game'])+random.uniform(away_bias_list[24],away_bias_list[25])*overall_bias_away),
        'personal_fouls': round(((biases['away_personal_fouls_bias'])+away_stats['personal_fouls_per_game'])+ random.uniform(away_bias_list[26],away_bias_list[27])*overall_bias_away),
        #'points': 
        away_game_stats['field_goals_made'] = round(away_game_stats['field_goals_attempted']*(away_game_stats['field_goals_percentage']/100))
        away_game_stats['free_throws_made'] = round((away_game_stats['free_throws_percentage']/100)*away_game_stats['free_throws_attempted'])
        away_game_stats['three_point_made'] = round((away_game_s
    '''


    player_avg = []
    for player in team_players:

        if player.free_throws_attempted == 0:
            free_throw_percentage = 0
        else:
            free_throw_percentage = round((player.free_throws_made/player.free_throws_attempted)*100,1)

        if player.field_goals_attempted == 0:
            field_goal_percentage = 0
        else:
            field_goal_percentage = round((player.field_goals_made/player.field_goals_attempted)*100,1)
        
        if player.three_point_attempted == 0:
            three_point_percentage = 0
        else:
            three_point_percentage = round((player.three_point_made/player.three_point_attempted)*100,1)

        players = []
        player_avg.append( {
            "player_name":player.full_name,"player_id":player.player_id,
            "points_per_game":round( (player.points_total/player.games_played) ,4),
            "assists_per_game":round( (player.assists_total/player.games_played) ,4),
            "offensive_rebounds_per_game":round( (player.offensive_rebounds_total/player.games_played) ,4),
            "defensive_rebounds_per_game":round( (player.defensive_rebounds_total/player.games_played) ,4),
            "rebounds_per_game":round( (player.rebounds_total/player.games_played), 4),
            "blocks_per_game":round( (player.blocks_total/player.games_played), 4),
            "steals_per_game":round( (player.steals_total/player.games_played), 4),
            "turnovers_per_game":round( (player.turnovers_total/player.games_played), 4),
            "personal_fouls_per_game":round( (player.personal_fouls_total/player.games_played),4),
            "free_throw_percentage":free_throw_percentage,
            "field_goal_percentage":field_goal_percentage,
            "minutes_per_game":round( (player.minutes_total/player.games_played)/(240), 4),
            "three_point_percentage":three_point_percentage,
            "free_throws_attempted_per_game":round( (player.free_throws_attempted/player.games_played),4),
            "free_throws_made_per_game":round( (player.free_throws_made/player.games_played), 4),
            "three_point_attempted_per_game":round( (player.three_point_attempted/player.games_played), 4),
            "three_point_made_per_game":round( (player.three_point_made/player.games_played), 4),
            "field_goals_attempted_per_game":round( (player.field_goals_attempted/player.games_played), 4),
            "field_goals_made_per_game":round( (player.field_goals_made/player.games_played), 4),
            'minutes':player.minutes_total/player.games_played,
            'games_played':player.games_played,
            'injured':player.is_injured

        })

        if player.player_id == '201939' or player.player_id == 201939: #steph curry has low 3pt so should fix
            player_avg[len(player_avg)-1]["three_point_attempted_per_game"]=9
            player_avg[len(player_avg)-1]["three_point_made_per_game"]=4
            player_avg[len(player_avg)-1]["field_goals_attempted_per_game"]=20
            player_avg[len(player_avg)-1]["field_goals_made_per_game"]=9

    stats_copy = copy.deepcopy(stats)
    #print('PLAYER AVG:',player_avg)
    player_stats = []
    team_stat = {}
    team_stat['team_id']=tid
    name_index = team.team_name.find(' ')
    team_stat['team_name']=team.team_name[name_index+1:]
    team_stat['team_city']=team.team_name[0:name_index]
    team_stat['team_abv']=team.team_abv
    team_stat['assists']=0
    team_stat['off_rebounds']=0
    team_stat['def_rebounds']=0
    team_stat['rebounds']=0
    team_stat['blocks']=0
    team_stat['steals']=0
    team_stat['turnovers']=0
    team_stat['personal_fouls']=0
    team_stat['FT_attempted']=0
    team_stat['FT_made']=0
    team_stat['FG_attempted']=0
    team_stat['FG_made']=0
    team_stat['3P_attempted']=0
    team_stat['3P_made']=0
    team_stat['points']=0


    for player in player_avg:
        if not player['injured']:
            player_stat = {}
            player_stat['name']=player['player_name']
            player_stat['player_id']=player['player_id']
            player_stat['team_id']=tid
            p = Player.objects.get(player_id=player['player_id'])

            # OREB
            off_rebound_min = 0 if (p.offensive_rebounds_total/p.games_played) < 1.2 else 0.5
            off_rebound_max = 2.6 if (p.offensive_rebounds_total/p.games_played) < 1.2 else 1.5
            
            #DREB
            def_rebound_min = 0.5 if (p.defensive_rebounds_total/p.games_played) < 3.5 else 0.6
            def_rebound_max = 2 if (p.defensive_rebounds_total/p.games_played) < 3.5 else 1.4
            
            #PERSONAL FOULS
            personal_fouls_min = 0.4 if (p.personal_fouls_total/p.games_played) < 4 else 0.5
            personal_fouls_max = 2.3 if (p.personal_fouls_total/p.games_played) < 4 else 1.2

            #TURNOVERS 
            turnovers_min = 0.4 if (p.turnovers_total/p.games_played) < 1.2 else 0.5
            turnovers_max = 2.3 if (p.turnovers_total/p.games_played) < 1.2 else 1.6

            # STEALS
            steal_min = 0 if (p.steals_total/p.games_played) < 1.2 else 0.5
            steal_max = 2.5 if (p.steals_total/p.games_played) < 1.2 else 1.5
            
            # BLOCKS
            blocks_min = 0 if (p.steals_total/p.games_played) < 1.2 else 0.5
            blocks_max = 2.2 if (p.steals_total/p.games_played) < 1.2 else 1.5

            #ASSISTS
            assists_min = 0 if (p.steals_total/p.games_played) < 3 else 0.5
            assists_max = 2.2 if (p.steals_total/p.games_played) < 3 else 1.8
            

            #FIELD GOAL ATTEMPTS
            if (p.field_goals_attempted/p.games_played) < 5:
                fg_att_min = 0.4
                fg_att_max = 1.6
            elif (p.field_goals_attempted/p.games_played) < 9:
                fg_att_min = 0.6 
                fg_att_max = 1.45
            else:
                fg_att_min = 0.75
                fg_att_max = 1.35
            
            #FIELD GOALS MADE
            if (p.field_goals_made/p.games_played) < 3:
                fg_made_min = 0.6
                fg_made_max = 1.8
            elif (p.field_goals_made/p.games_played) < 7:
                fg_made_min = 0.8 
                fg_made_max = 1.45
            else:
                fg_made_min = 0.78
                fg_made_max = 1.42
            

            #3PT FIELD GOAL ATTEMPTS
            if (p.three_point_attempted/p.games_played) < 3:
                three_pt_att_min = 0
                three_pt_att_max = 2
            elif (p.three_point_attempted/p.games_played) < 5:
                three_pt_att_min = 0.5 
                three_pt_att_max = 1.7
            elif (p.field_goals_attempted/p.games_played) < 10:
                three_pt_att_min = 0.6 
                three_pt_att_max = 1.48
            else:
                three_pt_att_min = 0.7 
                three_pt_att_max = 1.4
            
            #3PT FIELD GOAL MADE
            if (p.three_point_made/p.games_played) < 2:
                three_pt_made_min = 0
                three_pt_made_max = 1.7
            elif (p.three_point_made/p.games_played) < 5:
                three_pt_made_min = 0.59
                three_pt_made_max = 1.5
            elif (p.three_point_made/p.games_played) < 8:
                three_pt_made_min = 0.67
                three_pt_made_max = 1.4
            else:
                three_pt_made_min = 0.78
                three_pt_made_max = 1.33


            # FT FIELD GOALS MADE    
            if (p.free_throws_made/p.games_played) < 2:
                free_throws_made_min = 0 
                free_throws_made_max = 2
            elif (p.free_throws_made/p.games_played) < 5:
                free_throws_made_min = 0.6
                free_throws_made_max = 1.7
            elif (p.free_throws_made/p.games_played) < 8:
                free_throws_made_min = 0.74 
                free_throws_made_max = 1.69
            else:
                free_throws_made_min = 0.9
                free_throws_made_max = 1.32

            #FT FIELD GOAL ATTEMPTED    
            if (p.free_throws_attempted/p.games_played) < 2:
                free_throws_att_min = 0 
                free_throws_att_max = 2
            elif (p.free_throws_attempted/p.games_played) < 5:
                free_throws_att_min = 0.5
                free_throws_att_max = 1.8
            elif (p.free_throws_attempted/p.games_played) < 8:
                free_throws_att_min = 0.72 
                free_throws_att_max = 1.7
            else:
                free_throws_att_min = 0.82
                free_throws_att_max = 1.5
                
            

            #BUCKS 
            if tid == 1610612749:
                fg_att_max += 0.08
                fg_made_max += 0.14
                fg_made_min+=0.06
                free_throws_made_max+=0.1
                free_throws_att_max += 0.1
                three_pt_att_max += 0.06
                three_pt_made_max += 0.1

            #LAKERS
            if tid == 1610612747:
                fg_made_max += 0.1
                fg_made_min+=0.1
                free_throws_made_max+=0.1
                free_throws_att_max += 0.1
                three_pt_att_max += 0.06
                three_pt_made_max += 0.1

            #ROCKETS
            if tid == 1610612745:
                three_pt_made_max += 0.12
                fg_made_max += 0.1
                fg_made_min+=0.02
                free_throws_made_max+=0.16
                free_throws_att_max += 0.1
                three_pt_att_max += 0.06
                fg_att_max -= 0.08
                fg_att_min -= 0.0             
                three_pt_att_min -= 0.05              
                three_pt_made_min -= 0.02
                
            #76ERS
            if tid == 1610612755:
                three_pt_made_min -= 0.02
                three_pt_made_max -= 0.03
                fg_made_min += 0.03
                fg_made_max += 0.05
                free_throws_att_max += 0.05
                free_throws_made_max += 0.05
                three_pt_att_max -= 0.05
                fg_att_max += 0.08
                fg_att_min += 0.03
                three_pt_att_min -= 0.05

            # CLIPPERS
            if tid == 1610612746:
                fg_att_min -= 0.14
                fg_made_max += 0.05
                fg_made_min += 0.03
                three_pt_att_min -= 0.02
                three_pt_made_min -= 0.06
                three_pt_made_max += 0.04 
                free_throws_att_max += 0.1
                free_throws_made_max += 0.1
                three_pt_att_max += 0.05

            #PACERS
            if tid == 1610612754:
                fg_att_max += 0.05
                fg_att_min += 0.03
                fg_made_max += 0.05
                fg_made_min += 0.03
                free_throws_made_max += 0.1
                free_throws_made_min += 0.04
                free_throws_att_max += 0.1
                free_throws_att_min += 0.04
                three_pt_att_min += 0.03
                three_pt_att_max += 0.05
                three_pt_made_min += 0.05
                three_pt_made_max += 0.12
            
            #RAPTORS
            if tid == 1610612761:
                fg_att_min -= 0.04
                fg_att_max -= 0.04
                fg_made_min -= 0.02
                fg_made_max -= 0.01
                free_throws_att_max += 0.1
                free_throws_made_max += 0.1
                three_pt_att_max += 0.06
                three_pt_made_max += 0.12
                
            #HEAT
            if tid == 1610612748:
                fg_att_max += 0.1
                fg_att_min+=0.04
                fg_made_max +=0.1
                free_throws_made_max += 0.13
                free_throws_made_min += 0.01
                free_throws_att_max += 0.14
                free_throws_att_min += 0.01
                three_pt_att_max += 0.13
                three_pt_att_min += 0.06
                three_pt_made_max += 0.13

            #THUNDER
            if tid == 1610612760:
                fg_att_max += 0.135
                fg_att_min += 0.055
                fg_made_max += 0.12
                fg_made_min += 0.06
                free_throws_made_max += 0.13
                free_throws_made_min += 0.06
                free_throws_att_max += 0.15
                free_throws_att_min += 0.05
                three_pt_att_min += 0.05
                three_pt_att_max += 0.14
                three_pt_made_min += 0.05
                three_pt_made_max += 0.15

            # PELICANS
            if tid == 1610612740:
                fg_att_max -= 0.1
                fg_att_min -= 0.05
                fg_made_max -= 0.06
                fg_made_min -= 0.04
                three_pt_att_min -= 0.05
                three_pt_att_max -= 0.1
                three_pt_made_min -= 0.03
                three_pt_made_max -= 0.1
            
            #NUGGETS
            if tid == 1610612743:
                free_throws_att_max += 0.15
                free_throws_made_max += 0.15
                three_pt_att_max += 0.12
                three_pt_made_max += 0.15
                fg_att_max += 0.1
                fg_att_min += 0.05
                fg_made_max += 0.1
                fg_made_min += 0.05
                free_throws_made_min += 0.05
                free_throws_att_min += 0.05
                three_pt_att_min += 0.05
                three_pt_made_min += 0.05
                
            #NETS
            if  tid == 1610612751:
                fg_att_max -= 0.1
                fg_att_min -= 0.05
                fg_made_max -= 0.05
                fg_made_min -= 0.05
                free_throws_made_max += 0.1
                free_throws_made_min += 0.05
                free_throws_att_max += 0.1
                free_throws_att_min += 0.05
                three_pt_att_min += 0.05
                three_pt_att_max += 0.05
                three_pt_made_min += 0.05
                three_pt_made_max += 0.1            
                
            #DALLAS
            if tid == 1610612742:
                fg_att_max += 0.01
                fg_att_min -= 0.04
                fg_made_max += 0.05
                fg_made_min += 0.02
                free_throws_att_max += 0.1
                free_throws_made_max += 0.1
                three_pt_att_max += 0.06
                three_pt_made_max += 0.12

            # MAGIC
            if tid == 1610612753:
                fg_att_max -=0.05
                fg_made_max -=0.06
                free_throws_att_min -=0.06
                free_throws_made_max -=0.06
                three_pt_att_max -=0.06
                three_pt_made_max -=0.06

            #CELTICS
            if tid == 1610612738:
                free_throws_att_max += 0.1
                free_throws_made_max += 0.1
                three_pt_att_max += 0.06
                three_pt_made_max += 0.12
                fg_att_max += 0.1
                fg_made_max += 0.1
            
            #Jazz
            if tid == 1610612762:
                fg_att_max += 0.03
                fg_att_min += 0.005
                fg_made_max += 0.012
                fg_made_min += 0.005
                free_throws_made_max += 0.02
                free_throws_att_max += 0.06
                

            #PLAYER MINUTES
            if player['minutes'] > 25:
                player_stat['min']=round(player['minutes']*random.uniform(0.88,1.25))
            elif player['minutes'] > 18:
                player_stat['min']=round(player['minutes']*random.uniform(0.75,1.35))
            elif player['minutes'] > 10:
                player_stat['min']=round(player['minutes']*random.uniform(0.7,1.2))
            else:
                player_stat['min']=round(player['minutes']*random.uniform(0.65,1.02))

            # BOUND CHECKING MINUTES
            if stats_copy['minutes'] >= player_stat['min']:
                stats_copy['minutes'] -= player_stat['min']
            else:
                player_stat['min'] = stats_copy['minutes'] if stats_copy['minutes'] > 0 else 0
                stats_copy['minutes']-=player_stat['min'] 
            
            if stats_copy['minutes'] < 6 and stats_copy['minutes'] > 0:
                player_stat['min'] += stats_copy['minutes']
                stats_copy['minutes'] -= stats_copy['minutes']
            
            # BOUND CHECKING
            if player_stat['min'] > 0:
                player_stat['assists']= round(player['assists_per_game']*random.uniform(assists_min,assists_max))
                if stats_copy['assists'] >= player_stat['assists']:
                    stats_copy['assists'] -= player_stat['assists']
                else:
                    player_stat['assists'] = stats_copy['assists'] if stats_copy['assists'] > 0 else 0
                    stats_copy['assists'] -= player_stat['assists']

                player_stat['off_rebounds']= round(player['offensive_rebounds_per_game']*random.uniform(off_rebound_min,off_rebound_max))
                if stats_copy['off_rebounds'] >= player_stat['off_rebounds']:
                    stats_copy['off_rebounds'] -= player_stat['off_rebounds']
                else:
                    player_stat['off_rebounds'] = stats_copy['off_rebounds'] if stats_copy['off_rebounds'] > 0 else 0
                    stats_copy['off_rebounds']-=player_stat['off_rebounds']
                
                player_stat['def_rebounds']= round(player['defensive_rebounds_per_game']*random.uniform(def_rebound_min,def_rebound_max))
                if stats_copy['def_rebounds'] >= player_stat['def_rebounds']:
                    stats_copy['def_rebounds'] -= player_stat['def_rebounds']
                else:
                    player_stat['def_rebounds'] = stats_copy['def_rebounds'] if stats_copy['def_rebounds'] > 0 else 0
                    stats_copy['def_rebounds']-=player_stat['def_rebounds']

                #player_stat['rebounds']=player_stat['defensive_rebounds']+player_stat['offensive_rebounds']

                player_stat['blocks']= round(player['blocks_per_game']*random.uniform(blocks_min,blocks_max))
                if stats_copy['blocks'] >= player_stat['blocks']:
                    stats_copy['blocks'] -= player_stat['blocks']
                else:
                    player_stat['blocks'] = stats_copy['blocks'] if stats_copy['blocks'] > 0 else 0
                    stats_copy['blocks']-=player_stat['blocks']

                player_stat['steals']= round(player['steals_per_game']*random.uniform(steal_min,steal_max))
                if stats_copy['steals'] >= player_stat['steals']:
                    stats_copy['steals'] -= player_stat['steals']
                else:
                    player_stat['steals'] = stats_copy['steals'] if stats_copy['steals'] > 0 else 0
                    stats_copy['steals']-=player_stat['steals']

                player_stat['turnovers']= round(player['turnovers_per_game']*random.uniform(turnovers_min,turnovers_max))
                if stats_copy['turnovers'] >= player_stat['turnovers']:
                    stats_copy['turnovers'] -= player_stat['turnovers']
                else:
                    player_stat['turnovers'] = stats_copy['turnovers'] if stats_copy['turnovers'] > 0 else 0
                    stats_copy['turnovers'] -= player_stat['turnovers']

                player_stat['personal_fouls']=round(player['personal_fouls_per_game']*random.uniform(personal_fouls_min,personal_fouls_max))
                if stats_copy['personal_fouls'] >= player_stat['personal_fouls']:
                    stats_copy['personal_fouls'] -= player_stat['personal_fouls']
                else:
                    player_stat['personal_fouls'] = stats_copy['personal_fouls'] if stats_copy['personal_fouls'] > 0 else 0
                    stats_copy['personal_fouls'] -= player_stat['personal_fouls']

                player_stat['FT_attempted']=round(player['free_throws_attempted_per_game']*random.uniform(free_throws_att_min,free_throws_att_max))
                if stats_copy['free_throws_attempted'] >= player_stat['FT_attempted']:
                    stats_copy['free_throws_attempted'] -= player_stat['FT_attempted']
                else:
                    player_stat['FT_attempted'] = stats_copy['free_throws_attempted'] if stats_copy['free_throws_attempted'] > 0 else 0
                    stats_copy['free_throws_attempted'] -= player_stat['FT_attempted']

                player_stat['FT_made']=round(player['free_throws_made_per_game']*random.uniform(free_throws_made_min,free_throws_made_max))
                if stats_copy['free_throws_made'] >= player_stat['FT_made']:
                    if player_stat['FT_attempted'] < player_stat['FT_made']:
                        player_stat['FT_made'] = player_stat['FT_attempted']
                    stats_copy['free_throws_made'] -= player_stat['FT_made']
                else:
                    if player_stat['FT_attempted'] >= player_stat['FT_made']:
                        player_stat['FT_made'] = stats_copy['free_throws_made'] if stats_copy['free_throws_made'] > 0 else 0
                        stats_copy['free_throws_made'] -= player_stat['FT_made']
                    else:
                        player_stat['FT_made'] = 0

                fg_att_weight = random.uniform(fg_att_min,fg_att_max)
                player_stat['3P_attempted']=round(player['three_point_attempted_per_game']*fg_att_weight)
                if stats_copy['three_point_attempted'] >= player_stat['3P_attempted']:
                    stats_copy['three_point_attempted'] -= player_stat['3P_attempted']
                else:
                    player_stat['3P_attempted'] = stats_copy['three_point_attempted'] if stats_copy['three_point_attempted'] > 0 else 0
                    stats_copy['three_point_attempted'] -= player_stat['3P_attempted']

                fg_made_weight = random.uniform(fg_made_min,fg_made_max)
                player_stat['3P_made']=round(player['three_point_made_per_game']*fg_made_weight)
                if stats_copy['three_point_made'] >= player_stat['3P_made'] and player_stat['3P_attempted'] >= player_stat['3P_made']:
                    stats_copy['three_point_made'] -= player_stat['3P_made']
                else:
                    if player_stat['3P_attempted'] >= player_stat['3P_made']:
                        player_stat['3P_made'] = stats_copy['three_point_made'] if stats_copy['free_throws_attempted'] > 0 else 0
                        stats_copy['three_point_made'] -= player_stat['3P_made'] 
                    else:
                        player_stat['3P_made'] = 0

                player_stat['FG_attempted']=round(player['field_goals_attempted_per_game']*fg_att_weight)-player_stat['3P_attempted']
                if stats_copy['field_goals_attempted'] >= player_stat['FG_attempted']:
                    stats_copy['field_goals_attempted'] -= player_stat['FG_attempted']
                else:
                    player_stat['FG_attempted'] = stats_copy['field_goals_attempted'] if stats_copy['field_goals_attempted'] > 0 else 0
                    stats_copy['field_goals_attempted'] -= player_stat['FG_attempted']


                player_stat['FG_made']=round(player['field_goals_made_per_game']*fg_made_weight)-player_stat['3P_made']
                if stats_copy['field_goals_made'] >= player_stat['FG_made'] and player_stat['FG_attempted'] >= player_stat['FG_made']:
                    stats_copy['field_goals_made'] -= player_stat['FG_made']
                else:
                    if player_stat['FG_attempted'] >= player_stat['FG_made']:
                        player_stat['FG_made'] = stats_copy['field_goals_made'] if stats_copy['field_goals_made'] > 0 else 0
                        stats_copy['field_goals_made'] -= player_stat['FG_made']
                    else:
                        player_stat['FG_made']=0

                player_stat['FG_attempted']+=player_stat['3P_attempted']
                player_stat['FG_made']+=player_stat['3P_made']

                if player_stat['3P_attempted'] > player_stat['FG_attempted']:
                    player_stat['FG_attempted'] = player_stat['3P_attempted']


                if player_stat['min'] < 22 and player_stat['min'] > 0:
                    if player_stat['assists'] > player_stat['min']/2.4:
                        player_stat['assists']=round(player_stat['assists']/2)
                    if player_stat['off_rebounds']+player_stat['def_rebounds'] > player_stat['min']/2.4:
                        player_stat['off_rebounds']=round(player_stat['off_rebounds']/2)
                    #if player_stat['def_rebounds'] > player_stat['min']/2:
                        player_stat['def_rebounds']=round(player_stat['def_rebounds']/2)
                        player_stat['rebounds']=player_stat['def_rebounds']+player_stat['off_rebounds']
                    
                    if player_stat['blocks'] > player_stat['min']/3:
                        player_stat['blocks']=round(player_stat['blocks']/3)
                    if player_stat['steals'] > player_stat['min']/3:
                        player_stat['steals']=round(player_stat['steals']/3)
                    if player_stat['turnovers'] > player_stat['min']/3:
                        player_stat['turnovers']=round(player_stat['turnovers']/3)
                    if player_stat['personal_fouls'] > player_stat['min']/3:
                        player_stat['personal_fouls']=round(player_stat['personal_fouls']/3)
                    if player_stat['FT_attempted'] > player_stat['min']/2:
                        player_stat['FT_attempted']=round(player_stat['FT_attempted']/2)
                    if player_stat['FT_made'] > player_stat['min']/2:
                        player_stat['FT_made']=round(player_stat['FT_made']/2)
                    if player_stat['3P_attempted'] > player_stat['min']/2.5:
                        #print('3POINT')
                        player_stat['3P_attempted']=round(player_stat['3P_attempted']/2.5)
                    #if player_stat['3P_made'] > player_stat['min']/2.5:
                        player_stat['3P_made']=round(player_stat['3P_made']/2.5)
                    if player_stat['FG_attempted'] > player_stat['min']/2.5:
                        #print('FGOAL')
                        player_stat['FG_attempted']=round(player_stat['FG_attempted']/2.5)
                        player_stat['FG_attempted']+=player_stat['3P_attempted']
                    #if player_stat['FG_made']+player_stat['3P_made'] > player_stat['min']/2.5:
                        player_stat['FG_made']=round(player_stat['FG_made']/2.5)
                        player_stat['FG_made']+=player_stat['3P_made']

                player_stat['comment']='OK'
                if player_stat['FG_attempted'] < player_stat['FG_made']:
                    player_stat['FG_attempted']=player_stat['FG_made']

                player_stat['points']=(player_stat['3P_made']*3) + ((player_stat['FG_made']-player_stat['3P_made'])*2) + player_stat['FT_made']
                player_stat['rebounds']=player_stat['off_rebounds']+player_stat['def_rebounds']
                '''if player['games_played'] > 5 and player['minutes']<10:
                    player_stat['minutes']=player['minutes']*random.uniform(0.3,0.5)
                else:
                    player_stat['minutes']=player['minutes']*random.uniform(0.9,1.1)'''
            else:
                player_stat['assists']=0
                player_stat['off_rebounds']=0
                player_stat['def_rebounds']=0
                player_stat['rebounds']=0
                player_stat['blocks']=0
                player_stat['steals']=0
                player_stat['turnovers']=0
                player_stat['personal_fouls']=0
                player_stat['FT_attempted']=0
                player_stat['FT_made']=0
                player_stat['FG_attempted']=0
                player_stat['FG_made']=0
                player_stat['3P_attempted']=0
                player_stat['3P_made']=0
                player_stat['points']=0
                player_stat['min']=0
                player_stat['comment']="NONE"

            team_stat['assists']+=player_stat['assists']
            team_stat['off_rebounds']+=player_stat['off_rebounds']
            team_stat['def_rebounds']+=player_stat['def_rebounds']
            team_stat['rebounds']+=(player_stat['off_rebounds']+player_stat['def_rebounds'])
            team_stat['blocks']+=player_stat['blocks']
            team_stat['steals']+=player_stat['steals']
            team_stat['turnovers']+=player_stat['turnovers']
            team_stat['personal_fouls']+=player_stat['personal_fouls']
            team_stat['FT_attempted']+=player_stat['FT_attempted']
            team_stat['FT_made']+=player_stat['FT_made']
            team_stat['FG_attempted']+=player_stat['FG_attempted']
            team_stat['FG_made']+=player_stat['FG_made']
            team_stat['3P_attempted']+=player_stat['3P_attempted']
            team_stat['3P_made']+=player_stat['3P_made']
            team_stat['points']+=player_stat['points']

            player_stats.append(player_stat)

    if team_stat['points']==other_team_score:
        team_stat['FT_made']+=1
        team_stat['FT_attempted']+=1
        player_stats[0]['FT_made']+=1
        player_stats[0]['FT_attempted']+=1
        team_stat['points']+=1

    #print()
    #pprint.pprint(player_stats)
    pprint.pprint(team_stat)

    return [player_stats,team_stat]



def compute_points_by_quarter(total_points_home, total_points_away, num_ots):
    overtime_scores_away=[]
    overtime_scores_home=[]
    if (num_ots>0):
        #for i in range(0,num_ots): --->>>#ONLY ONE OT I hardcoded it
        if total_points_home < total_points_away:
            home_score = random.randint(5,10)
            away_score = random.randint(1,5)+home_score
            overtime_scores_away.append(away_score)
            overtime_scores_home.append(home_score)
            total_points_away -= away_score
            total_points_home -= home_score
        else:
            away_score = random.randint(5,10)
            home_score = random.randint(1,5)+away_score
            overtime_scores_away.append(away_score)
            overtime_scores_home.append(home_score)
            total_points_away -= away_score
            total_points_home -= home_score

    basis_home = int(total_points_home/4)

    quarter_1_home = random.randint(basis_home-6,basis_home+6)
    quarter_2_home = random.randint(basis_home-6,basis_home+6)
    quarter_3_home = random.randint(basis_home-6,basis_home+6)
    quarter_4_home = total_points_home - (quarter_1_home + quarter_2_home + quarter_3_home)
    if quarter_4_home < 18:
        quarter_1_home -= 4
        quarter_2_home -= 4
        quarter_3_home -= 4
        quarter_4_home += 12
    elif quarter_4_home > 32:
        quarter_1_home += 4
        quarter_2_home += 4
        quarter_3_home += 4
        quarter_4_home -= 12

    basis_away = int(total_points_away/4)
    quarter_1_away = random.randint(basis_away-6,basis_away+6)
    quarter_2_away = random.randint(basis_away-6,basis_away+6)
    quarter_3_away = random.randint(basis_away-6,basis_away+6)
    quarter_4_away = total_points_away - (quarter_1_away + quarter_2_away + quarter_3_away)
    if quarter_4_away < 18:
        quarter_1_away -= 4
        quarter_2_away -= 4
        quarter_3_away -= 4
        quarter_4_away += 12
    elif quarter_4_away > 32:
        quarter_1_away += 4
        quarter_2_away += 4
        quarter_3_away += 4
        quarter_4_away -= 12

    if len(overtime_scores_home)>0:
        return  {
                    'home_scores':[[quarter_1_home,quarter_2_home,
                            quarter_3_home,quarter_4_home]+overtime_scores_home],
                    'away_scores':[[quarter_1_away,quarter_2_away,
                            quarter_3_away,quarter_4_away]+overtime_scores_away]
                }

    
    return  {
                'home_scores':[quarter_1_home,quarter_2_home,
                        quarter_3_home,quarter_4_home],
                'away_scores':[quarter_1_away,quarter_2_away,
                        quarter_3_away,quarter_4_away]
            }

def get_bias_home(team_id):
    team_list_dist = {
        1610612749:[0.96, 1.18, -4, 5, 0.9, 1.11, -5, 5.5, 0.9, 1.05, -5, 7, -4, 5, -2, 3, -4, 5, -3, 3, -2, 3, -2, 3, -3, 3, -3, 3, -10, 10],#MIL
        1610612747:[0.95, 1.16, -4, 5, 0.9, 1.12, -5, 5.4, 0.87, 1.02, -5, 7, -4, 5, -2, 4, -3, 6, -4, 5, -3, 4, -2, 3, -3, 3, -3, 3, -7, 7], #LAL
        1610612738:[0.9, 1.14, -4, 5, 0.87, 1.1, -5.2, 5.5, 0.9, 1.03, -5, 6, -4, 4, -2, 2, -3, 3, -4, 6, -2, 3, -2, 3, -3, 2, -3, 3, -7, 10],#BOS
        1610612751:[0.87, 1.12, -4, 4.3, 0.87, 1.1, -5.2, 5, 0.9, 1.02, -5, 5, -4, 5, -3, 4, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#BKN
        1610612742:[0.91, 1.16, -4, 5.4, 0.9, 1.13, -5, 6, 0.93, 1.02, -5, 6, -3, 5, -4, 5, -3, 5, -3, 6, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DAL
        1610612743:[0.9, 1.13, -4, 5.3, 0.88, 1.13, -5, 6, 0.91, 1.02, -5, 5, -3, 4, -4, 4, -3, 4, -3, 4, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DEN
        1610612745:[0.87, 1.17, -4, 5, 0.89, 1.17, -5, 7.3, 0.93, 1.02, -2, 4, -3, 4, -3, 4, -3, 4, -3, 5, -2, 4, -2, 2, -2, 4, -3, 3, -7, 12],#HOU
        1610612754:[0.9, 1.15, -4, 5.3, 0.88, 1.12, -5, 6.2, 0.9, 1.02, -4, 4, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#IND
        1610612746:[0.91, 1.16, -4, 5, 0.88, 1.12, -5, 6, 0.9, 1.02, -4, 4, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#LAC
        1610612748:[0.91, 1.16, -4, 5.3, 0.88, 1.15, -5, 5.8, 0.94, 1.02, -5, 5, -3, 4, -4, 5, -3, 4, -3, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIA
        1610612740:[0.85, 1.08, -4, 4.5, 0.83, 1.08, -5, 5, 0.91, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NOR
        1610612760:[0.89, 1.16, -4, 6, 0.88, 1.13, -5, 5, 0.9, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#OKC
        1610612753:[0.85, 1.1, -4, 4.2, 0.82, 1.08, -5, 5, 0.88, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#ORL
        1610612755:[0.93, 1.2, -4, 5, 0.87, 1.1, -5, 5, 0.9, 1.02, -4, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHI
        1610612761:[0.91, 1.17, -4, 5.2, 0.87, 1.12, -5, 6, 0.88, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#TOR
        1610612762:[0.9, 1.14, -4, 5.2, 0.87, 1.13, -5, 5.5, 0.88, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#UTA
    }
    return team_list_dist[team_id]

def get_bias_away(team_id):
    team_list_dist = {
        1610612749:[0.91, 1.15, -4, 5, 0.88, 1.11, -5, 5.5, 0.89, 1.05, -5, 7, -3, 5, -3, 4, -3, 4, -3, 3, -2, 2, -2, 3, -2, 1, -3, -3, -10, 10],#MIL
        1610612747:[0.9, 1.15, -4, 5, 0.88, 1.11, -5, 5.4, 0.86, 1.02, -5, 7, -4, 5, -2, 4, -3, 4, -4, 5, -3, 4, -2, 3, -1, 1, -3, 3, -7, 7], #LAL
        1610612738:[0.88, 1.12, -4, 5, 0.86, 1.1, -5.2, 5.5, 0.89, 1.03, -5, 5, -4, 4, -2, 2, -3, 3, -3, 5, -1, 3, -2, 3, -3, 2, -3, 3, -7, 10],#BOS
        1610612751:[0.86, 1.1, -4, 4.3, 0.85, 1.1, -5, 5, 0.89, 1.02, -5, 5, -3, 5, -4, 5, -3, 3, -3, 3, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#BKN
        1610612742:[0.89, 1.12, -4, 5.4, 0.87, 1.11, -5, 6, 0.92, 1.02, -5, 6, -3, 5, -4, 5, -3, 5, -3, 6, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DAL
        1610612743:[0.89, 1.1, -4, 5.3, 0.87, 1.11,-5, 6, 0.9, 1.02, -5, 5, -3, 4, -4, 4, -3, 4, -3, 4, -2, 3, -2, 3, -4, 3, -3, 3, -7, 12],#DEN
        1610612745:[0.86, 1.12, -4, 5, 0.9, 1.12, -5, 7.3, 0.92, 1.02, -4, 6, -3, 4, -3, 4, -3, 4, -3, 5, -2, 4, -2, 2, -2, 4, -3, 3, -7, 12],#HOU
        1610612754:[0.89, 1.12, -4, 5.3, 0.87, 1.11, -5, 6.2, 0.89, 1.02, -3, 3, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#IND
        1610612746:[0.9, 1.12, -4, 5, 0.87, 1.13, -5, 6, 0.89, 1.02, -3, 3, -3, 3, -3, 3, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 8],#LAC
        1610612748:[0.9, 1.13, -4, 5.3, 0.91, 1.12, -5, 5.8, 0.93, 1.02, -5, 5, -3, 4, -4, 5, -3, 4, -3, 4, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#MIA
        1610612740:[0.78, 1.06, -4, 4.5, 0.78, 1.06, -5, 5, 0.9, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#NOR
        1610612760:[0.88, 1.14, -4, 5, 0.88, 1.13, -5, 5, 0.89, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#OKC
        1610612753:[0.8, 1.1, -4, 4.2, 0.8, 1.1, -5, 5, 0.87, 1.02, -5, 5, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#ORL
        1610612755:[0.88, 1.12, -4, 5, 0.85, 1.1, -4, 4, 0.89, 1.02, -4, 4, -3, 4, -4, 3, -3, 3, -2, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#PHI
        1610612761:[0.9, 1.14, -4, 5.3, 0.88, 1.12, -5, 6, 0.88, 1.03, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#TOR
        1610612762:[0.89, 1.14, -4, 5.3, 0.88, 1.12, -5, 5.5, 0.87, 1.02, -5, 5, -4, 5, -4, 5, -3, 3, -3, 5, -2, 2, -2, 3, -4, 3, -3, 3, -7, 10],#UTA

    }
    return team_list_dist[team_id]


def get_team(team1):
    list_teams = {        
        "boston":1610612738,
        "brooklyn":1610612751,        
        "dallas":1610612742,
        "denver":1610612743,
        "houston":1610612745,
        "indiana":1610612754,
        "l.a. clippers":1610612746,
        "l.a. lakers":1610612747,        
        "miami":1610612748,
        'milwaukee':1610612749,        
        "new orleans":1610612740,       
        "oklahoma city":1610612760,
        "orlando":1610612753,
        "philadelphia":1610612755,        
        "toronto":1610612761,
        "utah":1610612762,   
    }

    return list_teams[team1]


if __name__ == "__main__":
    make_playoff_games()