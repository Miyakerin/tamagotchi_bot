from datetime import timezone, timedelta

from tg_bot.utils.utils import *

from django.core.management.base import BaseCommand
from django.conf import settings
from tg_bot.models import *

from telebot import TeleBot
from telebot.types import *

import re
import json

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)
all_pages = r'(?:\A/back|\AНазад|\Aback' \
           r'|A/start' \
           r'|\A/help|\AПомощь|\Ahelp_page' \
           r'|\A/tamagotchi|\AТамагочи|\Atamagotchi_page' \
           r'|\A/show_all|\AПосмотреть всех|\Ashow_all_page' \
           r'|\A/newpet|\AНовый тамагочи|\Anewpet_page' \
           r'|\A/change_pogonyalo|Дать новое погоняло|change_pogonyalo_page)'


class Command(BaseCommand):
    def handle(self, *args, **kwargs):  # инициализация бота
        print("Bot initiation started")
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков

        bot.set_my_commands([BotCommand(command="/start", description="Запускает бота и отправляет приветствие"),
                             BotCommand(command="/help", description="Полезная информация о работе бота")])
        print("Bot initiation completed")
        bot.infinity_polling()

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        json_data = json.loads(self.data)
        if json_data.get('user_tamagotchi'):
            message, is_alive = CallbackHandlers.choose_tamagotchi(json_data.get('user_tamagotchi'), tg_user)
            markup = KeyBoardsTemplate.tamagotchi_choose_one_reply(is_alive)
        elif json_data.get('user_item'):
            message = CallbackHandlers.choose_item(json_data.get('user_item'), tg_user)
            markup = KeyBoardsTemplate.inventory_choose_one_reply()
        elif json_data.get('user_item_use'):
            markup = KeyBoardsTemplate.action_reply()
            response = CallbackHandlers.use_item(json_data.get('user_item_use'), tg_user)
            if response:
                message = "Предмет использован"
            else:
                message = "Не получилось использовать предмет"
        elif json_data.get('user_task'):
            markup = KeyBoardsTemplate.choose_task_reply()
            message = CallbackHandlers.choose_task(json_data.get('user_task'), tg_user)
        else:
            print(self.data)
            message = 'callback error'
            markup = KeyBoardsTemplate.main_reply()

        bot.send_message(self.from_user.id, message, reply_markup=markup)

    @bot.message_handler(regexp=r'(?:\A/back|\AНазад|\Aback)')
    def back_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_is_tamagotchi_selected(tg_user, False)
        ManageUser.set_is_item_selected(tg_user, False)
        if tg_user.last_page == 'main':
            Command.start_page_handler(self)
        elif tg_user.last_page == 'tamagotchi_page':
            Command.tamagotchi_page_handler(self)
        elif tg_user.last_page == 'inventory_page':
            Command.inventory_page_handler(self)
        elif tg_user.last_page == 'show_all_page':
            Command.show_all_handler(self)
        elif tg_user.last_page == 'show_inventory_page':
            Command.show_inventory_page_handler(self)
        elif tg_user.last_page == 'tasks_page':
            Command.tamagotchi_page_handler(self)

    @bot.message_handler(commands=['start'])  # handler команды /start, который регистрирует пользователя в бд
    def start_page_handler(self):
        tg_user_id = self.from_user.id
        chat_id = self.chat.id
        if not TgUser.objects.filter(telegram_user_id=tg_user_id).exists():  # проверка существования пользователя в бд
            tg_user = TgUser(telegram_user_id=tg_user_id,
                             username=self.from_user.username,
                             last_page='main')
            tg_user.save()

        tg_user = TgUser.objects.filter(telegram_user_id=tg_user_id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)  # необходимое зло
        ManageUser.set_is_item_selected(tg_user, False)

        message = f'Привет, {self.from_user.username},\nэто телеграм-бот, в котором ты можешь: ' \
                  f'выращивать своего питомца и ухаживать за ним'
        bot.send_message(chat_id, message, reply_markup=KeyBoardsTemplate.main_reply())

    @bot.message_handler(
        regexp=r'(?:\A/help|\AПомощь|\Ahelp_page)')  # handler команды /help, отправляет информацию о работе бота
    def help_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)  # необходимое зло
        ManageUser.set_is_item_selected(tg_user, False)

        message = 'Бот создан командой FTM, текущая версия v0.1'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.help_reply())

    # handlers of main page btns
    @bot.message_handler(regexp=r'(?:\AТамагочи|\Atamagotchi_page)')
    def tamagotchi_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)  # необходимое зло
        ManageUser.set_is_item_selected(tg_user, False)

        message = 'Выбери опцию:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.tamagotchi_main_reply())

    @bot.message_handler(regexp=r'(?:\AИнвентарь|\Ainventory_page)')
    def inventory_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)  # необходимое зло
        ManageUser.set_is_item_selected(tg_user, False)

        message = 'Выбери опцию:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.inventory_main_reply())

    @bot.message_handler(regexp=r'(?:\AЗабрать награды|\Atake_rewards)')
    def take_rewards_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_item_selected(tg_user, False)
        ManageUser.set_is_item_selected(tg_user, False)

        user_tamagotchis = TamagotchiInPossession.objects.filter(user_id=tg_user).all()
        message = 'Наград еще нет'
        for tamagotchi in user_tamagotchis:
            if tamagotchi.is_busy:
                end_time = tamagotchi.task_started_at + timedelta(minutes=tamagotchi.current_task.time_need_minutes)
                if end_time < datetime.now(tz=timezone.utc):

                    message = 'Награды начислены'
                    rewards = RewardForTask.objects.filter(task=tamagotchi.current_task).all()
                    for task_reward in rewards:
                        check = ManageInventory.check_if_item_in_inventory(task_reward.item, tg_user)
                        if check:
                            ManageInventory.update_quantity(check, task_reward.quantity)
                        else:
                            user_item = ItemInInventory(item=task_reward.item,
                                                        user_id=tg_user,
                                                        quantity=task_reward.quantity)
                            user_item.save()
                    ManageTamagotchi.set_is_busy(tamagotchi, False)
                    ManageTamagotchi.set_current_task(tamagotchi, None)

        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.inventory_main_reply())

    # handlers of tamagotchi page btns

    @bot.message_handler(regexp=r'(?:\AПосмотреть всех|\Ashow_all_page)')
    def show_all_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)  # необходимое зло
        ManageUser.set_is_item_selected(tg_user, False)

        user_tamagotchi = TamagotchiInPossession.objects.filter(user_id=tg_user)
        if user_tamagotchi.exists():
            message = 'Твои тамагочи:\n'
        else:
            message = 'У тебя пока нет тамагочи'

        bot.send_message(self.chat.id,
                         message,
                         reply_markup=KeyBoardsTemplate.tamagotchi_show_all_inline(user_tamagotchi))

    @bot.message_handler(
        regexp=r'(?:\AНовый тамагочи|\Anewpet_page)')  # handler команды /newpet, создает тамагочи
    def newpet_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)  # необходимое зло
        ManageUser.set_is_item_selected(tg_user, False)

        message = 'У вас слишком много тамагочи'

        if TamagotchiInPossession.objects.filter(user_id=tg_user).count() < tg_user.max_tamagotchi:
            tamagotchi = Roll.create_tamagotchi()
            tamagotchi_to_user = TamagotchiInPossession(tamagotchi=tamagotchi,
                                                        user_id=tg_user,
                                                        pogonyalo=tamagotchi.name,
                                                        health=tamagotchi.max_health,
                                                        thirst=tamagotchi.max_thirst,
                                                        hunger=tamagotchi.max_hunger,
                                                        happiness=tamagotchi.max_happiness)
            tamagotchi_to_user.save()
            message = f'Выпал тамагочи - {tamagotchi}'

        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.tamagotchi_main_reply())

    # handlers of choose tamagotchi page btns
    @bot.message_handler(regexp=r'(?:\AВоскресить|\Aresurrect_page)') # handler воскрешения
    def resurrect_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'show_all_page')
        ManageUser.set_is_item_selected(tg_user, False)

        tamagotchi = TamagotchiInPossession.objects.filter(id=tg_user.last_selected_tamagotchi).first()
        user_inventory = ItemInInventory.objects.filter(user_id=tg_user)

        # hardcoded id4 for resurrection
        item = user_inventory.filter(item_id=4).first()
        if not tamagotchi.is_alive and item.quantity > 0 and tg_user.is_tamagotchi_selected:
            ManageTamagotchi.set_is_alive(tamagotchi, True)
            ManageTamagotchi.set_health(tamagotchi, tamagotchi.tamagotchi.max_health)
            ManageInventory.update_quantity(item, -1)
            message = f'{str(tamagotchi)} воскрешен'
        elif tamagotchi.is_alive:
            message = 'Ваш тамагочи жив'
        elif item.quantity <= 0 or not item:
            message = 'Не хватает Scroll of resurrection'
        else:
            message = "error"

        ManageUser.set_is_tamagotchi_selected(tg_user, False)

        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.tamagotchi_main_reply())
        Command.show_all_handler(self)

    @bot.message_handler(regexp=r'(?:\AДействия|\Aactions_page)')
    def actions_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tamagotchi_page')
        ManageUser.set_is_item_selected(tg_user, False)

        message = 'Доступные действия:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.action_reply())

    @bot.message_handler(regexp=r'(?:\AЗадачи|\Atasks_page)')
    def tasks_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tasks_page')
        ManageUser.set_is_item_selected(tg_user, False)

        message = 'Доступные задачи:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.tasks_reply())

    @bot.message_handler(regexp=r'(?:\AОтправить на задание|\Asend_on_task_page)')
    def send_on_task_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tasks_page')
        ManageUser.set_is_item_selected(tg_user, False)

        task = Task.objects.filter(id=tg_user.last_selected_task).first()
        tamagotchi = TamagotchiInPossession.objects.filter(id=tg_user.last_selected_tamagotchi).first()
        if task and tamagotchi and tamagotchi.is_busy is False:
            ManageTamagotchi.set_is_busy(tamagotchi, True)
            ManageTamagotchi.set_task_started_at(tamagotchi, datetime.now(tz=timezone.utc))
            ManageTamagotchi.set_current_task(tamagotchi, task)
            message = 'Задача успешно поставлена'
        else:
            message = 'Не удалось присвоить задачу для тамагочи'

        ManageUser.set_is_tamagotchi_selected(tg_user, False)
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.tamagotchi_main_reply())



    @bot.message_handler(regexp=r'(?:\AНакормить|\Afeed_page)')
    def feed_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tamagotchi_page')
        ManageUser.set_is_item_selected(tg_user, False)

        user_inventory = ItemInInventory.objects.filter(user_id=tg_user).filter(
            item__hunger_on_consume__range=(1, 1000))

        message = 'Выберите предмет:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.action_inline(user_inventory))

    @bot.message_handler(regexp=r'(?:\AЛечить|\Aheal_page)')
    def health_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tamagotchi_page')
        ManageUser.set_is_item_selected(tg_user, False)

        user_inventory = ItemInInventory.objects.filter(user_id=tg_user).filter(
            item__health_on_consume__range=(1, 1000))

        message = 'Выберите предмет:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.action_inline(user_inventory))

    @bot.message_handler(regexp=r'(?:\AНапоить|\Athirst_page)')
    def thirst_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tamagotchi_page')
        ManageUser.set_is_item_selected(tg_user, False)

        user_inventory = ItemInInventory.objects.filter(user_id=tg_user).filter(
            item__thirst_on_consume__range=(1, 1000))

        message = 'Выберите предмет:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.action_inline(user_inventory))

    @bot.message_handler(regexp=r'(?:\AПовеселить|\Afun_page)')
    def fun_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'tamagotchi_page')
        ManageUser.set_is_item_selected(tg_user, False)

        user_inventory = ItemInInventory.objects.filter(user_id=tg_user).filter(
            item__happiness_on_consume__range=(1, 1000))

        message = 'Выберите предмет:'
        bot.send_message(self.chat.id, message, reply_markup=KeyBoardsTemplate.action_inline(user_inventory))


    # handlers of inventory page btns
    @bot.message_handler(regexp=r'(?:\AПосмотреть инвентарь|\Ashow_inventory_page)') # handler инвентаря
    def show_inventory_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        ManageUser.set_is_tamagotchi_selected(tg_user, False)
        ManageUser.set_is_item_selected(tg_user, False)

        user_inventory = ItemInInventory.objects.filter(user_id=tg_user)

        if user_inventory.exists():
            message = 'Инвентарь:'
        else:
            message = 'В инвентаре пусто'

        bot.send_message(self.chat.id,
                         message,
                         reply_markup=KeyBoardsTemplate.inventory_show_all_inline(user_inventory))

    # handlers of choose item page btns
    @bot.message_handler(regexp=r'(?:\AУдалить|\Adelete_item_page)') # handler удаления предмета
    def delete_item_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'show_inventory_page')

        if tg_user.is_item_selected:
            ItemInInventory.objects.filter(id=tg_user.last_selected_item).delete()
            message = 'Предмет удален'
        else:
            message = ''

        bot.send_message(self.chat.id,
                         message,
                         reply_markup=KeyBoardsTemplate.inventory_main_reply())
        Command.show_inventory_page_handler(self)



    # other

    @bot.message_handler(regexp=r'(?:\AДать новое погоняло|\Achange_pogonyalo_page)')
    def change_pogonyalo_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'show_all_page')
        bot.send_message(self.chat.id, "Дайте новое погоняло(разрешается только латиница и цифры)")

    @bot.message_handler(regexp=r"^[a-zA-Z0-9]+$", )
    def change_pogonyalo_check(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        if tg_user.last_page == 'show_all_page' and tg_user.is_tamagotchi_selected:
            tamagotchi = TamagotchiInPossession.objects.filter(id=tg_user.last_selected_tamagotchi).first()
            if len(self.text) > 50:
                bot.send_message(self.chat.id, "Ограничение на количество символов")
            elif tamagotchi:
                ManageTamagotchi.set_pogonyalo(tamagotchi, self.text)
                ManageUser.set_is_tamagotchi_selected(tg_user, False)
                Command.show_all_handler(self)
