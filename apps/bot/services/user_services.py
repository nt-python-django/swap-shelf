from ...users.models import User


# User.objects.filter(phone__isnull=True).exists()
def get_or_create_user(
    telegram_id: int, first_name: str, last_name: str, username: str, phone: str
):
    user = User.objects.filter(telegram_id=telegram_id)
    if user.exists():
        if user.first().phone is None:
            return "telefon raqami kiritilmagan"
        return "hamma malumotlar to'liq, foydalanuvchi topildi"

    return "foydalanuvchi topilmadi, yangi foydalanuvchi yaratildi"


def set_webhook(url: str):
    pass
