from tg_bot.utils.utils import *

from django.core.management.base import BaseCommand
from django.conf import settings
from tg_bot.models import *


from telebot import TeleBot
from telebot.types import *

import re

bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)
allpages = r'(?:\A/back|\AНазад|\Aback' \
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
                             BotCommand(command="/help", description="Полезная информация о работе бота"),
                             BotCommand(command="/newpet", description="Создает тамагочи")])
        print("Bot initiation completed")
        bot.infinity_polling()

    @bot.callback_query_handler(func=lambda call: True)
    def callback_handler(call):
        tg_user = TgUser.objects.filter(telegram_user_id=call.from_user.id).first()
        if re.match(r'user_tamagotchi; \d+', call.data):
            call.data = re.sub(r'user_tamagotchi; ', '', call.data)

            ManageUser.set_last_page(tg_user, 'tamagotchi_page')
            ManageUser.set_last_tamagotchi(tg_user, int(call.data))

            tamagotchi = TamagotchiInPossession.objects.filter(id=int(call.data)).first()

            markup = ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add('Дать новое погоняло')
            markup.row('Назад')
            message = f'Показатели:\n' \
                      f'Название - {tamagotchi.tamagotchi.name}\n' \
                      f'Погоняло - {tamagotchi.pogonyalo}\n' \
                      f'Редкость - {tamagotchi.tamagotchi.rarity}\n' \
                      f'Элемент - {tamagotchi.tamagotchi.element}\n' \
                      f'Здоровье - {tamagotchi.health}\{tamagotchi.tamagotchi.max_health}\n' \
                      f'Голод - {tamagotchi.hunger}\{tamagotchi.tamagotchi.max_hunger}\n' \
                      f'Жажда - {tamagotchi.thirst}\{tamagotchi.tamagotchi.max_thirst}\n' \
                      f'Счастье - {tamagotchi.happiness}\{tamagotchi.tamagotchi.max_happiness}'

            bot.send_message(call.from_user.id, message, reply_markup=markup)

    @bot.message_handler(regexp=r'(?:\A/back|\AНазад|\Aback)')
    def back_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        if tg_user.last_page == 'main':
            Command.send_welcome(self)
        elif tg_user.last_page == 'tamagotchi_page':
            Command.tamagotchi_page_handler(self)
        elif tg_user.last_page == 'inventory_page':
            pass
        elif tg_user.last_page == 'show_all_page':
            Command.show_all_handler(self)

    @bot.message_handler(commands=['start'])  # handler команды /start, который регистрирует пользователя в бд
    def send_welcome(self):
        tg_user_id = self.from_user.id
        chat_id = self.chat.id

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Тамагочи', 'Инвентарь', 'Помощь')

        if not TgUser.objects.filter(telegram_user_id=tg_user_id).exists():  # проверка существования пользователя в бд
            tg_user = TgUser(telegram_user_id=tg_user_id,
                             telegram_chat_id=chat_id,
                             username=self.from_user.username,
                             last_page='main')
            tg_user.save()

        tg_user = TgUser.objects.filter(telegram_user_id=tg_user_id).first()
        ManageUser.set_last_page(tg_user, 'main')

        bot.send_message(chat_id, f'Привет, {self.from_user.username},\nэто телеграм-бот, в котором ты можешь:'
                                  f' выращивать своего питомца и ухаживать за ним', reply_markup=markup)

    @bot.message_handler(regexp=r'(?:\A/help|\AПомощь|\Ahelp_page)')  # handler команды /help, отправляет информацию о работе бота
    def help_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Назад')

        bot.send_message(self.chat.id, 'Бот создан командой FTM, текущая версия v0.1', reply_markup=markup)

    @bot.message_handler(regexp=r'(?:\A/tamagotchi|\AТамагочи|\Atamagotchi_page)')
    def tamagotchi_page_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')

        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('Посмотреть всех', 'Новый тамагочи', 'Назад')

        bot.send_message(self.chat.id, 'Выбери опцию:', reply_markup=markup)

    @bot.message_handler(regexp=r'(?:\A/show_all|\AПосмотреть всех|\Ashow_all_page)')
    def show_all_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')
        user_tamagotchi = TamagotchiInPossession.objects.filter(user_id=tg_user)

        inline_markup = InlineKeyboardMarkup()
        inline_markup.add(*map(lambda x: InlineKeyboardButton(x.pogonyalo, callback_data='user_tamagotchi; ' + str(x.id)), user_tamagotchi))

        bot.send_message(self.chat.id, 'Твои тамагочи:\n', reply_markup=inline_markup)

    @bot.message_handler(regexp=r'(?:\A/newpet|\AНовый тамагочи|\Anewpet_page)')  # handler команды /newpet, создает тамагочи
    def newpet_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'main')

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
            bot.send_message(self.chat.id, f'Выпал тамагочи - {tamagotchi}')
        else:
            bot.send_message(self.chat.id, f'У вас уже есть тамагочи=(')

    @bot.message_handler(regexp=r'(?:\A/change_pogonyalo|\AДать новое погоняло|\Achange_pogonyalo_page)')
    def change_pogonyalo_handler(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        ManageUser.set_last_page(tg_user, 'show_all_page')
        bot.send_message(self.chat.id, "Дайте новое погоняло(разрешается только латиница и цифры)")

    @bot.message_handler(regexp=r"^[a-zA-Z0-9]+$", )
    def change_pogonyalo_check(self):
        tg_user = TgUser.objects.filter(telegram_user_id=self.from_user.id).first()
        if tg_user.last_page == 'show_all_page':
            tamagotchi = TamagotchiInPossession.objects.filter(id=tg_user.last_selected_tamagotchi).first()
            if len(self.text) > 50:
                bot.send_message(self.chat.id, "Ограничение на количество символов")
            if tamagotchi:
                ManageTamagotchi.set_pogonyalo(tamagotchi, self.text)
                Command.show_all_handler(self)
