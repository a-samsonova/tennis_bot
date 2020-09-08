from django.db import migrations


def set_group_status(apps, schema_editor):
    group_model = apps.get_model('base', 'TrainingGroup')

    groups = group_model.objects.filter(max_players=1)
    for group in groups:
        group.status = 'I'
        group.save()


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0018_auto_20200904_1422')
    ]
    operations = [
        migrations.RunPython(set_group_status)
    ]