# Generated by Django 4.1.7 on 2023-02-19 19:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homeCooked', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_sent',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
