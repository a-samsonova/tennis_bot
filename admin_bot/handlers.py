import datetime

import telegram

from base.models import Channel, User, GroupTrainingDay
from base.utils import DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN
from .utils import admin_handler_decor


@admin_handler_decor()
def start(bot, update, user):
    update.message.reply_text(
        "Привет! я переехал на @TennisTula_bot",
        parse_mode='HTML',
    )


@admin_handler_decor()
def permission_for_ind_train(bot, update, user):
    permission, user_id, tr_day_id = update.callback_query.data[len(PERMISSION_FOR_IND_TRAIN):].split('|')

    bot_token = Channel.objects.get(code='tennis').token
    tennis_bot = telegram.Bot(bot_token)

    player = User.objects.get(id=user_id)
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)

    start_time = tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    end_time = (datetime.datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration).time().strftime(TM_TIME_SCHEDULE_FORMAT)

    if permission == 'yes':
        admin_text = 'Отлично, приятной тренировки!'

        user_text = f'Отлично, тренер подтвердил тренировку <b>{tr_day.date.strftime(DT_BOT_FORMAT)}</b>\n' \
                    f'Время: <b>{start_time} — {end_time}</b>\n' \
                    f'Не забудь!'

    else:
        admin_text = 'Хорошо, сообщу игроку, что тренировка отменена.'

        user_text = f'Внимание!!! Индивидуальная тренировка <b> {tr_day.date.strftime(DT_BOT_FORMAT)}</b>\n' \
                    f'в <b>{start_time} — {end_time}</b>\n' \
                    f'<b>ОТМЕНЕНА</b>'

        tr_day.delete()

    bot.edit_message_text(
        admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
    )

    tennis_bot.send_message(
        player.id,
        user_text,
        parse_mode='HTML'
    )
