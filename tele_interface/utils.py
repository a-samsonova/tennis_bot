import calendar
import datetime
from datetime import date, time, timedelta, datetime
from functools import wraps

from django.db.models import (ExpressionWrapper,
                              F, Q,
                              DateTimeField,
                              Count,
                              DurationField)
from django.db.models.functions import TruncDate
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton as inlinebutt, \
    InlineKeyboardMarkup as inlinemark

from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup,)
from base.utils import TM_TIME_SCHEDULE_FORMAT, from_digit_to_month, DT_BOT_FORMAT
from tele_interface.manage_data import SHOW_INFO_ABOUT_SKIPPING_DAY, from_eng_to_rus_day_week, CLNDR_IGNORE, CLNDR_DAY, \
    CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH, CLNDR_ACTION_BACK, CLNDR_ACTION_TAKE_IND

from tennis_bot.settings import DEBUG

import telegram
import sys
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def handler_decor(check_status=False):
    """
    декоратор для всех handlers в телеграм боте
    :param check_status:
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
            try:
                user = User.objects.get(
                    id=user_details.id,
                )

            except User.DoesNotExist:
                user = User.objects.create(
                    username='{}'.format(user_details.id),
                    id=user_details.id,
                    telegram_username=user_details.username[:64] if user_details.username else '',
                    first_name=user_details.first_name[:30] if user_details.first_name else '',
                    last_name=user_details.last_name[:60] if user_details.last_name else '',
                    password='1',
                )
                bot.send_message(user.id, 'Привет! Я бот самого продвинутого тренера в Туле (России).\
                 Для дальнейшей работы нужно указать свои контактные данные.')
                bot.send_message(user.id,
                                 'Введи фамилию и имя через пробел в формате "Фамилия Имя", например: Иванов Иван.')

            if user.is_blocked:
                user.is_blocked = False
                user.save()

            else:
                try:
                    if check_status:
                        if user.status != User.STATUS_WAITING and user.status != User.STATUS_FINISHED:
                            res = func(bot, update, user)
                        else:
                            bot.send_message(user.id, 'Тренер еще не одобрил.')
                    else:
                        res = func(bot, update, user)
                except telegram.error.BadRequest as error:
                    if 'Message is not modified:' in error.message:
                        pass
                    else:
                        res = [bot.send_message(user.id, 'упс')]
                        tb = sys.exc_info()[2]
                        raise error.with_traceback(tb)
                except Exception as e:

                    res = [bot.send_message(user.id, e)]
                    tb = sys.exc_info()[2]
                    raise e.with_traceback(tb)

            return
        return wrapper
    return decor


def create_callback_data(purpose, action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([purpose, action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def get_available_dt_time4ind_train(duration: float):
    # todo: какой-то пиздец, без пол литра не разберешься, хз шо с этим делать
    poss_date = date.today()
    start_time = time(8, 0, 0)

    possible_times = []
    for i in range(8, 21): #занятия могут идти с 8 до 20
        for minute in [0, 30]: #с интервалом 30 минут
            possible_times.append(time(i, minute))
    del possible_times[-1]

    possible_dates = [poss_date]
    for _ in range(30): #для индивидуальных тренировок запись доступна примерно на месяц вперед
        poss_date += timedelta(days=1)
        possible_dates.append(poss_date)

    #почему я ищу только среди существующих tr_days --- хз
    tr_days = GroupTrainingDay.objects.filter(date__in=possible_dates, start_time__gte=start_time).annotate(
        end_time=ExpressionWrapper(F('start_time') + F('duration'), output_field=DateTimeField()),
        date_tmp=TruncDate('date')).values('date_tmp', 'start_time', 'end_time').order_by('date', 'start_time')

    #todo: полное копирование списка, мдэээ, надо что-то с этим делать
    poss_date_time_dict = {day['date_tmp']: possible_times[:] for day in tr_days}

    for day in tr_days:
        times_to_remove = []
        start = day['start_time']
        while start < day['end_time']:
            if start.minute == 0:
                start = time(start.hour, 30)
            elif start.minute == 30:
                hour = start.hour + 1
                start = time(hour, 0)
            times_to_remove.append(start)
        del times_to_remove[-1]
        for x in times_to_remove:
            if x in poss_date_time_dict[day['date_tmp']]:
                poss_date_time_dict[day['date_tmp']].remove(x)

    poss_date_for_train = []
    for poss_date in poss_date_time_dict:
        for i in range(len(poss_date_time_dict[poss_date]) - int(duration * 2)):
            if datetime.combine(poss_date, poss_date_time_dict[poss_date][i + int(duration * 2)]) - datetime.combine(
                    poss_date, poss_date_time_dict[poss_date][i]) == timedelta(hours=duration):
                poss_date_for_train.append(poss_date)
    available_days = sorted(list(set(poss_date_for_train)))

    return available_days, poss_date_time_dict


def select_tr_days_for_skipping(user):
    tmp = GroupTrainingDay.objects.filter(Q(group__users__in=[user]) | Q(visitors__in=[user]),
                                          date__gte=date.today()).exclude(
        absent__in=[user]).order_by('id').distinct(
        'id').values('date', 'start_time')
    available_grouptraining_dates = [x['date'] for x in tmp  # учитываем время до отмены, вычитаем 3 часа, т.к. на сервере -3 часа
                                     if datetime.combine(x['date'],
                                                         x['start_time']) - datetime.now() - timedelta(hours=3) >
                                     user.time_before_cancel]
    return available_grouptraining_dates


def get_potential_days_for_group_training(user):
    potential_free_places = GroupTrainingDay.objects.annotate(
        Count('absent', distinct=True),
        Count('group__users', distinct=True),
        Count('visitors', distinct=True),
        max_players=F('group__max_players'),
        diff=ExpressionWrapper(F('start_time') + F('date') - datetime.now() - timedelta(hours=3),
                               output_field=DurationField())).filter(
                                                                    max_players__gt=F('visitors__count') + F('group__users__count') - F('absent__count'),
                                                                    diff__gte=timedelta(hours=1),
                                                                    group__status=TrainingGroup.STATUS_GROUP,
                                                                    ).exclude(
                                                                            visitors__in=[user]).order_by('start_time')

    return potential_free_places


def create_calendar(purpose_of_calendar, year=None, month=None, dates_to_highlight=None):
    """
    Create an inline keyboard with the provided year and month
    :param list of dates dates_to_highlight : date we should highlight, e.g. days available for skipping
    :param str purpose_of_calendar: e.g. skipping, taking lesson
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = datetime.now()
    if year is None: year = now.year
    if month is None: month = now.month
    data_ignore = create_callback_data(purpose_of_calendar, CLNDR_IGNORE, year, month, 0)
    keyboard = []
    # First row - Month and Year
    row = [InlineKeyboardButton(from_digit_to_month[month] + " " + str(year), callback_data=data_ignore)]
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:

            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                day_info = str(day)
                if dates_to_highlight and (date(year, month, day) in dates_to_highlight):
                    day_info = f'{str(day)}✅'
                row.append(InlineKeyboardButton(day_info, callback_data=create_callback_data(purpose_of_calendar, CLNDR_DAY, year, month, day)))
        keyboard.append(row)
    # Last row - Buttons
    row = [InlineKeyboardButton("<", callback_data=create_callback_data(purpose_of_calendar, CLNDR_PREV_MONTH, year, month, day)),
           InlineKeyboardButton(" ", callback_data=data_ignore),
           InlineKeyboardButton(">", callback_data=create_callback_data(purpose_of_calendar, CLNDR_NEXT_MONTH, year, month, day))]
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


def construct_time_menu_for_group_lesson(button_text, tr_days, date, purpose):
    buttons = []
    row = []
    for day in tr_days:

        end_time = (datetime.combine(day.date, day.start_time)+day.duration).strftime(TM_TIME_SCHEDULE_FORMAT)
        row.append(
            InlineKeyboardButton(f'{day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time}',
                                 callback_data=button_text + str(day.id))
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton('⬅️ назад',
                   callback_data=create_callback_data(purpose, CLNDR_ACTION_BACK, date.year, date.month, 0)),
    ])

    return InlineKeyboardMarkup(buttons)


def construct_detail_menu_for_skipping(training_day, purpose, group_name, group_players):
    end_time = datetime.combine(training_day.date, training_day.start_time) + training_day.duration
    time = f'{training_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[training_day.date.weekday()]]
    text = f'<b>{training_day.date.strftime(DT_BOT_FORMAT)} ({day_of_week})\n{time}\n</b>' + group_name + group_players

    buttons = [[
        InlineKeyboardButton('Пропустить', callback_data=SHOW_INFO_ABOUT_SKIPPING_DAY + f'{training_day.id}')
    ], [
        InlineKeyboardButton('⬅️ назад',
                             callback_data=create_callback_data(purpose, CLNDR_ACTION_BACK, training_day.date.year, training_day.date.month, 0))
    ]]
    return InlineKeyboardMarkup(buttons), text


def construct_time_menu_4ind_lesson(button_text, poss_training_times: list, day: datetime.date, duration: float, user):
    buttons = []
    row = []
    for start_time in poss_training_times:

        end_time = datetime.combine(day, start_time) + timedelta(hours=duration)
        row.append(
            inlinebutt(f'{start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}',
                       callback_data=f"{button_text}{day.strftime(DT_BOT_FORMAT)}|{start_time}|{end_time.time()}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt('⬅️ назад',
                   callback_data=create_callback_data(f'{CLNDR_ACTION_TAKE_IND}{duration}', CLNDR_ACTION_BACK, day.year, day.month, 0))
    ])

    return inlinemark(buttons)