import calendar

from base.models import User, GroupTrainingDay
from base.utils import construct_admin_main_menu, DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN, SHOW_GROUPDAY_INFO, \
    from_eng_to_rus_day_week, CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, CLNDR_NEXT_MONTH, CLNDR_DAY, CLNDR_IGNORE, \
    CLNDR_PREV_MONTH
from tele_interface.utils import create_calendar, separate_callback_data, create_callback_data
from .utils import admin_handler_decor, day_buttons_coach_info
from tennis_bot.config import TELEGRAM_TOKEN
from datetime import date, datetime, timedelta
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

    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id)

    if tr_day.count():
        tr_day = tr_day.first()
        start_time = tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
        end_time = (datetime.datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration).time().strftime(
            TM_TIME_SCHEDULE_FORMAT)

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

        tennis_bot.send_message(
            player.id,
            user_text,
            parse_mode='HTML'
        )

    else:
        admin_text = 'Тренировка уже отменена.'

    bot.edit_message_text(
        admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
    )


def admin_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = date(int(year), int(month), 1)

    dates_highlight = None
    if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
        dates_highlight = list(GroupTrainingDay.objects.filter(is_available=True).values_list('date', flat=True))

    if action == CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == CLNDR_DAY:
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id
                              )
        return True, purpose, date(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(pre.year), int(pre.month), dates_highlight))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(ne.year), int(ne.month), dates_highlight))
    elif action == CLNDR_ACTION_BACK:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            text = 'Тренировочные дни'
        else:
            text = 'Тренировочные дни'

        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(year), int(month), dates_highlight))
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@admin_handler_decor()
def inline_calendar_handler(bot, update, user):
    selected, purpose, date_my = admin_calendar_selection(bot, update)
    if selected:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            tr_days = GroupTrainingDay.objects.filter(date=date_my).select_related('group').order_by('start_time')
            if tr_days.count():
                markup = day_buttons_coach_info(tr_days, SHOW_GROUPDAY_INFO)

                day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_my.weekday()]]
                text = '📅{} ({})'.format(date_my, day_of_week)
            else:
                tr_days = list(GroupTrainingDay.objects.filter(is_available=True).values_list('date', flat=True))
                text = 'Нет тренировок в этот день'
                markup = create_calendar(purpose, date_my.year, date_my.month, tr_days)
        bot.edit_message_text(text,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=markup,
                              parse_mode='HTML')


@admin_handler_decor()
def show_coach_schedule(bot, update, user):
    tr_days = list(GroupTrainingDay.objects.filter(is_available=True).values_list('date', flat=True))
    bot.send_message(user.id,
                     'Тренировочные дни',
                     reply_markup=create_calendar(CLNDR_ADMIN_VIEW_SCHEDULE, dates_to_highlight=tr_days))


def info_about_users(users, for_admin=False):
    """
    :param for_admin: show info for admin or not (number instead of smile)
    :param users: User instance
    :return: (first_name + last_name + \n){1,} -- str
    """
    if for_admin:
        return '\n'.join(
            (f"{i + 1}. {x['first_name']} {x['last_name']}" for i, x in enumerate(users.values('first_name', 'last_name'))))
    else:
        return '\n'.join(
                (f"👤{x['first_name']} {x['last_name']}" for i, x in enumerate(users.values('first_name', 'last_name'))))


@admin_handler_decor()
def show_traingroupday_info(bot, update, user):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    availability = '❌нет тренировки❌\n' if not tr_day.is_available else ''
    is_individual = '🧑🏻‍🦯индивидуальная🧑🏻‍🦯\n' if tr_day.is_individual else '🤼‍♂️групповая🤼‍♂️\n'
    affiliation = '🧔🏻моя тренировка🧔🏻\n\n' if tr_day.tr_day_status == GroupTrainingDay.MY_TRAIN_STATUS else '👥аренда👥\n\n'

    group_name = f"{tr_day.group.name}\n"

    if not tr_day.is_individual:
        group_players = f'Игроки группы:\n{info_about_users(tr_day.group.users.all().difference(tr_day.absent.all()), for_admin=True)}\n'
        visitors = f'\n➕Пришли из других:\n{info_about_users(tr_day.visitors, for_admin=True)}\n' if tr_day.visitors.count() else ''
        absents = f'\n➖Отсутствуют:\n{info_about_users(tr_day.absent, for_admin=True)}\n' if tr_day.absent.count() else ''
    else:
        group_players = ''
        visitors = ''
        absents = ''

    end_time = datetime.datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration
    time = f'{tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[tr_day.date.weekday()]]

    general_info = f'<b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({day_of_week})\n{time}</b>' + '\n' + availability + is_individual + affiliation
    users_info = group_name + group_players + visitors + absents
    text = general_info + users_info

    buttons = [[
        inlinebutt('⬅️ назад',
                   callback_data=create_callback_data(CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_DAY, tr_day.date.year, tr_day.date.month, tr_day.date.day)),
    ]]

    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=inlinemark(buttons))
