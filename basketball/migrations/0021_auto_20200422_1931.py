# Generated by Django 3.0.5 on 2020-04-22 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0020_auto_20200422_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='conference_losses',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='conference_wins',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
