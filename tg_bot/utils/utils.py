import random

from tg_bot.models import *
from telebot.types import *


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


class ManageInventory:
    def __init__(self):
        pass

    @staticmethod
    def set_quantity(item: ItemInInventory, value: int):
        item.quantity = value
        item.save(update_fields=['quantity'])

    @staticmethod
    def update_quantity(item: ItemInInventory, value: int):
        item.quantity += value
        if item.quantity >= 0:
            item.save(update_fields=['quantity'])
        else:
            item.delete()


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
    def set_is_alive(tamagotchi: TamagotchiInPossession, value: bool):
        tamagotchi.is_alive = value
        tamagotchi.save(update_fields=['is_alive'])

    @staticmethod
    def update_hunger(tamagotchi: TamagotchiInPossession, value: int):
        max_hunger = tamagotchi.tamagotchi.max_hunger
        tamagotchi.hunger = min(value+tamagotchi.hunger, max_hunger)
        tamagotchi.save(update_fields=['hunger'])

    @staticmethod
    def update_health(tamagotchi: TamagotchiInPossession, value: int):
        max_health = tamagotchi.tamagotchi.max_health
        tamagotchi.health = min(value+tamagotchi.health, max_health)
        tamagotchi.save(update_fields=['health'])

    @staticmethod
    def update_thirst(tamagotchi: TamagotchiInPossession, value: int):
        max_thirst = tamagotchi.tamagotchi.max_thirst
        tamagotchi.thirst = min(value+tamagotchi.thirst, max_thirst)
        tamagotchi.save(update_fields=['thirst'])

    @staticmethod
    def update_happiness(tamagotchi: TamagotchiInPossession, value: int):
        max_happiness = tamagotchi.tamagotchi.max_happiness
        tamagotchi.happiness = min(value+tamagotchi.happiness, max_happiness)
        tamagotchi.save(update_fields=['happiness'])


class ManageUser:
    def __init__(self):
        pass

    @staticmethod
    def set_telegram_user_id(user: TgUser, value: int):
        user.telegram_user_id = value
        user.save(update_fields=['telegram_user_id'])

    @staticmethod
    def set_username(user: TgUser, value: str):
        user.username = value
        user.save(update_fields=['username'])

    @staticmethod
    def set_last_message(user: TgUser, value: int):
        user.last_message = value
        user.save(update_fields=['last_message'])

    @staticmethod
    def set_last_page(user: TgUser, value: str):
        user.last_page = value
        user.save(update_fields=['last_page'])

    @staticmethod
    def set_max_tamagotchi(user: TgUser, value: int):
        user.max_tamagotchi = value
        user.save(update_fields=['max_tamagotchi'])

    @staticmethod
    def set_last_tamagotchi(user: TgUser, value: int):
        user.last_selected_tamagotchi = value
        user.save(update_fields=['last_selected_tamagotchi'])

    @staticmethod
    def set_is_tamagotchi_selected(user: TgUser, value: bool):
        user.is_tamagotchi_selected = value
        user.save(update_fields=['is_tamagotchi_selected'])

    @staticmethod
    def set_last_item_selected(user: TgUser, value: int):
        user.last_selected_item = value
        user.save(update_fields=['last_selected_item'])

    @staticmethod
    def set_is_item_selected(user: TgUser, value: bool):
        user.is_item_selected = value
        user.save(update_fields=['is_item_selected'])


class KeyBoardsTemplate:
    @staticmethod
    def main_reply():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Тамагочи', 'Инвентарь', 'Помощь')
        return markup

    @staticmethod
    def help_reply():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Назад')
        return markup

    # tamagotchi markups
    @staticmethod
    def tamagotchi_main_reply():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Посмотреть всех', 'Новый тамагочи', 'Назад')
        return markup

    @staticmethod
    def tamagotchi_show_all_inline(user_tamagotchis):
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(x.pogonyalo,
                                                       callback_data=f'{{"user_tamagotchi": {str(x.id)}}}'),
                        user_tamagotchis))
        return markup

    @staticmethod
    def tamagotchi_choose_one_reply(is_alive: bool):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        if is_alive:
            markup.add('Действия', 'Задачи', 'Назад')
        else:
            markup.add('Воскресить', 'Назад')
        return markup

    @staticmethod
    def action_reply():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*map(lambda x: str(x), Action.objects.all()), 'Назад')

        return markup

    @staticmethod
    def action_inline(user_inventory):
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(x.item.name,
                                                       callback_data=f'{{"user_item_use": {str(x.id)}}}'),
                        user_inventory))
        return markup

    # Inventory markups
    @staticmethod
    def inventory_main_reply():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Посмотреть инвентарь', 'Магазин', 'Назад')
        return markup

    @staticmethod
    def inventory_show_all_inline(user_inventory):
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(x.item.name,
                                                       callback_data=f'{{"user_item": {str(x.id)}}}'),
                        user_inventory))
        return markup

    @staticmethod
    def inventory_choose_one_reply():
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Удалить', 'Назад')
        return markup


class CallbackHandlers:
    @staticmethod
    def choose_tamagotchi(tamagotchi_id, user):
        ManageUser.set_last_page(user, 'tamagotchi_page')
        ManageUser.set_last_tamagotchi(user, tamagotchi_id)
        ManageUser.set_is_tamagotchi_selected(user, True)

        tamagotchi = TamagotchiInPossession.objects.filter(id=tamagotchi_id).first()

        message = f'Показатели:\n' \
                  f'Название - {tamagotchi.tamagotchi.name}\n' \
                  f'Погоняло - {tamagotchi.pogonyalo}\n' \
                  f'Редкость - {tamagotchi.tamagotchi.rarity}\n' \
                  f'Элемент - {tamagotchi.tamagotchi.element}\n' \
                  f'Здоровье - {tamagotchi.health}\\{tamagotchi.tamagotchi.max_health}\n' \
                  f'Голод - {tamagotchi.hunger}\\{tamagotchi.tamagotchi.max_hunger}\n' \
                  f'Жажда - {tamagotchi.thirst}\\{tamagotchi.tamagotchi.max_thirst}\n' \
                  f'Счастье - {tamagotchi.happiness}\\{tamagotchi.tamagotchi.max_happiness}'
        return message, tamagotchi.is_alive

    @staticmethod
    def choose_item(item_id, user):
        ManageUser.set_last_page(user, 'inventory_page')
        ManageUser.set_last_item_selected(user, item_id)
        ManageUser.set_is_item_selected(user, True)

        item = ItemInInventory.objects.filter(id=item_id).first()

        message = f'Показатели:\n' \
                  f'Название - {item.item.name}\n' \
                  f'Редкость - {item.item.rarity}\n' \
                  f'Количество - {item.quantity}\n'

        if item.item.health_on_consume > 0:
            message += f'Здоровья при использовании - {item.item.health_on_consume}\n'
        if item.item.hunger_on_consume > 0:
            message += f'Голода при использовании - {item.item.hunger_on_consume}\n'
        if item.item.thirst_on_consume > 0:
            message += f'Жажды при использовании - {item.item.thirst_on_consume}\n'
        if item.item.happiness_on_consume > 0:
            message += f'Счастья при использовании - {item.item.happiness_on_consume}\n'

        return message

    @staticmethod
    def use_item(item_id, user: TgUser):
        item = ItemInInventory.objects.filter(id=item_id).first()
        tamagotchi = TamagotchiInPossession.objects.filter(id=user.last_selected_tamagotchi).first()
        if not user.is_tamagotchi_selected or not tamagotchi:
            return None

        if item.item.happiness_on_consume > 0:
            ManageTamagotchi.update_happiness(tamagotchi, item.item.happiness_on_consume)
        if item.item.thirst_on_consume > 0:
            ManageTamagotchi.update_thirst(tamagotchi, item.item.thirst_on_consume)
        if item.item.hunger_on_consume > 0:
            ManageTamagotchi.update_hunger(tamagotchi, item.item.hunger_on_consume)
        if item.item.health_on_consume > 0:
            ManageTamagotchi.update_health(tamagotchi, item.item.health_on_consume)

        if item.item.consumable:
            ManageInventory.update_quantity(item, -1)



