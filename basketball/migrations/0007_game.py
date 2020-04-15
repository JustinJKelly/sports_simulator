# Generated by Django 3.0.5 on 2020-04-15 02:09

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0006_auto_20200414_2253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('home_team', models.IntegerField()),
                ('away_team', models.IntegerField()),
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
                ('winning_team_id', models.IntegerField()),
                ('losing_team_id', models.IntegerField()),
                ('home_team_score', models.IntegerField()),
                ('away_team_score', models.IntegerField()),
                ('top_scorer_home', models.IntegerField()),
                ('top_scorer_away', models.IntegerField()),
                ('attendance', models.IntegerField()),
                ('date_time', models.DateTimeField()),
                ('json', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
    ]