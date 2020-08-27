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
    choose_dt_for_cancel,
    choose_dt_for_group_lesson,
    select_precise_group_lesson_time,
    choose_type_of_training,
    select_dt_for_ind_lesson,
    choose_dt_time_for_ind_train,
    select_precise_ind_lesson_time,
    confirm_group_lesson,
    skip_lesson,
)
from tele_interface.manage_data import (
    SELECT_SKIP_TIME_BUTTON,
    SELECT_GROUP_LESSON_TIME,
    SELECT_PRECISE_GROUP_TIME,
    SELECT_TRAINING_TYPE,
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_IND_LESSON_TIME,
    SELECT_PRECISE_IND_TIME,
    CONFIRM_GROUP_LESSON,
    SHOW_INFO_ABOUT_SKIPPING_DAY,
    SKIP_LESSON,
    TAKE_LESSON,
    MY_DATA,
)
from tennis_bot.config import TELEGRAM_TOKEN


def add_handlers(updater):
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(RegexHandler(SKIP_LESSON, skip_lesson_main_menu_button))
    dp.add_handler(RegexHandler(TAKE_LESSON, choose_type_of_training))
    dp.add_handler(RegexHandler(MY_DATA, user_main_info))

    dp.add_handler(RegexHandler(r'^\w+\s\w+$', get_personal_data))
    dp.add_handler(RegexHandler(r'^\d+$', get_personal_data))

    dp.add_handler(CallbackQueryHandler(choose_dt_for_cancel, pattern='^{}'.format(SELECT_SKIP_TIME_BUTTON)))
    dp.add_handler(CallbackQueryHandler(choose_dt_for_group_lesson, pattern='^{}'.format(SELECT_GROUP_LESSON_TIME)))
    dp.add_handler(CallbackQueryHandler(select_precise_group_lesson_time, pattern='^{}'.format(SELECT_PRECISE_GROUP_TIME)))
    dp.add_handler(CallbackQueryHandler(take_lesson, pattern='^{}'.format(SELECT_TRAINING_TYPE)))
    dp.add_handler(CallbackQueryHandler(select_dt_for_ind_lesson, pattern='^{}'.format(SELECT_DURATION_FOR_IND_TRAIN)))
    dp.add_handler(CallbackQueryHandler(choose_dt_time_for_ind_train, pattern='^{}'.format(SELECT_IND_LESSON_TIME)))
    dp.add_handler(CallbackQueryHandler(select_precise_ind_lesson_time, pattern='^{}'.format(SELECT_PRECISE_IND_TIME)))
    dp.add_handler(CallbackQueryHandler(choose_type_of_training, pattern='^{}'.format(TAKE_LESSON)))
    dp.add_handler(CallbackQueryHandler(confirm_group_lesson, pattern='^{}'.format(CONFIRM_GROUP_LESSON)))
    dp.add_handler(CallbackQueryHandler(skip_lesson, pattern='^{}'.format(SHOW_INFO_ABOUT_SKIPPING_DAY)))


def main():
    updater = Updater(TELEGRAM_TOKEN, workers=8)
    add_handlers(updater)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
