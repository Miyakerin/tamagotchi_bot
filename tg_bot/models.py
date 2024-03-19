from django.db import models
from django.contrib.auth.models import User

class Rarity(models.Model):
    name = models.CharField(max_length=50)
    rarity = models.IntegerField()
    def __str__(self):
        return self.name

class Element(models.Model):
    name = models.CharField(max_length=50)
    element = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=50)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    health_on_consume = models.IntegerField(default=0)
    hunger_on_consume = models.IntegerField(default=0)
    thirst_on_consume = models.IntegerField(default=0)
    happiness_on_consume = models.IntegerField(default=0)
    usable = models.BooleanField(default=False)
    consumable = models.BooleanField(default=False)


    def __str__(self):
        return self.name

class Tamagochi(models.Model):
    name = models.CharField(max_length=50)
    pogonyalo = models.CharField(max_length=50)
    health = models.IntegerField()
    hunger = models.IntegerField()
    thirst = models.IntegerField()
    happiness = models.IntegerField()
    is_alive = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rarity = models.ForeignKey(Rarity, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

