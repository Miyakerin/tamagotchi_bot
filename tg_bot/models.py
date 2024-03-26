from django.db import models
from django.contrib.auth.models import User


class TgUser(models.Model):
    telegram_user_id = models.BigIntegerField(default=-1)
    username = models.CharField(max_length=50)

    last_message = models.BigIntegerField(default=-1)
    last_page = models.CharField(max_length=50, default='main')
    max_tamagotchi = models.IntegerField(default=1)
    last_selected_tamagotchi = models.IntegerField(default='-1')
    is_tamagotchi_selected = models.BooleanField(default=False)
    last_selected_item = models.IntegerField(default='-1')
    is_item_selected = models.BooleanField(default=False)

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
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)
    max_health = models.IntegerField(default=100)
    max_hunger = models.IntegerField(default=100)
    max_thirst = models.IntegerField(default=100)
    max_happiness = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class Action(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)


class Task(models.Model):
    name = models.CharField(max_length=50)
    time_need_minutes = models.IntegerField(default=0)

    def __str__(self):
        return str(self.name)


class ItemsForAction(models.Model):
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.action}: {self.item}'


class RewardForTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task}: {self.item}'


class ItemInInventory(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return str(self.item) + ": " + str(self.quantity)

    def __repr__(self):
        return str(self.item) + ": " + str(self.user_id)


class TamagotchiInPossession(models.Model):
    tamagotchi = models.ForeignKey(Tamagotchi, on_delete=models.CASCADE)
    user_id = models.ForeignKey(TgUser, on_delete=models.CASCADE)
    pogonyalo = models.CharField(max_length=50, default="Null")
    health = models.IntegerField(default=100)
    hunger = models.IntegerField(default=100)
    thirst = models.IntegerField(default=100)
    happiness = models.IntegerField(default=100)
    is_alive = models.BooleanField(default=True)

    def __str__(self):
        return self.pogonyalo

    def __repr__(self):
        return str(self.tamagotchi) + ": " + str(self.user_id)
