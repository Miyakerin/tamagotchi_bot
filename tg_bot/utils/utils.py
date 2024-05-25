import random

from tg_bot.models import *
from telebot.types import *


class Roll:
    '''Класс для ролла редкости, элемента и тамагочи'''
    rarity_ids = [1, 2, 3, 4]
    rarity_chances = [0.5, 0.3, 0.15, 0.05]

    element_ids = [1, 2, 3, 4, 5]
    element_chances = [0.2, 0.2, 0.2, 0.2, 0.2]

    def __init__(self):
        pass

    @staticmethod
    def roll_rarity(*args, **kwargs):  # метод для унифицированного ролла редкости
        '''Метод для ролла редкости'''
        rarity = Rarity.objects.filter(
            id=random.choices(Roll.rarity_ids, Roll.rarity_chances, k=1)[0]
        ).first()
        return rarity

    @staticmethod
    def roll_element(*args, **kwargs):  # метод для унифицированного рола элемента
        '''Метод для ролла элемента'''
        element = Element.objects.filter(
            id=random.choices(Roll.element_ids, Roll.element_chances, k=1)[0]
        ).first()
        return element

    @staticmethod
    def create_tamagotchi(*args, **kwargs):  # метод для унифицированного создания тамагочи
        '''Метод для создания тамагочи'''
        rarity = Roll.roll_rarity()
        element = Roll.roll_element()
        tamagotchi = random.choice(Tamagotchi.objects.filter(element=element).filter(rarity=rarity))
        return tamagotchi


class ManageInventory:
    '''Класс для управления инвентарем'''
    def __init__(self):
        pass

    @staticmethod
    def set_quantity(item: ItemInInventory, value: int):
        '''Метод для установки количества предмета в инвентаре'''
        item.quantity = value
        item.save(update_fields=['quantity'])

    @staticmethod
    def update_quantity(item: ItemInInventory, value: int):
        '''Метод для обновления количества предмета в инвентаре'''
        item.quantity += value
        if item.quantity >= 0:
            item.save(update_fields=['quantity'])
        else:
            item.delete()

    @staticmethod
    def check_if_item_in_inventory(item: Item, user: TgUser):
        '''Метод для проверки наличия предмета в инвентаре'''
        if ItemInInventory.objects.filter(user_id=user).filter(item=item).exists():
            return ItemInInventory.objects.filter(user_id=user).filter(item=item).first()
        else:
            return False


class ManageTamagotchi:
    '''Класс для управления тамагочи'''

    def __init__(self):
        pass

    @staticmethod
    def set_pogonyalo(tamagotchi: TamagotchiInPossession, value: str):
        '''Метод для установки погоняла тамагочи'''
        tamagotchi.pogonyalo = value
        tamagotchi.save(update_fields=['pogonyalo'])

    @staticmethod
    def set_hunger(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для установки голода тамагочи'''
        tamagotchi.hunger = value
        tamagotchi.save(update_fields=['hunger'])

    @staticmethod
    def set_health(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для установки здоровья тамагочи'''
        tamagotchi.health = value
        tamagotchi.save(update_fields=['health'])

    @staticmethod
    def set_thirst(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для установки жажды тамагочи'''
        tamagotchi.thirst = value
        tamagotchi.save(update_fields=['thirst'])

    @staticmethod
    def set_happiness(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для установки счастья тамагочи'''
        tamagotchi.happiness = value
        tamagotchi.save(update_fields=['happiness'])

    @staticmethod
    def set_is_alive(tamagotchi: TamagotchiInPossession, value: bool):
        '''Метод для установки жив ли тамагочи'''
        tamagotchi.is_alive = value
        tamagotchi.save(update_fields=['is_alive'])

    @staticmethod
    def set_is_busy(tamagotchi: TamagotchiInPossession, value: bool):
        '''Метод для установки занят ли тамагочи'''
        tamagotchi.is_busy = value
        tamagotchi.save(update_fields=['is_busy'])

    @staticmethod
    def update_hunger(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для обновления голода тамагочи'''
        max_hunger = tamagotchi.tamagotchi.max_hunger
        value = min(value+tamagotchi.hunger, max_hunger)
        value = 0 if value < 0 else value
        tamagotchi.hunger = value
        tamagotchi.save(update_fields=['hunger'])

    @staticmethod
    def update_health(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для обновления здоровья тамагочи'''
        max_health = tamagotchi.tamagotchi.max_health
        value = min(value+tamagotchi.health, max_health)
        value = 0 if value < 0 else value
        tamagotchi.health = value
        tamagotchi.save(update_fields=['health'])

    @staticmethod
    def update_thirst(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для обновления жажды тамагочи'''
        max_thirst = tamagotchi.tamagotchi.max_thirst
        value = min(value+tamagotchi.thirst, max_thirst)
        value = 0 if value < 0 else value
        tamagotchi.thirst = value
        tamagotchi.save(update_fields=['thirst'])

    @staticmethod
    def update_happiness(tamagotchi: TamagotchiInPossession, value: int):
        '''Метод для обновления счастья тамагочи'''
        max_happiness = tamagotchi.tamagotchi.max_happiness
        value = min(value+tamagotchi.happiness, max_happiness)
        value = 0 if value < 0 else value
        tamagotchi.happiness = value
        tamagotchi.save(update_fields=['happiness'])

    @staticmethod
    def set_task_started_at(tamagotchi: TamagotchiInPossession, value: datetime):
        '''Метод для установки времени начала задачи тамагочи'''
        tamagotchi.task_started_at = value
        tamagotchi.save(update_fields=['task_started_at'])

    @staticmethod
    def set_current_task(tamagotchi: TamagotchiInPossession, value: Task):
        '''Метод для установки текущей задачи тамагочи'''
        tamagotchi.current_task = value
        tamagotchi.save(update_fields=['current_task'])

    @staticmethod
    def update_stats(tamagotchi: TamagotchiInPossession):
        '''Метод для обновления статистики тамагочи'''
        current_time = datetime.now(tz=timezone.utc)
        hours_passed = int((current_time - tamagotchi.stats_update_time).total_seconds() / 3600)
        if hours_passed > 0:
            ManageTamagotchi.update_happiness(tamagotchi, -tamagotchi.happiness_drop_rate_per_hour*hours_passed)
            ManageTamagotchi.update_hunger(tamagotchi, -tamagotchi.hunger_drop_rate_per_hour*hours_passed)
            ManageTamagotchi.update_thirst(tamagotchi, -tamagotchi.thirst_drop_rate_per_hour*hours_passed)

            if tamagotchi.hunger == 0 or tamagotchi.thirst == 0 or tamagotchi.happiness == 0:
                ManageTamagotchi.update_health(tamagotchi, -tamagotchi.health_drop_rate_per_hour*hours_passed)
                if tamagotchi.health == 0:
                    tamagotchi.is_alive = False
            tamagotchi.stats_update_time = current_time
            tamagotchi.save()





class ManageUser:
    """
    Класс для управления пользователями.
    """

    def __init__(self):
        pass

    @staticmethod
    def set_telegram_user_id(user: TgUser, value: int):
        """
        Устанавливает и сохраняет идентификатор пользователя Telegram.

        Args:
            user (TgUser): Объект пользователя.
            value (int): Идентификатор пользователя Telegram.
        """
        user.telegram_user_id = value
        user.save(update_fields=['telegram_user_id'])

    @staticmethod
    def set_username(user: TgUser, value: str):
        """
        Устанавливает и сохраняет имя пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (str): Имя пользователя.
        """
        user.username = value
        user.save(update_fields=['username'])

    @staticmethod
    def set_last_message(user: TgUser, value: int):
        """
        Устанавливает и сохраняет последнее сообщение пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (int): Идентификатор последнего сообщения.
        """
        user.last_message = value
        user.save(update_fields=['last_message'])

    @staticmethod
    def set_last_page(user: TgUser, value: str):
        """
        Устанавливает и сохраняет последнюю страницу пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (str): Название последней страницы.
        """
        user.last_page = value
        user.save(update_fields=['last_page'])

    @staticmethod
    def set_max_tamagotchi(user: TgUser, value: int):
        """
        Устанавливает и сохраняет максимальное количество тамагочи у пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (int): Максимальное количество тамагочи.
        """
        user.max_tamagotchi = value
        user.save(update_fields=['max_tamagotchi'])

    @staticmethod
    def set_last_tamagotchi(user: TgUser, value: int):
        """
        Устанавливает и сохраняет последнее выбранное тамагочи пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (int): Идентификатор последнего выбранного тамагочи.
        """
        user.last_selected_tamagotchi = value
        user.save(update_fields=['last_selected_tamagotchi'])

    @staticmethod
    def set_is_tamagotchi_selected(user: TgUser, value: bool):
        """
        Устанавливает и сохраняет флаг выбранного тамагочи пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (bool): Флаг выбранного тамагочи.
        """
        user.is_tamagotchi_selected = value
        user.save(update_fields=['is_tamagotchi_selected'])

    @staticmethod
    def set_last_item_selected(user: TgUser, value: int):
        """
        Устанавливает и сохраняет последний выбранный предмет пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (int): Идентификатор последнего выбранного предмета.
        """
        user.last_selected_item = value
        user.save(update_fields=['last_selected_item'])

    @staticmethod
    def set_is_item_selected(user: TgUser, value: bool):
        """
        Устанавливает и сохраняет флаг выбранного предмета пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (bool): Флаг выбранного предмета.
        """
        user.is_item_selected = value
        user.save(update_fields=['is_item_selected'])

    @staticmethod
    def set_last_task(user: TgUser, value: int):
        """
        Устанавливает и сохраняет последнюю выбранную задачу пользователя.

        Args:
            user (TgUser): Объект пользователя.
            value (int): Идентификатор последней выбранной задачи.
        """
        user.last_selected_task = value
        user.save(update_fields=['last_selected_task'])

    @staticmethod
    def update_all_tamagotchis(user: TgUser):
        """
        Обновляет статистику всех тамагочи пользователя.

        Args:
            user (TgUser): Объект пользователя.
        """
        user_tamagotchis = TamagotchiInPossession.objects.filter(user_id=user)
        for tamagotchi in user_tamagotchis:
            ManageTamagotchi.update_stats(tamagotchi)


class KeyBoardsTemplate:
    """
    Класс для создания различных клавиатурных шаблонов.

    Методы:
        main_reply: Возвращает клавиатуру главного меню.
        help_reply: Возвращает клавиатуру для раздела "Помощь".
        tamagotchi_main_reply: Возвращает клавиатуру для раздела "Тамагочи".
        tamagotchi_show_all_inline: Возвращает встроенную клавиатуру для выбора тамагочи.
        tamagotchi_choose_one_reply: Возвращает клавиатуру для выбора действий с тамагочи.
        action_reply: Возвращает клавиатуру для выбора действия.
        action_inline: Возвращает встроенную клавиатуру для выбора предмета из инвентаря.
        inventory_main_reply: Возвращает клавиатуру для раздела "Инвентарь".
        inventory_show_all_inline: Возвращает встроенную клавиатуру для выбора предмета из инвентаря.
        inventory_choose_one_reply: Возвращает клавиатуру для выбора действий с предметом.
        tasks_reply: Возвращает встроенную клавиатуру для выбора задачи.
        choose_task_reply: Возвращает клавиатуру для выбора задачи.
    """

    @staticmethod
    def main_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру главного меню.

        Returns:
            ReplyKeyboardMarkup: Клавиатура главного меню.
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Тамагочи', 'Инвентарь', 'Помощь')
        return markup

    @staticmethod
    def help_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для раздела "Помощь".

        Returns:
            ReplyKeyboardMarkup: Клавиатура для раздела "Помощь".
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Назад')
        return markup

    # tamagotchi markups
    @staticmethod
    def tamagotchi_main_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для раздела "Тамагочи".

        Returns:
            ReplyKeyboardMarkup: Клавиатура для раздела "Тамагочи".
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Посмотреть всех', 'Новый тамагочи', 'Назад')
        return markup

    @staticmethod
    def tamagotchi_show_all_inline(user_tamagotchis) -> InlineKeyboardMarkup:
        """
        Возвращает встроенную клавиатуру для выбора тамагочи.

        Args:
            user_tamagotchis: Список тамагочи пользователя.

        Returns:
            InlineKeyboardMarkup: Встроенная клавиатура для выбора тамагочи.
        """
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(x.pogonyalo,
                                                       callback_data=f'{{"user_tamagotchi": {str(x.id)}}}'),
                        user_tamagotchis))
        return markup

    @staticmethod
    def tamagotchi_choose_one_reply(is_alive: bool) -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для выбора действий с тамагочи.

        Args:
            is_alive (bool): Флаг, указывающий, живо ли тамагочи.

        Returns:
            ReplyKeyboardMarkup: Клавиатура для выбора действий с тамагочи.
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        if is_alive:
            markup.add('Действия', 'Задачи', 'Назад')
        else:
            markup.add('Воскресить', 'Назад')
        return markup

    @staticmethod
    def action_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для выбора действия.

        Returns:
            ReplyKeyboardMarkup: Клавиатура для выбора действия.
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*map(lambda x: str(x), Action.objects.all()), 'Назад')

        return markup

    @staticmethod
    def action_inline(user_inventory) -> InlineKeyboardMarkup:
        """
        Возвращает встроенную клавиатуру для выбора предмета из инвентаря.

        Args:
            user_inventory: Список предметов в инвентаре пользователя.

        Returns:
            InlineKeyboardMarkup: Встроенная клавиатура для выбора предмета из инвентаря.
        """
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(x.item.name,
                                                       callback_data=f'{{"user_item_use": {str(x.id)}}}'),
                        user_inventory))
        return markup

    # Inventory markups
    @staticmethod
    def inventory_main_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для раздела "Инвентарь".

        Returns:
            ReplyKeyboardMarkup: Клавиатура для раздела "Инвентарь".
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Посмотреть инвентарь', 'Магазин', 'Забрать награды', 'Назад')
        return markup

    @staticmethod
    def inventory_show_all_inline(user_inventory) -> InlineKeyboardMarkup:
        """
        Возвращает встроенную клавиатуру для выбора предмета из инвентаря.

        Args:
            user_inventory: Список предметов в инвентаре пользователя.

        Returns:
            InlineKeyboardMarkup: Встроенная клавиатура для выбора предмета из инвентаря.
        """
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(x.item.name,
                                                       callback_data=f'{{"user_item": {str(x.id)}}}'),
                        user_inventory))
        return markup

    @staticmethod
    def inventory_choose_one_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для выбора действий с предметом.

        Returns:
            ReplyKeyboardMarkup: Клавиатура для выбора действий с предметом.
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Удалить', 'Назад')
        return markup

    @staticmethod
    def tasks_reply() -> InlineKeyboardMarkup:
        """
        Возвращает встроенную клавиатуру для выбора задачи.

        Returns:
            InlineKeyboardMarkup: Встроенная клавиатура для выбора задачи.
        """
        markup = InlineKeyboardMarkup()
        markup.add(*map(lambda x: InlineKeyboardButton(str(x), callback_data=f'{{"user_task": {str(x.id)}}}'),
                        Task.objects.all()))
        return markup

    @staticmethod
    def choose_task_reply() -> ReplyKeyboardMarkup:
        """
        Возвращает клавиатуру для выбора задачи.

        Returns:
            ReplyKeyboardMarkup: Клавиатура для выбора задачи.
        """
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Отправить на задание', 'Назад')
        return markup



class CallbackHandlers:
    """
    Класс CallbackHandlers содержит статические методы для обработки коллбэков в тамагочи боте.

    Методы:
    - choose_tamagotchi(tamagotchi_id, user): выбирает тамагочи и обновляет информацию о последнем выбранном тамагочи пользователем.
    - choose_item(item_id, user): выбирает предмет из инвентаря и обновляет информацию о последнем выбранном предмете пользователем.
    - use_item(item_id, user): использует выбранный предмет на выбранном тамагочи.
    - choose_task(task_id, user): выбирает задание и возвращает информацию о задании и его наградах.

    """
    @staticmethod
    def choose_tamagotchi(tamagotchi_id, user):
        """
        Метод choose_tamagotchi выбирает тамагочи и обновляет информацию о последнем выбранном тамагочи пользователем.

        Параметры:
        - tamagotchi_id (int): идентификатор выбранного тамагочи.
        - user (User): объект пользователя.

        Возвращает:
        - message (str): сообщение с информацией о выбранном тамагочи.
        - is_alive (bool): флаг, указывающий, жив ли выбранный тамагочи.

        """
        ManageUser.set_last_page(user, 'tamagotchi_page')
        ManageUser.set_last_tamagotchi(user, tamagotchi_id)
        ManageUser.set_is_tamagotchi_selected(user, True)

        tamagotchi = TamagotchiInPossession.objects.filter(id=tamagotchi_id).first()

        if tamagotchi.health <= 0:
            ManageTamagotchi.set_is_alive(tamagotchi, False)

        message = f'Показатели:\n' \
                  f'Название - {tamagotchi.tamagotchi.name}\n' \
                  f'Погоняло - {tamagotchi.pogonyalo}\n' \
                  f'Редкость - {tamagotchi.tamagotchi.rarity}\n' \
                  f'Элемент - {tamagotchi.tamagotchi.element}\n' \
                  f'Здоровье - {tamagotchi.health}\\{tamagotchi.tamagotchi.max_health}\n' \
                  f'Голод - {tamagotchi.hunger}\\{tamagotchi.tamagotchi.max_hunger}\n' \
                  f'Жажда - {tamagotchi.thirst}\\{tamagotchi.tamagotchi.max_thirst}\n' \
                  f'Счастье - {tamagotchi.happiness}\\{tamagotchi.tamagotchi.max_happiness}\n' \
                  f'Занят - {"Да" if tamagotchi.is_busy else "Нет"}'
        return message, tamagotchi.is_alive

    @staticmethod
    def choose_item(item_id, user):
        """
        Метод choose_item выбирает предмет из инвентаря и обновляет информацию о последнем выбранном предмете пользователем.

        Параметры:
        - item_id (int): идентификатор выбранного предмета.
        - user (User): объект пользователя.

        Возвращает:
        - message (str): сообщение с информацией о выбранном предмете.

        """
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
        """
        Метод use_item использует выбранный предмет на выбранном тамагочи.

        Параметры:
        - item_id (int): идентификатор выбранного предмета.
        - user (User): объект пользователя.

        Возвращает:
        - success (bool): флаг, указывающий, удалось ли использовать предмет.

        """
        item = ItemInInventory.objects.filter(id=item_id).first()
        tamagotchi = TamagotchiInPossession.objects.filter(id=user.last_selected_tamagotchi).first()
        if not user.is_tamagotchi_selected or not tamagotchi or not item:
            return False

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

        return True

    @staticmethod
    def choose_task(task_id, user: TgUser):
        """
        Метод choose_task выбирает задание и возвращает информацию о задании и его наградах.

        Параметры:
        - task_id (int): идентификатор выбранного задания.
        - user (User): объект пользователя.

        Возвращает:
        - message (str): сообщение с информацией о выбранном задании и его наградах.

        """
        task = Task.objects.filter(id=task_id).first()
        ManageUser.set_last_task(user, task_id)
        message = f'Задание - {task.name}\nВремя выполнения - {task.time_need_minutes} мин\nНаграды:\n'
        rewards = "\n". join(map(lambda x: f'{x.item}: {x.quantity}', RewardForTask.objects.filter(task=task).all()))
        message += rewards
        return message



