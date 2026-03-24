from random import randint

from django.core.cache import cache
from rest_framework import serializers
import re

from .models import User


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    def validate_phone_number(self, value):
        pattern = r"^998\d{9}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam '+998901234567' formatda bo‘lishi kerak."
            )

        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "Bunday telefon raqamiga ega foydalanuvchi topilmadi."
            )

        opt = randint(100000, 999999)

        if cache.get(f"{value}"):
            return value
        else:
            cache.set(f"{value}", opt, timeout=120)
            return value


class VerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verify_code = serializers.CharField(min_length=6, max_length=6)

    def validate_phone_number(self, value):
        pattern = r"^\+998\d{9}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Telefon raqam '+998901234567' formatda bo‘lishi kerak."
            )

        if not User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(
                "Bunday telefon raqamiga ega foydalanuvchi topilmadi."
            )

        if not cache.get(value):
            raise serializers.ValidationError("Yaroqsiz tekshirish kodi.")

        cache.delete(value)

        return value
