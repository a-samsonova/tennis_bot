from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN
from admin_bot.handlers import (
    start,
    permission_for_ind_train
)
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN


def add_handlers(updater):
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CallbackQueryHandler(permission_for_ind_train, pattern='^{}'.format(PERMISSION_FOR_IND_TRAIN)))


def main():
    # bot_code = sys.argv[1]
    # telebot_instance = Channel.objects.get(code=bot_code)
    updater = Updater(ADMIN_TELEGRAM_TOKEN)
    add_handlers(updater)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()