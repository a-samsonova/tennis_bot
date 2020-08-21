from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from datetime import timedelta, datetime
from base.utils import construct_main_menu, send_message
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from base.utils import send_alert_about_changing_tr_day_status
from tennis_bot.config import TELEGRAM_TOKEN

import telegram


class ModelwithTimeManager(models.Manager):
    def tr_day_is_my_available(self, *args, **kwargs):
        return self.filter(is_available=True, tr_day_status=GroupTrainingDay.MY_TRAIN_STATUS, *args, **kwargs)


class ModelwithTime(models.Model):
    dttm_added = models.DateTimeField(default=timezone.now)
    dttm_deleted = models.DateTimeField(null=True, blank=True)

    objects = ModelwithTimeManager()

    class Meta:
        abstract = True


class User(AbstractUser):
    STATUS_WAITING = 'W'
    STATUS_TRAINING = 'G'
    STATUS_FINISHED = 'F'
    STATUS_ARBITRARY = 'A'
    STATUS_IND_TRAIN = 'I'
    STATUSES = (
        (STATUS_WAITING, 'в ожидании'),
        (STATUS_TRAINING, 'групповые тренировки'),
        (STATUS_ARBITRARY, 'свободный график'),
        (STATUS_FINISHED, 'закончил'),
    )

    tarif_for_status = {
        STATUS_TRAINING: 400,
        STATUS_ARBITRARY: 600,
        STATUS_IND_TRAIN: 1400,
    }

    id = models.BigIntegerField(primary_key=True)  # telegram id
    telegram_username = models.CharField(max_length=64, null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True, verbose_name='Имя')
    phone_number = models.CharField(max_length=16, null=True, verbose_name='Номер телефона')

    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUSES, default=STATUS_WAITING, verbose_name='статус')

    time_before_cancel = models.DurationField(null=True, help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ',
                                              verbose_name='Время, за которое нужно предупредить', default='6:0:0')
    bonus_lesson = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name='Количество отыгрышей')

    add_info = models.CharField(max_length=128, null=True, blank=True, verbose_name='Доп. информация')

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'

    def __str__(self):
        return '{} {} -- {}'.format(self.first_name, self.last_name, self.phone_number)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'status', 'time_before_cancel', 'bonus_lesson',
                  'add_info']

    def clean(self):
        if 'status' in self.changed_data:
            new_status = self.cleaned_data.get('status')
            if self.instance.status == User.STATUS_WAITING and (new_status == User.STATUS_ARBITRARY or new_status == User.STATUS_TRAINING):
                bot = telegram.Bot(TELEGRAM_TOKEN)
                send_message([self.instance], 'Теперь тебе доступен мой функционал, поздравляю!', bot)


class TrainingGroup(ModelwithTime):
    name = models.CharField(max_length=32, verbose_name='имя')
    users = models.ManyToManyField(User)
    max_players = models.SmallIntegerField(default=6, verbose_name='Максимальное количество игроков в группе')

    class Meta:
        verbose_name = 'банда'
        verbose_name_plural = 'банды'

    def __str__(self):
        return '{}, max_players: {}'.format(self.name, self.max_players)


class TrainingGroupForm(forms.ModelForm):
    class Meta:
        model = TrainingGroup
        fields = ['name', 'users', 'max_players']

    def clean(self):
        users = self.cleaned_data.get('users')
        max_players = self.cleaned_data.get('max_players')
        if users.count() > max_players:
            raise ValidationError({'max_players': 'Количество игроков в группе должно быть не больше {}, вы указали {}.'. \
                                  format(max_players, users.count())})


class GroupTrainingDay(ModelwithTime):
    MY_TRAIN_STATUS = 'M'
    RENT_TRAIN_STATUS = 'R'

    TR_DAY_STATUSES = (
        (MY_TRAIN_STATUS, 'моя тренировка'),
        (RENT_TRAIN_STATUS, 'аренда')
    )

    group = models.ForeignKey(TrainingGroup, on_delete=models.PROTECT, verbose_name='Группа')
    absent = models.ManyToManyField(User, blank=True, help_text='Кто сегодня отсутствует', verbose_name='Отсутствующие')
    date = models.DateField(default=timezone.now, verbose_name='Дата Занятия')
    is_available = models.BooleanField(default=True, help_text='Будет ли в этот день тренировка у этой группы')
    start_time = models.TimeField(null=True, help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ', verbose_name='Время начала занятия')
    duration = models.DurationField(null=True, default='1:0:0', help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ',
                                    verbose_name='Продолжительность занятия')
    visitors = models.ManyToManyField(User, blank=True, help_text='Пришли из других групп\n', related_name='visitors',
                                      verbose_name='Игроки из других групп')
    tr_day_status = models.CharField(max_length=1, default=MY_TRAIN_STATUS, help_text='Моя тренировка или аренда',
                                     choices=TR_DAY_STATUSES, verbose_name='Статус')

    class Meta:
        ordering = ['-date']
        verbose_name = 'тренировочный день'
        verbose_name_plural = 'тренировочные дни'

    def __str__(self):
        return 'Группа: {}, дата тренировки {}, время начала: {}'.format(self.group, self.date, self.start_time)


class GroupTrainingDayForm(forms.ModelForm):
    class Meta:
        model = GroupTrainingDay
        fields = ['group', 'absent', 'visitors', 'date', 'is_available', 'tr_day_status', 'start_time', 'duration']

    def clean(self):
        group = self.cleaned_data.get('group')
        current_amount_of_players = self.cleaned_data.get(
            'visitors').count() + group.users.count() - self.cleaned_data.get('absent').count()
        if current_amount_of_players > group.max_players:
            raise ValidationError(
                'Превышен лимит игроков в группе — сейчас {}, максимум {}'.format(current_amount_of_players,
                                                                                  group.max_players))

        if ('start_time' or 'duration') in self.changed_data:
            """
                Если добавляется новый grouptrainingday, то нужно
                проверить, не накладывается ли время тренировки
                на уже существущие.
            """
            today_trainings = GroupTrainingDay.objects.filter(date=self.cleaned_data.get('date'))
            start_time = datetime.combine(self.cleaned_data.get('date'), self.cleaned_data.get('start_time'))

            for train in today_trainings:
                exist_train_start_time = datetime.combine(train.date, train.start_time)
                if exist_train_start_time <= start_time < exist_train_start_time + train.duration:
                    raise ValidationError('Нельзя добавить тренировку на это время в этот день, т.к. уже есть запись на {}'\
                                          ' с продолжительностью {}.'.format(train.start_time, train.duration))

        if 'is_available' in self.changed_data:
            bot = telegram.Bot(TELEGRAM_TOKEN)
            send_alert_about_changing_tr_day_status(self.instance, self.cleaned_data.get('is_available'), bot)


class Channel(models.Model):
    name = models.CharField(max_length=64, default='')
    username = models.CharField(max_length=64, default='')
    code = models.CharField(max_length=32, default='')
    token = models.CharField(max_length=256, default='')


"""раздел с сигналами, в отедльном файле что-то не пошло"""


@receiver(post_save, sender=GroupTrainingDay)
def create_training_days_for_next_two_months(sender, instance, created, **kwargs):
    """
    При создании instance GroupTrainingDay автоматом добавляем
    еще таких же записей примерно на 2 месяца вперед.
    Используем bulk_create, т.к. иначе получим рекурсию.
    """
    if created and instance.group.max_players > 1:
        date = instance.date + timedelta(days=7)
        dates = [date]
        for _ in range(24):
            date += timedelta(days=7)
            dates.append(date)
        objs = [GroupTrainingDay(group=instance.group, date=dat, start_time=instance.start_time,
                                 duration=instance.duration) for dat in dates]
        GroupTrainingDay.objects.bulk_create(objs)


@receiver(post_delete, sender=GroupTrainingDay)
def delete_training_days(sender, instance, **kwargs):
    """
        При удалении instance GroupTrainingDay автоматом удаляем
        занятие в это время для более поздних дат.
    """
    GroupTrainingDay.objects.filter(group=instance.group, start_time=instance.start_time, duration=instance.duration,
                                    date__gt=instance.date).delete()


@receiver(post_save, sender=User)
def create_group_for_arbitrary(sender, instance, created, **kwargs):
    """
        Если игрок ходит по свободному графику, то создадим
        для него группу, состояющую только из него.
    """
    if instance.status == User.STATUS_ARBITRARY:
        group, _= TrainingGroup.objects.update_or_create(name=instance.first_name + instance.last_name, max_players=1)
        if not group.users.count():
            group.users.add(instance)



