# Generated by Django 3.2.5 on 2021-07-29 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trace_cockpit', '0003_auto_20210729_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='traceconfig',
            name='max_event_count_per_module',
            field=models.PositiveIntegerField(default=300),
        ),
    ]
