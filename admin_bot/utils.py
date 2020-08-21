from base.models import User
from functools import wraps

from base.utils import DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT
from tele_interface.manage_data import SELECT_DAY_TO_SHOW_COACH_SCHEDULE
from tennis_bot.settings import DEBUG
from telegram import (InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark,)

import datetime
import telegram
import sys
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def admin_handler_decor():
    """
    декоратор для всех handlers в телеграм боте
    :param bot:
    :return:
    """

    def decor(func):
        @wraps(func)
        def wrapper(bot, update):

            if DEBUG:
                logger.info(str(update) + '\n {}'.format(func.__name__))

            if update.callback_query:
                user_details = update.callback_query.from_user
            elif update.inline_query:
                user_details = update.inline_query.from_user
            else:
                user_details = update.message.from_user

            user = User.objects.get(id=user_details.id)

            if user.is_staff:
                try:
                    res = func(bot, update, user)
                except telegram.error.BadRequest as error:
                    if 'Message is not modified:' in error.message:
                        pass
                    else:
                        res = [bot.send_message(user.id, 'ошибкааааа ' + str(error))]
                        tb = sys.exc_info()[2]
                        raise error.with_traceback(tb)
                except Exception as e:

                    res = [bot.send_message(user.id, 'ошибка, блин ' + str(e))]
                    tb = sys.exc_info()[2]
                    raise e.with_traceback(tb)
            else:
                bot.send_message(
                    user.id,
                    "Привет! я переехал на @TennisTula_bot",
                    parse_mode='HTML',
                )
            return
        return wrapper
    return decor


def day_buttons_coach_info(tr_days, button_text):
    buttons = []
    row = []
    for day in tr_days:

        end_time = datetime.datetime.combine(day.date,
                                             day.start_time) + day.duration

        row.append(
            inlinebutt(f'{day.group.name}', callback_data=f"{button_text}{day.id}")
        )
        row.append(
            inlinebutt(
                f'{day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}',
                callback_data=f"{button_text}{day.id}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt('⬅️ назад',
                   callback_data=f"{SELECT_DAY_TO_SHOW_COACH_SCHEDULE}{tr_days.first().date.strftime(DT_BOT_FORMAT)}|month"),
    ])

    return inlinemark(buttons)