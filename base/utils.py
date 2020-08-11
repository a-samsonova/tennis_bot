import datetime
import re
from calendar import monthrange

from telegram import (ReplyKeyboardMarkup,
                      InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark,)

from tele_interface.manage_data import (
    SELECT_GROUP_LESSON_TIME,
    SELECT_IND_LESSON_TIME,
    SELECT_TRAINING_TYPE,)

DTTM_BOT_FORMAT = '%Y.%m.%d.%H.%M'
DT_BOT_FORMAT = '%Y.%m.%d'
TM_HOUR_BOT_FORMAT = '%H'
TM_DAY_BOT_FORMAT = '%d'
TM_TIME_SCHEDULE_FORMAT = '%H:%M'


def construct_main_menu():
    return ReplyKeyboardMarkup([
        ['Мои данные'],
        ['Пропустить занятие', 'Записаться на занятие']],
        resize_keyboard=True)


def construct_dt_menu(button_text, dates, date=None):
    if date is None:
        date = datetime.datetime.now().replace(hour=0, minute=0, second=0)
    else:
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
    button_info, month = button_text.split('*')
    months = sorted(list(set([x.month for x in dates])))
    if int(month) not in months:
        month = str((int(month) + 1) % 12)
        date = date - datetime.timedelta(days=date.day - monthrange(date.year, date.month)[1]-1)
    button_text = button_info
    posting_dttms = sorted([x for x in dates if x.month == int(month)])
    buttons = []
    row = []
    for dttm in posting_dttms:
        row.append(
            inlinebutt(dttm.strftime(TM_DAY_BOT_FORMAT),
                       callback_data=button_text + dttm.strftime(DT_BOT_FORMAT) + '|day')
        )

        if len(row) >= 5:
            buttons.append(row)
            row = []

    if len(row):
        buttons.append(row)

    number_of_days_in_month = monthrange(date.year, date.month)[1]
    day = date.day
    prev_dt = date - datetime.timedelta(days=day + 1)
    next_dt = date + datetime.timedelta(days=number_of_days_in_month-day + 1)

    from_digit_to_month = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
        7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь',
    }

    if len(months) > 1:
        if months.index(int(month)) == 0:
            buttons.append([
                inlinebutt(from_digit_to_month[date.month], callback_data='None'),
                inlinebutt(from_digit_to_month[next_dt.month] + ' ➡️',
                           callback_data=button_text + next_dt.strftime(DT_BOT_FORMAT) + '|month'),
            ])
        elif months.index(int(month)) == len(months)-1:
            buttons.append([
                inlinebutt('⬅️ ' + from_digit_to_month[prev_dt.month],
                           callback_data=button_text + prev_dt.strftime(DT_BOT_FORMAT) + '|month'),
                inlinebutt(from_digit_to_month[date.month], callback_data='None'),
            ])
        else:
            buttons.append([
                inlinebutt('⬅️ ' + from_digit_to_month[prev_dt.month],
                           callback_data=button_text + prev_dt.strftime(DT_BOT_FORMAT) + '|month'),
                inlinebutt(from_digit_to_month[date.month], callback_data='None'),
                inlinebutt(from_digit_to_month[next_dt.month] + ' ➡️',
                           callback_data=button_text + next_dt.strftime(DT_BOT_FORMAT) + '|month'),
            ])
    elif len(months) == 1:
        buttons.append([
            inlinebutt(from_digit_to_month[date.month], callback_data='None')
        ])
    back_data = SELECT_TRAINING_TYPE + 'ind' if re.findall(r'^{}'.format(SELECT_IND_LESSON_TIME),
                                                           button_info) else 'Записаться на занятие'

    buttons.append([
        inlinebutt('⬅️ назад',
                   callback_data=back_data),
    ])
    return inlinemark(buttons)


def construct_time_menu_for_group_lesson(button_text, tr_days):
    buttons = []
    row = []
    for day in tr_days:

        end_time = (datetime.datetime.combine(day.date, day.start_time)+day.duration).strftime(TM_TIME_SCHEDULE_FORMAT)
        row.append(
            inlinebutt(f'{day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time}',
                       callback_data=button_text + str(day.id))
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt('⬅️ назад',
                   callback_data=SELECT_GROUP_LESSON_TIME + tr_days[0].date.strftime(DT_BOT_FORMAT) + '|month'),
    ])

    return inlinemark(buttons)


def construct_time_menu_4ind_lesson(button_text, poss_training_times: list, day: datetime.date, duration: float, user):
    buttons = []
    row = []
    for start_time in poss_training_times:

        end_time = datetime.datetime.combine(datetime.datetime.strptime(day, DT_BOT_FORMAT), start_time) + datetime.timedelta(hours=duration)
        row.append(
            inlinebutt(f'{start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}',
                       callback_data=f"{button_text}{day}|{start_time}|{end_time.time()}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt('⬅️ назад',
                   callback_data=f"{SELECT_IND_LESSON_TIME}|{duration}{day}|month"),
    ])

    return inlinemark(buttons)