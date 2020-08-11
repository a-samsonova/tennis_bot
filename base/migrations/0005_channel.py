# Generated by Django 2.0.5 on 2020-07-15 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20200714_2051'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=64)),
                ('username', models.CharField(default='', max_length=64)),
                ('code', models.CharField(default='', max_length=32)),
                ('token', models.CharField(default='', max_length=256)),
            ],
        ),
    ]