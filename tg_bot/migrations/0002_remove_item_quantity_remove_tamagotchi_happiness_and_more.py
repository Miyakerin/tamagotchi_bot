# Generated by Django 5.0.3 on 2024-03-21 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='tamagotchi',
            name='happiness',
        ),
        migrations.RemoveField(
            model_name='tamagotchi',
            name='health',
        ),
        migrations.RemoveField(
            model_name='tamagotchi',
            name='hunger',
        ),
        migrations.RemoveField(
            model_name='tamagotchi',
            name='is_alive',
        ),
        migrations.RemoveField(
            model_name='tamagotchi',
            name='pogonyalo',
        ),
        migrations.RemoveField(
            model_name='tamagotchi',
            name='thirst',
        ),
        migrations.AddField(
            model_name='itemininventory',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='happiness',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='health',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='hunger',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='is_alive',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='pogonyalo',
            field=models.CharField(default='Null', max_length=50),
        ),
        migrations.AddField(
            model_name='tamagotchiinpossession',
            name='thirst',
            field=models.IntegerField(default=100),
        ),
    ]
