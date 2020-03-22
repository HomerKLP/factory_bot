from django.urls import path
from .views import UserView, TgPostView

urlpatterns = [
    path('user/', UserView.as_view()),
    path('send-message/', TgPostView.as_view())
]
