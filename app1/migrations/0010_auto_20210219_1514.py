# Generated by Django 3.0.8 on 2021-02-19 21:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_auto_20210218_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 19, 21, 11, 59, 472816, tzinfo=utc)),
        ),
    ]
