# Generated by Django 3.0.8 on 2020-09-12 22:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_auto_20200908_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 12, 22, 57, 42, 997512, tzinfo=utc)),
        ),
    ]
