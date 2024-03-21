import uuid

from django.db import models
from django.contrib.auth.models import User


class TgUser(models.Model):
    telegram_user_id = models.BigIntegerField()
    telegram_chat_id = models.BigIntegerField()
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username


class Rarity(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Element(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    health_on_consume = models.IntegerField(default=0)
    hunger_on_consume = models.IntegerField(default=0)
    thirst_on_consume = models.IntegerField(default=0)
    happiness_on_consume = models.IntegerField(default=0)
    usable = models.BooleanField(default=False)
    consumable = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Tamagotchi(models.Model):
    name = models.CharField(max_length=50)
    pogonyalo = models.CharField(max_length=50)
    health = models.IntegerField(default=100)
    hunger = models.IntegerField(default=100)
    thirst = models.IntegerField(default=100)
    happiness = models.IntegerField(default=100)
    is_alive = models.BooleanField(default=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ItemInInventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item) + ": " + str(self.user_id)


class TamagotchiInPossession(models.Model):
    tamagotchi = models.ForeignKey(Tamagotchi, on_delete=models.CASCADE)
    user_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.tamagotchi) + ": " + str(self.user_id)
