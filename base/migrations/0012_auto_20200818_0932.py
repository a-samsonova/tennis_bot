# Generated by Django 2.0.5 on 2020-08-18 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_auto_20200818_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grouptrainingday',
            name='tr_day_status',
            field=models.CharField(choices=[('M', 'моя тренировка'), ('R', 'аренда')], default='M', help_text='Моя тренировка или аренда', max_length=1, verbose_name='Статус'),
        ),
    ]
