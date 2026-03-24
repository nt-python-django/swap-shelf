from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


phone_validator = RegexValidator(
    regex=r"^\+?998\d{9}$",
    message="Phone number must be in the format +998XXXXXXXXX or 998XXXXXXXXX",
)


class UserManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("Telegram id kiritish majburiy")
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(telegram_id, password, **extra_fields)

    def get_by_natural_key(self, username):
        try:
            return self.get(**{self.model.USERNAME_FIELD: int(username)})
        except (ValueError, TypeError, self.model.DoesNotExist):
            raise self.model.DoesNotExist


class User(AbstractUser):
    username = None

    telegram_id = models.BigIntegerField(unique=True)
    phone = models.CharField(
        validators=[phone_validator], max_length=15, unique=True, null=True
    )
    name = models.CharField(max_length=64)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)], default=0
    )
    telegram_username = models.CharField(
        max_length=64, null=True, blank=True, unique=True
    )

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"({self.telegram_id}) - {self.name}"
