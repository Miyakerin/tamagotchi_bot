# Generated by Django 5.0.3 on 2024-03-24 21:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0009_tguser_is_tamagotchi_renaming'),
    ]

    operations = [
        migrations.AddField(
            model_name='tamagotchi',
            name='happiness_deprivation',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tamagotchi',
            name='hunger_deprivation',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='tamagotchi',
            name='thirst_deprivation',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='happiness_deprivation',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='happiness_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 25, 0, 30, 43, 838957)),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='health_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 25, 0, 30, 43, 838957)),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='hunger_deprivation',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='hunger_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 25, 0, 30, 43, 838957)),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='thirst_deprivation',
            field=models.IntegerField(default=4),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='thirst_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 25, 0, 30, 43, 838957)),
        ),
    ]
