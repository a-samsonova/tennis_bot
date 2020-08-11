# Generated by Django 2.0.5 on 2020-07-14 12:29

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('telegram_username', models.CharField(blank=True, max_length=64, null=True)),
                ('first_name', models.CharField(max_length=32, null=True)),
                ('phone_number', models.CharField(max_length=16, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('W', 'waiting list'), ('T', 'training'), ('F', 'finished')], default='W', max_length=1)),
                ('time_before_cancel', models.DurationField(null=True)),
                ('bonus_lesson', models.SmallIntegerField(blank=True, default=0, null=True)),
                ('add_info', models.CharField(blank=True, max_length=128, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='GroupTrainingDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('is_available', models.BooleanField(default=True, help_text='будет ли в этот день тренировка у этой группы')),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('absent', models.ManyToManyField(blank=True, help_text='кто сегодня отсутствует', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Tarif',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_hour', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainingGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dttm_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('dttm_deleted', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=32)),
                ('max_players', models.SmallIntegerField(default=6, verbose_name='Максимальное количество игроков в группе')),
                ('tarif', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.Tarif')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='grouptrainingday',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='base.TrainingGroup'),
        ),
    ]