import calendar

from base.models import User, GroupTrainingDay
from base.utils import DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT, construct_admin_main_menu, construct_dt_menu
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN, SELECT_DAY_TO_SHOW_COACH_SCHEDULE, SHOW_GROUPDAY_INFO, \
    from_eng_to_rus_day_week
from .utils import admin_handler_decor, day_buttons_coach_info
from tennis_bot.config import TELEGRAM_TOKEN
from datetime import date, datetime
from telegram import (InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark,)

import datetime
import telegram


@admin_handler_decor()
def start(bot, update, user):
    update.message.reply_text(
        "Привет! я переехал на @TennisTula_bot",
        parse_mode='HTML',
        reply_markup=construct_admin_main_menu(),
    )


@admin_handler_decor()
def permission_for_ind_train(bot, update, user):
    permission, user_id, tr_day_id = update.callback_query.data[len(PERMISSION_FOR_IND_TRAIN):].split('|')

    tennis_bot = telegram.Bot(TELEGRAM_TOKEN)

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
        reply_markup=construct_admin_main_menu()
    )

    tennis_bot.send_message(
        player.id,
        user_text,
        parse_mode='HTML'
    )


@admin_handler_decor()
def show_coach_schedule(bot, update, user):
    tr_days = [x['date'] for x in GroupTrainingDay.objects.all().distinct('date').values('date')]
    buttons = construct_dt_menu(SELECT_DAY_TO_SHOW_COACH_SCHEDULE + '*' + str(date.today().month), tr_days)
    bot.send_message(user.id,
                     'Тренировочные дни',
                     reply_markup=buttons)


@admin_handler_decor()
def choose_dt_for_coach_time_schedule(bot, update, user):
    date_btn, date_type = update.callback_query.data[len(SELECT_DAY_TO_SHOW_COACH_SCHEDULE):].split('|')
    date_dt = datetime.datetime.strptime(date_btn, DT_BOT_FORMAT)
    if date_type == 'day':
        tr_days = GroupTrainingDay.objects.filter(date=date_dt).select_related('group').order_by('start_time')
        buttons = day_buttons_coach_info(tr_days, SHOW_GROUPDAY_INFO)

        day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_dt.date().weekday()]]
        bot.edit_message_text('📅{} ({})'.format(date_btn, day_of_week),
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=buttons)

    else:
        all_tr_days = [x['date'] for x in GroupTrainingDay.objects.all().distinct('date').values('date')]
        buttons = construct_dt_menu(SELECT_DAY_TO_SHOW_COACH_SCHEDULE + '*' + str(date_dt.month),
                                    all_tr_days, date=date_dt)
        bot.edit_message_text(text='Тренировочные дни',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=buttons)


def info_about_users(users):
    """
    :param users: User instance
    :return: (first_name + last_name + \n){1,} -- str
    """
    return '\n'.join(
            ('👤' + x['first_name'] + ' ' + x['last_name'] for x in users.values('first_name', 'last_name')))


@admin_handler_decor()
def show_traingroupday_info(bot, update, user):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    availability = '❌нет тренировки❌\n' if not tr_day.is_available else ''
    affiliation = '🧔🏻моя тренировка🧔🏻\n\n' if tr_day.tr_day_status == GroupTrainingDay.MY_TRAIN_STATUS else '👥аренда👥\n\n'

    group_name = f"{tr_day.group.name}\n"

    if tr_day.group.max_players > 1:
        group_players = f'Игроки группы:\n{info_about_users(tr_day.group.users)}\n'
        visitors = f'\n➕Пришли из других:\n{info_about_users(tr_day.visitors)}\n' if tr_day.visitors.count() else ''
        absents = f'\n➖Отсутствуют:\n{info_about_users(tr_day.absent)}\n' if tr_day.absent.count() else ''
    else:
        group_players = ''
        visitors = ''
        absents = ''

    end_time = datetime.datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration
    time = f'{tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[tr_day.date.weekday()]]

    general_info = f'<b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({day_of_week})\n{time}</b>' + '\n' + availability + affiliation
    users_info = group_name + group_players + visitors + absents
    text = general_info + users_info

    buttons = [[
        inlinebutt('⬅️ назад',
                   callback_data=f"{SELECT_DAY_TO_SHOW_COACH_SCHEDULE}{tr_day.date.strftime(DT_BOT_FORMAT)}|day"),
    ]]

    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=inlinemark(buttons))
