import telebot.types
from django.core.management.base import BaseCommand
from django.conf import settings
from tg_bot.models import *


from telebot import TeleBot


bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


class Command(BaseCommand):
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        print("Bot initiation started")
        bot.enable_save_next_step_handlers(delay=2)  # Сохранение обработчиков
        bot.load_next_step_handlers()  # Загрузка обработчиков
        bot.set_my_commands([telebot.types.BotCommand(command="/start",
                                                      description="Запускает бота и отправляет приветствие"),
                             telebot.types.BotCommand(command="/help",
                                                      description="Полезная информация о работе бота")])
        print("Bot initiation completed")
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])  # handler команды /start, который регистрирует пользователя в бд
    def send_welcome(self):
        tg_user_id = self.from_user.id
        chat_id = self.chat.id
        if not TgUser.objects.filter(telegram_user_id=tg_user_id):
            tg_user = TgUser(telegram_user_id=tg_user_id, telegram_chat_id=chat_id, username=self.from_user.username)
            tg_user.save()
        bot.send_message(chat_id, f'Привет, {self.from_user.username},\nэто телеграм-бот, в котором ты можешь:'
                                  f' выращивать своего питомца и ухаживать за ним')

    @bot.message_handler(commands=['help'])
    def help_handler(self):
        bot.send_message(self.chat.id, "Бот создан командой FTM, текущая версия v0.1")
