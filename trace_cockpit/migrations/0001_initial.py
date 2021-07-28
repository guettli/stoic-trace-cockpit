# Generated by Django 3.2.5 on 2021-07-28 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TraceConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order')),
                ('name', models.CharField(max_length=1024)),
                ('is_active', models.BooleanField(default=True)),
                ('trace_request_eval', models.CharField(blank=True, default='', help_text='Trace a request, if the expression matches.\n                                   Example: "request.user.username==\'foo\'"\n                                   If empty, then every request gets traced', max_length=1024)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TraceLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('json', models.JSONField(default=list)),
                ('success', models.BooleanField(default=True)),
                ('error_message', models.TextField(default='')),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trace_cockpit.traceconfig')),
            ],
        ),
    ]
