# Generated by Django 3.0.5 on 2020-04-22 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0021_auto_20200422_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='opponent_points_total',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]