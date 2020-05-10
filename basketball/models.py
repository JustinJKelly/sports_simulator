from django.db import models
from jsonfield import JSONField
from datetime import date

#all stats are for 2019-2020 season
class Player(models.Model):
    full_name = models.CharField(max_length=100,null=False)
    player_id = models.IntegerField(primary_key=True)
    position = models.CharField(max_length=20,null=False)
    height = models.CharField(max_length=20,null=False)
    weight = models.CharField(max_length=4,null=False)
    jersey_number = models.CharField(max_length=20,null=False)
    player_age = models.CharField(max_length=3,null=False)
    team_name = models.CharField(max_length=50,null=False)
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
    minutes_total = models.IntegerField(null=False)
    three_point_made = models.IntegerField(null=False)
    three_point_attempted = models.IntegerField(null=False)
    field_goals_made = models.IntegerField(null=False)
    field_goals_attempted = models.IntegerField(null=False)
    games_played = models.IntegerField(null=False)
    team_id = models.IntegerField(null=False)
    is_starter = models.BooleanField(default=False)
    is_injured = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


class Game(models.Model):
    home_team = models.IntegerField(null=False)
    away_team = models.IntegerField(null=False)
    home_team_name = models.CharField(max_length=35,null=False)
    away_team_name = models.CharField(max_length=35,null=False)
    game_id = models.IntegerField(primary_key=True)
    winning_team_id = models.IntegerField(null=False)
    winner_name = models.CharField(max_length=35,null=False)
    loser_name = models.CharField(max_length=35,null=False)
    losing_team_id = models.IntegerField(null=False)
    home_team_score = models.IntegerField(null=False)
    away_team_score = models.IntegerField(null=False)
    top_scorer_home_points = models.IntegerField(null=False)
    top_scorer_away_points = models.IntegerField(null=False)
    top_scorer_home = models.IntegerField(null=False)
    top_scorer_away = models.IntegerField(null=False)
    attendance = models.IntegerField(null=False,default=0)
    date = models.DateField(default=date.today)
    time = models.TimeField(default=None, null=True)
    home_team_record = models.CharField(max_length=10,null=False)
    away_team_record = models.CharField(max_length=10,null=False)
    data = JSONField()
    home_team_win_percentage_start = models.DecimalField(max_digits=4,decimal_places=3,default=0.0)
    away_team_win_percentage_start = models.DecimalField(max_digits=4,decimal_places=3,default=0.0)
    is_playoff = models.BooleanField(default=False)
    playoff_type = models.CharField(max_length=4,default='No') #QF=Quarter Finals, SF=Semi Finals, CF= Conference Finals, F = Finals
    is_simulated = models.BooleanField(default=False)

    def __str__(self):
        return '%s @ %s %s' % (self.home_team_name,self.away_team_name, self.date) 

class GameLog(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
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
    off_rebounds = models.IntegerField(null=False,default=0)
    def_rebounds = models.IntegerField(null=False,default=0)
    rebounds = models.IntegerField(null=False,default=0)
    assists = models.IntegerField(null=False,default=0)
    steals = models.IntegerField(null=False,default=0)
    blocks = models.IntegerField(null=False,default=0)
    turnovers = models.IntegerField(null=False,default=0)
    personal_fouls = models.IntegerField(null=False,default=0)
    points = models.IntegerField(null=False,default=0)

class Team(models.Model):
    team_name = models.CharField(max_length=40,null=False)
    team_abv = models.CharField(max_length=5,null=False)
    team_wins = models.IntegerField(null=False)
    team_losses = models.IntegerField(null=False)
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
    team_id = models.IntegerField(primary_key=True)
    players = JSONField()
    home_wins = models.IntegerField(null=False)
    away_wins = models.IntegerField(null=False)
    home_losses = models.IntegerField(null=False)
    away_losses = models.IntegerField(null=False)
    conference_wins = models.IntegerField(null=False)
    conference_losses = models.IntegerField(null=False)
    opponent_points_total = models.IntegerField(null=False)
    divisional_wins = models.IntegerField(null=False)
    divisional_losses = models.IntegerField(null=False)

    def __str__(self):
        return str(self.team_name)

'''class MVPPoll(models.Model):
    data = JSONField()
    def __str__(self):
        return "MVP Poll"'''


class MVPPoll(models.Model):
    data = JSONField()
    
    def __str__(self):
        return self.player.full_name



class MVPVote(models.Model):
    player_id = models.IntegerField(null=False)
    player_name = models.CharField(null=False,max_length=40)
    team_abv = models.CharField(null=False,max_length=4)
    votes = models.IntegerField(default=0)
    points_pg = models.IntegerField(default=0)
    
    def __str__(self):
        return self.player_name

class Serie(models.Model):
    votes_higher_seed = models.IntegerField(default=0)
    votes_lower_seed = models.IntegerField(default=0)
    higher_seed_id = models.IntegerField(null=False)
    lower_seed_id = models.IntegerField(null=False)
    higher_seed_name = models.CharField(max_length=35,null=False)
    lower_seed_name = models.CharField(max_length=35,null=False)
    higher_seed_abv = models.CharField(max_length=4,default='')
    lower_seed_abv = models.CharField(max_length=4,default='')
    higher_seed_wins = models.IntegerField(default=0)
    lower_seed_wins = models.IntegerField(default=0)
    higher_seed_loses = models.IntegerField(default=0)
    lower_seed_loses = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    playoff_type = models.CharField(max_length=35,null=False) #Quarter=QF,Semi=S,Conference=C,Finals=F
    game_ids = JSONField() #holds ids of games played
    series_id = models.IntegerField(primary_key=True)
    current = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s vs. %s' % (self.lower_seed_name, self.higher_seed_name)
    


class GamePreview(models.Model):
    game_date = models.DateField(default=date.today)
    home_team_id = models.IntegerField(null=False)
    away_team_id = models.IntegerField(null=False)
    higher_seeding_id = models.IntegerField(null=False)
    lower_seeding_id = models.IntegerField(null=False)
    higher_seeding_name = models.CharField(max_length=35,null=False)
    lower_seeding_name = models.CharField(max_length=35,null=False)
    home_team_name = models.CharField(max_length=35,null=False)
    away_team_name = models.CharField(max_length=35,null=False)
    game_preview_id = models.IntegerField(primary_key=True)
    votes_home_team = models.IntegerField(default=0)
    votes_home_away = models.IntegerField(default=0)
    series = models.ForeignKey(Serie, on_delete=models.CASCADE)
    is_necessary = models.BooleanField(default=True)
    game_number = models.IntegerField(null=False)
    
    def __str__(self):
        return '%s vs. %s Game %d' % (self.lower_seeding_name, self.higher_seeding_name, self.game_number)
    




    

