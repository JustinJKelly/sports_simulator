# Generated by Django 3.0.5 on 2020-05-03 16:44

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0027_auto_20200428_0212'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_playoff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='playoff_type',
            field=models.CharField(default='No', max_length=4),
        ),
        migrations.AlterField(
            model_name='game',
            name='data',
            field=jsonfield.fields.JSONField(),
        ),
        migrations.AlterField(
            model_name='team',
            name='players',
            field=jsonfield.fields.JSONField(),
        ),
    ]