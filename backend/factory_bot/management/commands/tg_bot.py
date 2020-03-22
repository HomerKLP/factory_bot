import telebot

from django.core.management.base import BaseCommand
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from factory_bot.models import TelegramUsers

User = get_user_model()


def set_tg_user(username, TG_user_id, user_id):
    try:
        TelegramUsers.objects.create(
            TG_username=username,
            TG_user_id=TG_user_id,
            user_id=user_id
        )
    except:
        return False
    return True


class Command(BaseCommand):
    help = 'TG_BOT'
    bot = telebot.TeleBot(settings.TG_TOKEN)

    def handle(self, *args, **options):
        me = self.bot.get_me()
        print(me)

        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            welcome_text = 'To register your account write your token below'
            self.bot.send_message(message.chat.id, welcome_text)
            self.bot.register_next_step_handler(message,
                                                callback=register_token)

        def register_token(message):
            token = message.text.strip()
            try:
                my_token = Token.objects.get(key__exact=token)
                if set_tg_user(message.from_user.username,
                               message.from_user.id,
                               my_token.user_id):
                    self.bot.send_message(message.chat.id,
                                          f"Hello, {my_token.user.username}!\n"
                                          f"Your token has been registered!")
                else:
                    self.bot.send_message(message.chat.id,
                                          "Something went wrong, "
                                          "user has not been registered!")
            except Token.DoesNotExist:
                self.bot.send_message(message.chat.id, "Insufficient token")

        @self.bot.message_handler(content_types=['text'])
        def other_message(message):
            self.bot.send_message(message.chat.id, "I don't understand")

        self.bot.polling()
