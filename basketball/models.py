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
    attendance = models.IntegerField(null=False)
    date = models.DateField(default=date.today)
    time = models.TimeField(default=None, null=True)
    home_team_record = models.CharField(max_length=10,null=False)
    away_team_record = models.CharField(max_length=10,null=False)
    data = JSONField()
    home_team_win_percentage_start = models.DecimalField(max_digits=4,decimal_places=3)
    away_team_win_percentage_start = models.DecimalField(max_digits=4,decimal_places=3)

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
    



    

