# Generated by Django 5.0.6 on 2024-05-09 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0019_rewardfortask_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='is_busy',
            field=models.BooleanField(default=False),
        ),
    ]
