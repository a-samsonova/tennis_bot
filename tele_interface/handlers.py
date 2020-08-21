from .utils import (handler_decor,
                    get_available_dt_time4ind_train, select_tr_days_for_skipping,
                    get_potential_days_for_group_training, )
from base.utils import (construct_main_menu,
                        construct_dt_menu,
                        construct_time_menu_for_group_lesson,
                        construct_time_menu_4ind_lesson,
                        from_digit_to_month, send_message, )
from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup,)
from .manage_data import (
    SELECT_SKIP_TIME_BUTTON,
    SELECT_GROUP_LESSON_TIME,
    SELECT_PRECISE_GROUP_TIME,
    from_eng_to_rus_day_week,
    SELECT_TRAINING_TYPE,
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_IND_LESSON_TIME,
    SELECT_PRECISE_IND_TIME,
    PERMISSION_FOR_IND_TRAIN, CONFIRM_GROUP_LESSON,
)
from calendar import monthrange
from tennis_bot.config import ADMIN_TELEGRAM_TOKEN
from datetime import date, datetime, timedelta
from django.db.models import Q
from base.utils import DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT

from telegram import (
    InlineKeyboardButton as inline_button,
    InlineKeyboardMarkup as inline_markup,
)

import re
import telegram
import calendar


def update_user_info(update, user):
    user_details = update.message.from_user if update.message else None

    if user_details:
        user.is_blocked = False
        user.telegram_username = user_details.username[:64] if user_details.username else ''
        user.save()


@handler_decor()
def start(bot, update, user):
    update_user_info(update, user)


@handler_decor()
def get_personal_data(bot, update, user):
    text = update.message.text
    phone_number_candidate = re.findall(r'\d+', text)
    if phone_number_candidate:
        if len(phone_number_candidate[0]) != 11:
            bot.send_message(user.id, 'Неправильный формат данных, было введено {} цифр.'.
                             format(len(phone_number_candidate[0])))
        else:
            user.phone_number = int(phone_number_candidate[0])
            user.save()
            bot.send_message(user.id,
                             'Как только тренер подтвердит твою кандидатуру, я напишу.',
                             reply_markup=construct_main_menu())
            admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
            admins = User.objects.filter(is_staff=True)

            for admin in admins:
                admin_bot.send_message(admin.id,
                                       # todo: сделать вместо ссылки кнопки при отправке этого сообешния
                                       'Пришел новый клиент:\n<b>{}</b>\n<a href="http://vladlen82.fvds.ru/admin/base/user/{}/change/">Настроить данные </a>'.format(
                                           user, user.id),
                                       parse_mode='HTML')

    else:
        if user.last_name and user.first_name and user.phone_number:
            bot.send_message(user.id, 'Контактные данные уже есть.')
        else:
            last_name, first_name = text.split(' ')
            user.last_name = last_name
            user.first_name = first_name
            user.save()
            bot.send_message(user.id, 'Введи номер телефона в формате "89991112233" (11 цифр подряд).')


@handler_decor(check_status=True)
def user_main_info(bot, update, user):
    """посмотреть, основную инфу:
        статус
        группа, если есть
        отыгрыши
        сколько должен заплатить
    """

    from_user_to_intro = {
        User.STATUS_WAITING: 'в листе ожидания.',
        User.STATUS_TRAINING: 'тренируешься в группе.',
        User.STATUS_FINISHED: 'закончил тренировки.',
        User.STATUS_ARBITRARY: 'тренируешься по свободному графику.'
    }

    intro = f'В данный момент ты {from_user_to_intro[user.status]}\n\n'

    group = TrainingGroup.objects.filter(users__in=[user]).exclude(max_players=1).first()

    teammates = group.users.values('first_name', 'last_name') if group else []

    group_info = "Твоя группа:\n{}\n\n".format(
        '\n'.join([' ' + x['first_name'] + ' ' + x['last_name'] for x in teammates])) if teammates else ''

    number_of_add_games = 'Количество отыгрышей: <b>{}</b>\n\n'.format(user.bonus_lesson)

    today = date.today()
    number_of_days_in_month = monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)
    number_of_days_in_next_month = monthrange(next_month.year, next_month.month)[1]
    last_day_in_next_month = date(next_month.year, next_month.month, number_of_days_in_next_month)

    tr_days_num = GroupTrainingDay.objects.filter(Q(group__users__in=[user]) | Q(visitors__in=[user]),
                                                  is_available=True,
                                                  date__gte=next_month,
                                                  date__lte=last_day_in_next_month).count()
    should_pay_money = tr_days_num * User.tarif_for_status[user.status]
    should_pay_info = 'В следующем месяце ({}) <b>нужно заплатить {} ₽</b>.'.format(
        from_digit_to_month[next_month.month], should_pay_money)

    text = intro + group_info + number_of_add_games + should_pay_info

    bot.send_message(user.id,
                     text,
                     parse_mode='HTML',
                     reply_markup=construct_main_menu())


@handler_decor(check_status=True)
def skip_lesson(bot, update, user):
    available_grouptraining_dates = select_tr_days_for_skipping(user)
    if available_grouptraining_dates:
        buttons = construct_dt_menu(SELECT_SKIP_TIME_BUTTON + '*' + str(date.today().month),
                                    available_grouptraining_dates)
        bot.send_message(user.id,
                         'Выбери дату тренировки для отмены.',
                         reply_markup=buttons)
    else:
        bot.send_message(user.id,
                         'Пока что нечего пропускать.')


@handler_decor()
def choose_dt_for_cancel(bot, update, user):
    date_btn, date_type = update.callback_query.data[len(SELECT_SKIP_TIME_BUTTON):].split('|')
    date_dt = datetime.strptime(date_btn, DT_BOT_FORMAT)
    if date_type == 'day':
        training_day = GroupTrainingDay.objects.filter(Q(group__users__in=[user]) | Q(visitors__in=[user]),
                                                       date=date_dt).order_by('id').distinct('id').first()
        if user in training_day.visitors.all():  # проверяем его ли эта группа или он удаляется из занятия другой группы
            training_day.visitors.remove(user)
        else:
            training_day.absent.add(user)
        bot.edit_message_text('Окей, занятие {} отменено'.format(date_btn),
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id)
        user.bonus_lesson += 1
        user.save()
    else:
        available_grouptraining_dates = select_tr_days_for_skipping(user)
        buttons = construct_dt_menu(SELECT_SKIP_TIME_BUTTON + '*' + str(date_dt.month),
                                    available_grouptraining_dates, date=date_dt)
        bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=buttons)


@handler_decor(check_status=True)
def choose_type_of_training(bot, update, user):
    buttons = [[
        inline_button('Индивидуальная', callback_data=SELECT_TRAINING_TYPE + 'ind')
    ], [
        inline_button('Групповая', callback_data=SELECT_TRAINING_TYPE + 'group')
    ]]
    text = 'Выбери тип тренировки.'
    if update.callback_query:
        bot.edit_message_text(
            text,
            reply_markup=inline_markup(buttons),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
        )
    else:
        bot.send_message(user.id,
                         text,
                         reply_markup=inline_markup(buttons))


@handler_decor(check_status=True)
def take_lesson(bot, update, user):
    """записаться на тренировку"""
    tr_type = update.callback_query.data[len(SELECT_TRAINING_TYPE):]
    if tr_type == 'group':

        potential_free_places = get_potential_days_for_group_training(user)
        potential_free_places = potential_free_places.filter(date__gt=datetime.now())
        days_with_free_places = list(set([x.date for x in potential_free_places]))
        buttons = construct_dt_menu(SELECT_GROUP_LESSON_TIME + '*' + str(date.today().month),
                                    days_with_free_places)
        if user.bonus_lesson > 0:
            text = 'Выбери тренировку для записи.\n' \
                   'Пожертвуешь одним отыгрышем.'
        else:
            text = '⚠️ATTENTION⚠️\n' \
                   'В данный момент у тебя нет отыгрышей.\n' \
                   '<b> Занятие будет стоить 600₽ </b>'
        bot.edit_message_text(
            text,
            reply_markup=buttons,
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            parse_mode='HTML',
        )
    else:
        buttons = [[
            inline_button('1 час', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.0')
        ], [
            inline_button('1.5 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.5')
        ], [
            inline_button('2 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '2.0')
        ], [
            inline_button('⬅️ назад',
                          callback_data='Записаться на занятие'),
        ]]

        bot.edit_message_text(
            'Выбери продолжительность занятия',
            reply_markup=inline_markup(buttons),
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id,
            parse_mode='HTML',
        )


@handler_decor()
def select_dt_for_ind_lesson(bot, update, user):
    duration = float(update.callback_query.data[len(SELECT_DURATION_FOR_IND_TRAIN):])
    available_days, _ = get_available_dt_time4ind_train(duration)

    if available_days:
        buttons = construct_dt_menu(SELECT_IND_LESSON_TIME + '|' + str(duration) + '*' + str(available_days[0].month),
                                    available_days)

        bot.edit_message_text('Выбери дату тренировки.',
                              reply_markup=buttons,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,)
    else:
        bot.edit_message_text('В данный момент нет доступных дней для записи.',
                              reply_markup=None,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              )


@handler_decor()
def choose_dt_time_for_ind_train(bot, update, user):
    date_btn, date_type = update.callback_query.data[len(SELECT_IND_LESSON_TIME)+4:].split('|')
    _, duration = update.callback_query.data[:len(SELECT_IND_LESSON_TIME)+4].split('|')
    date_dt = datetime.strptime(date_btn, DT_BOT_FORMAT)
    available_days, date_time_dict = get_available_dt_time4ind_train(float(duration))
    poss_time_for_train = []

    if date_type == 'day':
        for i in range(len(date_time_dict[date_dt.date()]) - int(float(duration) * 2)):
            if datetime.combine(date_dt.date(), date_time_dict[date_dt.date()][i + int(float(duration) * 2)]) - datetime.combine(
                    date_dt.date(), date_time_dict[date_dt.date()][i]) == timedelta(hours=float(duration)):
                poss_time_for_train.append(date_time_dict[date_dt.date()][i])
        buttons = construct_time_menu_4ind_lesson(SELECT_PRECISE_IND_TIME, poss_time_for_train, date_btn,
                                                  float(duration), user)

        bot.edit_message_text('Выбери время',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=buttons)
    else:
        buttons = construct_dt_menu(SELECT_IND_LESSON_TIME + '|' + str(duration) + '*' + str(date_dt.month),
                                    available_days, date=date_dt)
        bot.edit_message_reply_markup(chat_id=update.callback_query.message.chat_id,
                                      message_id=update.callback_query.message.message_id,
                                      reply_markup=buttons)


@handler_decor()
def select_precise_ind_lesson_time(bot, update, user):
    day_dt, start_time, end_time = update.callback_query.data[len(SELECT_PRECISE_IND_TIME):].split('|')
    date_dt = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj = datetime.strptime(start_time, '%H:%M:%S')
    end_time_obj = datetime.strptime(end_time, '%H:%M:%S')
    duration = end_time_obj - st_time_obj

    day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_dt.date().weekday()]]

    group, _ = TrainingGroup.objects.get_or_create(name=user.first_name+user.last_name,
                                                   max_players=1)

    tr_day = GroupTrainingDay.objects.create(group=group, date=date_dt, start_time=st_time_obj, duration=duration)

    bot.edit_message_text(f"Сообщу тренеру, что ты хочешь прийти на индивидуальное занятие"
                          f" <b>{day_dt} ({day_of_week}) </b>\n"
                          f"Время: <b>{start_time} — {end_time}</b>",
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML')

    admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
    admins = User.objects.filter(is_staff=True, is_blocked=False)
    buttons = [[
        inline_button('Да', callback_data=f"{PERMISSION_FOR_IND_TRAIN}yes|{user.id}|{tr_day.id}")
    ], [
        inline_button('Нет', callback_data=f"{PERMISSION_FOR_IND_TRAIN}no|{user.id}|{tr_day.id}")
    ]]
    text = f"<b>{user.first_name} {user.last_name} — {user.phone_number}</b>\n" \
           f"Хочет прийти на индивидуальное занятие <b>{day_dt} ({day_of_week}) </b>" \
           f" в <b>{start_time} — {end_time}</b>\n" \
           f"<b>Разрешить?</b>"

    send_message(admins, text, admin_bot, markup=inline_markup(buttons))


@handler_decor()
def choose_dt_for_group_lesson(bot, update, user):
    date_btn, date_type = update.callback_query.data[len(SELECT_GROUP_LESSON_TIME):].split('|')
    date_dt = datetime.strptime(date_btn, DT_BOT_FORMAT)

    potential_free_places = get_potential_days_for_group_training(user)

    if date_type == 'day':

        training_days = potential_free_places.filter(date=date_dt)
        buttons = construct_time_menu_for_group_lesson(SELECT_PRECISE_GROUP_TIME, training_days)

        day_of_week = calendar.day_name[date_dt.weekday()]
        bot.edit_message_text(f'Выбери время занятия на {date_btn} ({from_eng_to_rus_day_week[day_of_week]}).',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=buttons)
    else:
        potential_free_places = potential_free_places.filter(date__gt=datetime.now())
        days_with_free_places = list(set([x.date for x in potential_free_places]))

        buttons = construct_dt_menu(SELECT_GROUP_LESSON_TIME + '*' + str(date_dt.month),
                                    days_with_free_places, date=date_dt)

        bot.edit_message_text('Выбери тренировку для записи.',
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=buttons)


@handler_decor()
def select_precise_group_lesson_time(bot, update, user):
    """
    после того, как выбрал точное время для групповой тренировки,
    показываем инфу об этом дне с кнопкой записаться и назад
    :param bot:
    :param update:
    :param user:
    :return:
    """

    tr_day_id = update.callback_query.data[len(SELECT_PRECISE_GROUP_TIME):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)
    start_time = tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    end_time = (datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration).strftime(
        TM_TIME_SCHEDULE_FORMAT)

    day_of_week = calendar.day_name[tr_day.date.weekday()]

    #сколько сейчас свободных мест
    n_free_places = tr_day.group.max_players - tr_day.visitors.count() + tr_day.absent.count() - tr_day.group.users.count()
    all_players = tr_day.group.users.union(tr_day.visitors.all()).difference(tr_day.absent.all()).values('first_name',
                                                                                                         'last_name')

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))
    text = f'{tr_day.group.name}\n' \
           f'📅Дата: <b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]})</b>\n' \
           f'⏰Время: <b>{start_time} — {end_time}</b>\n\n' \
           f'👥Присутствующие:\n{all_players}\n\n' \
           f'Свободных мест: {n_free_places}'

    buttons = [[
        inline_button('Записаться', callback_data=f"{CONFIRM_GROUP_LESSON}{tr_day_id}")
    ], [
        inline_button('⬅️ назад',
                      callback_data=SELECT_GROUP_LESSON_TIME + tr_day.date.strftime(DT_BOT_FORMAT) + '|month')
    ]]

    bot.edit_message_text(
        text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode='HTML',
        reply_markup=inline_markup(buttons)
    )



@handler_decor()
def confirm_group_lesson(bot, update, user):
    tr_day_id = update.callback_query.data[len(CONFIRM_GROUP_LESSON):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)
    start_time = tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    end_time = (datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration).strftime(
        TM_TIME_SCHEDULE_FORMAT)

    day_of_week = calendar.day_name[tr_day.date.weekday()]

    n_free_places = tr_day.group.max_players - tr_day.visitors.count() + tr_day.absent.count() - tr_day.group.users.count()

    if n_free_places:
        tr_day.visitors.add(user)

        text = f'Записал тебя на <b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]})</b>\n' \
               f'Время: <b>{start_time} — {end_time}</b>'

        markup = None

        if user.bonus_lesson > 0:
            user.bonus_lesson -= 1
            user.save()
    else:
        text = 'Упс, похоже уже не осталось свободных мест на это время, выбери другое.'
        buttons = [[
            inline_button('⬅️ назад',
                          callback_data=SELECT_GROUP_LESSON_TIME + tr_day.date.strftime(DT_BOT_FORMAT) + '|month')
        ]]
        markup = inline_markup(buttons)

    bot.edit_message_text(
        text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )