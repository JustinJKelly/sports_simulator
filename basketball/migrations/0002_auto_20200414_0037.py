# Generated by Django 3.0.5 on 2020-04-14 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='assists_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='blocks_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='field_goal_percentage',
        ),
        migrations.RemoveField(
            model_name='player',
            name='free_throw_percentage',
        ),
        migrations.RemoveField(
            model_name='player',
            name='minutes_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='personal_fouls_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='point_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='rebounds_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='steals_per_game',
        ),
        migrations.RemoveField(
            model_name='player',
            name='three_point_percentage',
        ),
        migrations.RemoveField(
            model_name='player',
            name='turnovers_per_game',
        ),
        migrations.AddField(
            model_name='player',
            name='assists_total',
            field=models.IntegerField(default='0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='blocks_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='field_goals_attempted',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='field_goals_made',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='free_throws_attempted',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='free_throws_made',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='minutes_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='personal_fouls_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='points_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='rebounds_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='steals_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='three_point_attempted',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='three_point_made',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='player',
            name='turnovers_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
