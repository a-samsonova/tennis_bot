# Generated by Django 2.0.5 on 2020-08-25 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_payment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['year', 'month'], 'verbose_name': 'оплата', 'verbose_name_plural': 'оплата'},
        ),
    ]