# Generated by Django 2.1.1 on 2018-10-18 19:54

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pixel', '0009_auto_20181018_1546'),
    ]

    operations = [
        migrations.AddField(
            model_name='pixelevent',
            name='params',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=dict),
        ),
    ]