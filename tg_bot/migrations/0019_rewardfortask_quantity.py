# Generated by Django 5.0.6 on 2024-05-09 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tg_bot', '0018_tguser_is_item_selected_tguser_last_selected_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='rewardfortask',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
