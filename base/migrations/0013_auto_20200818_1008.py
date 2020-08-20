# Generated by Django 2.0.5 on 2020-08-18 10:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auto_20200818_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouptrainingday',
            name='absent',
            field=models.ManyToManyField(blank=True, help_text='Кто сегодня отсутствует', to=settings.AUTH_USER_MODEL, verbose_name='Отсутствующие'),
        ),
        migrations.AlterField(
            model_name='grouptrainingday',
            name='visitors',
            field=models.ManyToManyField(blank=True, help_text='Пришли из других групп\n', related_name='visitors', to=settings.AUTH_USER_MODEL, verbose_name='Игроки из других групп'),
        ),
    ]