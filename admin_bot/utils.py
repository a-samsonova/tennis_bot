import datetime
from telegram import (
    InlineKeyboardButton as inlinebutt,
    InlineKeyboardMarkup as inlinemark,
)
from base.models import User, Channel
from functools import wraps
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

#
# def construct_menu_for_user_set_up(user):
#     """
#
#     Делает кнопки для настроек параметров нового пользователя.
#     :return:
#     """
#     markup = inlinemark([inlinebutt('Время до отмены', callback_data=)])