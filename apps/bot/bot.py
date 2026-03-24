from telegram import Bot, Update
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler
from django.conf import settings

from apps.bot.handlers.messages import contact_save, get_OTP_code

from .handlers.commands import login, start

bot = Bot(settings.TOKEN)
dispatcher = Dispatcher(bot, None, workers=4, use_context=True)

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("login", login))
dispatcher.add_handler(CommandHandler("help", help))
dispatcher.add_handler(MessageHandler(Filters.contact, contact_save))
dispatcher.add_handler(
    MessageHandler(Filters.regex("^🔢 OTP kod olish$"), get_OTP_code)
)


def hendle_update(data: dict):
    update = Update.de_json(data, bot)
    dispatcher.process_update(update)
