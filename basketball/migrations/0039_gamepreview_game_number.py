# Generated by Django 3.0.5 on 2020-05-10 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0038_auto_20200509_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamepreview',
            name='game_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
