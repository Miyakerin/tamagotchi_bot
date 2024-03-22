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


class ManageTamagotchi:
    def __init__(self):
        pass

    @staticmethod
    def set_pogonyalo(tamagotchi: TamagotchiInPossession, value: str):
        tamagotchi.pogonyalo = value
        tamagotchi.save(update_fields=['pogonyalo'])

    @staticmethod
    def set_hunger(tamagotchi: TamagotchiInPossession, value: int):
        tamagotchi.hunger = value
        tamagotchi.save(update_fields=['hunger'])

    @staticmethod
    def set_health(tamagotchi: TamagotchiInPossession, value: int):
        tamagotchi.health = value
        tamagotchi.save(update_fields=['health'])

    @staticmethod
    def set_thirst(tamagotchi: TamagotchiInPossession, value: int):
        tamagotchi.thirst = value
        tamagotchi.save(update_fields=['thirst'])

    @staticmethod
    def set_happiness(tamagotchi: TamagotchiInPossession, value: int):
        tamagotchi.happiness = value
        tamagotchi.save(update_fields=['happiness'])

    @staticmethod
    def update_hunger(tamagotchi: TamagotchiInPossession, value: int):
        max_hunger = tamagotchi.tamagotchi.max_hunger
        tamagotchi.hunger = max(value+tamagotchi.hunger, max_hunger)
        tamagotchi.save(update_fields=['hunger'])

    @staticmethod
    def update_health(tamagotchi: TamagotchiInPossession, value: int):
        max_health = tamagotchi.tamagotchi.max_health
        tamagotchi.health = max(value + tamagotchi.health, max_health)
        tamagotchi.save(update_fields=['health'])

    @staticmethod
    def update_thirst(tamagotchi: TamagotchiInPossession, value: int):
        max_thirst = tamagotchi.tamagotchi.max_thirst
        tamagotchi.thirst = max(value + tamagotchi.thirst, max_thirst)
        tamagotchi.save(update_fields=['thirst'])

    @staticmethod
    def update_happiness(tamagotchi: TamagotchiInPossession, value: int):
        max_happiness = tamagotchi.tamagotchi.max_happiness
        tamagotchi.happiness = max(value + tamagotchi.happiness, max_happiness)
        tamagotchi.save(update_fields=['happiness'])


class ManageUser:
    def __init__(self):
        pass

    @staticmethod
    def set_last_page(user: TgUser, value: str):
        user.last_page = value
        user.save(update_fields=['last_page'])

    @staticmethod
    def set_last_tamagotchi(user: TgUser, value: int):
        user.last_selected_tamagotchi = value
        user.save(update_fields=['last_selected_tamagotchi'])

