# Generated by Django 3.2.5 on 2021-07-29 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trace_cockpit', '0005_tracelog_http_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traceconfig',
            name='max_event_count_per_module',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
