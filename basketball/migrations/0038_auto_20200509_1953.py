# Generated by Django 3.0.5 on 2020-05-10 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basketball', '0037_gamepreview_is_necessary'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamepreview',
            old_name='series_id',
            new_name='series',
        ),
    ]
