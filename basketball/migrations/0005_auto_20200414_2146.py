# Generated by Django 3.0.5 on 2020-04-14 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0004_auto_20200414_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='player_age',
            field=models.CharField(max_length=3),
        ),
    ]