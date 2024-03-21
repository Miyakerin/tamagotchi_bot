from django.core.management.base import BaseCommand
from django.conf import settings
from tg_bot.models import *


from telebot import TeleBot


# Объявление переменной бота
bot = TeleBot(settings.TELEGRAM_BOT_API_KEY, threaded=False)


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):
        print("Bot initiation started")
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()		# Загрузка обработчиков
        print("Bot initiation completed")
        bot.infinity_polling()

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """)
