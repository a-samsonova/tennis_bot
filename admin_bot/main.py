from telegram.ext import (
    Updater,
    CallbackQueryHandler,
    CommandHandler,
    RegexHandler
)
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from tennis_bot.config import ADMIN_TELEGRAM_TOKEN
from admin_bot.handlers import (
    start,
    permission_for_ind_train,
    show_coach_schedule,
    choose_dt_for_coach_time_schedule,
    show_traingroupday_info
)
from tele_interface.manage_data import (
    PERMISSION_FOR_IND_TRAIN,
    ADMIN_TIME_SCHEDULE_BUTTON,
    SELECT_DAY_TO_SHOW_COACH_SCHEDULE,
    SHOW_GROUPDAY_INFO
)


def add_handlers(updater):
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CallbackQueryHandler(permission_for_ind_train, pattern='^{}'.format(PERMISSION_FOR_IND_TRAIN)))
    dp.add_handler(RegexHandler(fr'^{ADMIN_TIME_SCHEDULE_BUTTON}$', show_coach_schedule))
    dp.add_handler(CallbackQueryHandler(choose_dt_for_coach_time_schedule, pattern='^{}'.format(SELECT_DAY_TO_SHOW_COACH_SCHEDULE)))
    dp.add_handler(CallbackQueryHandler(show_traingroupday_info, pattern='^{}'.format(SHOW_GROUPDAY_INFO)))


def main():
    updater = Updater(ADMIN_TELEGRAM_TOKEN)
    add_handlers(updater)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()