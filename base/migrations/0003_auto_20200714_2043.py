# Generated by Django 2.0.5 on 2020-07-14 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20200714_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarif',
            name='name',
            field=models.CharField(blank=True, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('W', 'waiting list'), ('T', 'training'), ('F', 'finished'), ('A', 'arbitrary')], default='W', max_length=1),
        ),
    ]
