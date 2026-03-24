from random import randint

from django.core.cache import cache

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext

from apps.users.models import User

Start_Keyboard = [
    [KeyboardButton("📞 Telefon raqamni kiritish", request_contact=True)],
    ["❓ Yordam"],
]

Menu_Keyboard = [
    ["🏠 Bosh sahifa", "📚 Mening kitoblarim"],
    ["🔍 Kitoblarni qidirish", "📥 Menga kelgan so‘rovlar"],
    ["📤 Yuborgan so‘rovlar", "🔄 Almashuvlarim"],
    ["🔢 OTP kod olish", "🔔 Bildirishnomalar"],
    ["👤 Profilim", "❓ Yordam"],
]

Start_massage = """📚 *SwapShelf botiga xush kelibsiz!*

Bu bot orqali siz:

🔐 *Saytga kirish uchun OTP kod* olasiz  
🔔 *Swap request* va *almashuvlar* haqida xabar olasiz  
⚡ Ba'zi *tezkor amallarni* bot orqali bajarishingiz mumkin

Boshlash uchun quyidagilardan birini tanlang:

📱 *Telefon raqamni kiritish*  
❓ *Yordam*"""

Againg_start_massage = """📚 *SwapShelf botiga xush kelibsiz!*

Bu bot orqali siz:

🔐 *Saytga kirish uchun OTP kod* olasiz  
🔔 *Swap request* va *almashuvlar* haqida xabar olasiz  
⚡ Ba'zi *tezkor amallarni* bot orqali bajarishingiz mumkin

Quyidagilardan birini tanlang:

🏠 Bosh sahifa, 📚 Mening kitoblarim
🔍 Kitoblarni qidirish, 📥 Menga kelgan so‘rovlar
📤 Yuborgan so‘rovlar, 🔄 Almashuvlarim
🔢 OTP kod olish, 🔔 Bildirishnomalar
👤 Profilim, ❓ Yordam
"""


def start(update: Update, context: CallbackContext):
    telegram_id = update.message.from_user.id
    telegram_username = update.effective_user.username
    telegram_first_name = update.effective_user.first_name
    telegram_last_name = update.effective_user.last_name

    user = User.objects.filter(telegram_id=telegram_id).first()

    if user:
        if user.phone is not None and user.phone != "":
            update.message.reply_text(
                Againg_start_massage,
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(
                    Menu_Keyboard,
                    resize_keyboard=True,
                ),
            )
            return
        else:
            update.message.reply_text(
                Start_massage,
                parse_mode="Markdown",
                reply_markup=ReplyKeyboardMarkup(Start_Keyboard, resize_keyboard=True),
            )
            return
    else:
        User.objects.create(
            telegram_id=telegram_id,
            telegram_username=telegram_username,
            name=f"{telegram_first_name} {telegram_last_name}".strip(),
        )
        update.message.reply_text(
            Start_massage,
            parse_mode="Markdown",
            reply_markup=ReplyKeyboardMarkup(Start_Keyboard, resize_keyboard=True),
        )
        return


def help(update: Update, context: CallbackContext):
    update.message.reply_text("Yordam uchun /help buyrug'ini bering.")


def login(update: Update, context: CallbackContext):
    opt = randint(100000, 999999)

    if cache.get(f"{update.message.chat_id}_opt"):
        opt = cache.get(f"{update.message.chat_id}_opt")
    cache.set(f"{update.message.chat_id}_opt", opt, timeout=120)

    update.message.reply_text(f"Telefon raqamingizni kiriting:\n{opt}")
