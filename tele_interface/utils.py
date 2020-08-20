from datetime import date, time, timedelta, datetime
from functools import wraps

from django.db.models import (ExpressionWrapper,
                              F, Q,
                              DateTimeField, Count, )
from django.db.models.functions import TruncDate

from base.models import (User,
                         GroupTrainingDay, )
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


def get_available_dt_time4ind_train(duration: float):
    poss_date = date.today()
    start_time = time(8, 0, 0)

    possible_times = []
    for i in range(8, 21):
        for minute in [0, 30]:
            possible_times.append(time(i, minute))
    del possible_times[-1]

    possible_dates = []
    for _ in range(8):
        poss_date += timedelta(days=1)
        possible_dates.append(poss_date)

    tr_days = GroupTrainingDay.objects.tr_day_is_my_available().filter(date__in=possible_dates,
                                                                       start_time__gte=start_time).annotate(
        end_time=ExpressionWrapper(F('start_time') + F('duration'), output_field=DateTimeField()),
        date_tmp=TruncDate('date')).values('date_tmp', 'start_time', 'end_time').order_by('date', 'start_time')
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
                                                                   date__gt=date.today()).exclude(
        absent__in=[user]).order_by('id').distinct(
        'id').values('date', 'start_time')
    available_grouptraining_dates = [x['date'] for x in tmp  # учитываем время до отмены
                                     if datetime.combine(x['date'],
                                                         x['start_time']) - datetime.now() >
                                     user.time_before_cancel]
    return available_grouptraining_dates


def get_potential_days_for_group_training(user):
    potential_free_places = GroupTrainingDay.objects.tr_day_is_my_available().annotate(
        n_absent=Count('absent'),
        max_players=F('group__max_players'),
        n_players=Count('group__users'),
        n_visitors=Count('visitors')).filter(
        max_players__gt=F('n_visitors') + F('n_players') - F('n_absent')).exclude(
        Q(visitors__in=[user]) | Q(group__users__in=[user])).order_by(
        'start_time')

    return potential_free_places