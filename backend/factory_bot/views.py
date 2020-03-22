from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import telebot

from .serializers import UserSerializer, UserListSerializer
from django.conf import settings
from .models import TelegramUsers

User = get_user_model()


class TGBot:
    bot = telebot.TeleBot(token=settings.TG_TOKEN)


class UserView(ListCreateAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        else:
            return UserListSerializer


class TgPostView(APIView, TGBot):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        try:
            tg_user = TelegramUsers.objects.get(user__exact=request.user.id)
        except TelegramUsers.DoesNotExist:
            return Response({"ok": False,
                             "error": "Account is not registered in TG_BOT"},
                            status=status.HTTP_400_BAD_REQUEST)

        TGBot.bot.send_message(chat_id=tg_user.TG_user_id,
                               text=f"Hello, {tg_user.TG_username}!\n"
                                    f"I received your message:\n"
                                    f"{request.data['text']}")
        return Response({"ok": True})
