# Generated by Django 5.0.3 on 2024-03-24 21:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0010_tamagotchi_happiness_deprivation_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tamagotchiinpossession',
            name='happiness_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 24, 21, 37, 25, 457897, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tamagotchiinpossession',
            name='health_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 24, 21, 37, 25, 457897, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tamagotchiinpossession',
            name='hunger_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 24, 21, 37, 25, 457897, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='tamagotchiinpossession',
            name='thirst_update_time',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 24, 21, 37, 25, 457897, tzinfo=datetime.timezone.utc)),
        ),
    ]
