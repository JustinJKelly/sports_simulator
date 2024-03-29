# Generated by Django 3.0.5 on 2020-04-11 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('full_name', models.CharField(max_length=100)),
                ('player_id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('point_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('assists_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('rebounds_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('blocks_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('steals_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('turnovers_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('personal_fouls_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('free_throw_percentage', models.DecimalField(decimal_places=1, max_digits=5)),
                ('field_goal_percentage', models.DecimalField(decimal_places=1, max_digits=5)),
                ('minutes_per_game', models.DecimalField(decimal_places=1, max_digits=5)),
                ('three_point_percentage', models.DecimalField(decimal_places=1, max_digits=5)),
                ('games_played', models.IntegerField()),
                ('team_id', models.IntegerField()),
            ],
        ),
    ]
