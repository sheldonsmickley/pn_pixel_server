# Generated by Django 2.1.1 on 2018-10-15 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pixel', '0002_auto_20181015_1908'),
    ]

    operations = [
        migrations.AddField(
            model_name='pixelevent',
            name='ga_cookie_id',
            field=models.CharField(default=2, max_length=200),
            preserve_default=False,
        ),
    ]
