from django.urls import path

from apps.users.views import TelegramWebhookView, UserLoginView, TokenVerifyView

urlpatterns = [
    path("telegram/webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
    path("auth/login/", UserLoginView.as_view(), name="login"),
    path("auth/verify/", TokenVerifyView.as_view(), name="verify"),
]
