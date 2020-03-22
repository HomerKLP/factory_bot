from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Message(models.Model):
    external_id = models.BigIntegerField()
    text = models.TextField()
    send_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class TelegramUsers(models.Model):
    TG_username = models.CharField(max_length=128)
    TG_user_id = models.BigIntegerField()
    user = models.OneToOneField(User, on_delete=models.PROTECT)
