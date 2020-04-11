from django.db import models

# Create your models here.

#all stats are for 2019-2020 season
class Player(models.Model):
    full_name = models.CharField(max_length=100,null=False)
    player_id = models.CharField(max_length=20,primary_key=True)
    point_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    assists_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    rebounds_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    blocks_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    steals_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    turnovers_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    personal_fouls_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    free_throw_percentage = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    field_goal_percentage = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    minutes_per_game = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    three_point_percentage = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    games_played = models.IntegerField()
    team_id = models.IntegerField()

    def __str__(self):
        return self.full_name

    

