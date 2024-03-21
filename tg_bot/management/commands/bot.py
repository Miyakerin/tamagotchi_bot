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
    def send_welcome(self):
        tg_user_id = self.from_user.id
        chat_id = self.chat.id
        if not TgUser.objects.filter(telegram_user_id=tg_user_id):
            tg_user = TgUser(telegram_user_id=tg_user_id, telegram_chat_id=chat_id, username=self.from_user.username)
            tg_user.save()
        bot.send_message(chat_id, f'Привет, {self.from_user.username},\nэто телеграм-бот, в котором ты можешь:'
                                  f' выращивать своего питомца и ухаживать за ним')
