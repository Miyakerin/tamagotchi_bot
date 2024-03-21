import random

from tg_bot.models import *


class Roll:
    rarity_ids = [1, 2, 3, 4]
    rarity_chances = [0.5, 0.3, 0.15, 0.05]

    element_ids = [1, 2, 3, 4, 5]
    element_chances = [0.2, 0.2, 0.2, 0.2, 0.2]

    def __init__(self):
        pass

    @staticmethod
    def roll_rarity(*args, **kwargs):  # метод для унифицированного ролла редкости
        rarity = Rarity.objects.filter(
            id=random.choices(Roll.rarity_ids, Roll.rarity_chances, k=1)[0]
        ).first()
        return rarity

    @staticmethod
    def roll_element(*args, **kwargs):  # метод для унифицированного рола элемента
        element = Element.objects.filter(
            id=random.choices(Roll.element_ids, Roll.element_chances, k=1)[0]
        ).first()
        return element

    @staticmethod
    def create_tamagotchi(*args, **kwargs):  # метод для унифицированного создания тамагочи
        rarity = Roll.roll_rarity()
        element = Roll.roll_element()
        tamagotchi = random.choice(Tamagotchi.objects.filter(element=element).filter(rarity=rarity))
        return tamagotchi
