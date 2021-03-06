# Generated by Django 3.2.5 on 2021-07-29 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trace_cockpit', '0002_tracelog_skipped_modules'),
    ]

    operations = [
        migrations.AddField(
            model_name='tracelog',
            name='skipped_events_because_max_reached',
            field=models.JSONField(blank=True, default=dict, editable=False),
        ),
        migrations.AlterField(
            model_name='tracelog',
            name='skipped_modules',
            field=models.JSONField(blank=True, default=dict, editable=False),
        ),
    ]
