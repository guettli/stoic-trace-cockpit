# Generated by Django 3.2.5 on 2021-07-29 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trace_cockpit', '0004_traceconfig_max_event_count_per_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracelog',
            name='http_method',
            field=models.CharField(default='', max_length=1024),
        ),
    ]
