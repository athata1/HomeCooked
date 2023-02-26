# Generated by Django 4.1.7 on 2023-02-19 19:58

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('homeCooked', '0002_alter_message_message_sent'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_completed',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='post_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='post',
            name='post_recipe',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='homeCooked.recipe'),
            preserve_default=False,
        ),
    ]