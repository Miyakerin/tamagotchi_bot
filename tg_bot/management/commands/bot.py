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
        print("Lets go")
        bot.enable_save_next_step_handlers(delay=2) # Сохранение обработчиков
        bot.load_next_step_handlers()				# Загрузка обработчиков
        bot.infinity_polling()

    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.reply_to(message, """\
    Hi there, I am EchoBot.
    I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
    """)

    # Handle all other messages with content_type 'text' (content_types defaults to ['text'])
    @bot.message_handler(func=lambda message: True)
    def echo_message(message):
        el = Element.objects.first()
        text  = message.text + str(el)
        bot.reply_to(message, text)