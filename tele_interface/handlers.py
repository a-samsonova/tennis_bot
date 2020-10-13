from admin_bot.handlers import info_about_users
from .utils import (handler_decor,
                    get_available_dt_time4ind_train, select_tr_days_for_skipping,
                    get_potential_days_for_group_training, separate_callback_data, create_callback_data,
                    create_calendar, construct_time_menu_for_group_lesson, construct_detail_menu_for_skipping,
                    construct_time_menu_4ind_lesson, )
from base.utils import (construct_main_menu,
                        from_digit_to_month, send_message, DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT, )
from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup,)
from .manage_data import (
    SELECT_PRECISE_GROUP_TIME,
    from_eng_to_rus_day_week,
    SELECT_TRAINING_TYPE,
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_PRECISE_IND_TIME,
    PERMISSION_FOR_IND_TRAIN,
    CONFIRM_GROUP_LESSON,
    SHOW_INFO_ABOUT_SKIPPING_DAY, TAKE_LESSON_BUTTON, CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH,
    CLNDR_ACTION_BACK, CLNDR_ACTION_SKIP, CLNDR_ACTION_TAKE_GROUP, CLNDR_ACTION_TAKE_IND,
)
from calendar import monthrange
from tennis_bot.config import ADMIN_TELEGRAM_TOKEN
from datetime import date, datetime, timedelta
from django.db.models import Q

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
    bot.send_message(user.id, 'Я здесь', reply_markup=construct_main_menu())


@handler_decor()
def get_help(bot, update, user):
    bot.send_message(user.id, 'По всем вопросам пиши @ta2asho.\n'
                              'Желательно описывать свою проблему со скриншотами.', reply_markup=construct_main_menu())


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

    group_info = "Твоя группа -- {}:\n{}\n\n".format(group.name, info_about_users(teammates)) if teammates else ''

    number_of_add_games = 'Количество отыгрышей: <b>{}</b>\n\n'.format(user.bonus_lesson)

    today = date.today()
    first_day = today - timedelta(days=today.day - 1)
    number_of_days_in_month = monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)
    number_of_days_in_next_month = monthrange(next_month.year, next_month.month)[1]
    last_day_in_next_month = date(next_month.year, next_month.month, number_of_days_in_next_month)

    tr_days_this_month = GroupTrainingDay.objects.filter(date__gte=first_day, date__lte=last_day, is_available=True)
    tr_days_next_month = GroupTrainingDay.objects.filter(date__gte=next_month, date__lte=last_day_in_next_month, is_available=True)

    if user.status == User.STATUS_TRAINING:
        tr_days_num_this_month = tr_days_this_month.filter(group__users__in=[user],
                                                           group__status=TrainingGroup.STATUS_GROUP)
        tr_days_num_next_month = tr_days_next_month.filter(group__users__in=[user],
                                                           group__status=TrainingGroup.STATUS_GROUP)

    elif user.status == User.STATUS_ARBITRARY:
        tr_days_num_this_month = tr_days_this_month.filter(visitors__in=[user])
        tr_days_num_next_month = tr_days_next_month.filter(visitors__in=[user])

    balls_this_month = tr_days_this_month.filter(Q(visitors__in=[user]) | Q(group__users__in=[user])).count()

    balls_next_month = tr_days_num_next_month.filter(Q(visitors__in=[user]) | Q(group__users__in=[user])).count()

    should_pay_money_next = tr_days_num_next_month.count() * User.tarif_for_status[user.status]
    should_pay_this_month = tr_days_num_this_month.count() * User.tarif_for_status[user.status]
    should_pay_info = 'В этом месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи.</b>\n' \
                      'В следующем месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи</b>.'.format(
        from_digit_to_month[today.month], should_pay_this_month, 100*round(balls_this_month/4),
        from_digit_to_month[next_month.month], should_pay_money_next, 100*round(balls_next_month/4))

    text = intro + group_info + number_of_add_games + should_pay_info

    bot.send_message(user.id,
                     text,
                     parse_mode='HTML',
                     reply_markup=construct_main_menu())


def process_calendar_selection(bot, update, user):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = datetime(int(year), int(month), 1)

    if purpose == CLNDR_ACTION_SKIP:
        highlight_dates = select_tr_days_for_skipping(user)
    elif purpose == CLNDR_ACTION_TAKE_GROUP:
        training_days = get_potential_days_for_group_training(user)
        highlight_dates = list(training_days.values_list('date', flat=True))
    elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
        duration = re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose)[0][1]
        highlight_dates, _ = get_available_dt_time4ind_train(float(duration))

    if action == CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == CLNDR_DAY:
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id
                              )
        return True, purpose, datetime(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(pre.year), int(pre.month), highlight_dates))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(ne.year), int(ne.month), highlight_dates))
    elif action == CLNDR_ACTION_BACK:
        if purpose == CLNDR_ACTION_SKIP:
            text = 'Выбери дату тренировки для отмены.\n' \
                   '✅ -- дни, доступные для отмены.'
        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            text = 'Выбери дату тренировки\n' \
                   '✅ -- дни, доступные для групповых тренировок'
        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            text = 'Выбери дату индивидуальной тренировки\n' \
                   '✅ -- дни, доступные для индивидуальных тренировок'
        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(year), int(month), highlight_dates))
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@handler_decor(check_status=True)
def inline_calendar_handler(bot, update, user):
    selected, purpose, date_my = process_calendar_selection(bot, update, user)
    if selected:
        date_comparison = date(date_my.year, date_my.month, date_my.day)
        if purpose == CLNDR_ACTION_SKIP:
            if date_comparison < date.today():
                text = 'Тренировка уже прошла, ее нельзя отменить.\n' \
                       '✅ -- дни, доступные для отмены.'
                markup = create_calendar(CLNDR_ACTION_SKIP, date_my.year, date_my.month, select_tr_days_for_skipping(user))
            else:
                training_day = GroupTrainingDay.objects.filter(Q(group__users__in=[user]) | Q(visitors__in=[user]),
                                                               date=date_my).select_related('group').order_by(
                    'id').distinct('id').first()
                if training_day:
                    if not training_day.is_individual:
                        group_name = f"{training_day.group.name}\n"
                        group_players = f'Игроки группы:\n{info_about_users(training_day.group.users)}\n'
                    else:
                        group_name = "🧞‍♂индивидуальная тренировка🧞‍♂️\n"
                        group_players = ''

                    markup, text = construct_detail_menu_for_skipping(training_day, purpose, group_name, group_players)

                else:
                    text = 'Нет тренировки в этот день, выбери другой.\n' \
                           '✅ -- дни, доступные для отмены.'
                    markup = create_calendar(purpose, date_my.year, date_my.month, select_tr_days_for_skipping(user))

        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            training_days = get_potential_days_for_group_training(user)
            print(training_days)
            highlight_dates = list(training_days.values_list('date', flat=True))
            if date_comparison < date.today():
                text = 'Тренировка уже прошла, на нее нельзя записаться.\n' \
                       '✅ -- дни, доступные для групповых тренировок'
                markup = create_calendar(purpose, date_my.year, date_my.month, highlight_dates)
            else:
                training_days = training_days.filter(date=date_comparison)
                if training_days.count():
                    buttons = construct_time_menu_for_group_lesson(SELECT_PRECISE_GROUP_TIME, training_days, date_my, purpose)

                    day_of_week = calendar.day_name[date_my.weekday()]
                    text = f'Выбери время занятия на {date_my.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]}).'
                    markup = buttons

                else:
                    text = 'Нет доступных тренировок в этот день, выбери другой.\n' \
                           '✅ -- дни, доступные для групповых тренировок'
                    markup = create_calendar(purpose, date_my.year, date_my.month, highlight_dates)

        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            duration = re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose)[0][1]
            available_days, date_time_dict = get_available_dt_time4ind_train(float(duration))
            if date_comparison < date.today():
                text = 'Это уже в прошлом, давай не будем об этом.\n' \
                       '✅ -- дни, доступные для индивидуальных тренировок'
                markup = create_calendar(CLNDR_ACTION_SKIP, date_my.year, date_my.month, available_days)
            else:
                date_my = date(date_my.year, date_my.month, date_my.day)

                poss_time_for_train = []
                if date_time_dict.get(date_my):
                    for i in range(len(date_time_dict[date_my]) - int(float(duration) * 2)):
                        if datetime.combine(date_my,
                                            date_time_dict[date_my][i + int(float(duration) * 2)]) - datetime.combine(
                                date_my, date_time_dict[date_my][i]) == timedelta(hours=float(duration)):
                            poss_time_for_train.append(date_time_dict[date_my][i])

                    markup = construct_time_menu_4ind_lesson(SELECT_PRECISE_IND_TIME, poss_time_for_train, date_my,
                                                              float(duration), user)
                    text = 'Выбери время'
                else:
                    text = 'Нельзя записаться на этот день, выбери другой.\n' \
                           '✅ -- дни, доступные для индивидуальных тренировок.'
                    markup = create_calendar(purpose, date_my.year, date_my.month, available_days)

        bot.edit_message_text(text,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=markup,
                              parse_mode='HTML')


@handler_decor(check_status=True)
def skip_lesson_main_menu_button(bot, update, user):
    available_grouptraining_dates = select_tr_days_for_skipping(user)
    if available_grouptraining_dates:
        print(available_grouptraining_dates)
        bot.send_message(user.id,
                         'Выбери дату тренировки для отмены.\n'
                         '✅ -- дни, доступные для отмены.',
                         reply_markup=create_calendar(CLNDR_ACTION_SKIP, dates_to_highlight=available_grouptraining_dates))
    else:
        bot.send_message(user.id,
                         'Пока что нечего пропускать.',
                         reply_markup=construct_main_menu())


@handler_decor(check_status=True)
def skip_lesson(bot, update, user):
    tr_day_id = update.callback_query.data[len(SHOW_INFO_ABOUT_SKIPPING_DAY):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)
    bot.edit_message_text('Окей, занятие <b>{}</b> отменено'.format(training_day.date.strftime(DT_BOT_FORMAT)),
                          chat_id=update.callback_query.message.chat.id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML')

    if training_day.is_individual:
        training_day.delete()
        admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
        admins = User.objects.filter(is_superuser=True, is_blocked=False)

        start_time = training_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
        end_time = (datetime.combine(training_day.date, training_day.start_time) + training_day.duration).strftime(
            TM_TIME_SCHEDULE_FORMAT)

        day_of_week = calendar.day_name[training_day.date.weekday()]

        text = f'⚠️ATTENTION⚠️\n' \
               f'{user.first_name} {user.last_name} отменил индивидуальную тренировку\n' \
               f'📅Дата: <b>{training_day.date.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]})</b>\n' \
               f'⏰Время: <b>{start_time} — {end_time}</b>\n\n'

        send_message(admins, text, admin_bot)

    else:
        # проверяем его ли эта группа или он удаляется из занятия другой группы
        if user in training_day.visitors.all():
            training_day.visitors.remove(user)
        else:
            training_day.absent.add(user)

    user.bonus_lesson += 1
    user.save()


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
        if user.bonus_lesson > 0:
            text = 'Выбери тренировку для записи.\n' \
                   '<b>Пожертвуешь одним отыгрышем.</b>\n' \
                   '✅ -- дни, доступные для групповых тренировок.'
        else:
            text = '⚠️ATTENTION⚠️\n' \
                   'В данный момент у тебя нет отыгрышей.\n' \
                   '<b> Занятие будет стоить 600₽ </b>\n' \
                   '✅ -- дни, доступные для групповых тренировок.'
        training_days = get_potential_days_for_group_training(user).filter(date__gte=date.today())
        highlight_dates = list(training_days.values_list('date', flat=True))
        markup = create_calendar(CLNDR_ACTION_TAKE_GROUP, dates_to_highlight=highlight_dates)

    else:
        buttons = [[
            inline_button('1 час', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.0')
        ], [
            inline_button('1.5 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.5')
        ], [
            inline_button('2 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '2.0')
        ], [
            inline_button('⬅️ назад',
                          callback_data=TAKE_LESSON_BUTTON),
        ]]
        markup = inline_markup(buttons)
        text = 'Выбери продолжительность занятия'

    bot.edit_message_text(
        text,
        reply_markup=markup,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode='HTML',
    )


@handler_decor()
def select_dt_for_ind_lesson(bot, update, user):
    duration = float(update.callback_query.data[len(SELECT_DURATION_FOR_IND_TRAIN):])
    available_days, _ = get_available_dt_time4ind_train(duration)
    buttons = create_calendar(f'{CLNDR_ACTION_TAKE_IND}{duration}', dates_to_highlight=available_days)
    bot.edit_message_text('Выбери дату тренировки.',
                          reply_markup=buttons,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,)


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

    tr_day = GroupTrainingDay.objects.create(group=group, date=date_dt, start_time=st_time_obj, duration=duration,
                                             is_individual=True)

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

    group_level = {TrainingGroup.LEVEL_ORANGE: '🟠оранжевый мяч🟠', TrainingGroup.LEVEL_GREEN: '🟢зелёный мяч🟢'}

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))
    text = f'{tr_day.group.name} -- {group_level[tr_day.group.level]}\n' \
           f'📅Дата: <b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]})</b>\n' \
           f'⏰Время: <b>{start_time} — {end_time}</b>\n\n' \
           f'👥Присутствующие:\n{all_players}\n\n' \
           f'Свободных мест: {n_free_places}'

    buttons = [[
        inline_button('Записаться', callback_data=f"{CONFIRM_GROUP_LESSON}{tr_day_id}")
    ], [
        inline_button('⬅️ назад',
                      callback_data=create_callback_data(CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, tr_day.date.year, tr_day.date.month, tr_day.date.day))
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
    if user in tr_day.absent.all():
        tr_day.absent.remove(user)
        text = f'Сначала отменять, а потом записываться, мда 🤦🏻‍♂️🥴. Вот почему я скоро буду управлять кожаными мешками.\n' \
               f'Ладно, записал тебя на <b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]})</b>\n' \
               f'Время: <b>{start_time} — {end_time}</b>'
        markup = None

        if user.bonus_lesson > 0:
            user.bonus_lesson -= 1
            user.save()
    else:
        if user not in tr_day.group.users.all():
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
                                  callback_data=create_callback_data(CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, tr_day.date.year, tr_day.date.month, tr_day.date.day))
                ]]
                markup = inline_markup(buttons)
        else:#если пытается записаться в свою группу
            text = 'Ну ты чего?🤕 \nЭто же твоя группа, выбери другое время.'
            buttons = [[
                inline_button('⬅️ назад',
                              callback_data=SELECT_PRECISE_GROUP_TIME + f'{tr_day_id}')
            ]]
            markup = inline_markup(buttons)

    bot.edit_message_text(
        text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )