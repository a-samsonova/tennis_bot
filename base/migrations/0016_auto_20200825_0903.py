# Generated by Django 2.0.5 on 2020-08-25 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_auto_20200825_0849'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['year'], 'verbose_name': 'оплата', 'verbose_name_plural': 'оплата'},
        ),
    ]
