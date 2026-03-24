from django.core import cache

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..bot.services.user_services import get_or_create_user
from ..bot.bot import hendle_update
from .serializers import LoginSerializer, VerifySerializer


class TelegramWebhookView(APIView):
    def post(self, request: Request):
        data = request.data
        hendle_update(data)
        return Response("ok")


class UserLoginView(APIView):
    def post(self, request: Request):
        serializser = LoginSerializer(data=request.data)
        if serializser.is_valid(raise_exception=True):
            return Response(
                {"message": "Tekshirish kodi Telegramdan yuborildi."}, status=200
            )


class TokenVerifyView(APIView):
    # authentication_classes = JWTAuthentication
    # permission_classes = [IsAuthenticated]
    def post(self, request: Request):
        serializser = VerifySerializer(data=request.data)
        if serializser.is_valid(raise_exception=True):
            refresh = RefreshToken.for_user(request.user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=200,
            )
