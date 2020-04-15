from django.db import models
from jsonfield import JSONField

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
    game_id = models.IntegerField(primary_key=True)
    winning_team_id = models.IntegerField(null=False)
    losing_team_id = models.IntegerField(null=False)
    home_team_score = models.IntegerField(null=False)
    away_team_score = models.IntegerField(null=False)
    top_scorer_home = models.IntegerField(null=False)
    top_scorer_away = models.IntegerField(null=False)
    attendance = models.IntegerField(null=False)
    date_time = models.DateTimeField(null=False)
    json = JSONField()

    def __str__(self):
        return str(self.game_id)

    

