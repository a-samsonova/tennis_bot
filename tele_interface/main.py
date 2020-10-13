from telegram.ext import (
    Updater,
    CommandHandler,
    RegexHandler,
    CallbackQueryHandler,
)
import django

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from tele_interface.handlers import (
    get_personal_data,
    start,
    skip_lesson_main_menu_button,
    take_lesson,
    user_main_info,
    select_precise_group_lesson_time,
    choose_type_of_training,
    select_dt_for_ind_lesson,
    select_precise_ind_lesson_time,
    confirm_group_lesson,
    skip_lesson,
    get_help,
    inline_calendar_handler,
)
from tele_interface.manage_data import (
    SELECT_PRECISE_GROUP_TIME,
    SELECT_TRAINING_TYPE,
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_PRECISE_IND_TIME,
    CONFIRM_GROUP_LESSON,
    SHOW_INFO_ABOUT_SKIPPING_DAY,
    SKIP_LESSON_BUTTON,
    TAKE_LESSON_BUTTON,
    MY_DATA_BUTTON, HELP_BUTTON,
)
from tennis_bot.config import TELEGRAM_TOKEN


def add_handlers(updater):
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(RegexHandler(SKIP_LESSON_BUTTON, skip_lesson_main_menu_button))
    dp.add_handler(RegexHandler(TAKE_LESSON_BUTTON, choose_type_of_training))
    dp.add_handler(RegexHandler(MY_DATA_BUTTON, user_main_info))
    dp.add_handler(RegexHandler(HELP_BUTTON, get_help))

    dp.add_handler(RegexHandler(r'^\w+\s\w+$', get_personal_data))
    dp.add_handler(RegexHandler(r'^\d+$', get_personal_data))

    dp.add_handler(CallbackQueryHandler(select_precise_group_lesson_time, pattern='^{}'.format(SELECT_PRECISE_GROUP_TIME)))
    dp.add_handler(CallbackQueryHandler(take_lesson, pattern='^{}'.format(SELECT_TRAINING_TYPE)))
    dp.add_handler(CallbackQueryHandler(select_dt_for_ind_lesson, pattern='^{}'.format(SELECT_DURATION_FOR_IND_TRAIN)))
    dp.add_handler(CallbackQueryHandler(select_precise_ind_lesson_time, pattern='^{}'.format(SELECT_PRECISE_IND_TIME)))
    dp.add_handler(CallbackQueryHandler(choose_type_of_training, pattern='^{}'.format(TAKE_LESSON_BUTTON)))
    dp.add_handler(CallbackQueryHandler(confirm_group_lesson, pattern='^{}'.format(CONFIRM_GROUP_LESSON)))
    dp.add_handler(CallbackQueryHandler(skip_lesson, pattern='^{}'.format(SHOW_INFO_ABOUT_SKIPPING_DAY)))
    dp.add_handler(CallbackQueryHandler(inline_calendar_handler))


def main():
    updater = Updater(TELEGRAM_TOKEN, workers=8)
    add_handlers(updater)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
