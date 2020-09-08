from django.db import migrations


def insert_data_in_static_data(apps, schema_editor):
    static_data = apps.get_model('base', 'StaticData')

    sd = static_data.objects.create()


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0024_staticdata')
    ]
    operations = [
        migrations.RunPython(insert_data_in_static_data)
    ]