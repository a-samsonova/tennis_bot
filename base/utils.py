from telegram import (ReplyKeyboardMarkup)
from tele_interface.manage_data import (
    ADMIN_TIME_SCHEDULE_BUTTON,
    MY_DATA_BUTTON,
    SKIP_LESSON_BUTTON,
    TAKE_LESSON_BUTTON, HELP_BUTTON, )

import telegram

DTTM_BOT_FORMAT = '%Y.%m.%d.%H.%M'
DT_BOT_FORMAT = '%Y.%m.%d'
TM_HOUR_BOT_FORMAT = '%H'
TM_DAY_BOT_FORMAT = '%d'
TM_TIME_SCHEDULE_FORMAT = '%H:%M'

from_digit_to_month = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
    }


def send_message(users, message: str, bot, markup=None):
    """
    :param users: instance of User model, iterable object
    :param message: text
    :param bot: instance of telegram.Bot
    :param markup: telegram markup
    :return: send message to users in telegram bot
    """

    for user in users:
        try:
            bot.send_message(user.id,
                             message,
                             reply_markup=markup,
                             parse_mode='HTML')
        except (telegram.error.Unauthorized, telegram.error.BadRequest):
            user.is_blocked = True
            user.status = 'F'
            user.save()


def construct_main_menu():
    return ReplyKeyboardMarkup([
        [MY_DATA_BUTTON, HELP_BUTTON],
        [SKIP_LESSON_BUTTON, TAKE_LESSON_BUTTON]],
        resize_keyboard=True)


def construct_admin_main_menu():
    return ReplyKeyboardMarkup([
        [ADMIN_TIME_SCHEDULE_BUTTON]],
        resize_keyboard=True)


def send_alert_about_changing_tr_day_status(tr_day, new_is_available: bool, bot):
    group_members = tr_day.group.users.all()
    visitors = tr_day.visitors.all()

    if not new_is_available:
        text = 'Тренировка <b>{} в {}</b> отменена.'.format(tr_day.date,
                                                            tr_day.start_time)
    else:
        text = 'Тренировка <b>{} в {}</b> доступна, ура!'.format(tr_day.date,
                                                                 tr_day.start_time)

    send_message(group_members.union(visitors), text, bot, construct_main_menu())
