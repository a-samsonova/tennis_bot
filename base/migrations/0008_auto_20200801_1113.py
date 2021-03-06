# Generated by Django 2.0.5 on 2020-08-01 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_auto_20200716_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='grouptrainingday',
            options={'ordering': ['-date'], 'verbose_name': 'тренировочный день', 'verbose_name_plural': 'тренировочные дни'},
        ),
        migrations.AlterModelOptions(
            name='tarif',
            options={'verbose_name': 'тариф', 'verbose_name_plural': 'тарифы'},
        ),
        migrations.AlterModelOptions(
            name='traininggroup',
            options={'verbose_name': 'банда', 'verbose_name_plural': 'банды'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'игрок', 'verbose_name_plural': 'игроки'},
        ),
        migrations.AddField(
            model_name='grouptrainingday',
            name='visitors',
            field=models.ManyToManyField(blank=True, help_text='Пришли из других групп', related_name='visitors', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='grouptrainingday',
            name='duration',
            field=models.DurationField(default='1:0:0', help_text='ДНИ ЧАСЫ:МИНУТЫ:СЕКУНДЫ', null=True, verbose_name='Продолжительность занятия'),
        ),
        migrations.AlterField(
            model_name='grouptrainingday',
            name='start_time',
            field=models.TimeField(help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ', null=True, verbose_name='Время начала занятия'),
        ),
        migrations.AlterField(
            model_name='tarif',
            name='price_per_hour',
            field=models.IntegerField(verbose_name='Цена за час'),
        ),
        migrations.AlterField(
            model_name='traininggroup',
            name='name',
            field=models.CharField(max_length=32, verbose_name='имя'),
        ),
        migrations.AlterField(
            model_name='traininggroup',
            name='tarif',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Tarif', verbose_name='тариф'),
        ),
        migrations.AlterField(
            model_name='user',
            name='add_info',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Доп. информация'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bonus_lesson',
            field=models.SmallIntegerField(blank=True, default=0, null=True, verbose_name='Количество отыгрышей'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=32, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=16, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('W', 'в ожидании'), ('G', 'групповые тренировки'), ('A', 'свободный график'), ('F', 'закончил')], default='W', max_length=1, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='user',
            name='time_before_cancel',
            field=models.DurationField(help_text='ДНИ ЧАСЫ:МИНУТЫ:СЕКУНДЫ', null=True, verbose_name='Время, за которое нужно предупредить'),
        ),
    ]
